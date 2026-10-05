/* Simulador de escaños D'Hondt — nacional y provincial. Sin dependencias. */
(function () {
  "use strict";

  function safe(fn) { try { fn(); } catch (e) { if (window.console) console.error("[sim]", e); } }

  var NS = "http://www.w3.org/2000/svg";
  var fmt1 = new Intl.NumberFormat("es-ES", { maximumFractionDigits: 1, minimumFractionDigits: 1 });

  /* D'Hondt con umbral (porcentaje sobre votos válidos, blanco incluido). */
  function dhondt(shares, blank, seats, threshold) {
    var total = blank;
    var k;
    for (k in shares) total += shares[k];
    var limit = total * threshold;
    var eligible = [];
    for (k in shares) if (shares[k] > 0 && shares[k] >= limit) eligible.push(k);
    var out = {};
    eligible.forEach(function (p) { out[p] = 0; });
    for (var s = 0; s < seats; s++) {
      var best = null, bestQ = -1;
      for (var i = 0; i < eligible.length; i++) {
        var p = eligible[i];
        var q = shares[p] / (out[p] + 1);
        if (q > bestQ || (q === bestQ && shares[p] > shares[best])) { bestQ = q; best = p; }
      }
      if (best === null) break;
      out[best] += 1;
    }
    return out;
  }

  /* Hemiciclo: devuelve posiciones ordenadas de izquierda a derecha. */
  function hemicycleLayout(n) {
    var rows = n <= 10 ? 1 : n <= 30 ? 2 : n <= 60 ? 4 : n <= 150 ? 7 : 12;
    var r0 = rows === 1 ? 1 : 0.42;
    var radii = [];
    for (var i = 0; i < rows; i++) radii.push(rows === 1 ? 1 : r0 + (1 - r0) * i / (rows - 1));
    var sumR = radii.reduce(function (a, b) { return a + b; }, 0);
    var counts = radii.map(function (r) { return Math.max(1, Math.round(n * r / sumR)); });
    var diff = n - counts.reduce(function (a, b) { return a + b; }, 0);
    var idx = rows - 1;
    while (diff !== 0) {
      counts[idx] += diff > 0 ? 1 : -1;
      diff += diff > 0 ? -1 : 1;
      idx = (idx - 1 + rows) % rows;
    }
    var pts = [];
    radii.forEach(function (r, ri) {
      var c = counts[ri];
      for (var j = 0; j < c; j++) {
        var t = c === 1 ? Math.PI / 2 : Math.PI * (1 - j / (c - 1));
        pts.push({ x: r * Math.cos(t), y: r * Math.sin(t), t: t, r: r });
      }
    });
    pts.sort(function (a, b) { return b.t - a.t || a.r - b.r; });
    var dot = rows === 1 ? Math.min(0.12, 1.4 / Math.max(n, 1)) : (1 - r0) / (rows - 1) * 0.42;
    return { pts: pts, dot: dot };
  }

  function drawHemicycle(svg, seats, order, colors, total) {
    var lay = svg.__layout;
    if (!lay || lay.n !== total) {
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      lay = hemicycleLayout(total);
      lay.n = total;
      lay.nodes = lay.pts.map(function (p) {
        var c = document.createElementNS(NS, "circle");
        c.setAttribute("cx", (p.x * 100).toFixed(2));
        c.setAttribute("cy", (-p.y * 100).toFixed(2));
        c.setAttribute("r", (lay.dot * 100).toFixed(2));
        svg.appendChild(c);
        return c;
      });
      var pad = lay.dot * 100 + 2;
      svg.setAttribute("viewBox", (-100 - pad) + " " + (-100 - pad) + " " + (200 + pad * 2) + " " + (100 + pad * 2));
      svg.__layout = lay;
    }
    var i = 0;
    order.forEach(function (p) {
      for (var k = 0; k < (seats[p] || 0); k++) {
        if (lay.nodes[i]) lay.nodes[i].setAttribute("fill", colors[p] || "#888");
        i++;
      }
    });
    for (; i < lay.nodes.length; i++) lay.nodes[i].setAttribute("fill", "var(--rule)");
  }

  function el(tag, attrs, text) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    return e;
  }

  function init(root) {
    var dataNode = root.querySelector("script[type='application/json']");
    var D = JSON.parse(dataNode.textContent);
    var parties = D.parties;            // [{id,name,color,base}]
    var colors = {};
    parties.forEach(function (p) { colors[p.id] = p.color; });
    var form = root.querySelector("[data-inputs]");
    var svg = root.querySelector("svg.hemi");
    var list = root.querySelector("[data-seatlist]");
    var sumEl = root.querySelector("[data-sum]");
    var majEl = root.querySelector("[data-majority]");
    var totalSeats = D.mode === "national" ? D.provinces.reduce(function (a, p) { return a + p.seats; }, 0) : D.seats;
    var values = {};
    var inputs = {};

    parties.forEach(function (p) {
      values[p.id] = p.base;
      var row = el("div", { "class": "prow" });
      var sw = el("i", { "aria-hidden": "true" }); sw.style.background = p.color;
      var lab = el("label", { "for": "pct-" + p.id });
      lab.appendChild(document.createTextNode(p.short || p.id));
      if (p.name && p.name !== p.short) lab.appendChild(el("small", null, p.name));
      var box = el("div", { "class": "pct" });
      var inp = el("input", { type: "number", id: "pct-" + p.id, min: "0", max: "100", step: "0.1", inputmode: "decimal", value: p.base.toFixed(1) });
      box.appendChild(inp); box.appendChild(el("span", null, "%"));
      var rng = el("input", { type: "range", min: "0", max: String(p.max || 50), step: "0.1", value: String(p.base), "aria-label": "Porcentaje de " + (p.short || p.id) });
      row.appendChild(sw); row.appendChild(lab); row.appendChild(box); row.appendChild(rng);
      form.appendChild(row);
      inputs[p.id] = { num: inp, rng: rng };
      inp.addEventListener("input", function () {
        var v = parseFloat(String(inp.value).replace(",", "."));
        if (!isFinite(v) || v < 0) v = 0;
        if (v > 100) v = 100;
        values[p.id] = v; rng.value = String(v); schedule();
      });
      rng.addEventListener("input", function () {
        values[p.id] = parseFloat(rng.value); inp.value = values[p.id].toFixed(1); schedule();
      });
    });

    var reset = root.querySelector("[data-reset]");
    if (reset) reset.addEventListener("click", function () {
      parties.forEach(function (p) {
        values[p.id] = p.base; inputs[p.id].num.value = p.base.toFixed(1); inputs[p.id].rng.value = String(p.base);
      });
      schedule();
    });

    // El cálculo completo (52 repartos D'Hondt) tarda menos de 1 ms: se hace en el acto.
    function schedule() { compute(); }

    function compute() {
      var seats = {};
      parties.forEach(function (p) { seats[p.id] = 0; });
      var sum = 0;
      parties.forEach(function (p) { sum += values[p.id]; });

      if (D.mode === "national") {
        D.provinces.forEach(function (prov) {
          var shares = {};
          parties.forEach(function (p) {
            if (p.id === "OTROS") return;
            var base = prov.shares[p.id];
            if (base != null && p.base > 0) shares[p.id] = base * values[p.id] / p.base;
            else if (!p.regional) shares[p.id] = values[p.id];
            else shares[p.id] = 0;
          });
          var otros = prov.shares.OTROS || 0;
          var otrosNat = parties.filter(function (p) { return p.id === "OTROS"; })[0];
          if (otrosNat && otrosNat.base > 0) otros = otros * values.OTROS / otrosNat.base;
          var used = otros;
          for (var k in shares) used += shares[k];
          var scale = used > 0 ? (100 - prov.blank) / used : 0;
          for (k in shares) shares[k] *= scale;
          var r = dhondt(shares, prov.blank, prov.seats, 0.03);
          for (k in r) seats[k] += r[k];
        });
      } else {
        var sh = {};
        parties.forEach(function (p) { if (p.id !== "OTROS") sh[p.id] = values[p.id]; });
        // "Otros" y el voto en blanco cuentan para el umbral del 3 %, pero no reciben escaños
        var tot = (D.blank || 0) + (values.OTROS || 0);
        for (var key in sh) tot += sh[key];
        var filtered = {};
        for (key in sh) if (sh[key] >= tot * 0.03) filtered[key] = sh[key];
        var r2 = dhondt(filtered, 0, totalSeats, 0);
        for (key in r2) seats[key] = r2[key];
      }

      if (sumEl) {
        sumEl.querySelector("b").textContent = fmt1.format(sum) + " %";
        sumEl.classList.toggle("is-off", Math.abs(sum + (D.mode === "national" ? D.blankNat : D.blank || 0) - 100) > 2);
      }
      var order = parties.map(function (p) { return p.id; }).filter(function (id) { return seats[id] > 0; })
        .sort(function (a, b) { return seats[b] - seats[a]; });
      drawHemicycle(svg, seats, order, colors, totalSeats);

      list.textContent = "";
      order.forEach(function (id) {
        var p = parties.filter(function (x) { return x.id === id; })[0];
        var li = el("li");
        var dot = el("i", { "aria-hidden": "true" }); dot.style.background = p.color;
        li.appendChild(dot);
        li.appendChild(el("span", null, p.short || p.id));
        li.appendChild(el("b", null, String(seats[id])));
        if (p.ref != null) {
          var d = seats[id] - p.ref;
          li.appendChild(el("span", { "class": "delta", title: "Diferencia con 2023" }, d === 0 ? "=" : (d > 0 ? "+" + d : String(d))));
        }
        list.appendChild(li);
      });

      if (majEl) {
        var need = Math.floor(totalSeats / 2) + 1;
        var top = order[0];
        majEl.innerHTML = "";
        var txt = "Mayoría absoluta: <b>" + need + "</b> escaños. ";
        if (top) {
          var pt = parties.filter(function (x) { return x.id === top; })[0];
          txt += seats[top] >= need
            ? "<b>" + (pt.short || top) + "</b> la alcanzaría en solitario."
            : "Ningún partido la alcanza; el más votado se queda a <b>" + (need - seats[top]) + "</b>.";
        }
        majEl.innerHTML = txt;
      }
    }
    compute();
  }

  function boot() {
    var roots = document.querySelectorAll("[data-sim]");
    for (var i = 0; i < roots.length; i++) (function (r) { safe(function () { init(r); }); })(roots[i]);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
