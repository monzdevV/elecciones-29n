/* Test de afinidad política — todo en el navegador, sin guardar respuestas. */
(function () {
  "use strict";

  function safe(fn) { try { fn(); } catch (e) { if (window.console) console.error("[test]", e); } }

  var LABELS = [
    { v: 2, t: "Muy de acuerdo" },
    { v: 1, t: "De acuerdo" },
    { v: 0, t: "Neutral" },
    { v: -1, t: "En desacuerdo" },
    { v: -2, t: "Muy en desacuerdo" }
  ];

  function init(root) {
    var D = JSON.parse(root.querySelector("script[type='application/json']").textContent);
    var Q = D.preguntas, P = D.partidos;
    var answers = new Array(Q.length);
    var idx = 0;

    var stage = root.querySelector("[data-stage]");
    var topic = root.querySelector("[data-topic]");
    var qtext = root.querySelector("[data-q]");
    var count = root.querySelector("[data-count]");
    var bar = root.querySelector("[data-progress]");
    var scale = root.querySelector("[data-scale]");
    var prev = root.querySelector("[data-prev]");
    var skip = root.querySelector("[data-skip]");
    var result = root.querySelector("[data-result]");
    var resList = root.querySelector("[data-reslist]");
    var restart = root.querySelector("[data-restart]");

    var buttons = LABELS.map(function (l) {
      var b = document.createElement("button");
      b.type = "button"; b.textContent = l.t; b.setAttribute("aria-pressed", "false");
      b.addEventListener("click", function () { answer(l.v); });
      scale.appendChild(b);
      return b;
    });

    function render() {
      var q = Q[idx];
      topic.textContent = q.tema;
      qtext.textContent = q.texto;
      count.textContent = "Pregunta " + (idx + 1) + " de " + Q.length;
      bar.style.transform = "scaleX(" + (idx / Q.length) + ")";
      buttons.forEach(function (b, i) { b.setAttribute("aria-pressed", String(answers[idx] === LABELS[i].v)); });
      prev.disabled = idx === 0;
    }

    function answer(v) {
      answers[idx] = v;
      if (idx < Q.length - 1) { idx++; render(); } else finish();
    }

    function finish() {
      var answered = 0;
      var scores = P.map(function (p) {
        var got = 0, max = 0;
        Q.forEach(function (q, i) {
          if (answers[i] == null) return;
          var pos = q.posiciones[p.id];
          if (pos == null) return;
          max += 4;
          got += 4 - Math.abs(answers[i] - pos);
        });
        return { p: p, pct: max ? Math.round(got / max * 100) : 0 };
      });
      answers.forEach(function (a) { if (a != null) answered++; });
      scores.sort(function (a, b) { return b.pct - a.pct; });
      resList.textContent = "";
      scores.forEach(function (s) {
        var row = document.createElement("div"); row.className = "bar";
        var n = document.createElement("span"); n.className = "p"; n.textContent = s.p.nombre_corto || s.p.id;
        var tr = document.createElement("div"); tr.className = "bar__track";
        var f = document.createElement("div"); f.className = "bar__fill"; f.style.background = s.p.color; f.style.width = s.pct + "%";
        tr.appendChild(f);
        var v = document.createElement("span"); v.className = "s"; v.textContent = s.pct + " %";
        row.appendChild(n); row.appendChild(tr); row.appendChild(v);
        resList.appendChild(row);
      });
      root.querySelector("[data-answered]").textContent = answered;
      bar.style.transform = "scaleX(1)";
      stage.hidden = true;
      result.hidden = false;
      result.focus({ preventScroll: false });
    }

    prev.addEventListener("click", function () { if (idx > 0) { idx--; render(); } });
    skip.addEventListener("click", function () { answers[idx] = null; if (idx < Q.length - 1) { idx++; render(); } else finish(); });
    restart.addEventListener("click", function () {
      answers = new Array(Q.length); idx = 0; result.hidden = true; stage.hidden = false; render();
    });
    document.addEventListener("keydown", function (e) {
      if (stage.hidden || e.target.tagName === "INPUT") return;
      var n = parseInt(e.key, 10);
      if (n >= 1 && n <= 5) answer(LABELS[n - 1].v);
    });
    render();
  }

  function boot() {
    var r = document.querySelector("[data-quiz]");
    if (r) safe(function () { init(r); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
