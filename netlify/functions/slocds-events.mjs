/* ============================================================
   Cavalli Estates: SLO-CDS chapter calendar (serverless)
   ------------------------------------------------------------
   Pulls the San Luis Obispo Chapter of the California Dressage
   Society's public event feed and returns upcoming events (plus a
   few recent ones) for the Equestrian page.

   Freshness: Netlify's CDN keeps the response for 24 hours, then
   fetches the chapter feed again (serving the last copy while it
   refreshes, for up to a week if the chapter site is down). New
   chapter events appear on Cavalli within a day of being published.

   Feed URL defaults to the chapter's Netlify site. When the chapter
   moves to slocds.org, set SLOCDS_EVENTS_URL in Netlify environment
   variables (e.g. https://www.slocds.org/events.json).
   ============================================================ */
const FEED = process.env.SLOCDS_EVENTS_URL || "https://slocds.netlify.app/events.json";

const todayPacific = () =>
  new Intl.DateTimeFormat("en-CA", { timeZone: "America/Los_Angeles" }).format(new Date());

export default async () => {
  const headers = {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "public, max-age=900",
    "netlify-cdn-cache-control": "public, durable, s-maxage=86400, stale-while-revalidate=604800",
  };
  try {
    const res = await fetch(FEED, { headers: { accept: "application/json" } });
    if (!res.ok) throw new Error("feed " + res.status);
    const data = await res.json();
    const base = new URL(FEED);
    const today = todayPacific();
    const all = (data.events || []).map((e) => ({
      title: e.title,
      start: e.start,
      end: e.end || e.start,
      dateLabel: e.dateLabel || null,
      time: e.time || null,
      venue: e.venue || null,
      kind: e.kind || "other",
      chapterHosted: !!e.chapterHosted,
      atCavalli: /cavalli/i.test(e.venue || "") || /cavalli/i.test(e.title || ""),
      summary: e.summary || null,
      link: e.link || null,
      url: e.calendar ? new URL(e.calendar, base).href : new URL("/calendar", base).href,
    }));
    const upcoming = all.filter((e) => e.end >= today);
    const recent = all.filter((e) => e.end < today).reverse().slice(0, 3);
    return new Response(
      JSON.stringify({
        source: new URL("/calendar", base).href,
        fetched: new Date().toISOString(),
        upcoming,
        recent,
      }),
      { headers }
    );
  } catch (err) {
    return new Response(JSON.stringify({ error: String(err.message || err), upcoming: [], recent: [] }), {
      status: 502,
      headers: { "content-type": "application/json", "cache-control": "no-store" },
    });
  }
};

export const config = { path: "/api/slocds-events" };
