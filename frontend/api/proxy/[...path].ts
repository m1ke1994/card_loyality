import type { VercelRequest, VercelResponse } from "@vercel/node";

const BACKEND_BASE =
  process.env.BACKEND_BASE_URL || "http://45.151.69.84:8000";

export default async function handler(req: VercelRequest, res: VercelResponse) {
  const pathParam = req.query.path;
  const targetPath = Array.isArray(pathParam)
    ? pathParam.join("/")
    : typeof pathParam === "string"
    ? pathParam
    : "";

  const url = `${BACKEND_BASE}/${targetPath}`;

  const headers: Record<string, string> = {};
  for (const [k, v] of Object.entries(req.headers)) {
    if (typeof v === "string") headers[k] = v;
  }
  delete headers["host"];

  const method = (req.method || "GET").toUpperCase();
  const hasBody = !["GET", "HEAD"].includes(method);

  const upstream = await fetch(url, {
    method,
    headers,
    body: hasBody ? JSON.stringify(req.body ?? {}) : undefined,
  });

  res.status(upstream.status);
  upstream.headers.forEach((value, key) => {
    if (key.toLowerCase() === "transfer-encoding") return;
    res.setHeader(key, value);
  });

  const buf = Buffer.from(await upstream.arrayBuffer());
  res.send(buf);
}
