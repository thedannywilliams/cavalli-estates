"""
Rebuild the shop from shop-data/catalog.py.

    python3 shop-data/build_shop.py

Writes:
  shop.html                      product grid, collection filters, product data
  shop-data/shopify-products.csv Shopify product import (Products > Import)
"""
import csv, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from catalog import COLLECTIONS, PRODUCTS  # noqa: E402

LIVE = "https://cavalliestates.netlify.app"
IMG_DIR = "assets/img/shop/p"
COLL = dict(COLLECTIONS)
counts = json.load(open(os.path.join(HERE, "photo-counts.json")))
REV = json.load(open(os.path.join(HERE, "etsy-reviews.json"), encoding="utf-8"))
# Products added after the first Shopify import; written to shopify-new-products.csv.
NEW_IN_SHOPIFY = ["linen-mist-set"]
MONTHS = "January February March April May June July August September October November December".split()


def month_year(d):
    m = re.match(r"(\w{3}) \d{1,2}, (\d{4})", d)
    return "%s %s" % (next(x for x in MONTHS if x.startswith(m.group(1))), m.group(2)) if m else d


def reviews_for(handle):
    rs = [r for r in REV["reviews"] if r["handle"] == handle]
    shown = [{"n": "Customer" if r["name"].lower() == "etsy buyer" else r["name"], "d": month_year(r["date"]), "r": r["rating"], "t": r["text"]} for r in rs if not r["hide"]]
    avg = round(sum(r["rating"] for r in rs) / len(rs), 1) if rs else None
    return avg, len(rs), shown


def esc(s):
    return html.escape(s, quote=True)


def norm_value(v, base):
    """('Label', price, 'sold out') | ('Label', price) | 'Label' -> dict"""
    if isinstance(v, str):
        return {"v": v, "p": None, "out": False}
    return {"v": v[0], "p": v[1] if len(v) > 1 else None, "out": len(v) > 2 and v[2] == "sold out"}


def product_record(p):
    opts = [{"name": n, "values": [norm_value(v, p["price"]) for v in vals]} for n, vals in p["options"]]
    prices = [v["p"] for o in opts for v in o["values"] if v["p"] is not None and not v["out"]]
    low = min(prices) if prices else p["price"]
    high = max(prices) if prices else p["price"]
    n = counts.get(p["handle"], 1)
    imgs = ["%s/%s-%d.jpg" % (IMG_DIR, p["handle"], i) for i in range(1, n + 1)]
    avg, nrev, shown = reviews_for(p["handle"])
    return {
        "notes": bool(p.get("notes")), "rating": avg, "reviewCount": nrev, "reviews": shown,
        "handle": p["handle"], "title": p["title"], "tag": p["tag"], "collection": p["collection"],
        "collectionName": COLL[p["collection"]], "price": p["price"], "low": low, "high": high,
        "blurb": p["blurb"], "body": p["body"], "details": p["details"], "options": opts,
        "card": "%s/%s-card.jpg" % (IMG_DIR, p["handle"]), "images": imgs,
    }


def money(x):
    return "$%.2f" % x


# Products marked hidden=True in catalog.py stay off the site and out of the Shopify CSV.
records = [product_record(p) for p in PRODUCTS if not p.get("hidden")]

# ---------------------------------------------------------------- shop.html
cards = []
for r in records:
    price = money(r["low"]) if r["low"] == r["high"] else "From " + money(r["low"])
    cards.append(
        '      <article class="product" data-collection="%(c)s">\n'
        '        <div class="product__media"><img src="%(card)s" alt="%(alt)s" loading="lazy" width="900" height="1125" /><span class="product__tag">%(tag)s</span></div>\n'
        '        <img class="product__mark" src="assets/img/brand/icon-192.png" alt="" aria-hidden="true" loading="lazy" />\n'
        '        <h3 class="product__name">%(title)s</h3>\n'
        '        <p class="product__desc">%(blurb)s</p>\n'
        '%(rating)s'
        '        <p class="product__price">%(price)s</p>\n'
        '        <div class="product__buy" data-product="%(h)s">\n'
        '          <button class="btn gold" type="button" data-open-product><span>View Item</span></button>\n'
        '        </div>\n'
        '      </article>' % dict(
            c=r["collection"], card=r["card"], alt=esc(r["title"] + ", from the Cavalli lavender farm"),
            tag=esc(r["tag"]), title=esc(r["title"]), blurb=esc(r["blurb"]), price=price, h=r["handle"],
            rating=('        <p class="product__rating" aria-label="Rated %.1f out of 5 from %d review%s"><span aria-hidden="true">&#9733;</span> %.1f <span>(%d)</span></p>\n'
                    % (r["rating"], r["reviewCount"], "" if r["reviewCount"] == 1 else "s", r["rating"], r["reviewCount"])) if r["reviewCount"] else ""))

