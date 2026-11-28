/* Cavalli Estates: home page concept. Header state, menu, scroll reveals. */
(function () {
  "use strict";
  var header = document.querySelector(".c-header");
  var heroText = document.querySelector(".c-hero__line");
  var limit = 120, tall = 0;
  // Solid header just before the hero's words would slide up under the logo.
  function measure() {
    if (!header.classList.contains("scrolled")) tall = header.offsetHeight;
    limit = Math.max(24, heroText.getBoundingClientRect().top + window.scrollY - tall - 48);
    onScroll();
  }
  function onScroll() { header.classList.toggle("scrolled", window.scrollY > limit); }
  measure();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", measure);
  window.addEventListener("load", measure);

  var btn = document.querySelector(".c-menu-btn");
  function setMenu(open) {
    document.body.classList.toggle("menu-open", open);
    btn.setAttribute("aria-expanded", String(open));
    var label = btn.querySelector("span");
    if (label) label.textContent = open ? "Close" : "Menu";
  }
  btn.addEventListener("click", function () { setMenu(!document.body.classList.contains("menu-open")); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });

  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  var today = new Date().toISOString().slice(0, 10);
  document.querySelectorAll('.c-avail input[type="date"]').forEach(function (i) {
    i.min = today;
    function mark() { i.parentElement.classList.toggle("has-value", !!i.value); }
    i.addEventListener("input", mark);
    i.addEventListener("change", mark);
    mark();
  });
})();
