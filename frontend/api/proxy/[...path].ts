export const config = { runtime: "edge" };
const UPSTREAM_ORIGIN = (process.env.UPSTREAM_ORIGIN || process.env.BACKEND_ORIGIN || process.env.API_ORIGIN || "").trim();

function withCors(h: Headers) {
  h.set("access-control-allow-origin", "*");
  h.set("access-control-allow-methods", "GET,POST,PUT,PATCH,DELETE,OPTIONS");
  h.set("access-control-allow-headers", "authorization,content-type,accept");
  h.set("access-control-max-age", "86400");
  return h;
}

export default async function handler(req: Request): Promise<Response> {
  const method = req.method.toUpperCase();
  if (method === "OPTIONS") {
    return new Response(null, { status: 204, headers: withCors(new Headers()) });
  }

  const u = new URL(req.url);
  const prefix = "/api/proxy";
  const rest = u.pathname.startsWith(prefix) ? u.pathname.slice(prefix.length) : u.pathname;
  const path = rest.startsWith("/") ? rest : `/${rest}`;

  if (path === "/__ping") {
    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: withCors(new Headers({ "content-type": "application/json" })),
    });
  }

  if (!UPSTREAM_ORIGIN) {
    return new Response("Missing UPSTREAM_ORIGIN", { status: 500, headers: withCors(new Headers()) });
  }

  const upstream = new URL(`${path}${u.search}`, UPSTREAM_ORIGIN);
  const headers = new Headers(req.headers);
  headers.delete("host");
  headers.delete("content-length");
  headers.delete("accept-encoding");

  const body = method === "GET" || method === "HEAD" ? undefined : await req.arrayBuffer();

  const r = await fetch(upstream.toString(), { method, headers, body, redirect: "manual" });
  const out = new Headers(r.headers);
  withCors(out);
  return new Response(r.body, { status: r.status, headers: out });
}
