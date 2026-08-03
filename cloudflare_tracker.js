/**
 * ╔══════════════════════════════════════════════════════════╗
 * ║   DEAL BAZAAR — Click Tracker (Cloudflare Worker)       ║
 * ║   Free tier: 100k requests/day, 1GB KV storage          ║
 * ║                                                          ║
 * ║   Endpoints:                                             ║
 * ║   POST /track  — log a click {asin, name, price, cat}   ║
 * ║   GET  /stats  — return all click counts as JSON        ║
 * ║   GET  /top    — return top 10 products by clicks       ║
 * ╚══════════════════════════════════════════════════════════╝
 *
 * Setup (5 min):
 *   1. workers.cloudflare.com → sign up free
 *   2. Create Worker → paste this code → Deploy
 *   3. Workers & Pages → KV → Create namespace "CLICKS"
 *   4. Worker → Settings → Variables → KV Bindings → add CLICKS
 *   5. Copy your Worker URL → add to config.py as TRACKER_URL
 */

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS });
    }

    // ── POST /track ──────────────────────────────────────────
    if (request.method === "POST" && url.pathname === "/track") {
      try {
        const body = await request.json();
        const { asin, name, price, category, discount } = body;
        if (!asin) return new Response("Missing asin", { status: 400 });

        // Increment click count
        const countKey = `clicks:${asin}`;
        const existing = await env.CLICKS.get(countKey);
        const count = existing ? parseInt(existing) + 1 : 1;
        await env.CLICKS.put(countKey, String(count));

        // Store product metadata (first time only — saves KV writes)
        const metaKey = `meta:${asin}`;
        if (!existing) {
          await env.CLICKS.put(metaKey, JSON.stringify({
            name: name || "Unknown",
            price: price || 0,
            category: category || "Unknown",
            discount: discount || 0,
            first_seen: new Date().toISOString()
          }));
        }

        // Increment daily counter for today
        const today = new Date().toISOString().slice(0, 10);
        const dailyKey = `daily:${today}:${asin}`;
        const dailyExisting = await env.CLICKS.get(dailyKey);
        const dailyCount = dailyExisting ? parseInt(dailyExisting) + 1 : 1;
        await env.CLICKS.put(dailyKey, String(dailyCount), {
          expirationTtl: 7 * 24 * 3600  // auto-delete after 7 days
        });

        return new Response(JSON.stringify({ ok: true, asin, count }), {
          headers: { ...CORS, "Content-Type": "application/json" }
        });
      } catch (e) {
        return new Response(JSON.stringify({ error: e.message }), {
          status: 500,
          headers: { ...CORS, "Content-Type": "application/json" }
        });
      }
    }

    // ── GET /stats ───────────────────────────────────────────
    if (request.method === "GET" && url.pathname === "/stats") {
      const list = await env.CLICKS.list({ prefix: "clicks:" });
      const stats = {};
      for (const key of list.keys) {
        const asin = key.name.replace("clicks:", "");
        const count = await env.CLICKS.get(key.name);
        const meta = await env.CLICKS.get(`meta:${asin}`);
        stats[asin] = {
          clicks: parseInt(count || 0),
          ...(meta ? JSON.parse(meta) : {})
        };
      }
      return new Response(JSON.stringify(stats, null, 2), {
        headers: { ...CORS, "Content-Type": "application/json" }
      });
    }

    // ── GET /top ─────────────────────────────────────────────
    if (request.method === "GET" && url.pathname === "/top") {
      const limit = parseInt(url.searchParams.get("n") || "10");
      const list = await env.CLICKS.list({ prefix: "clicks:" });
      const items = [];
      for (const key of list.keys) {
        const asin = key.name.replace("clicks:", "");
        const count = await env.CLICKS.get(key.name);
        const meta = await env.CLICKS.get(`meta:${asin}`);
        items.push({
          asin,
          clicks: parseInt(count || 0),
          ...(meta ? JSON.parse(meta) : { name: asin, price: 0, category: "Unknown", discount: 0 })
        });
      }
      items.sort((a, b) => b.clicks - a.clicks);
      return new Response(JSON.stringify(items.slice(0, limit), null, 2), {
        headers: { ...CORS, "Content-Type": "application/json" }
      });
    }

    // ── GET /today ───────────────────────────────────────────
    if (request.method === "GET" && url.pathname === "/today") {
      const today = new Date().toISOString().slice(0, 10);
      const list = await env.CLICKS.list({ prefix: `daily:${today}:` });
      const items = [];
      for (const key of list.keys) {
        const asin = key.name.split(":")[2];
        const count = await env.CLICKS.get(key.name);
        const meta = await env.CLICKS.get(`meta:${asin}`);
        items.push({
          asin,
          clicks_today: parseInt(count || 0),
          ...(meta ? JSON.parse(meta) : { name: asin, price: 0, category: "Unknown", discount: 0 })
        });
      }
      items.sort((a, b) => b.clicks_today - a.clicks_today);
      return new Response(JSON.stringify({
        date: today,
        total_clicks: items.reduce((s, i) => s + i.clicks_today, 0),
        top_products: items.slice(0, 10)
      }, null, 2), {
        headers: { ...CORS, "Content-Type": "application/json" }
      });
    }

    return new Response("Deal Bazaar Click Tracker — endpoints: /track (POST), /stats, /top, /today", {
      headers: CORS
    });
  }
};
