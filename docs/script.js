// Portfolio maurux01 — interacciones mínimas, sin dependencias.
(function () {
  "use strict";

  // Año dinámico en el footer
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  // Animar barras de skills al entrar en viewport
  var bars = document.querySelectorAll(".bar i[data-w]");
  function fillBar(el) {
    el.style.width = el.getAttribute("data-w") + "%";
  }
  if ("IntersectionObserver" in window && bars.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            fillBar(entry.target);
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );
    bars.forEach(function (b) { io.observe(b); });
  } else {
    bars.forEach(fillBar);
  }

  // Resaltar link de nav según sección visible
  var links = Array.prototype.slice.call(document.querySelectorAll(".nav-links a"));
  var sections = links
    .map(function (a) { return document.querySelector(a.getAttribute("href")); })
    .filter(Boolean);
  if ("IntersectionObserver" in window && sections.length) {
    var navIo = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var id = "#" + entry.target.id;
          links.forEach(function (a) {
            a.classList.toggle("active", a.getAttribute("href") === id);
          });
        });
      },
      { rootMargin: "-40% 0px -55% 0px" }
    );
    sections.forEach(function (s) { navIo.observe(s); });
  }

  // Formulario de contacto: abre el email del visitante con el mensaje prellenado
  var form = document.getElementById("contactForm");
  var note = document.getElementById("formNote");
  if (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var data = new FormData(form);
      var nombre = String(data.get("nombre") || "").trim();
      var email = String(data.get("email") || "").trim();
      var asunto = String(data.get("asunto") || "").trim();
      var mensaje = String(data.get("mensaje") || "").trim();
      if (!nombre || !email || !asunto || !mensaje) {
        if (note) note.textContent = "Completá todos los campos.";
        return;
      }
      var subject = encodeURIComponent("[Portfolio] " + asunto + " — " + nombre);
      var body = encodeURIComponent(mensaje + "\n\n— " + nombre + " (" + email + ")");
      window.location.href =
        "mailto:mauroinfantefreelancer@gmail.com?subject=" + subject + "&body=" + body;
      if (note) note.textContent = "Abriendo tu cliente de email para enviar el mensaje...";
      form.reset();
    });
  }
})();
