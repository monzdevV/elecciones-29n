/* Mapa interactivo de las 52 circunscripciones. Sin dependencias.
   Contenedor: <div data-map data-layer="ganador" [data-highlight="slug"] [data-layers]>
   Si el contenedor ya trae el <svg> (portada), solo lo enriquece; si no, lo construye desde /assets/data/mapa.json. */
(function () {
  "use strict";

  function safe(fn) { try { fn(); } catch (e) { if (window.console) console.error("[mapa]", e); } }

  var NS = "http://www.w3.org/2000/svg";
  var VER = (document.currentScript && document.currentScript.src.split("?v=")[1]) || "";
  var cache = {};
  var lectores = null;          // resultados de la votación simbólica
  var maps = [];

  function getJSON(path) {
    if (!cache[path]) cache[path] = fetch(path + "?v=" + VER).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
    return cache[path];
  }

  var SEQ = ["var(--seq-0)", "var(--seq-1)", "var(--seq-2)", "var(--seq-3)", "var(--seq-4)", "var(--seq-5)"];
  function seatQ(n) { return n <= 2 ? 0 : n === 3 ? 1 : n === 4 ? 2 : n <= 6 ? 3 : n <= 11 ? 4 : 5; }
  var fmt = new Intl.NumberFormat("es-ES", { maximumFractionDigits: 1, minimumFractionDigits: 1 });

  function leaderOf(counts) {
    var best = null, total = 0;
    for (var k in counts) { total += counts[k]; if (!best || counts[k] > counts[best]) best = k; }
    return { party: best, total: total };
  }

  function fillFor(layer, p, mini) {
    if (layer === "escanos") return SEQ[seatQ(p.s)];
    if (layer === "lectores") {
      if (!lectores) return "var(--map-empty)";
      if (!lectores.revelado) {
        var v = (lectores.participacion || {})[p.slug] || 0;
        return v ? SEQ[v < 5 ? 1 : v < 20 ? 2 : v < 100 ? 3 : v < 500 ? 4 : 5] : "var(--map-empty)";
      }
      var c = lectores.provincias && lectores.provincias[p.slug];
      if (!c) return "var(--map-empty)";
      var L = leaderOf(c);
      if (L.total < 3) return "var(--map-empty)";
      return (mini.colors[L.party]) || "var(--map-empty)";
    }
    return p.r[0] ? p.r[0][2] : "var(--map-empty)";
  }

  function buildSVG(geo) {
    var svg = document.createElementNS(NS, "svg");
    svg.setAttribute("viewBox", geo.viewBox);
    svg.setAttribute("class", "map__svg");
    svg.setAttribute("role", "img");
    var box = geo.canarias_box;
    var rect = document.createElementNS(NS, "rect");
    rect.setAttribute("x", box[0]); rect.setAttribute("y", box[1]); rect.setAttribute("width", box[2]); rect.setAttribute("height", box[3]);
    rect.setAttribute("class", "map__inset");
    svg.appendChild(rect);
    for (var slug in geo.paths) {
      var a = document.createElementNS(NS, "a");
      a.setAttribute("href", "/provincias/" + slug + "/");
      a.setAttribute("data-slug", slug);
      var path = document.createElementNS(NS, "path");
      path.setAttribute("d", geo.paths[slug]);
      a.appendChild(path);
      svg.appendChild(a);
    }
    return svg;
  }

  function Map(root, mini) {
    var self = this;
    var svg = root.querySelector("svg.map__svg");
    var layer = root.getAttribute("data-layer") || "ganador";
    var hi = root.getAttribute("data-highlight");
    var tip = root.querySelector(".map__tip");
    var legend = root.querySelector("[data-legend]");
    var bySlug = {};
    mini.p.forEach(function (p) { bySlug[p.slug] = p; });
    var links = svg.querySelectorAll("a[data-slug]");

    links.forEach(function (a) {
      var p = bySlug[a.getAttribute("data-slug")];
      if (!p) return;
      a.setAttribute("aria-label", p.n + ": " + p.s + " diputados");
      if (hi && p.slug === hi) a.classList.add("is-hi");
    });

    function paint() {
      links.forEach(function (a) {
        var p = bySlug[a.getAttribute("data-slug")];
        if (!p) return;
        var path = a.firstElementChild;
        path.style.fill = (hi && p.slug !== hi && layer === "locator") ? "var(--map-empty)" : (layer === "locator" ? "var(--sepia)" : fillFor(layer, p, mini));
      });
      if (legend) renderLegend();
    }

    function renderLegend() {
      legend.textContent = "";
      if (layer === "escanos") {
        [["1–2", 0], ["3", 1], ["4", 2], ["5–6", 3], ["7–11", 4], ["12+", 5]].forEach(function (x) { legend.appendChild(chip(SEQ[x[1]], x[0])); });
        legend.appendChild(note("Diputados que elige cada provincia en 2026"));
      } else if (layer === "lectores") {
        if (!lectores) { legend.appendChild(note("Cargando la votación de los lectores…")); return; }
        if (!lectores.revelado) {
          [["1–4", 1], ["5–19", 2], ["20–99", 3], ["100–499", 4], ["500+", 5]].forEach(function (x) { legend.appendChild(chip(SEQ[x[1]], x[0])); });
          var tv = lectores.total || 0;
          legend.appendChild(note(tv.toLocaleString("es-ES") + (tv === 1 ? " voto simbólico" : " votos simbólicos") + ". El resultado por partido se desvela el 29 de noviembre a las 21:00."));
          return;
        }
        var seen = {};
        for (var s in (lectores.provincias || {})) { var L = leaderOf(lectores.provincias[s]); if (L.total >= 3) seen[L.party] = 1; }
        Object.keys(seen).forEach(function (k) { legend.appendChild(chip(mini.colors[k], mini.names[k] || k)); });
        legend.appendChild(note((lectores.total || 0).toLocaleString("es-ES") + " votos simbólicos · no es una encuesta"));
      } else {
        var seen2 = {};
        mini.p.forEach(function (p) { if (p.r[0]) seen2[p.r[0][0]] = p.r[0][2]; });
        Object.keys(seen2).forEach(function (k) { legend.appendChild(chip(seen2[k], mini.names[k] || k)); });
        legend.appendChild(note("Candidatura más votada en 2023"));
      }
    }
    function chip(color, label) {
      var s = document.createElement("span"); s.className = "legend";
      var i = document.createElement("i"); i.style.background = color; s.appendChild(i);
      s.appendChild(document.createTextNode(label)); return s;
    }
    function note(t) { var s = document.createElement("span"); s.className = "legend legend--note"; s.textContent = t; return s; }

    /* Tarjeta flotante */
    var current = null;
    function fillTip(p) {
      var rows = p.r.slice(0, 3).map(function (r) {
        return '<div class="tipbar"><span>' + esc(mini.names[r[0]] || r[0]) + '</span><b style="--w:' + Math.min(100, r[1] * 2) + '%;--c:' + r[2] + '"></b><em>' + fmt.format(r[1]) + ' %</em></div>';
      }).join("");
      var extra = "";
      if (layer === "lectores" && lectores && !lectores.revelado) {
        var nv = (lectores.participacion || {})[p.slug] || 0;
        extra = '<p class="tip__lect">' + (nv ? "Lectores: " + nv + " voto" + (nv === 1 ? "" : "s") + " simbólico" + (nv === 1 ? "" : "s") : "Aún no hay votos de lectores aquí") + "</p>";
      } else if (layer === "lectores" && lectores) {
        var c = lectores.provincias && lectores.provincias[p.slug];
        var L = c ? leaderOf(c) : { total: 0 };
        extra = '<p class="tip__lect">' + (L.total ? "Lectores: " + L.total + " voto" + (L.total === 1 ? "" : "s") + (L.party ? " · gana " + esc(mini.names[L.party] || L.party) : "") : "Aún no hay votos de lectores aquí") + "</p>";
      }
      tip.innerHTML = '<p class="tip__name">' + esc(p.n) + '</p><p class="tip__seats"><b>' + p.s + "</b> diputados en 2026</p>" +
        '<p class="tip__sub">Resultado 2023</p>' + rows + extra + '<a class="tip__go" href="/provincias/' + p.slug + '/">Ver la provincia</a>';
    }
    function showTip(a, x, y) {
      var p = bySlug[a.getAttribute("data-slug")];
      if (!p || !tip) return;
      if (current !== a) { fillTip(p); if (current) current.classList.remove("is-on"); current = a; a.classList.add("is-on"); }
      var r = root.getBoundingClientRect();
      var tx = x - r.left + 16, ty = y - r.top + 16;
      var w = tip.offsetWidth || 220, h = tip.offsetHeight || 160;
      if (tx + w > r.width) tx = x - r.left - w - 16;
      if (ty + h > r.height) ty = Math.max(0, y - r.top - h - 16);
      tip.style.transform = "translate(" + Math.max(0, tx) + "px," + ty + "px)";
      tip.classList.add("is-open");
    }
    function hideTip() { if (tip) tip.classList.remove("is-open"); if (current) current.classList.remove("is-on"); current = null; }

    var finePointer = window.matchMedia && window.matchMedia("(hover: hover) and (pointer: fine)").matches;
    if (tip) {
      svg.addEventListener("pointermove", function (e) {
        if (e.pointerType !== "mouse") return;
        var a = e.target.closest && e.target.closest("a[data-slug]");
        if (a) showTip(a, e.clientX, e.clientY); else hideTip();
      });
      svg.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse") hideTip(); });
      // En táctil: el primer toque enseña la tarjeta, el enlace de la tarjeta navega.
      svg.addEventListener("click", function (e) {
        var a = e.target.closest && e.target.closest("a[data-slug]");
        if (!a) return;
        if (!finePointer) {
          e.preventDefault();
          var b = a.getBoundingClientRect();
          showTip(a, b.left + b.width / 2, b.top + b.height / 2);
        }
      });
      document.addEventListener("click", function (e) { if (!root.contains(e.target)) hideTip(); });
      svg.addEventListener("focusin", function (e) {
        var a = e.target.closest && e.target.closest("a[data-slug]");
        if (a) { var b = a.getBoundingClientRect(); showTip(a, b.left + b.width / 2, b.top + b.height / 2); }
      });
      svg.addEventListener("focusout", hideTip);
    }

    /* Selector de capas */
    var seg = root.querySelector("[data-layers]");
    if (seg) seg.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-l]");
      if (!b) return;
      layer = b.getAttribute("data-l");
      seg.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      hideTip();
      paint();
      if (layer === "lectores" && !lectores) loadLectores();
    });

    self.repaint = paint;
    paint();
  }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function loadLectores() {
    if (window.E29N_VOTO && window.E29N_VOTO.resultados) {
      window.E29N_VOTO.resultados().then(function (r) { setLectores(r); }).catch(function () {});
    }
  }
  function setLectores(r) { lectores = r; maps.forEach(function (m) { m.repaint(); }); }
  document.addEventListener("e29n:resultados", function (e) { setLectores(e.detail); });

  function init(root) {
    var inline = root.querySelector("script[type='application/json']");
    var miniP = inline ? Promise.resolve(JSON.parse(inline.textContent)) : getJSON("/assets/data/provincias-mini.json");
    var needSvg = !root.querySelector("svg.map__svg");
    var geoP = needSvg ? getJSON("/assets/data/mapa.json") : Promise.resolve(null);
    Promise.all([miniP, geoP]).then(function (res) {
      if (needSvg) {
        var holder = root.querySelector(".map__canvas") || root;
        holder.appendChild(buildSVG(res[1]));
      }
      var m = new Map(root, res[0]);
      maps.push(m);
      if (root.getAttribute("data-layer") === "lectores") loadLectores();
      root.classList.add("is-ready");
    }).catch(function (e) { if (window.console) console.error("[mapa]", e); root.classList.add("is-error"); });
  }

  function boot() {
    var roots = document.querySelectorAll("[data-map]");
    for (var i = 0; i < roots.length; i++) (function (r) { safe(function () { init(r); }); })(roots[i]);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
