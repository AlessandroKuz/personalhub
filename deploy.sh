#!/bin/sh
# deploy.sh — run this on the VPS after pulling new code, before `docker compose up`.
# It builds the new image, prepares static assets, then starts/restarts services.
set -e

echo "==> Building new image..."
docker compose build

echo "==> Compressing SCSS/JS assets..."
# --rm removes the temporary container after the command finishes.
# We run this against the newly built image before starting the main service.
docker compose run --rm web \
  python manage.py compress --force

echo "==> Collecting static files..."
docker compose .yml run --rm web \
  python manage.py collectstatic --noinput

echo "==> Starting services..."
# --no-build skips rebuilding since we already did it above.
docker compose up -d --no-build

echo "==> Done. Tailing logs (Ctrl+C to exit)..."
docker compose logs -f web
