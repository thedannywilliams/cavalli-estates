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
      // Take guests to the Residences to SEE availability (on-site), dates carried along.
      window.location.href = "stays.html" + (params.toString() ? "?" + params.toString() : "");
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

  /* Carry dates from the homepage "Check Availability" bar onto the Residences
     overview (notice + links) so guests land on live availability. */
  (function () {
    var q = new URLSearchParams(location.search);
    var a = q.get("arrive"), d = q.get("depart");
    if (!a || !d) return;
    var dq = "?arrive=" + a + "&depart=" + d;
    document.querySelectorAll('a[href="stays-ranchhouse.html"],a[href="stays-villa.html"],a[href="stays-vineyard-house.html"]').forEach(function (el) {
      el.setAttribute("href", el.getAttribute("href").split("?")[0] + dq);
    });
    if (/stays\.html$/.test(location.pathname) || location.pathname.replace(/\/$/, "").endsWith("/stays")) {
      var hero = document.querySelector(".page-hero");
      function fd(s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString("en-US", { month: "short", day: "numeric" }); }
      if (hero) {
        var n = document.createElement("div"); n.className = "section-sm"; n.style.paddingBottom = "0";
        n.innerHTML = '<div class="wrap center"><p class="eyebrow center">Availability</p><p class="body-lead" style="margin:.6rem auto 0">Showing open dates for <strong>' + fd(a) + " – " + fd(d) + "</strong>. Choose a residence below to see its calendar.</p></div>";
        hero.after(n);
      }
    }
  })();

  /* Availability calendar (residence pages) — shows each home's Airbnb-blocked
     dates (view only). Guests pick an open range and inquire DIRECTLY with us. */
  var calRoots = document.querySelectorAll("[data-cal]");
  if (calRoots.length) {
    var calPromise = null;
    function getCalData() {
      if (!calPromise) {
        var url = "/.netlify/functions/availability" + (/[?&]demo\b/.test(location.search) ? "?demo=1" : "");
        calPromise = fetch(url).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
      }
      return calPromise;
    }
    calRoots.forEach(function (root) {
      root.innerHTML = '<p class="cal-loading">Loading availability…</p>';
      var key = root.getAttribute("data-availability");
      getCalData().then(function (j) {
        var busy = (j && j.listings && j.listings[key]) ? new Set(j.listings[key]) : new Set();
        buildCalendar(root, busy);
      });
    });
  }

  function buildCalendar(root, busy) {
    var summary = root.parentElement.querySelector("[data-cal-summary]");
    var today = new Date(); today.setHours(0, 0, 0, 0);
    var minMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    var offset = 0, start = null, end = null;
    var DOW = ["S", "M", "T", "W", "T", "F", "S"];

    function iso(d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
    function parse(s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
    function fmt(s) { return parse(s).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }); }
    function nightsBusy(a, b) { for (var d = parse(a); d < parse(b); d.setDate(d.getDate() + 1)) { if (busy.has(iso(d))) return true; } return false; }

    function pick(ds) {
      if (!start || end) { start = ds; end = null; }
      else if (ds > start) { if (nightsBusy(start, ds)) { start = ds; end = null; } else { end = ds; } }
      else { start = ds; end = null; }
      paint(); updateSummary(); updateFields();
    }
    function paint() {
      root.querySelectorAll(".cal-day").forEach(function (c) {
        var ds = c.dataset.date; if (!ds) return;
        c.classList.remove("sel-start", "sel-end", "in-range");
        if (ds === start) c.classList.add("sel-start");
        if (end && ds === end) c.classList.add("sel-end");
        if (start && end && ds > start && ds < end) c.classList.add("in-range");
      });
    }
    function updateSummary() {
      if (!summary) return;
      if (start && end) {
        summary.innerHTML = "<p><strong>" + fmt(start) + "</strong> &rarr; <strong>" + fmt(end) + "</strong> are open.</p><div class=\"cta-row\"><a class=\"btn gold\" href=\"contact.html?arrive=" + start + "&depart=" + end + "\"><span>Inquire About These Dates</span></a></div>";
      } else if (start) { summary.innerHTML = "<p>Arrival <strong>" + fmt(start) + "</strong> selected — now choose your departure.</p>"; }
      else { summary.innerHTML = "<p>Select your arrival and departure to check availability, then inquire with us directly.</p>"; }
    }
    function monthEl(first) {
      var m = document.createElement("div"); m.className = "cal-month";
      var t = document.createElement("div"); t.className = "cal-month__title";
      t.textContent = first.toLocaleString("en-US", { month: "long", year: "numeric" }); m.appendChild(t);
      var grid = document.createElement("div"); grid.className = "cal-grid";
      DOW.forEach(function (d) { var e = document.createElement("div"); e.className = "cal-dow"; e.textContent = d; grid.appendChild(e); });
      for (var i = 0; i < first.getDay(); i++) { var pad = document.createElement("div"); pad.className = "cal-day empty"; grid.appendChild(pad); }
      var dim = new Date(first.getFullYear(), first.getMonth() + 1, 0).getDate();
      for (var day = 1; day <= dim; day++) {
        var date = new Date(first.getFullYear(), first.getMonth(), day);
        var cell = document.createElement("div"); cell.className = "cal-day"; cell.textContent = day; cell.dataset.date = iso(date);
        if (date < today) cell.classList.add("past");
        else if (busy.has(iso(date))) cell.classList.add("busy");
        else { cell.classList.add("avail"); cell.addEventListener("click", function () { pick(this.dataset.date); }); }
        grid.appendChild(cell);
      }
      m.appendChild(grid); return m;
    }
    function updateFields() {
      var ci = root.querySelector("[data-ci]"), co = root.querySelector("[data-co]");
      if (ci) { ci.textContent = start ? fmt(start) : "Add date"; ci.classList.toggle("empty", !start); }
      if (co) { co.textContent = end ? fmt(end) : "Add date"; co.classList.toggle("empty", !end); }
      var f = root.querySelector(".cal-fields");
      if (f) { f.classList.toggle("active-in", !start || !!end); f.classList.toggle("active-out", !!start && !end); }
    }
    function render() {
      root.innerHTML = "";
      var fields = document.createElement("div"); fields.className = "cal-fields";
      fields.innerHTML = '<div><label>Check-in</label><div class="val empty" data-ci>Add date</div></div><div><label>Check-out</label><div class="val empty" data-co>Add date</div></div>';
      root.appendChild(fields);
      var legend = document.createElement("div"); legend.className = "cal-legend";
      legend.innerHTML = '<span><i></i>Available</span><span><i class="busy"></i>Booked</span><span><i class="sel"></i>Your dates</span>';
      root.appendChild(legend);
      var nav = document.createElement("div"); nav.className = "cal-nav";
      var prev = document.createElement("button"); prev.setAttribute("aria-label", "Previous months"); prev.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M15 5l-7 7 7 7"/></svg>';
      var next = document.createElement("button"); next.setAttribute("aria-label", "Next months"); next.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 5l7 7-7 7"/></svg>';
      var label = document.createElement("span"); label.className = "cal-nav__label";
      var base = new Date(minMonth.getFullYear(), minMonth.getMonth() + offset, 1);
      label.textContent = base.toLocaleString("en-US", { month: "short", year: "numeric" });
      prev.disabled = offset <= 0;
      prev.addEventListener("click", function () { if (offset > 0) { offset -= 2; if (offset < 0) offset = 0; render(); } });
      next.addEventListener("click", function () { offset += 2; render(); });
      nav.appendChild(prev); nav.appendChild(label); nav.appendChild(next); root.appendChild(nav);
      var wrap = document.createElement("div"); wrap.className = "cal-months";
      wrap.appendChild(monthEl(new Date(base.getFullYear(), base.getMonth(), 1)));
      wrap.appendChild(monthEl(new Date(base.getFullYear(), base.getMonth() + 1, 1)));
      root.appendChild(wrap);
      paint(); updateFields();
    }
    render(); updateSummary();

    // Pre-select dates carried from the homepage / Residences overview
    var pq = new URLSearchParams(location.search);
    var pa = pq.get("arrive"), pd = pq.get("depart");
    if (pa && pd && pd > pa && !busy.has(pa) && !nightsBusy(pa, pd)) {
      start = pa; end = pd;
      var ad = parse(pa);
      var diff = (ad.getFullYear() - minMonth.getFullYear()) * 12 + (ad.getMonth() - minMonth.getMonth());
      offset = Math.max(0, diff - (diff % 2));
      render(); updateSummary();
      setTimeout(function () { root.scrollIntoView({ behavior: "smooth", block: "center" }); }, 300);
    }
  }
})();
