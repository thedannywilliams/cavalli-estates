# Cavalli shop: moving from Etsy to Shopify

All 28 products from the CavalliFarm Etsy shop (pulled November 13, 2026) live in
`catalog.py`: titles, prices, every option and its price, descriptions, details,
and up to 6 photos each (in `assets/img/shop/p/`).

## Editing products
1. Edit `catalog.py` (price, copy, options, sold-out values).
2. Run `python3 shop-data/build_shop.py`. It rebuilds the grid in `shop.html` and
   `shopify-products.csv`.
3. Commit and push. Netlify deploys in about 30 seconds.

## Going live on Shopify
1. Create the Shopify store (Basic plan is enough).
2. Products > Import > upload `shopify-products.csv`. Photos are pulled from the
   live site automatically. Keep the handles and option names as imported: the
   site uses them to find each product and variant.
3. Set shipping rates and taxes in Shopify settings.
4. Settings > Apps and sales channels > Develop apps > Create an app >
   Storefront API: allow product listings and checkouts > Install > copy the
   **Storefront API access token**. (Installing the free Headless channel works too.)
5. In `js/shop.js`, fill in `domain` (your-store.myshopify.com) and
   `storefrontAccessToken`, set `enabled: true`, commit and push.

From then on the bag's button reads "Checkout" and opens Shopify's secure checkout
with the guest's items already in the cart. Until then it emails the order to
cavalli.estates@gmail.com.

Sold out on Etsy at import: Ralph the pony, Lavender Rose bath salts. They import
with 0 inventory and show as sold out on the site.

Once Shopify checkout is live, the Etsy shop can be closed.

## Live sync with Shopify (since 2026-11-18)

The shop page reads the live product list from Shopify on every visit
(js/shop.js `products()`, applied in js/bag.js `syncFromShopify`).
Shopify is the source of truth:

- New products appear at the top of the shop, tagged "New", in the filter
  whose name matches the product's Type in Shopify (e.g. "Gift Sets").
- Name, price, options, photos, description and sold-out state follow Shopify.
- Products deleted or unpublished in Shopify disappear from the site.
- Tag a product `hide-from-website` in Shopify to keep it off the site.
- Reviews, short card blurbs and card tags come from catalog.py /
  etsy-reviews.json (run build_shop.py to refresh the built copy, which is
  what search engines and visitors without JavaScript see).
