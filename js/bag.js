/* ============================================================
   Cavalli Estates — Shop bag & product detail
   ------------------------------------------------------------
   Clickable product cards open a detail view (variant + quantity),
   Add to Bag keeps a cart in localStorage, and the bag drawer
   totals the order. Until Shopify checkout is live, "Email Your
   Order" sends the bag contents to the estate's inbox.
   ============================================================ */
(function () {
  "use strict";

  var ORDER_EMAIL = "cavalli.estates@gmail.com";
  var KEY = "cavalli-bag";

  function readBag() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; }
  }
  function writeBag(items) {
    try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) {}
    renderBadge();
  }
  function money(n) { return "$" + n.toFixed(2); }

  /* ---------- Collect product data from the cards ---------- */
  function cardData(card) {
    var buy = card.querySelector("[data-product]");
    return {
      slug: buy.getAttribute("data-product"),
      price: parseFloat(buy.getAttribute("data-price") || "0"),
      options: (buy.getAttribute("data-options") || "").split("|").filter(Boolean),
      name: card.querySelector(".product__name").textContent.trim(),
      desc: card.querySelector(".product__desc").textContent.trim(),
      img: card.querySelector(".product__media img").getAttribute("src"),
      tag: (card.querySelector(".product__tag") || {}).textContent || ""
    };
  }

  /* ---------- Build overlay skeletons once ---------- */
  var overlay = document.createElement("div");
  overlay.className = "shop-overlay";
  overlay.innerHTML =
    '<div class="shop-overlay__scrim" data-close></div>' +
    '<div class="pmodal" role="dialog" aria-modal="true" aria-label="Product details">' +
    '  <button class="pmodal__close" type="button" data-close aria-label="Close">&times;</button>' +
    '  <div class="pmodal__media"><img alt="" /></div>' +
    '  <div class="pmodal__body">' +
    '    <p class="eyebrow" data-m-tag></p>' +
    '    <h3 data-m-name></h3>' +
    '    <p class="pmodal__desc" data-m-desc></p>' +
    '    <div class="pmodal__field" data-m-optwrap hidden><label>Selection</label><select data-m-options></select></div>' +
    '    <div class="pmodal__field"><label>Quantity</label>' +
    '      <div class="qty"><button type="button" data-qty-minus aria-label="Decrease">&minus;</button><span data-m-qty>1</span><button type="button" data-qty-plus aria-label="Increase">+</button></div>' +
    '    </div>' +
    '    <p class="pmodal__price"><span data-m-subtotal></span></p>' +
    '    <button class="btn gold pmodal__add" type="button" data-add><span>Add to Bag</span></button>' +
    '    <p class="pmodal__note">Secure online checkout arrives with our Shopify launch. Until then, send your order by email and we will take care of the rest.</p>' +
    '  </div>' +
    '</div>';
  document.body.appendChild(overlay);

  var drawer = document.createElement("aside");
  drawer.className = "bag-drawer";
  drawer.setAttribute("aria-label", "Shopping bag");
  drawer.innerHTML =
    '<div class="bag-drawer__head"><h3>Your Bag</h3><button class="pmodal__close" type="button" data-bag-close aria-label="Close bag">&times;</button></div>' +
    '<div class="bag-drawer__items" data-bag-items></div>' +
    '<div class="bag-drawer__foot">' +
    '  <p class="bag-drawer__total">Subtotal <b data-bag-total>$0.00</b></p>' +
    '  <a class="btn gold" data-bag-email href="#"><span>Email Your Order</span></a>' +
    '  <p class="pmodal__note">Online checkout is coming with our Shopify launch. Email your order and our team will confirm availability, payment, and pickup or shipping.</p>' +
    '</div>';
  document.body.appendChild(drawer);

  var bagBtn = document.createElement("button");
  bagBtn.className = "bag-fab";
  bagBtn.type = "button";
  bagBtn.setAttribute("aria-label", "Open shopping bag");
  bagBtn.innerHTML =
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 8h12l-1 13H7L6 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>' +
    '<span class="bag-fab__count" data-bag-count hidden>0</span>';
  document.body.appendChild(bagBtn);

  /* ---------- Product modal ---------- */
  var current = null, qty = 1;
  var mImg = overlay.querySelector(".pmodal__media img");
  var mTag = overlay.querySelector("[data-m-tag]");
  var mName = overlay.querySelector("[data-m-name]");
  var mDesc = overlay.querySelector("[data-m-desc]");
  var mOptWrap = overlay.querySelector("[data-m-optwrap]");
  var mOptions = overlay.querySelector("[data-m-options]");
  var mQty = overlay.querySelector("[data-m-qty]");
  var mSubtotal = overlay.querySelector("[data-m-subtotal]");

  function refreshSubtotal() {
    mQty.textContent = qty;
    mSubtotal.textContent = money(current.price * qty);
  }
  function openModal(data) {
    current = data; qty = 1;
    mImg.src = data.img; mImg.alt = data.name;
    mTag.textContent = data.tag;
    mName.textContent = data.name;
    mDesc.textContent = data.desc;
    if (data.options.length) {
      mOptions.innerHTML = data.options.map(function (o) { return "<option>" + o + "</option>"; }).join("");
      mOptWrap.hidden = false;
    } else { mOptWrap.hidden = true; }
    refreshSubtotal();
    overlay.classList.add("open");
    document.body.style.overflow = "hidden";
  }
  function closeModal() {
    overlay.classList.remove("open");
    document.body.style.overflow = "";
  }

  document.querySelectorAll(".product").forEach(function (card) {
    var open = function () { openModal(cardData(card)); };
    var media = card.querySelector(".product__media");
    var name = card.querySelector(".product__name");
    [media, name].forEach(function (el) {
      if (!el) return;
      el.style.cursor = "pointer";
      el.addEventListener("click", open);
    });
    var btn = card.querySelector("[data-open-product]");
    if (btn) btn.addEventListener("click", open);
  });

  overlay.addEventListener("click", function (e) {
    if (e.target.closest("[data-close]")) closeModal();
  });
  overlay.querySelector("[data-qty-minus]").addEventListener("click", function () { qty = Math.max(1, qty - 1); refreshSubtotal(); });
  overlay.querySelector("[data-qty-plus]").addEventListener("click", function () { qty = Math.min(20, qty + 1); refreshSubtotal(); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { closeModal(); closeBag(); }
  });

  overlay.querySelector("[data-add]").addEventListener("click", function () {
    var variant = (!mOptWrap.hidden && mOptions.value) ? mOptions.value : "";
    var items = readBag();
    var match = items.find(function (i) { return i.slug === current.slug && i.variant === variant; });
    if (match) { match.qty = Math.min(20, match.qty + qty); }
    else { items.push({ slug: current.slug, name: current.name, variant: variant, price: current.price, img: current.img, qty: qty }); }
    writeBag(items);
    closeModal();
    openBag();
  });

  /* ---------- Bag drawer ---------- */
  var itemsEl = drawer.querySelector("[data-bag-items]");
  var totalEl = drawer.querySelector("[data-bag-total]");
  var emailEl = drawer.querySelector("[data-bag-email]");
  var countEl = bagBtn.querySelector("[data-bag-count]");

  function renderBadge() {
    var n = readBag().reduce(function (a, i) { return a + i.qty; }, 0);
    countEl.textContent = n;
    countEl.hidden = n === 0;
  }
  function renderBag() {
    var items = readBag();
    if (!items.length) {
      itemsEl.innerHTML = '<p class="bag-empty">Your bag is empty. The fields are waiting.</p>';
    } else {
      itemsEl.innerHTML = items.map(function (i, idx) {
        return '<div class="bag-item">' +
          '<img src="' + i.img + '" alt="" />' +
          '<div class="bag-item__info"><b>' + i.name + "</b>" +
          (i.variant ? '<span class="bag-item__variant">' + i.variant + "</span>" : "") +
          '<div class="qty qty--sm"><button type="button" data-i="' + idx + '" data-dec aria-label="Decrease">&minus;</button><span>' + i.qty + '</span><button type="button" data-i="' + idx + '" data-inc aria-label="Increase">+</button></div></div>' +
          '<div class="bag-item__end"><span>' + money(i.price * i.qty) + '</span><button class="bag-item__remove" type="button" data-i="' + idx + '" data-remove>Remove</button></div>' +
          "</div>";
      }).join("");
    }
    var total = items.reduce(function (a, i) { return a + i.price * i.qty; }, 0);
    totalEl.textContent = money(total);
    var lines = items.map(function (i) {
      return i.qty + " x " + i.name + (i.variant ? " (" + i.variant + ")" : "") + " - " + money(i.price * i.qty);
    });
    var body = "Hello Cavalli Estates,%0D%0A%0D%0AI would like to place an order:%0D%0A%0D%0A" +
      lines.map(encodeURIComponent).join("%0D%0A") +
      "%0D%0A%0D%0ASubtotal: " + encodeURIComponent(money(total)) +
      "%0D%0A%0D%0AName:%0D%0APhone:%0D%0APickup or shipping:%0D%0A%0D%0AThank you!";
    emailEl.href = "mailto:" + ORDER_EMAIL + "?subject=" + encodeURIComponent("Cavalli Lavender Shop Order") + "&body=" + body;
    renderBadge();
  }
  function openBag() { renderBag(); drawer.classList.add("open"); }
  function closeBag() { drawer.classList.remove("open"); }

  bagBtn.addEventListener("click", function () {
    if (drawer.classList.contains("open")) closeBag(); else openBag();
  });
  drawer.addEventListener("click", function (e) {
    if (e.target.closest("[data-bag-close]")) { closeBag(); return; }
    var btn = e.target.closest("button[data-i]");
    if (!btn) return;
    var items = readBag();
    var i = parseInt(btn.getAttribute("data-i"), 10);
    if (btn.hasAttribute("data-inc")) items[i].qty = Math.min(20, items[i].qty + 1);
    if (btn.hasAttribute("data-dec")) items[i].qty = Math.max(1, items[i].qty - 1);
    if (btn.hasAttribute("data-remove")) items.splice(i, 1);
    writeBag(items);
    renderBag();
  });

  renderBadge();
})();
