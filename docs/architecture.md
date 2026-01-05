# Architecture

- Frontend: Vercel (HTTPS). Apps: Client PWA, Staff PWA, Admin Web, Docs page, widget.js. API base `/api`.
- Backend: Django + DRF + Celery on server (`http://45.151.69.84`). PostgreSQL, Redis, Gunicorn. All browser requests go through Vercel proxy `/api/*` → backend.
- Auth: Telegram-only. Bot starts session, frontend consumes token and receives JWT (access/refresh).
- QR: `/api/v1/tokens/issue` (TTL 30s) for client; `/api/v1/tokens/verify` for staff with active-visit lock.
- Data: multi-tenant with slug header `X-Tenant-Slug`. Tenants, domains, places, users, staff, loyalty accounts, transactions, visits, active visits, coupons, promotions, audit logs.
- Background: Celery beat auto-closes stale active visits after `ACTIVE_VISIT_AUTO_CLOSE_HOURS`.
- Docs & API: Swagger at `/api/docs/`, schema at `/api/schema/`.

## Deploy flow
1. `docker compose -f docker-compose.prod.yml up -d postgres redis`.
2. Build backend image (gunicorn) + Celery worker/beat.
3. `deploy/migrate.sh`, `deploy/seed.sh`.
4. Deploy frontend to Vercel with `vercel.json` rewrites.
