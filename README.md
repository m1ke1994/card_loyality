# Loyalty SaaS

Multi-tenant loyalty platform with Telegram-only auth, dynamic QR, and Vercel-proxied frontend.

## Structure
- `backend/` — Django + DRF + Celery + PostgreSQL/Redis.
- `frontend/` — Vue 3 + Vite monorepo (client PWA, staff PWA, admin, widget).
- `docs/` — architecture, API, widget integration.
- `docker-compose.prod.yml` — production stack (web, worker, beat, postgres, redis).
- `deploy/` — helper scripts (setup, migrate, seed).

## Quick start
1. Copy `.env.example` to `.env` and fill secrets.
2. `docker compose -f docker-compose.prod.yml up -d postgres redis`.
3. `docker compose -f docker-compose.prod.yml run --rm web python manage.py migrate`.
4. `docker compose -f docker-compose.prod.yml run --rm web python manage.py loaddata backend/fixtures/seed.json`.
5. Deploy frontend to Vercel with `frontend/vercel.json` proxying `/api` to backend.

Swagger docs available at `/api/docs/`, schema at `/api/schema/`.
