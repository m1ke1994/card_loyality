import type { VercelRequest, VercelResponse } from "@vercel/node";
import httpProxy from "http-proxy";

const proxy = httpProxy.createProxyServer({});

export default function handler(req: VercelRequest, res: VercelResponse) {
  return new Promise((resolve, reject) => {
    proxy.web(
      req,
      res,
      {
        target: `http://45.151.69.84/${req.url?.replace(/^\\/api\\/proxy\\//, "")}`,
        changeOrigin: true,
        secure: false
      },
      (err) => {
        reject(err);
      }
    );
    proxy.once("proxyRes", () => resolve(null));
  });
}
