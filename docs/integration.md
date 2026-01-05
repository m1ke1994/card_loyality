# Widget Integration Guide

## Quick start
Add a single script tag on your site (Tilda/WordPress/Next.js):

```html
<script
  src="https://<vercel-domain>/widget.js"
  data-tenant="restaurant-slug"
  data-theme="auto"
  data-button-text="Карта лояльности">
</script>
```

The script renders a floating button and opens a modal with an iframe to `https://<vercel-domain>/w/restaurant-slug`.

## Script attributes
- `data-tenant` (required): tenant slug.
- `data-theme`: `light` | `dark` | `auto`.
- `data-button-text`: custom CTA text.

## postMessage events
- `loyalty:open` — modal opened.
- `loyalty:close` — modal closed.
- `loyalty:auth` — user authorized inside iframe (close modal if needed).

## FAQ
- **HTTPS only?** Widget works on HTTPS; API is proxied via Vercel `/api`.
- **Can I style the button?** Wrap the script in a container and override button styles via CSS.
- **Caching?** Proxy responses are `Cache-Control: no-store`.

## CSP
Allow:
- `script-src https://<vercel-domain>`
- `frame-src https://<vercel-domain>`

## Platform snippets
- **Tilda**: add the script to “Дополнительный HTML”.
- **WordPress**: add to Theme > Custom HTML or a widget area.
- **Next.js**: add to `_app.tsx` using `next/script` with `strategy="afterInteractive"`.
