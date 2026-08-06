# Cavalli Estates — Open Questions for the Client

Everything the new site needs confirmed before launch. Placeholders are marked in-page with a gold italic "By enquiry" / "to be confirmed" style (`.todo`).

## Brand
- **Palette & type are a proposed direction** (ivory + warm charcoal + muted bronze-gold; Cormorant Garamond + Jost). Confirm, or provide a logo / style guide. All colors/fonts are tokenized in `css/style.css` — a single edit swaps them site-wide.
- **Logo:** currently a text wordmark ("Cavalli Estates"). The old `SDSFSD.png` was not reused. Provide a real vector wordmark if available.
- **Tagline:** kept "Come for the lavender, stay for the magic" in the footer only; the site is now positioned estate-first (weddings, events, sanctuary, stays, lavender). Confirm this direction.

## Content / facts to confirm
- **Per-residence specs & pricing** — sleeps, bedrooms, baths, nightly/weekend rates for Ranchhouse, Villa, Vineyard House. Currently shown as "By enquiry."
- **Event capacities** — max guests for the barn / poolside / lavender-field ceremonies. Any figures are flagged for confirmation.
- **Animal Sanctuary copy is a draft** — written generally from the photos (Highland cattle, horses, goats, lambs, hens). Confirm which animals to feature and whether visits/feedings are offered to guests (and any schedule).
- **Open Farm Days date is stale** — the site's original "June 20 & 21, 2026" has already passed. The lavender page now presents Open Farm Days as a recurring seasonal event with the specific dates flagged "to be confirmed." Provide the next dates.
- **"500+ guests hosted" stat** on the home page — placeholder; confirm or replace with a real figure.

## Contact & booking
- **One brand email** — standardized to `cavalli.estates@gmail.com` (the address you already promote). Recommend a branded `stay@cavalliestates.com`. The scattered gmails, the personal Yahoo address, and the county code-enforcement/complaint line were intentionally kept OFF all public pages.
- **Booking phone** — using 805-242-1154 everywhere. Confirm this is the right public line.
- **Direct booking** — the hero "Check Availability" bar and all forms currently route to a lead-capture enquiry (Netlify Forms). Decide the long-term route: (a) lead-capture only, or (b) a real booking engine (Lodgify / OwnerRez / Hospitable) embedded, with Airbnb as one channel. This is the biggest revenue decision.
- **Social handles** — Instagram & Facebook links are placeholders (`#`). Provide the real handles.

## Deployment
- **No git repo / Netlify link yet.** To go live with working forms + auto-deploy, connect this folder to a GitHub repo and a Netlify site. Forms are already wired for Netlify (`data-netlify`, hidden `form-name`, honeypot).
- **Higher-resolution photo masters** would improve the full-bleed hero art (current images are web-scaled ~1024–2100px).