chips = ['<button type="button" class="shop-filter is-on" data-filter="all" aria-pressed="true">All <span>%d</span></button>' % len(records)]
for key, name in COLLECTIONS:
    n = sum(1 for r in records if r["collection"] == key)
    chips.append('<button type="button" class="shop-filter" data-filter="%s" aria-pressed="false">%s <span>%d</span></button>' % (key, esc(name), n))

data = json.dumps({r["handle"]: r for r in records}, ensure_ascii=False, separators=(",", ":"))
data = data.replace("</", "<\\/")

section = """<!-- Products -->
<section class="section" style="padding-top:0" id="products">
  <div class="wrap-wide">
    <div class="shop-filters" role="toolbar" aria-label="Filter products by collection" data-reveal>
      %s
    </div>
    <div class="products" data-reveal>

%s

    </div>
    <div class="pay-strip" data-reveal>
      <p class="pay-strip__title">We accept all major credit &amp; debit cards</p>
      <ul class="pay-marks" aria-label="Accepted cards">
        <li class="pay-mark"><img src="assets/img/pay/visa.svg" alt="Visa" /></li>
        <li class="pay-mark"><img src="assets/img/pay/mastercard.svg" alt="Mastercard" /></li>
        <li class="pay-mark"><img src="assets/img/pay/americanexpress.svg" alt="American Express" /></li>
        <li class="pay-mark"><img src="assets/img/pay/discover.svg" alt="Discover" /></li>
      </ul>
      <p class="pay-strip__note">Secure checkout by Shopify &middot; Shipping and tax calculated at checkout</p>
    </div>
  </div>
  <script type="application/json" id="shop-catalog">%s</script>
</section>

""" % ("\n      ".join(chips), "\n\n".join(cards), data)

# ---------------------------------------------------------- Shop reviews
STAR = "&#9733;"


def stars(n):
    return STAR * n + '<span class="review-card__dim">%s</span>' % (STAR * (5 - n)) if n < 5 else STAR * 5


def item_name(r):
    if r["handle"]:
        return next(p["title"] for p in PRODUCTS if p["handle"] == r["handle"])
    return r["item"] or "Past order"


def display_name(r):
    return "Customer" if r["name"].lower() == "etsy buyer" else r["name"]


def review_card(r, cls="review-card"):
    return ('      <figure class="%s">\n'
            '        <p class="review-card__stars" aria-label="Rated %d out of 5">%s</p>\n'
            '        <blockquote>&ldquo;%s&rdquo;</blockquote>\n'
            '        <figcaption><b>%s</b><span>%s</span><span>%s</span></figcaption>\n'
            '      </figure>') % (cls, r["rating"], stars(r["rating"]), esc(r["text"]).replace("\n", "<br>"),
                                   esc(display_name(r)), esc(item_name(r)), month_year(r["date"]))


visible = [r for r in REV["reviews"] if not r["hide"]]
featured = [r for r in visible if r["featured"]]
rest = [r for r in visible if not r["featured"]]
reviews_section = """<!-- Shop reviews (generated by shop-data/build_shop.py) -->
<section class="section dark" id="shop-reviews">
  <div class="wrap">
    <div class="review-head review-head--photo" data-reveal>
      <figure class="review-head__photo"><img src="assets/img/real/harvester-team.jpg" alt="The Cavalli team with the Starr lavender harvester among the blooming rows" loading="lazy" /></figure>
      <div class="review-head__text">
      <p class="eyebrow center">Customer Reviews</p>
      <h2>Loved well beyond the farm</h2>
      <p class="review-score"><span class="review-score__num">%(score).1f</span><span class="review-score__stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span><span class="review-score__count">%(count)d customer reviews</span></p>
      <ul class="review-badges"><li>%(sales)d+ orders shipped</li><li>Grown &amp; made in Edna Valley</li></ul>
      </div>
    </div>
    <div class="review-grid" data-reveal>
%(featured)s
    </div>
    <details class="review-more">
      <summary><span class="review-more__open">Read all %(nvis)d reviews</span><span class="review-more__close">Show fewer</span></summary>
      <div class="review-grid review-grid--all">
%(rest)s
      </div>
    </details>
    <p class="review-source">Reviews from customers of the Cavalli lavender shop, as of %(checked)s. The rating counts every review; a few off-topic comments are not shown.</p>
  </div>
</section>

""" % dict(score=REV["shopRating"], count=REV["shopCount"], sales=REV["sales"], nvis=len(visible),
           featured="\n".join(review_card(r) for r in featured),
           rest="\n".join(review_card(r) for r in rest),
           checked="November 18, 2026")
