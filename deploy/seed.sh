#!/usr/bin/env bash
set -euo pipefail
docker compose -f docker-compose.prod.yml run --rm web python manage.py loaddata backend/fixtures/seed.json
