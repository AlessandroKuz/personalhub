#!/bin/sh
# deploy.sh — run on VPS after pulling code, before `docker compose up`.
# Builds the new image, prepares static assets, then restarts services
# and purges Cloudflare cache for JS files (avoids stale vimNav.js).
set -e

# Load Cloudflare credentials from optional .env.prod file
[ -f .env.prod ] && . .env.prod

echo "==> Pulling new image from GHCR..."
docker compose pull web

echo "==> Running pre-start tasks..."
docker compose run --rm web sh -c "
  python manage.py migrate --noinput &&
  python manage.py compress --force &&
  python manage.py collectstatic --noinput &&
  python manage.py compilemessages
"

echo "==> Restarting web service..."
docker compose up -d --no-deps web

echo "==> Purging Cloudflare static JS cache..."
curl -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/purge_cache" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"prefixes":["https://alessandrokuz.com/static/js/"]}'

echo "==> Done."
