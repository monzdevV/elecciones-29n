/* Votación simbólica de los lectores (no es una encuesta). Guarda el voto en Supabase vía dos funciones públicas. */
(function () {
  "use strict";

  function safe(fn) { try { fn(); } catch (e) { if (window.console) console.error("[voto]", e); } }

  var meta = document.querySelector("meta[name='e29n-voto']");
  var CFG = meta ? meta.getAttribute("content").split("|") : [];
  var URL_ = CFG[0], KEY = CFG[1];

  function rpc(fn, body) {
    if (!URL_ || !KEY) return Promise.reject(new Error("sin-config"));
    return fetch(URL_ + "/rest/v1/rpc/" + fn, {
      method: "POST",
      headers: { "Content-Type": "application/json", apikey: KEY },
      body: JSON.stringify(body || {})
    }).then(function (r) {
      return r.json().then(function (j) {
        if (!r.ok) { var err = new Error((j && j.message) || ("HTTP " + r.status)); err.status = r.status; throw err; }
        return j;
      });
    });
  }

  var lastResults = null;
  function publish(r) {
    lastResults = r;
    try { document.dispatchEvent(new CustomEvent("e29n:resultados", { detail: r })); } catch (e) {}
    return r;
  }
  var pending = null;
  function resultados() {
    if (lastResults) return Promise.resolve(lastResults);
    if (!pending) pending = rpc("e29n_resultados").then(publish).catch(function (e) { pending = null; throw e; });
    return pending;
  }
  window.E29N_VOTO = { resultados: resultados };

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function deviceId() {
    var id = store("e29n-dev");
    if (!id) {
      id = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : (Date.now().toString(36) + Math.random().toString(36).slice(2) + Math.random().toString(36).slice(2));
      store("e29n-dev", id);
    }
    return id;
  }

  var fmt = new Intl.NumberFormat("es-ES", { maximumFractionDigits: 1, minimumFractionDigits: 1 });

  function init(root) {
    var D = JSON.parse(root.querySelector("script[type='application/json']").textContent);
    var form = root.querySelector("form");
    var sel = root.querySelector("select");
    var btn = root.querySelector("[data-submit]");
    var msg = root.querySelector("[data-msg]");
    var out = root.querySelector("[data-results]");
    var bars = root.querySelector("[data-bars]");
    var total = root.querySelector("[data-total]");
    var mine = root.querySelector("[data-mine]");
    var share = root.querySelector("[data-share]");

    var prev = null;
    try { prev = JSON.parse(store("e29n-voto") || "null"); } catch (e) {}
    if (prev) {
      var r0 = form.querySelector("input[value='" + prev.p + "']");
      if (r0) r0.checked = true;
      if (prev.v) sel.value = prev.v;
      mine.textContent = "Ya votaste " + (D.names[prev.p] || prev.p) + ". Puedes cambiar tu voto cuando quieras.";
    }
    var hl = root.getAttribute("data-province");
    if (!prev && hl) sel.value = hl;

    function state(s) { root.setAttribute("data-state", s); }
    function render(r) {
      if (!r) return;
      if (!r.revelado) {
        // Hasta el cierre de urnas solo se muestra la participación (LOREG, art. 69, y doctrina de la JEC).
        var n = r.total || 0;
        bars.innerHTML = '<div class="reveal"><p class="reveal__n"></p><p class="reveal__l"></p>' +
          '<p class="reveal__when">El resultado por partido se desvela el <b>domingo 29 de noviembre a las 21:00</b>, cuando cierran los últimos colegios (Canarias). Antes no se puede mostrar: la ley electoral lo trataría como una encuesta.</p></div>';
        bars.querySelector(".reveal__n").textContent = n.toLocaleString("es-ES");
        bars.querySelector(".reveal__l").textContent = n === 1 ? "voto registrado" : "votos registrados";
        total.textContent = "Votación simbólica: no es una encuesta ni tiene valor estadístico. Solo vota quien entra en la web.";
        out.hidden = false;
        return;
      }
      var arr = Object.keys(r.partidos || {}).map(function (k) { return [k, r.partidos[k]]; }).filter(function (x) { return x[1] > 0; })
        .sort(function (a, b) { return b[1] - a[1]; });
      var sum = r.total || 0;
      bars.innerHTML = "";
      arr.forEach(function (x, i) {
        var pct = sum ? x[1] / sum * 100 : 0;
        var row = document.createElement("div");
        row.className = "vbar";
        row.style.setProperty("--i", i);
        row.innerHTML = '<span class="vbar__p"></span><span class="vbar__t"><span class="vbar__f"></span></span><span class="vbar__v"></span>';
        row.querySelector(".vbar__p").textContent = D.names[x[0]] || x[0];
        var f = row.querySelector(".vbar__f");
        f.style.background = D.colors[x[0]] || "var(--ink-3)";
        f.style.setProperty("--w", (arr[0][1] ? x[1] / arr[0][1] : 0));
        row.querySelector(".vbar__v").textContent = fmt.format(pct) + " %";
        bars.appendChild(row);
      });
      total.textContent = sum ? sum.toLocaleString("es-ES") + " votos simbólicos de lectores. No es una encuesta: solo vota quien entra en la web." : "Todavía no hay votos. Sé el primero.";
      out.hidden = false;
      requestAnimationFrame(function () { root.classList.add("has-results"); });
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var choice = form.querySelector("input[name='partido']:checked");
      if (!choice) { msg.textContent = "Elige una opción."; state("error"); return; }
      if (!sel.value) { msg.textContent = "Elige tu provincia."; sel.focus(); state("error"); return; }
      state("sending");
      btn.disabled = true;
      msg.textContent = "";
      rpc("e29n_votar", { p_partido: choice.value, p_provincia: sel.value, p_dispositivo: deviceId() }).then(function (r) {
        store("e29n-voto", JSON.stringify({ p: choice.value, v: sel.value }));
        mine.textContent = "Voto registrado: " + (D.names[choice.value] || choice.value) + ". Puedes cambiarlo cuando quieras.";
        publish(r);
        render(r);
        state("done");
        if (share) share.hidden = false;
      }).catch(function (err) {
        var m = String(err && err.message || "");
        msg.textContent = /segundos/.test(m) ? "Acabas de votar: espera unos segundos para cambiar el voto."
          : /demasiados/.test(m) ? "Hay demasiados votos desde tu conexión. Inténtalo dentro de un rato."
          : "No se ha podido registrar el voto. Revisa tu conexión e inténtalo de nuevo.";
        state("error");
      }).then(function () { btn.disabled = false; });
    });

    form.addEventListener("change", function () { if (root.getAttribute("data-state") === "error") { msg.textContent = ""; state("idle"); } });

    if (share) {
      share.addEventListener("click", function (e) {
        var a = e.target.closest("[data-net]");
        if (!a) return;
        var text = "He votado en la votación simbólica de las elecciones del 29N. ¿Y tú?";
        var url = location.origin + "/votacion/";
        if (a.getAttribute("data-net") === "copy") {
          e.preventDefault();
          (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () { a.textContent = "Enlace copiado"; }).catch(function () { a.textContent = url; });
          return;
        }
        if (a.getAttribute("data-net") === "native" && navigator.share) { e.preventDefault(); navigator.share({ title: document.title, text: text, url: url }).catch(function () {}); return; }
        var href = a.getAttribute("data-net") === "wa" ? "https://wa.me/?text=" + encodeURIComponent(text + " " + url)
          : "https://twitter.com/intent/tweet?text=" + encodeURIComponent(text) + "&url=" + encodeURIComponent(url);
        a.setAttribute("href", href);
      });
    }

    if (root.hasAttribute("data-autoload") || prev) resultados().then(render).catch(function () {});
  }

  function boot() {
    var roots = document.querySelectorAll("[data-voto]");
    for (var i = 0; i < roots.length; i++) (function (r) { safe(function () { init(r); }); })(roots[i]);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
