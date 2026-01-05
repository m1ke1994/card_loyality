# API (v1)

Auth / Telegram
- `POST /api/v1/telegram/session/start` — bot creates login token (header `X-Bot-Token`).
- `POST /api/v1/auth/telegram/consume` — exchange token → JWT.
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`

Client
- `GET /api/v1/me`
- `GET /api/v1/me/visits`
- `GET /api/v1/me/transactions`
- `GET /api/v1/me/coupons`
- `POST /api/v1/tokens/issue`

Staff
- `GET /api/v1/staff/me`
- `GET /api/v1/staff/places`
- `POST /api/v1/tokens/verify` { token, place_id }
- `POST /api/v1/visits/checkout` { visit_id, amount_total, points_spent, coupon_code? }
- `POST /api/v1/points/adjust`

Admin
- CRUD places: `admin/places`
- CRUD staff: `admin/staff`
- CRUD coupons: `admin/coupons`
- CRUD promotions: `admin/promotions`
- Reports: `/admin/reports/summary`, `/admin/reports/visits`, `/admin/reports/transactions`

Docs
- Swagger UI: `/api/docs/`
- OpenAPI schema: `/api/schema/`
