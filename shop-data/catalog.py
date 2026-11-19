"""
Cavalli Estates shop catalog: single source of truth.

Every product here was moved over from the CavalliFarm Etsy shop
(November 2026). `etsy` is the original Etsy listing id, kept for reference.

Run `python3 shop-data/build_shop.py` after editing. It rebuilds:
  - the product grid in shop.html (plus the product data the bag reads)
  - shop-data/shopify-products.csv (Shopify's product import format)
  - resized product photos in assets/img/shop/ (from shop-data/photos/)

Options: each option is (name, [values]). A value is either "Label" or
("Label", price) or ("Label", price, "sold out"). A price on a value sets
the price for that choice; otherwise the product's base price applies.
"""

COLLECTIONS = [
    ("dried", "Bouquets & Dried"),
    ("sachets", "Lavender Buds"),
    ("body", "Spa & Wellness"),
    ("kitchen", "Kitchen"),
    ("gifts", "Gift Sets"),
    ("farm", "Farm & Garden"),
]

PRODUCTS = [
    # ---------------- Bouquets & Dried ----------------
    dict(
        etsy="4298380625", handle="dried-lavender-bouquet", collection="dried", featured=True,
        title="Long-Stem Dried Lavender Bouquet", price=20.00, tag="Signature",
        blurb="Long-stem lavender, hand-tied with twine and wrapped in kraft paper at the estate.",
        body=[
            "Hand-harvested and air-dried on our 15-acre family farm, each bouquet keeps the soft purple color, delicate texture, and calming scent of the fields it came from.",
            "Hand-tied with twine and wrapped in simple kraft paper, it suits a farmhouse table as well as a modern room, and it is a favorite for weddings and showers.",
        ],
        details=["One dried lavender bouquet", "About 22 inches tall", "Hand-tied with twine, wrapped in kraft paper", "Grown without chemicals or preservatives", "Naturally air-dried, so expect a little shedding"],
        options=[],
    ),
    dict(
        etsy="4298339165", handle="lavender-posy", collection="dried",
        title="Lavender Posy", price=10.00, tag="Hand-tied",
        blurb="A small hand-tied posy of farm-grown lavender, in purple or white.",
        body=[
            "Freshly harvested and air-dried to keep its color and fragrance, each posy is tied by hand with twine or ribbon.",
            "Set them in vases, tuck them into wreaths, or give them away. They are lovely at rustic weddings, bridal showers, and anywhere you want a little calm.",
        ],
        details=["About 12 inches long", "Purple (Sachet variety) or white (Melissa variety)", "100% Cavalli lavender, grown without pesticides", "Hand-tied with twine or ribbon", "Naturally air-dried, so expect a little shedding"],
        options=[
            ("Quantity", [("Single posy", 10.00), ("2 posies", 15.00), ("4 posies", 28.00), ("10 posies", 65.00)]),
            ("Variety", ["Purple: Sachet", "White: Melissa"]),
        ],
    ),
    dict(
        etsy="4483269408", handle="mini-lavender-posies", collection="dried",
        title="Mini Lavender Posies", price=10.00, tag="Place settings",
        blurb="Petite lavender bundles for place settings and favors, in four wrapping styles.",
        body=[
            "Grown and gathered at Cavalli Farm, each petite bundle of dried lavender is wrapped by hand in one of four styles, from rustic twine and burlap to soft florals and paper accents.",
            "Set one at every place for a wedding or dinner party and let guests take them home. Because each is arranged by hand, no two are exactly alike.",
        ],
        details=["Four wrapping styles", "About 9 inches", "Farm-grown, naturally dried lavender", "Sold in sets"],
        options=[
            ("Count", [("2 posies", 10.00), ("6 posies", 24.00), ("10 posies", 38.00), ("20 posies", 65.00), ("30 posies", 86.00), ("40 posies", 105.00)]),
            ("Style", ["Style 1", "Style 2", "Style 3", "Style 4"]),
        ],
    ),
    dict(
        etsy="4298574387", handle="lavender-wedding-confetti", collection="dried",
        title="Lavender Wedding Confetti", price=25.00, tag="Weddings",
        blurb="A biodegradable toss of dried lavender buds and flower petals, mixed by hand.",
        body=[
            "A romantic, eco-friendly alternative to paper confetti: fragrant dried lavender buds and flower petals, hand-mixed on the farm and packed in individual \"Toss Me\" bags.",
            "Gentle on the venue and beautiful in photographs, with a soft lavender scent as it falls. Lovely for the send-off, flower girl baskets, the aisle, or the table.",
        ],
        details=["Individual \"Toss Me\" bags, 4 x 3 inches", "100% natural dried lavender and petals", "Biodegradable and safe outdoors", "Packed fresh in resealable bags"],
        options=[],
    ),
    dict(
        etsy="4318187786", handle="bulk-dried-lavender", collection="dried",
        title="Bulk Dried Lavender", price=35.00, tag="By the pound",
        blurb="This year's harvest by the pound, in Grosso or our Blue Blend.",
        body=[
            "Naturally air-dried and packed with care for crafts, sachets, weddings, soap and candle making, or simply a bowl of lavender on the table.",
            "Grosso is light purple with a strong scent and is the classic variety for oil. The Blue Blend is deeper blue with a softer, sweeter fragrance. Because it ships in a large bag, expect a few leaves and stems.",
        ],
        details=["Grosso or Blue Blend", "1, 2, or 3 pounds", "100% natural, no additives or preservatives", "Freshly budded from this year's harvest"],
        options=[
            ("Variety & weight", [("Grosso, 1 lb", 35.00), ("Grosso, 2 lb", 60.00), ("Grosso, 3 lb", 85.00), ("Blue Blend, 1 lb", 35.00), ("Blue Blend, 2 lb", 60.00), ("Blue Blend, 3 lb", 85.00)]),
        ],
    ),

    # ---------------- Sachets & Home ----------------
    dict(
        etsy="4391408727", handle="lavanoodle", collection="body", featured=True,
        title="The LavaNoodle", price=5.00, tag="Home",
        blurb="A lavender-filled fabric tube that stops drafts, freshens closets, and keeps insects away.",
        body=[
            "Hand-filled with dried, farm-grown Cavalli lavender, this soft fabric tube releases a calming scent while naturally repelling insects and freshening enclosed spaces.",
            "Lay it along a drafty door or window, tuck it into closets, drawers, suitcases, or the car, or line a windowsill. It is reusable and chemical-free.",
        ],
        details=["Mini, 3 inches: 1.2 oz lavender, for the car, drawers, or a purse", "1 foot: 4 oz lavender, for drawers, cars, or travel", "3 feet: 10 oz lavender, for doorways and closets", "4 feet: 15 oz lavender, for doorways or under pillows", "Handcrafted in California"],
        options=[
            ("Size", [("Mini", 5.00), ("Mini, 2 pack", 8.00), ("1 foot", 12.00), ("1 foot, 2 pack", 20.00), ("3 feet", 27.00), ("3 feet, 2 pack", 49.00), ("4 feet", 35.00), ("4 feet, 2 pack", 55.00)]),
        ],
    ),
    dict(
        etsy="4417876793", handle="estate-linen-mist", collection="body", featured=True,
        title="Estate Linen Mist", price=12.00, tag="Six blends",
        blurb="A natural room and fabric mist in six estate blends. 50 ml.",
        body=[
            "Made with natural botanicals and farm-grown lavender, this fine mist lightly refreshes sheets, pillows, towels, clothing, and living spaces without being overpowering.",
            "Each 50 ml bottle is sized for the bedside table, the suitcase, or the car.",
        ],
        details=["No. 00 Pure Bliss: lavender", "No. 01 Evening Calm: lavender, chamomile, cedarwood", "No. 02 Citrus Grove: lavender, bergamot, lemon, orange", "No. 03 Rose Petal: lavender, rose, bergamot", "No. 04 Golden Dust: lavender, chamomile, bergamot, sweet orange, sandalwood", "No. 05 Coastal Grove: lavender, lemon, eucalyptus, rosemary"],
        options=[
            ("Blend", ["No. 00 Pure Bliss", "No. 01 Evening Calm", "No. 02 Citrus Grove", "No. 03 Rose Petal", "No. 04 Golden Dust", "No. 05 Coastal Grove"]),
        ],
    ),
    dict(
        etsy="4344128565", handle="lavender-soy-candle", collection="body",
        title="Lavender Soy Candle", price=20.00, tag="Hand-poured",
        blurb="Hand-poured soy wax scented with farm-grown lavender, in a reusable glass jar.",
        body=[
            "Poured by hand in small batches at the estate, this clean-burning soy candle fills a room with a soft, calming lavender scent.",
            "Finished in a reusable glass jar with a simple label, it belongs in the bedroom, the bath, or wrapped as a gift.",
        ],
        details=["One wick, 8 oz, or three wick, 16 oz", "Natural soy wax", "Made with farm-grown lavender", "Reusable glass jar"],
        options=[
            ("Size", [("One wick, 8 oz", 20.00), ("Three wick, 16 oz", 30.00)]),
        ],
    ),
    dict(
        etsy="4304443161", handle="lavender-sachet", collection="sachets",
        title="Lavender Sachet", price=8.00, tag="5 x 7 in",
        blurb="A generous 5 x 7 sachet of estate lavender for drawers, closets, and sleep.",
        body=[
            "Filled with hand-harvested, naturally dried lavender buds from our 15-acre family farm. Nothing added, just lavender.",
            "Freshen drawers, closets, and linens, keep moths away, or slip it under your pillow. Squeeze the bag gently to refresh the scent.",
        ],
        details=["One sachet, 5 x 7 inches, about 2 oz lavender", "Light purple is Grosso; purple-blue is Betty, Hidcote, Provence, or a blend", "Grown without chemicals or additives", "Grown and handmade in California"],
        options=[
            ("Variety", ["Light purple: Grosso", "Purple-blue: Blend"]),
        ],
    ),
    dict(
        etsy="4298358055", handle="lavender-sachet-pair", collection="sachets",
        title="Lavender Sachets, Pair", price=7.00, tag="2 pack",
        blurb="Two small tagged sachets of farm lavender, in purple, white, or one of each.",
        body=[
            "Two small sachets gently packed with fragrant lavender buds from our farm and tied with care.",
            "Tuck them into drawers, closets, or a suitcase, or use them as wedding favors and in spa gift sets. Lavender is a plant, so color can vary.",
        ],
        details=["Two sachets, about 3.5 x 4.5 inches, each with a tag", "100% dried Cavalli lavender", "Grown without chemicals or additives"],
        options=[
            ("Color", ["2 purple", "2 white", "1 purple & 1 white"]),
        ],
    ),
    dict(
        etsy="4298511108", handle="lavender-sachet-variety-pack", collection="sachets",
        title="Lavender Sachet Variety Pack", price=12.00, tag="5 pack",
        blurb="Five sachets: two Melissa, two Royal, and one lavender with flower petals.",
        body=[
            "A curated five-pack of hand-filled sachets from our 15-acre family estate on the Central Coast.",
            "Use them in drawers and closets as a natural moth repellent, among pillows and linens for restful sleep, or in gym bags, cars, and suitcases. They make easy housewarming and bridesmaid gifts.",
        ],
        details=["2 Melissa lavender sachets", "2 Royal lavender sachets", "1 mixed lavender and flower petal sachet", "Each 3.5 x 4.5 inches"],
        options=[],
    ),
    dict(
        etsy="4305081949", handle="garden-botanical-sachets", collection="sachets",
        title="Garden Botanical Sachets, Pair", price=8.00, tag="2 pack",
        blurb="Two tagged sachets of lavender buds and dried garden flowers.",
        body=[
            "Lavender from our family farm mixed with dried flowers from the garden, packed into two small sachets and tied with care.",
            "Lovely in drawers, closets, and suitcases, or under the pillow for restful sleep.",
        ],
        details=["Two sachets, 3.5 x 4.5 inches, each with a tag", "Cavalli lavender and dried garden petals", "Grown without chemicals or additives"],
        options=[],
    ),
    dict(
        etsy="1854927966", handle="closet-lavender-sachet", collection="sachets",
        title="Closet & Drawer Sachet", price=9.00, tag="5 x 7 in",
        blurb="A large sachet of lavender and garden petals for closets, drawers, and bedside.",
        body=[
            "Dried lavender from our 15 acres, blended with home-grown flowers for a naturally soothing scent. No chemicals, no artificial fragrance.",
            "Hang it in a closet, lay it in a drawer, or keep it by the bed. A gentle squeeze refreshes the scent.",
        ],
        details=["One sachet, 5 x 7 inches", "Cavalli lavender and garden petals", "Naturally grown without chemicals", "Grown and handcrafted in California"],
        options=[],
    ),
    dict(
        etsy="4304458359", handle="lavender-potpourri", collection="sachets",
        title="Lavender Potpourri", price=22.00, tag="10 oz",
        blurb="Ten ounces of lavender and dried petals, with five empty sachet bags to fill.",
        body=[
            "Lavender mixed with dried flower petals, grown and dried on the Central Coast with no chemicals and no pesticides.",
            "Five empty sachet bags are included, so you can make your own scented pouches for drawers, closets, and cars, or to give away.",
        ],
        details=["10 oz lavender with dried flower petals", "Includes 5 reusable sachet bags", "Hand-harvested and dried on the Central Coast", "No chemicals, no pesticides"],
        options=[],
    ),
    dict(
        # Hidden 2026-11-16: every pony and bird is one of a kind, so the
        # site and Etsy can't share stock. Set hidden=False to bring it back.
        hidden=True,
        etsy="4533731961", handle="lavender-pony-and-bird", collection="sachets",
        title="Lavender Pony & Bird", price=15.00, tag="One of a kind",
        blurb="A handmade pony or bird filled with estate lavender, each with its own name.",
        body=[
            "Each pony and bird is made by hand at Cavalli Farms and filled with lavender from our own fields. A gentle squeeze releases its calming scent.",
            "No two are alike, and each comes with its own name. A sweet gift for horse lovers, birthdays, and holidays.",
        ],
        details=["Pony: about 8 inches tall", "Bird: about 2.5 inches tall and 4 inches wide", "Filled with estate-grown lavender", "Handmade, so fabric and shape vary"],
        options=[
            ("Choose yours", [("Buttercup the pony", 30.00), ("Ralph the pony", 30.00, "sold out"), ("Bird 1", 15.00), ("Bird 2", 15.00), ("Bird 3", 15.00), ("Bird 4", 15.00)]),
        ],
    ),

    # ---------------- Bath & Body ----------------
    dict(
        etsy="4404390848", handle="lavender-essential-oil", collection="body", featured=True,
        title="Lavender Essential Oil", price=18.00, tag="10 ml",
        blurb="Grown, hand-harvested, and steam-distilled here on the farm. 100% pure.",
        body=[
            "Our lavender is harvested by hand and steam-distilled in small batches right here at Cavalli Estates, capturing the fields in every drop.",
            "Pure, with no additives or fillers. Use it in a diffuser, the bath, or blended with a carrier oil for massage.",
        ],
        details=["100% pure lavender essential oil", "Steam-distilled in small batches on the farm", "10 ml amber glass bottle"],
        options=[],
    ),
    dict(
        etsy="4499514333", handle="lavender-body-lotion", collection="body", featured=True,
        title="Lavender Body Lotion", price=20.00, tag="3.75 oz",
        blurb="A light, quick-absorbing lotion made with estate-grown lavender. 3.75 oz.",
        body=[
            "A plant-based formula made in small batches with lavender from our estate. It hydrates deeply and absorbs quickly without feeling greasy.",
            "Free from harsh preservatives. Use it after the shower, before bed, or whenever skin needs it.",
        ],
        details=["3.75 oz bottle", "Small-batch and handmade", "Ingredients: water, rice bran oil, emulsifying wax, Leuconostoc/radish root ferment filtrate, willow bark extract, sweet almond oil, mango seed butter, hemp seed oil, Lactobacillus, coconut fruit extract, olive oil, cetearyl alcohol, goldenseal leaf extract, allantoin, lavender flower oil, vitamin E"],
        options=[],
    ),
    dict(
        etsy="4499510303", handle="lavender-face-cream", collection="body",
        title="Lavender Face Cream", price=28.00, tag="2 oz",
        blurb="A rich, soothing daily face cream made with estate-grown lavender. 2 oz.",
        body=[
            "Handcrafted in small batches with lavender from our estate, this plant-based cream delivers deep hydration with a light, luxurious feel.",
            "Smooth a small amount onto clean skin, face and neck, morning and night.",
        ],
        details=["2 oz jar", "Small-batch and handmade", "Ingredients: water, aloe vera, olive oil, hemp seed oil, emulsifying wax, Leuconostoc/radish root ferment filtrate, cetearyl alcohol, mango seed butter, willow bark extract, sunflower seed oil, Lupinus albus seed extract, Abyssinian seed oil, vitamin E, Lactobacillus, coconut fruit extract, rosehip fruit oil, evening primrose oil, allantoin, lavender flower oil"],
        options=[],
    ),
    dict(
        etsy="4363090586", handle="lavender-soap", collection="body",
        title="Handcrafted Lavender Soap", price=7.00, tag="3.5 oz",
        blurb="A small-batch bar made with homegrown lavender, in three blends.",
        body=[
            "Each bar is made in small batches with lavender from our fields and soothing botanicals: gentle and moisturizing enough for every day.",
            "Lavender is classic and pure. Lavender Lilac adds soft floral notes; Lavender Gardenia adds sweet gardenia.",
        ],
        details=["About 3.5 oz", "Homegrown lavender and natural botanicals", "No harsh chemicals or synthetic fragrance"],
        options=[
            ("Blend", ["Lavender", "Lavender Lilac", "Lavender Gardenia"]),
        ],
    ),
    dict(
        etsy="4363259970", handle="lavender-bath-salts", collection="body",
        title="Lavender Bath Salts", price=12.00, tag="16 oz",
        blurb="Mineral salts and farm lavender with a gentle fizz, for a long, slow soak. 16 oz.",
        body=[
            "Mineral-rich salts blended with farm-grown lavender and botanicals, with a touch of citric acid for a gentle fizz.",
            "Add a handful to a warm bath, breathe deeply, and let the day go.",
        ],
        details=["16 oz bag", "Made with Cavalli lavender", "Handcrafted in small batches", "No harsh chemicals or synthetic fragrance"],
        options=[
            ("Blend", ["Lavender", ("Lavender Rose", 12.00, "sold out"), "Lavender Chamomile"]),
        ],
    ),
    dict(
        etsy="4487280251", handle="botanical-roll-on-oil", collection="body",
        title="Botanical Roll-On Oil", price=14.00, tag="10 ml",
        blurb="A soft, natural perfume oil for wrists and neck, in three blends.",
        body=[
            "Plant-based oils and botanicals blended into a subtle, grounding fragrance that melts into the skin rather than sitting on top of it.",
            "Roll onto wrists, neck, and behind the ears. Small enough for a purse, or the tack trunk.",
        ],
        details=["Signature Lavender", "Calm: lavender, cedarwood, chamomile", "Rose: lavender, rose, bergamot", "10 ml glass roller bottle", "Small-batch and handmade"],
        options=[
            ("Blend", ["Signature Lavender", "Calm", "Rose"]),
        ],
    ),

    # ---------------- Kitchen ----------------
    dict(
        etsy="4308941891", handle="culinary-lavender-trio", collection="kitchen",
        title="Culinary Lavender Trio", price=17.50, tag="3 pack",
        blurb="Food-grade Royal, Melissa, and a blend of both, with a recipe card.",
        body=[
            "Three bags of culinary lavender buds, hand-harvested and air-dried on the farm, so you can taste the difference between varieties.",
            "Melissa is soft, sweet, and lightly lemony, made for shortbread and tea. Royal is bold and classic, for savory dishes, syrups, and cocktails. The blend sits in between. A recipe card is included.",
        ],
        details=["3 bags, 0.4 oz each", "Melissa (white), Royal (blue-purple), and a blend", "Culinary grade, pesticide-free", "Recipe card included"],
        options=[],
    ),
    dict(
        etsy="4312649807", handle="culinary-lavender-sugar", collection="kitchen",
        title="Lavender Sugar", price=8.00, tag="4 oz",
        blurb="Cane sugar infused with our culinary lavender, for baking, tea, and cocktail rims.",
        body=[
            "Pure cane sugar blended with culinary lavender grown at Cavalli Estates for a delicate, distinct floral sweetness.",
            "Bake it into shortbread and scones, stir it into tea or lemonade, sprinkle it over fruit, or rim a cocktail glass.",
        ],
        details=["A little over 4 oz per container", "Ingredients: pure cane sugar, dried culinary lavender", "Grown and blended at Cavalli Estates"],
        options=[],
    ),

    # ---------------- Gift Sets ----------------
    dict(
        etsy="4394414319", handle="lavender-wellness-gift-box", collection="gifts", featured=True,
        title="Lavender Wellness Gift Box", price=70.00, tag="Gift box",
        blurb="Bath salts, soap, candle, roll-on, and a sachet, ribbon-tied and ready to give.",
        body=[
            "A gift box filled with our farm's lavender products, for birthdays, holidays, bridesmaids, or anyone who deserves an evening of calm.",
            "It arrives beautifully packaged, wrapped with care, and tied with ribbon.",
        ],
        details=["Pure Lavender: lavender bath salts, lavender soap, lavender candle, lavender roll-on, garden botanical sachet", "Calming Lavender: lavender chamomile bath salts, lavender lilac soap, lavender candle, lavender-chamomile-cedarwood roll-on, garden botanical sachet"],
        options=[
            ("Box", ["Pure Lavender", "Calming Lavender"]),
        ],
    ),
    dict(
        etsy="4506940021", handle="lavender-gift-trio", collection="gifts",
        title="Lavender Gift Trio", price=25.00, tag="Mist, oil & sachet",
        blurb="A linen mist, a roll-on oil, and a potpourri sachet, gift-ready.",
        body=[
            "Three of our favorites together: a mist for pillows and linens, a roll-on for the purse, and a sachet for a drawer or the car.",
            "Gift-ready and handcrafted in small batches, it is an easy hostess, bridesmaid, or birthday gift.",
        ],
        details=["Lavender: Signature Lavender roll-on, lavender mist, potpourri sachet", "Relax: lavender, cedarwood, and chamomile roll-on, lavender chamomile mist, potpourri sachet", "Botanical: lavender, cedarwood, and chamomile roll-on, lavender rose mist, potpourri sachet"],
        options=[
            ("Set", ["Lavender", "Relax", "Botanical"]),
        ],
    ),
    dict(
        # notes=True: the scent picks travel to Shopify as order notes on a
        # single variant, instead of 216 scent combinations.
        notes=True,
        etsy="4618848757", handle="linen-mist-set", collection="gifts", featured=True,
        title="Linen Mist Set, Gift Box", price=35.00, tag="Choose 3 scents",
        blurb="Three estate linen mists of your choosing, boxed for gifting.",
        body=[
            "Choose your three favorite scents to make a personal set. Our linen mists freshen bedding, linens, towels, and living spaces with a light, natural fragrance.",
            "Each set arrives beautifully packaged in a gift box, ready to give.",
        ],
        details=["Three linen mists, your choice of scents, in a gift box", "No. 00 Pure Bliss: lavender", "No. 01 Evening Calm: lavender, chamomile, cedarwood", "No. 02 Citrus Grove: lavender, bergamot, lemon, orange", "No. 03 Rose Petal: lavender, rose, bergamot", "No. 04 Golden Dust: lavender, chamomile, bergamot, sweet orange, sandalwood", "No. 05 Coastal Grove: lavender, lemon, eucalyptus, rosemary"],
        options=[
            ("Scent 1", ["No. 00 Pure Bliss", "No. 01 Evening Calm", "No. 02 Citrus Grove", "No. 03 Rose Petal", "No. 04 Golden Dust", "No. 05 Coastal Grove"]),
            ("Scent 2", ["No. 00 Pure Bliss", "No. 01 Evening Calm", "No. 02 Citrus Grove", "No. 03 Rose Petal", "No. 04 Golden Dust", "No. 05 Coastal Grove"]),
            ("Scent 3", ["No. 00 Pure Bliss", "No. 01 Evening Calm", "No. 02 Citrus Grove", "No. 03 Rose Petal", "No. 04 Golden Dust", "No. 05 Coastal Grove"]),
        ],
    ),
    dict(
        etsy="4375980171", handle="soap-gift-set", collection="gifts",
        title="Handmade Soap Gift Set", price=15.00, tag="Boxed",
        blurb="A lavender bar, a mini oatmeal bar, and your choice of lilac or gardenia, boxed.",
        body=[
            "Our small-batch soaps, packaged in a gift box tied with twine and ready to give for birthdays, holidays, or thank-yous.",
        ],
        details=["1 lavender soap", "1 mini oatmeal soap, gently exfoliating", "1 Lavender Lilac or Lavender Gardenia soap", "Handmade in small batches"],
        options=[
            ("Pairing", ["Lavender & Lavender Lilac", "Lavender & Lavender Gardenia"]),
        ],
    ),

    # ---------------- Farm & Garden ----------------
    dict(
        etsy="4387103105", handle="lavender-guard", collection="farm",
        title="Lavender Guard", price=19.98, tag="Pest repellent",
        blurb="A plant-based pest and rodent repellent for homes, gardens, barns, and tack rooms.",
        body=[
            "A blend of lavender buds, dried petals, and essential oils that repels pests and rodents by scent, without harsh chemicals, and leaves a clean lavender smell behind. Made for homes, farms, and stables.",
            "Sprinkle it generously around the perimeter of homes, gardens, barns, and sheds, and reapply after heavy rain or when pests are active.",
        ],
        details=["Purple box, about 14 oz: lavender blend and essential oils only, for prevention and enclosed spaces", "White box, about 19 oz: adds food-grade diatomaceous earth, for barns, stalls, and heavier activity"],
        options=[
            ("Formula", [("Lavender only (purple box)", 19.98), ("With diatomaceous earth (white box)", 24.98)]),
        ],
    ),
    dict(
        etsy="4305077327", handle="peck-and-petal-nesting-blend", collection="farm",
        title="Peck & Petal Nesting Blend", price=20.00, tag="16 oz",
        blurb="An herb and flower blend for nesting boxes that keeps coops fresh and hens happy.",
        body=[
            "A fragrant, all-natural blend of herbs and flowers that keeps nesting boxes cozy and fresh and encourages hens to lay.",
            "Sprinkle a little into each nesting box, toss a handful onto the coop floor to help with pests and odors, and refresh as needed.",
        ],
        details=["16 oz bag", "Lavender, rosemary, calendula, rose petals, lemongrass, mint, and marigold", "100% natural"],
        options=[],
    ),
]