section = section + reviews_section

page = os.path.join(ROOT, "shop.html")
s = open(page, encoding="utf-8").read()
a = s.index("<!-- Products -->")
b = s.index("<!-- How it's made -->")
s = s[:a] + section + s[b:]
open(page, "w", encoding="utf-8").write(s)

# ---------------------------------------------------------- Shopify CSV
COLS = ["Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type", "Tags", "Published",
        "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value",
        "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Qty",
        "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price", "Variant Requires Shipping",
        "Variant Taxable", "Image Src", "Image Position", "Image Alt Text", "Status"]


def body_html(r):
    out = "".join("<p>%s</p>" % esc(par) for par in r["body"])
    out += "<ul>%s</ul>" % "".join("<li>%s</li>" % esc(d) for d in r["details"])
    return out


def variants(r):
    opts = [] if r["notes"] else r["options"]
    if not opts:
        return [((), r["price"], False)]
    import itertools
    out = []
    for vals in itertools.product(*[o["values"] for o in opts]):
        price = r["price"]
        for v in vals:
            if v["p"] is not None:
                price = v["p"]
        out.append((tuple(v["v"] for v in vals), price, any(v["out"] for v in vals)))
    return out


rows = []
for r in records:
    vs = variants(r)
    imgs = r["images"]
    n = max(len(vs), len(imgs))
    for i in range(n):
        row = dict.fromkeys(COLS, "")
        row["Handle"] = r["handle"]
        if i == 0:
            row.update({
                "Title": r["title"], "Body (HTML)": body_html(r), "Vendor": "Cavalli Estates",
                "Type": r["collectionName"], "Tags": "lavender, cavalli farm, " + r["collectionName"].lower(),
                "Published": "TRUE", "Status": "active",
            })
            if r["options"] and not r["notes"]:
                for k, o in enumerate(r["options"][:3]):
                    row["Option%d Name" % (k + 1)] = o["name"]
            else:
                row["Option1 Name"] = "Title"
        if i < len(vs):
            vals, price, out = vs[i]
            row["Option1 Value"] = vals[0] if vals else "Default Title"
            for k in range(1, len(vals)):
                row["Option%d Value" % (k + 1)] = vals[k]
            row.update({
                "Variant SKU": "%s-%d" % (r["handle"], i + 1),
                "Variant Grams": "0",
                "Variant Inventory Tracker": "shopify" if out else "",
                "Variant Inventory Qty": "0" if out else "",
                "Variant Inventory Policy": "deny" if out else "continue",
                "Variant Fulfillment Service": "manual",
                "Variant Price": "%.2f" % price,
                "Variant Requires Shipping": "TRUE",
                "Variant Taxable": "TRUE",
            })
        if i < len(imgs):
            row["Image Src"] = "%s/%s" % (LIVE, imgs[i])
            row["Image Position"] = str(i + 1)
            row["Image Alt Text"] = r["title"]
        rows.append(row)

with open(os.path.join(HERE, "shopify-products.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)

with open(os.path.join(HERE, "shopify-new-products.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows([row for row in rows if row["Handle"] in NEW_IN_SHOPIFY])

nvar = sum(len(variants(r)) for r in records)
print("shop.html: %d products in %d collections" % (len(records), len(COLLECTIONS)))
print("shopify-products.csv: %d rows, %d variants, %d images" % (len(rows), nvar, sum(len(r["images"]) for r in records)))
