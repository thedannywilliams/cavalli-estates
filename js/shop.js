/* ============================================================
   Cavalli Estates: Shopify checkout
   ------------------------------------------------------------
   The shop runs today with an emailed order. To switch the bag's
   button to real Shopify checkout:

   1. Import shop-data/shopify-products.csv in Shopify
      (Products > Import). Handles and option names must stay as
      imported; they are how the site finds each product.
   2. Shopify admin > Settings > Apps and sales channels > Develop
      apps > create an app > configure Storefront API scopes
      (unauthenticated_read_product_listings,
      unauthenticated_write_checkouts) > install > copy the
      Storefront API access token.
   3. Fill in CONFIG below, set enabled: true, commit and push.

   The token is a public Storefront token (read products, create
   carts); it is designed to live in browser code.
   ============================================================ */
(function () {
  "use strict";

  var CONFIG = {
    enabled: false,
    domain: "cavalliestates.myshopify.com",
    storefrontAccessToken: "REPLACE_ME_STOREFRONT_TOKEN",
    apiVersion: "2026-07"
  };

  function gql(query, variables) {
    return fetch("https://" + CONFIG.domain + "/api/" + CONFIG.apiVersion + "/graphql.json", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Shopify-Storefront-Access-Token": CONFIG.storefrontAccessToken },
      body: JSON.stringify({ query: query, variables: variables || {} })
    }).then(function (r) {
      if (!r.ok) throw new Error("Shopify " + r.status);
      return r.json();
    }).then(function (j) {
      if (j.errors && j.errors.length) throw new Error(j.errors[0].message);
      return j.data;
    });
  }

  var PRODUCT_Q = "query($h:String!){product(handle:$h){variants(first:100){nodes{id availableForSale selectedOptions{name value}}}}}";
  var CART_M = "mutation($lines:[CartLineInput!]!){cartCreate(input:{lines:$lines}){cart{checkoutUrl} userErrors{message}}}";

  function variantFor(item) {
    return gql(PRODUCT_Q, { h: item.slug }).then(function (d) {
      if (!d.product) throw new Error(item.name + " is not in the Shopify store yet");
      var nodes = d.product.variants.nodes;
      var want = item.options || [];
      var v = nodes.find(function (n) {
        var vals = n.selectedOptions.map(function (o) { return o.value; }).filter(function (x) { return x !== "Default Title"; });
        return vals.length === want.length && want.every(function (w) { return vals.indexOf(w) !== -1; });
      }) || (want.length ? null : nodes[0]);
      if (!v) throw new Error(item.name + " (" + item.variant + ") was not found in Shopify");
      if (!v.availableForSale) throw new Error(item.name + " is sold out");
      return { merchandiseId: v.id, quantity: item.qty };
    });
  }

  window.CavalliShopify = {
    enabled: CONFIG.enabled && CONFIG.domain.indexOf("REPLACE_ME") === -1,
    checkout: function (items) {
      return Promise.all(items.map(variantFor)).then(function (lines) {
        return gql(CART_M, { lines: lines });
      }).then(function (d) {
        var res = d.cartCreate;
        if (res.userErrors && res.userErrors.length) throw new Error(res.userErrors[0].message);
        return res.cart.checkoutUrl;
      });
    }
  };
})();
