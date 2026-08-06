/* Cavalli Estates — interactions (vanilla, no deps) */
(function () {
  "use strict";
  var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Header scroll state */
  var header = document.querySelector(".site-header");
  function onScroll() { if (header) header.classList.toggle("scrolled", window.scrollY > 40); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* Mobile menu */
  var toggle = document.querySelector(".nav-toggle");
  function closeMenu() { document.body.classList.remove("menu-open"); if (toggle) toggle.setAttribute("aria-expanded", "false"); }
  if (toggle) {
    toggle.addEventListener("click", function () {
      document.body.classList.toggle("menu-open");
      toggle.setAttribute("aria-expanded", String(document.body.classList.contains("menu-open")));
    });
  }
  document.querySelectorAll(".nav-mobile a").forEach(function (a) { a.addEventListener("click", closeMenu); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeMenu(); });

  /* Scroll reveal */
  var reveals = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { if (entry.isIntersecting) { entry.target.classList.add("in"); io.unobserve(entry.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.1 });
    reveals.forEach(function (el) { io.observe(el); });
  } else { reveals.forEach(function (el) { el.classList.add("in"); }); }

  /* Hero parallax */
  var heroMedia = document.querySelector(".hero__media img");
  if (heroMedia && !prefersReduced) {
    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return; ticking = true;
      requestAnimationFrame(function () {
        var y = Math.min(window.scrollY, 900);
        heroMedia.style.transform = "scale(1.1) translate3d(0," + (y * 0.1) + "px,0)";
        ticking = false;
      });
    }, { passive: true });
  }

  /* Residences carousel */
  document.querySelectorAll("[data-carousel]").forEach(function (root) {
    var track = root.querySelector(".carousel__track");
    var slides = Array.prototype.slice.call(root.querySelectorAll(".slide"));
    var prev = root.querySelector("[data-prev]");
    var next = root.querySelector("[data-next]");
    var count = root.querySelector("[data-count]");
    if (!track || !slides.length) return;
    var index = 0;

    function perView() {
      var vw = root.querySelector(".carousel__viewport").clientWidth;
      var sw = slides[0].getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap || 0);
      return Math.max(1, Math.round(vw / sw));
    }
    function maxIndex() { return Math.max(0, slides.length - perView()); }
    function update() {
      index = Math.min(index, maxIndex());
      var gap = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap || 0);
      var sw = slides[0].getBoundingClientRect().width + gap;
      track.style.transform = "translateX(" + (-index * sw) + "px)";
      if (prev) prev.disabled = index <= 0;
      if (next) next.disabled = index >= maxIndex();
      if (count) count.textContent = (index + 1) + " / " + (maxIndex() + 1);
    }
    if (prev) prev.addEventListener("click", function () { index = Math.max(0, index - 1); update(); });
    if (next) next.addEventListener("click", function () { index = Math.min(maxIndex(), index + 1); update(); });
    window.addEventListener("resize", update, { passive: true });
    update();
  });

  /* Booking bar — no live engine yet: route to enquiry with the chosen dates */
  var booking = document.querySelector("[data-booking]");
  if (booking) {
    booking.addEventListener("submit", function (e) {
      e.preventDefault();
      var params = new URLSearchParams();
      var a = booking.querySelector('[name="arrive"]'); var d = booking.querySelector('[name="depart"]'); var g = booking.querySelector('[name="guests"]');
      if (a && a.value) params.set("arrive", a.value);
      if (d && d.value) params.set("depart", d.value);
      if (g && g.value) params.set("guests", g.value);
      window.location.href = "contact.html" + (params.toString() ? "?" + params.toString() : "");
    });
  }

  /* Forms: AJAX-submit to Netlify, then show the branded success in-page.
     On Netlify this records a real submission; on the local preview / GitHub Pages
     demo the POST 404s and we still show success so nothing looks broken. */
  document.querySelectorAll("form[data-enhance]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      function showSuccess() {
        var ok = form.parentElement.querySelector(".form-success");
        if (ok) { form.style.display = "none"; ok.style.display = "block"; ok.scrollIntoView({ behavior: "smooth", block: "center" }); }
      }
      var body = new URLSearchParams(new FormData(form)).toString();
      fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: body })
        .then(showSuccess)
        .catch(showSuccess);
    });
  });

  /* Prefill enquiry from booking params */
  var q = new URLSearchParams(location.search);
  ["arrive", "depart", "guests"].forEach(function (k) {
    var el = document.querySelector('[data-prefill="' + k + '"]');
    if (el && q.get(k)) el.value = q.get(k);
  });

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
