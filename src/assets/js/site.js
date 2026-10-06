/* Comportamiento común: menú móvil y cuenta atrás. */
(function () {
  "use strict";

  function safe(fn) { try { fn(); } catch (e) { if (window.console) console.error("[site]", e); } }

  function menu() {
    var btn = document.querySelector("[data-menu]");
    var drawer = document.getElementById("drawer");
    if (!btn || !drawer) return;
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
      drawer.hidden = open;
    });
  }

  /* Cuenta atrás hasta la apertura de colegios: 29/11/2026 09:00 (hora peninsular, CET). */
  function countdown() {
    var nodes = document.querySelectorAll("[data-countdown]");
    if (!nodes.length) return;
    var target = Date.UTC(2026, 10, 29, 8, 0, 0);
    var close = Date.UTC(2026, 10, 29, 19, 0, 0);
    var now = Date.now();
    var txt;
    if (now < target) {
      var days = Math.ceil((target - now) / 86400000);
      txt = days === 1 ? "Mañana se vota" : "Faltan " + days + " días";
    } else if (now < close) {
      txt = "Hoy se vota, hasta las 20:00";
    } else {
      txt = "Elecciones celebradas";
    }
    for (var i = 0; i < nodes.length; i++) nodes[i].textContent = txt;
  }

  /* Cuenta atrás grande de la portada: días, horas y minutos. */
  function bigCountdown() {
    var box = document.querySelector("[data-cd]");
    if (!box) return;
    var d = box.querySelector("[data-cd-d]"), h = box.querySelector("[data-cd-h]"), m = box.querySelector("[data-cd-m]");
    var target = Date.UTC(2026, 10, 29, 8, 0, 0);
    function pad(n) { return n < 10 ? "0" + n : String(n); }
    function tick() {
      var ms = Math.max(0, target - Date.now());
      var mins = Math.floor(ms / 60000);
      d.textContent = String(Math.floor(mins / 1440));
      h.textContent = pad(Math.floor(mins % 1440 / 60));
      m.textContent = pad(mins % 60);
    }
    tick();
    setInterval(tick, 20000);
  }

  /* Marca el próximo hito del calendario. */
  function timeline() {
    var items = document.querySelectorAll(".timeline li[data-date]");
    if (!items.length) return;
    var today = new Date(); today.setHours(0, 0, 0, 0);
    var marked = false;
    for (var i = 0; i < items.length; i++) {
      var d = new Date(items[i].getAttribute("data-date") + "T00:00:00");
      var end = items[i].getAttribute("data-end") ? new Date(items[i].getAttribute("data-end") + "T00:00:00") : d;
      if (end < today) items[i].classList.add("past");
      else if (!marked) { items[i].classList.add("next"); marked = true; }
    }
  }

  function boot() { safe(menu); safe(countdown); safe(bigCountdown); safe(timeline); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
