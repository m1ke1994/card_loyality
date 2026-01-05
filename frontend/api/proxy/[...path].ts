export const config = { runtime: "edge" };

const UPSTREAM_ORIGIN =
  (process.env.UPSTREAM_ORIGIN ||
    process.env.BACKEND_ORIGIN ||
    process.env.API_ORIGIN ||
    "").trim();

function withCors(headers: Headers) {
  // можно убрать, если не нужно. Ќо так надЄжнее дл€ любых запросов/префлайтов.
  headers.set("access-control-allow-origin", "*");
  headers.set("access-control-allow-methods", "GET,POST,PUT,PATCH,DELETE,OPTIONS");
  headers.set("access-control-allow-headers", "authorization,content-type,accept");
  headers.set("access-control-max-age", "86400");
  return headers;
}

export default async function handler(req: Request): Promise<Response> {
  if (!UPSTREAM_ORIGIN) {
    return new Response("Missing UPSTREAM_ORIGIN (or BACKEND_ORIGIN/API_ORIGIN) env var", {
      status: 500,
    });
  }

  const method = req.method.toUpperCase();

  // preflight
  if (method === "OPTIONS") {
    return new Response(null, { status: 204, headers: withCors(new Headers()) });
  }

  const incomingUrl = new URL(req.url);

  // /api/proxy/<rest>
  const prefix = "/api/proxy";
  const restPath = incomingUrl.pathname.startsWith(prefix)
    ? incomingUrl.pathname.slice(prefix.length)
    : incomingUrl.pathname;

  // гарантируем, что путь начинаетс€ с /
  const normalizedPath = restPath.startsWith("/") ? restPath : `/${restPath}`;

  const upstreamUrl = new URL(`${normalizedPath}${incomingUrl.search}`, UPSTREAM_ORIGIN);

  // копируем заголовки, но убираем те, что ломают прокси/длину
  const headers = new Headers(req.headers);
  headers.delete("host");
  headers.delete("content-length");
  headers.delete("accept-encoding"); // пусть платформа сама решает

  const body =
    method === "GET" || method === "HEAD" ? undefined : await req.arrayBuffer();

  const upstreamRes = await fetch(upstreamUrl.toString(), {
    method,
    headers,
    body,
    redirect: "manual",
  });

  // возвращаем ответ как есть
  const outHeaders = new Headers(upstreamRes.headers);
  withCors(outHeaders);

  return new Response(upstreamRes.body, {
    status: upstreamRes.status,
    headers: outHeaders,
  });
}
