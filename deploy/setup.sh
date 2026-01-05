#!/usr/bin/env bash
set -euo pipefail
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d postgres redis
sleep 5
