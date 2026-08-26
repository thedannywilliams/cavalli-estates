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

  /* Booking bar — tied to Airbnb availability via /.netlify/functions/availability.
     Unavailable (fully booked) dates are flagged; dates default to today+. Until the
     client's Airbnb iCal URLs are set in Netlify env vars, availability is unrestricted. */
  var booking = document.querySelector("[data-booking]");
  if (booking) {
    var arrive = booking.querySelector('[name="arrive"]');
    var depart = booking.querySelector('[name="depart"]');
    var guests = booking.querySelector('[name="guests"]');
    var todayISO = new Date().toISOString().slice(0, 10);
    [arrive, depart].forEach(function (i) { if (i) i.min = todayISO; });

    var fullyBooked = null;
    fetch("/.netlify/functions/availability")
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) { if (j && j.fullyBooked) fullyBooked = new Set(j.fullyBooked); })
      .catch(function () {});

    var note = document.createElement("p");
    note.style.cssText = "display:none;margin:.7rem auto 0;text-align:center;font-family:var(--sans);font-size:.8rem;color:#FAF7F0;background:rgba(20,17,14,.6);padding:.55rem 1rem;max-width:40rem;";
    booking.parentElement.appendChild(note);

    function rangeDates(a, b) {
      var out = [], d = new Date(a), end = new Date(b);
      for (; d < end; d.setUTCDate(d.getUTCDate() + 1)) out.push(d.toISOString().slice(0, 10));
      return out;
    }

    booking.addEventListener("submit", function (e) {
      e.preventDefault();
      note.style.display = "none";
      if (fullyBooked && fullyBooked.size && arrive.value && depart.value) {
        var conflict = rangeDates(arrive.value, depart.value).some(function (d) { return fullyBooked.has(d); });
        if (conflict) {
          note.textContent = "Some of those nights are already booked. Please choose other dates, or send an inquiry and we'll help you find a stay.";
          note.style.display = "block";
          return;
        }
      }
      var params = new URLSearchParams();
      if (arrive && arrive.value) params.set("arrive", arrive.value);
      if (depart && depart.value) params.set("depart", depart.value);
      if (guests && guests.value) params.set("guests", guests.value);
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

  /* Prefill inquiry from booking params */
  var q = new URLSearchParams(location.search);
  ["arrive", "depart", "guests"].forEach(function (k) {
    var el = document.querySelector('[data-prefill="' + k + '"]');
    if (el && q.get(k)) el.value = q.get(k);
  });

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* Per-home availability check (residence pages) — validates against that
     listing's Airbnb calendar via /.netlify/functions/availability. */
  var availForms = document.querySelectorAll("[data-availability]");
  if (availForms.length) {
    var availPromise = null;
    function getAvail() {
      if (!availPromise) availPromise = fetch("/.netlify/functions/availability").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
      return availPromise;
    }
    availForms.forEach(function (form) {
      var key = form.getAttribute("data-availability");
      var airbnb = form.getAttribute("data-airbnb") || "#";
      var arrive = form.querySelector('[name="arrive"]');
      var depart = form.querySelector('[name="depart"]');
      var result = form.parentElement.querySelector("[data-avail-result]");
      var todayISO = new Date().toISOString().slice(0, 10);
      [arrive, depart].forEach(function (i) { if (i) i.min = todayISO; });

      function show(msg, cls, ctas) {
        if (!result) return;
        result.className = "avail-result " + (cls || "");
        result.innerHTML = "<p>" + msg + "</p>" + (ctas ? '<div class="cta-row">' + ctas + "</div>" : "");
        result.hidden = false;
        result.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        if (!arrive.value || !depart.value || depart.value <= arrive.value) {
          show("Please choose an arrival date and a later departure date.", "", "");
          return;
        }
        var q = "?arrive=" + arrive.value + "&depart=" + depart.value;
        getAvail().then(function (j) {
          var busy = (j && j.listings && j.listings[key]) ? new Set(j.listings[key]) : new Set();
          var days = [], d = new Date(arrive.value), end = new Date(depart.value);
          for (; d < end; d.setUTCDate(d.getUTCDate() + 1)) days.push(d.toISOString().slice(0, 10));
          var conflict = days.some(function (x) { return busy.has(x); });
          if (!j || !j.configured) {
            show("Send us your dates and we’ll confirm availability right away.", "open",
              '<a class="btn gold" href="contact.html' + q + '"><span>Inquire</span></a> <a class="btn outline" href="' + airbnb + '" target="_blank" rel="noopener"><span>Book on Airbnb</span></a>');
          } else if (conflict) {
            show("Those dates are booked. Try different dates, or send an inquiry and we’ll help you find a stay.", "busy",
              '<a class="btn gold" href="contact.html' + q + '"><span>Inquire</span></a>');
          } else {
            show("Good news — those dates look open. Reserve now to lock them in.", "open",
              '<a class="btn gold" href="' + airbnb + '" target="_blank" rel="noopener"><span>Book on Airbnb</span></a> <a class="btn outline" href="contact.html' + q + '"><span>Inquire Directly</span></a>');
          }
        });
      });
    });
  }
})();
