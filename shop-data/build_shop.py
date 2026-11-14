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
    return {
        "handle": p["handle"], "title": p["title"], "tag": p["tag"], "collection": p["collection"],
        "collectionName": COLL[p["collection"]], "price": p["price"], "low": low, "high": high,
        "blurb": p["blurb"], "body": p["body"], "details": p["details"], "options": opts,
        "card": "%s/%s-card.jpg" % (IMG_DIR, p["handle"]), "images": imgs,
    }


def money(x):
    return "$%.2f" % x


records = [product_record(p) for p in PRODUCTS]

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
        '        <p class="product__price">%(price)s</p>\n'
        '        <div class="product__buy" data-product="%(h)s">\n'
        '          <button class="btn gold" type="button" data-open-product><span>View Item</span></button>\n'
        '        </div>\n'
        '      </article>' % dict(
            c=r["collection"], card=r["card"], alt=esc(r["title"] + ", from the Cavalli lavender farm"),
            tag=esc(r["tag"]), title=esc(r["title"]), blurb=esc(r["blurb"]), price=price, h=r["handle"]))

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
  </div>
  <script type="application/json" id="shop-catalog">%s</script>
</section>

""" % ("\n      ".join(chips), "\n\n".join(cards), data)

page = os.path.join(ROOT, "shop.html")
s = open(page, encoding="utf-8").read()
a = s.index("<!-- Products -->")
b = s.index("<!-- How it's made -->")
s = s[:a] + section + s[b:]
open(page, "w", encoding="utf-8").write(s)

# ---------------------------------------------------------- Shopify CSV
COLS = ["Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type", "Tags", "Published",
        "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value",
        "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Qty",
        "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price", "Variant Requires Shipping",
        "Variant Taxable", "Image Src", "Image Position", "Image Alt Text", "Status"]


def body_html(r):
    out = "".join("<p>%s</p>" % esc(par) for par in r["body"])
    out += "<ul>%s</ul>" % "".join("<li>%s</li>" % esc(d) for d in r["details"])
    return out


def variants(r):
    opts = r["options"]
    if not opts:
        return [((), r["price"], False)]
    combos = [((v,), v) for v in opts[0]["values"]]
    if len(opts) > 1:
        combos = [((v1, v2), None) for v1 in opts[0]["values"] for v2 in opts[1]["values"]]
    out = []
    for vals, _ in combos:
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
            if r["options"]:
                row["Option1 Name"] = r["options"][0]["name"]
                if len(r["options"]) > 1:
                    row["Option2 Name"] = r["options"][1]["name"]
            else:
                row["Option1 Name"] = "Title"
        if i < len(vs):
            vals, price, out = vs[i]
            row["Option1 Value"] = vals[0] if vals else "Default Title"
            if len(vals) > 1:
                row["Option2 Value"] = vals[1]
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

nvar = sum(len(variants(r)) for r in records)
print("shop.html: %d products in %d collections" % (len(records), len(COLLECTIONS)))
print("shopify-products.csv: %d rows, %d variants, %d images" % (len(rows), nvar, sum(len(r["images"]) for r in records)))
