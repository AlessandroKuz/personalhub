#!/bin/sh
# Using /bin/sh (POSIX shell) rather than /bin/bash because slim images
# may not have bash installed. POSIX sh is always available.

# Exit immediately if any command fails. This prevents the server from
# starting if migrations or collectstatic fail, which would hide errors.
set -e

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Compressing SCSS and JS assets (offline compression)..."
# compress must run BEFORE collectstatic.
# It compiles SCSS → CSS, writes output files, and generates a manifest
# that Django uses to serve pre-compiled assets without runtime compilation.
python manage.py compress --force

echo "==> Collecting static files..."
# WhiteNoise serves static files directly from Django, so we need
# collectstatic to gather everything into STATIC_ROOT before starting.
python manage.py collectstatic --noinput

echo "==> Starting Uvicorn (ASGI)..."
# `exec` replaces this shell process with uvicorn, making uvicorn PID 1.
# PID 1 receives OS signals (SIGTERM, SIGINT) directly from Docker.
# Without exec, the shell would be PID 1 and signals might not reach uvicorn,
# causing slow or unclean shutdowns.
exec uvicorn config.asgi:application \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 2
# --workers: For a small VPS, 2 async workers is a good starting point.
# Each worker is an independent process with its own event loop.
# For async Django with Uvicorn, you can also use --worker-class uvicorn.workers.UvicornWorker
# via gunicorn for more process management control — a future consideration.
