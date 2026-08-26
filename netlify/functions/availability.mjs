/* ============================================================
   Cavalli Estates — Airbnb availability (serverless)
   ------------------------------------------------------------
   Reads each listing's Airbnb iCal export feed server-side (no CORS
   issues), parses the booked/blocked dates, and returns them as JSON
   so the "Check Availability" bar can flag unavailable dates — always
   in sync with Airbnb.

   TO ACTIVATE (once the client has the iCal links):
   In Airbnb → Calendar → pick the listing → Availability →
     "Connect to another website" → Export calendar → copy the .ics URL.
   Then in Netlify → Site settings → Environment variables, add:
     CAVALLI_ICAL_RANCHHOUSE = https://www.airbnb.com/calendar/ical/....ics
     CAVALLI_ICAL_VILLA      = https://www.airbnb.com/calendar/ical/....ics
     CAVALLI_ICAL_VINEYARD   = https://www.airbnb.com/calendar/ical/....ics
   No redeploy needed for the data; the function reads them live.
   Until they're set, this returns empty availability (no restrictions).
   ============================================================ */

export default async (req) => {
  // Demo mode (?demo=1): sample booked dates so the calendar can be previewed
  // before the real Airbnb iCal feeds are connected.
  let demo = false;
  try { demo = new URL(req.url).searchParams.has("demo"); } catch {}
  if (demo) {
    const mk = (ranges) => {
      const out = [], base = new Date(); base.setHours(12, 0, 0, 0);
      for (const [a, b] of ranges) for (let i = a; i <= b; i++) { const d = new Date(base); d.setDate(d.getDate() + i); out.push(d.toISOString().slice(0, 10)); }
      return out;
    };
    const listings = {
      ranchhouse: mk([[3, 6], [20, 23], [38, 40]]),
      villa: mk([[8, 12], [27, 27], [34, 36]]),
      vineyard: mk([[2, 2], [14, 17], [30, 33], [45, 48]]),
    };
    return new Response(JSON.stringify({ updated: new Date().toISOString(), configured: true, demo: true, listings, fullyBooked: [] }), {
      headers: { "content-type": "application/json", "cache-control": "no-store" },
    });
  }

  const feeds = {
    ranchhouse: process.env.CAVALLI_ICAL_RANCHHOUSE,
    villa: process.env.CAVALLI_ICAL_VILLA,
    vineyard: process.env.CAVALLI_ICAL_VINEYARD,
  };

  const listings = {};
  const busySets = [];

  await Promise.all(
    Object.entries(feeds).map(async ([key, url]) => {
      if (!url) { listings[key] = []; return; }
      try {
        const res = await fetch(url, { headers: { "User-Agent": "CavalliEstates/1.0 (+availability)" } });
        if (!res.ok) { listings[key] = []; return; }
        const dates = parseBusyDates(await res.text());
        listings[key] = dates;
        busySets.push(new Set(dates));
      } catch {
        listings[key] = [];
      }
    })
  );

  // Dates where EVERY listing is booked = the estate has nothing open.
  let fullyBooked = [];
  if (busySets.length) {
    const [first, ...rest] = busySets;
    fullyBooked = [...first].filter((d) => rest.every((s) => s.has(d))).sort();
  }

  const configured = Object.values(feeds).some(Boolean);

  return new Response(JSON.stringify({ updated: new Date().toISOString(), configured, listings, fullyBooked }), {
    headers: { "content-type": "application/json", "cache-control": "public, max-age=900" },
  });
};

function parseBusyDates(ics) {
  const out = new Set();
  const events = String(ics).split("BEGIN:VEVENT").slice(1);
  for (const ev of events) {
    const s = matchDate(ev, "DTSTART");
    const e = matchDate(ev, "DTEND");
    if (!s) continue;
    const start = toDate(s);
    const end = e ? toDate(e) : addDays(start, 1); // Airbnb DTEND is exclusive
    for (let d = new Date(start); d < end; d = addDays(d, 1)) out.add(iso(d));
  }
  return [...out].sort();
}
function matchDate(block, key) {
  const m = block.match(new RegExp(key + "[^:\\n]*:(\\d{8})"));
  return m ? m[1] : null;
}
function toDate(v) {
  return new Date(Date.UTC(+v.slice(0, 4), +v.slice(4, 6) - 1, +v.slice(6, 8)));
}
function addDays(dt, n) {
  const x = new Date(dt);
  x.setUTCDate(x.getUTCDate() + n);
  return x;
}
function iso(dt) {
  return dt.toISOString().slice(0, 10);
}
