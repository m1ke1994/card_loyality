import type { VercelRequest, VercelResponse } from "@vercel/node";

const BACKEND_BASE_URL = (process.env.BACKEND_BASE_URL || "http://45.151.69.84:8000").replace(/\/+$/, "");

export default async function handler(req: VercelRequest, res: VercelResponse) {
  const pathParam = req.query.path;
  const rawPath = Array.isArray(pathParam) ? pathParam.join("/") : pathParam || "";
  const targetPath = rawPath.toString().replace(/^\/+/, "");
  const targetUrl = `${BACKEND_BASE_URL}/api/${targetPath}`;

  const method = (req.method || "GET").toUpperCase();

  const headers: Record<string, string> = {};
  for (const [key, value] of Object.entries(req.headers)) {
    if (key.toLowerCase() === "host") continue;
    if (Array.isArray(value)) {
      headers[key] = value.join(", ");
    } else if (typeof value === "string") {
      headers[key] = value;
    }
  }

  let body: Buffer | undefined;
  if (method !== "GET" && method !== "HEAD") {
    const chunks: Buffer[] = [];
    for await (const chunk of req) {
      chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
    }
    body = Buffer.concat(chunks);
  }

  const upstream = await fetch(targetUrl, {
    method,
    headers,
    body
  });

  res.status(upstream.status);
  upstream.headers.forEach((value, key) => {
    res.setHeader(key, value);
  });
  const responseBuffer = Buffer.from(await upstream.arrayBuffer());
  res.send(responseBuffer);
}
