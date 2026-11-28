#!/usr/bin/env python3
"""Build the v2 ("quiet luxury") version of the Cavalli Estates site.

Reads the original pages in the site root and writes restyled copies to v2/.
The originals are never modified. Run from anywhere:

    python3 tools/build_v2.py

What changes on each page:
  * header + phone menu  -> Menu / logo / Availability / Reserve + full-screen menu
  * footer               -> the v2 footer
  * css/v2.css and js/v2.js are added (style.css and main.js stay, so the shop,
    forms, calendar, lightbox and cookie banner keep working)
  * h1/h2 headings become title case with one italic phrase
The home page is built from concept.html (the approved home design).

v2 pages keep the same relative paths as the originals (assets/, css/, js/);
netlify.toml rewrites /v2/assets, /v2/css and /v2/js to the real folders.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "v2")
SKIP = {"concept.html", "index.html"}

HEADER = '''<!-- Header: menu, logo, two actions -->
<header class="c-header" id="top">
  <button class="c-menu-btn" type="button" aria-expanded="false" aria-controls="c-menu"><i aria-hidden="true"></i><span>Menu</span></button>
  <a href="index.html" aria-label="Cavalli Estates home"><span class="c-logo" aria-hidden="true"></span></a>
  <nav class="c-actions" aria-label="Quick links">
    <a class="hide-s" href="stays.html">Availability</a>
    <a href="contact.html">Reserve</a>
  </nav>
</header>

<!-- Full-screen menu -->
<nav class="c-menu" id="c-menu" aria-label="Site">
  <div class="c-menu__grid">
    <div>
      <h3>Stay</h3>
      <ul>
        <li><a href="stays.html">The Residences</a></li>
        <li><a href="stays-ranchhouse.html">The Ranchhouse</a></li>
        <li><a href="stays-villa.html">The Villa</a></li>
        <li><a href="stays-vineyard-house.html">The Vineyard House</a></li>
      </ul>
    </div>
    <div>
      <h3>Gather</h3>
      <ul>
        <li><a href="events.html">Weddings &amp; Events</a></li>
        <li><a href="events-weddings.html">Weddings</a></li>
        <li><a href="events-retreats.html">Corporate Retreats</a></li>
        <li><a href="events-celebrations.html">Private Celebrations</a></li>
      </ul>
    </div>
    <div>
      <h3>The Farm</h3>
      <ul>
        <li><a href="lavender.html">The Lavender Farm</a></li>
        <li><a href="sanctuary.html">Meet the Herd</a></li>
        <li><a href="equestrian.html">Equestrian</a></li>
        <li><a href="shop.html">Shop</a></li>
      </ul>
    </div>
    <div>
      <h3>Visit</h3>
      <ul>
        <li><a href="experiences.html">Experiences</a></li>
        <li><a href="tasting-room.html">Tasting Room</a></li>
        <li><a href="restaurant.html">The Restaurant</a></li>
        <li><a href="about.html">About Us</a></li>
      </ul>
    </div>
  </div>
  <div class="c-menu__side">
    <div>
      <h3>Location</h3>
      <p>445 Green Gate Road<br>San Luis Obispo, CA 93401</p>
    </div>
    <div>
      <h3>Contact</h3>
      <p><a href="tel:+18052421154">805 · 242 · 1154</a></p>
    </div>
    <figure class="c-menu__photo"><img src="assets/img/twilight/CavalliTwilight06.jpg" alt="The Ranchhouse at dusk, windows glowing beyond the brick garden paths" loading="lazy" /></figure>
  </div>
  <div class="c-menu__foot"><a href="contact.html">Reserve</a><a href="privacy.html">Privacy &amp; Cookies</a></div>
</nav>
'''

FOOTER = '''<footer class="c-foot">
  <div class="c-foot__top">
    <a href="index.html" aria-label="Cavalli Estates home"><span class="c-foot__logo" aria-hidden="true"></span></a>
    <div class="c-foot__cols">
      <div><h3>Stay</h3><ul><li><a href="stays.html">The Residences</a></li><li><a href="stays-ranchhouse.html">The Ranchhouse</a></li><li><a href="stays-villa.html">The Villa</a></li><li><a href="stays-vineyard-house.html">The Vineyard House</a></li></ul></div>
      <div><h3>The Estate</h3><ul><li><a href="events.html">Weddings &amp; Events</a></li><li><a href="lavender.html">The Lavender Farm</a></li><li><a href="sanctuary.html">Meet the Herd</a></li><li><a href="equestrian.html">Equestrian</a></li></ul></div>
      <div><h3>Visit</h3><ul><li><a href="experiences.html">Experiences</a></li><li><a href="tasting-room.html">Tasting Room</a></li><li><a href="restaurant.html">The Restaurant</a></li><li><a href="shop.html">Shop</a></li></ul></div>
      <div><h3>Contact</h3><ul><li><a href="tel:+18052421154">805 · 242 · 1154</a></li><li><a href="https://maps.google.com/?q=445+Green+Gate+Road,+San+Luis+Obispo,+CA+93401" target="_blank" rel="noopener">445 Green Gate Road<br>San Luis Obispo, CA 93401</a></li><li><a href="about.html">About Us</a></li></ul></div>
    </div>
  </div>
  <div class="c-foot__bottom"><span>© <span data-year>2026</span> Cavalli Estates</span><span class="grp"><a href="privacy.html">Privacy &amp; Cookies</a><button type="button" data-cookie-settings>Cookie Settings</button></span></div>
</footer>'''

SMALL = {"a", "an", "the", "and", "but", "or", "nor", "for", "on", "at", "to", "from", "by", "of", "in", "with", "as"}
TOKEN = re.compile(r"(<br\s*/?>|\s+)")
PHRASES = [["the", "vineyard", "house"], ["edna", "valley"], ["cavalli", "estates"], ["gio", "&amp;", "lisa"]]


def cap(word):
    """Capitalize the first letter of a lowercase word, leaving entities, numbers and existing capitals alone."""
    if any(ch.isupper() for ch in word):
        return word
    m = re.match(r"^((?:&[a-z]+;|[^A-Za-z&])*)([a-z])(.*)$", word, re.S)
    return (m.group(1) + m.group(2).upper() + m.group(3)) if m else word


def restyle_heading(inner):
    """Title-case a heading and wrap one closing phrase in <em>."""
    if re.search(r"<(?!br\s*/?>)", inner):          # nested tags: leave as written
        return inner
    parts = TOKEN.split(inner.strip())
    idx = [i for i, p in enumerate(parts) if p and not TOKEN.fullmatch(p)]
    if not idx:
        return inner
    for n, i in enumerate(idx):
        w = parts[i]
        core = re.sub(r"[^A-Za-z]", "", w)
        if n > 0 and core in SMALL:
            continue
        parts[i] = cap(w)
    words = [parts[i] for i in idx]
    start = None
    low = [w.lower() for w in words]
    commas = [n for n, w in enumerate(words[:-1]) if w.rstrip().endswith(",")]
    phrase = next((ph for ph in PHRASES if low[-len(ph):] == ph and len(words) > len(ph)), None)
    if len(words) <= 2:
        start = None                                  # short headings and names stay plain
    elif phrase:
        start = len(words) - len(phrase)              # a proper name is italicized whole
    elif commas and 1 <= len(words) - 1 - commas[-1] <= 3:
        start = commas[-1] + 1
    elif re.sub(r"[^A-Za-z]", "", words[-2]).lower() in SMALL:
        start = len(words) - 2
    else:
        start = len(words) - 1
    if start is not None:
        parts[idx[start]] = "<em>" + parts[idx[start]]
        parts[idx[-1]] = parts[idx[-1]] + "</em>"
    return "".join(parts)


def convert(name, s):
    s, n = re.subn(r"<!-- Header -->\s*", "", s)
    s, n1 = re.subn(r'<header class="site-header".*?</header>\s*(?:<!-- Mobile drawer -->\s*)?<nav class="nav-mobile".*?</nav>', lambda m: HEADER, s, flags=re.S)
    s, n2 = re.subn(r'<footer class="site-footer">.*?</footer>', lambda m: FOOTER, s, flags=re.S)
    assert n1 == 1 and n2 == 1, (name, n1, n2)
    assert 'href="css/style.css"' in s, name
    s = s.replace('<link rel="stylesheet" href="css/style.css" />', '<link rel="stylesheet" href="css/style.css" />\n<link rel="stylesheet" href="css/v2.css" />', 1)
    s = s.replace("</title>", "</title>\n<meta name=\"robots\" content=\"noindex, nofollow\" />", 1)
    s, n3 = re.subn(r"<body([^>]*)>", lambda m: '<body class="v2"%s>' % m.group(1), s, count=1)
    assert n3 == 1, name
    s = re.sub(r"<(h1|h2)((?:\s[^>]*)?)>(.*?)</\1>", lambda m: "<%s%s>%s</%s>" % (m.group(1), m.group(2), restyle_heading(m.group(3)), m.group(1)), s, flags=re.S)
    assert "</body>" in s
    s = s.replace("</body>", '<script src="js/v2.js"></script>\n</body>', 1)
    return s


EXPLORE = '''<!-- Where will the day take you -->
<section class="c-sec" style="padding-top:0">
  <div class="c-explore__head reveal">
    <p class="label">On the Estate &amp; Nearby</p>
    <h2 class="display d-l">Where Will the Day <em>Take You?</em></h2>
  </div>
  <div class="c-explore__list">
    <article class="c-card reveal">
      <a class="ph" href="experiences.html"><img src="assets/img/nature/Fishing-in-big-pond-scaled-1.jpg" alt="Casting a line on the estate's stocked pond beneath the Edna Valley hills" loading="lazy" /></a>
      <h3>Experiences</h3>
      <p>Fishing, bridle trails, treehouse dining, and picnics in the lavender.</p>
    </article>
    <article class="c-card reveal d1">
      <a class="ph" href="equestrian.html"><img src="assets/img/equestrian/center-breezeway.jpg" alt="The shaded stable breezeway at golden hour, stall doors in warm redwood" loading="lazy" /></a>
      <h3>Equestrian</h3>
      <p>A training center for horse and rider, and a gentle retirement sanctuary.</p>
    </article>
    <article class="c-card reveal">
      <a class="ph" href="tasting-room.html"><img src="assets/img/tasting/tasting-patio-hero.jpg" alt="Lounge chairs on the tasting patio beneath the oaks, looking across the vineyards" loading="lazy" /></a>
      <h3>Tasting Room</h3>
      <p>Small-production SLO Coast wines, just down the road at Edna.</p>
    </article>
    <article class="c-card reveal d1">
      <a class="ph" href="restaurant.html"><img src="assets/img/restaurant/edna-dining-room-vineyard-view.jpg" alt="The dining room at The Restaurant at Edna, windows framing the vineyards" loading="lazy" /></a>
      <h3>The Restaurant</h3>
      <p>Seasonal cooking from Jeremy Fox, 2.4 miles from the estate.</p>
    </article>
  </div>
</section>

'''


def build_home():
    s = open(os.path.join(ROOT, "concept.html"), encoding="utf-8").read()
    s = s.replace("<title>Cavalli Estates | Home Page Concept</title>", "<title>Cavalli Estates | A Luxury Estate in Edna Valley, San Luis Obispo</title>")
    s = s.replace('<link rel="stylesheet" href="css/concept.css" />', '<link rel="stylesheet" href="css/style.css" />\n<link rel="stylesheet" href="css/v2.css" />')
    s = s.replace("<body>", '<body class="v2 v2-home">', 1)
    s = s.replace('href="concept.html"', 'href="index.html"')
    a = s.index("<footer class=\"c-foot\">"); b = s.index("</footer>", a) + len("</footer>")
    s = s[:a] + FOOTER + s[b:]
    anchor = "<!-- Guest line -->"
    assert s.count(anchor) == 1
    s = s.replace(anchor, EXPLORE + anchor)
    s = s.replace('<script src="js/concept.js"></script>', '<script src="js/main.js" defer></script>\n<script src="js/v2.js"></script>')
    return s


def main():
    os.makedirs(OUT, exist_ok=True)
    done = []
    for name in sorted(os.listdir(ROOT)):
        if not name.endswith(".html") or name in SKIP:
            continue
        s = open(os.path.join(ROOT, name), encoding="utf-8").read()
        open(os.path.join(OUT, name), "w", encoding="utf-8").write(convert(name, s))
        done.append(name)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(build_home())
    done.append("index.html")
    print("v2: %d pages -> %s" % (len(done), OUT))


if __name__ == "__main__":
    main()
