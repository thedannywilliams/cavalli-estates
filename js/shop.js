/* ============================================================
   Cavalli Estates — Shop / Shopify integration
   ------------------------------------------------------------
   The Shop page works right now with graceful fallbacks (each
   product links to Etsy). When the Shopify store is live, fill in
   CONFIG below and every product card turns into a real Shopify
   "Add to Cart" with a hosted cart + checkout — no other changes.

   HOW TO GO LIVE (once the client has a Shopify store):
   1. In Shopify: Settings → Apps and sales channels → Develop apps →
      create an app → Storefront API → install → copy the
      "Storefront API access token".
   2. Set CONFIG.domain to "your-store.myshopify.com" and
      CONFIG.storefrontAccessToken to that token.
   3. For each product, copy its numeric Product ID (from the product
      URL in Shopify admin) into CONFIG.products below, keyed by the
      data-product value on the card in shop.html.
   4. Set CONFIG.enabled = true. Commit + push — it auto-deploys.
   ============================================================ */
(function () {
  "use strict";

  var CONFIG = {
    enabled: false,                                  // ← set true once the values below are real
    domain: "REPLACE_ME.myshopify.com",              // ← your Shopify domain
    storefrontAccessToken: "REPLACE_ME_STOREFRONT_TOKEN",
    // Map each card's data-product handle → its Shopify numeric Product ID
    products: {
      "lavender-bundle":   "REPLACE_ME_PRODUCT_ID",
      "lavender-posies":   "REPLACE_ME_PRODUCT_ID",
      "lavender-buds":     "REPLACE_ME_PRODUCT_ID",
      "culinary-lavender": "REPLACE_ME_PRODUCT_ID",
      "lavender-sachets":  "REPLACE_ME_PRODUCT_ID",
      "dried-bunches":     "REPLACE_ME_PRODUCT_ID"
    }
  };

  if (!CONFIG.enabled) return; // fallback (Etsy links) stays in place

  var SDK = "https://sdk.shopify.com/js/buybutton.js";
  function boot() {
    var client = window.ShopifyBuy.buildClient({
      domain: CONFIG.domain,
      storefrontAccessToken: CONFIG.storefrontAccessToken
    });
    var ui = window.ShopifyBuy.UI.init(client);

    var money = "${{amount}}";
    var brand = { gold: "#9C7C46", ink: "#24211C", ivory: "#FAF7F0", serif: "Cormorant Garamond, serif", sans: "Jost, sans-serif" };

    var productOptions = {
      product: {
        iframe: false,
        contents: { img: false, title: false, price: false }, // card already shows these
        text: { button: "Add to Cart" },
        styles: {
          button: {
            "font-family": brand.sans, "font-size": "12px", "letter-spacing": "0.24em",
            "text-transform": "uppercase", "padding": "16px 24px", "border-radius": "0",
            "background-color": brand.ink,
            ":hover": { "background-color": brand.gold },
            ":focus": { "background-color": brand.gold }
          }
        }
      },
      cart: {
        styles: { button: { "background-color": brand.ink, ":hover": { "background-color": brand.gold }, "border-radius": "0" } },
        text: { title: "Your Cart", total: "Subtotal", button: "Checkout" }
      },
      toggle: { styles: { toggle: { "background-color": brand.ink, ":hover": { "background-color": brand.gold } } } }
    };

    document.querySelectorAll("[data-shopify-mount][data-product]").forEach(function (mount) {
      var handle = mount.getAttribute("data-product");
      var id = CONFIG.products[handle];
      if (!id || String(id).indexOf("REPLACE_ME") === 0) return; // leave fallback if not mapped
      mount.innerHTML = ""; // remove the Etsy fallback for this product
      ui.createComponent("product", { id: id, node: mount, moneyFormat: money, options: productOptions });
    });
  }

  if (window.ShopifyBuy && window.ShopifyBuy.UI) { boot(); }
  else {
    var s = document.createElement("script");
    s.async = true; s.src = SDK;
    s.onload = boot;
    document.head.appendChild(s);
  }
})();
