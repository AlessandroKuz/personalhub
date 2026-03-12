#!/usr/bin/env bash
# scripts/dev.sh — start both dev servers, kill both on exit

set -e

cleanup() {
    echo ""
    echo "Shutting down dev servers..."
    kill $(jobs -p) 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "Starting Django (ASGI) on http://127.0.0.1:8080"
echo "Starting MkDocs on    http://127.0.0.1:8001"
echo "Press Ctrl+C to stop both."
echo ""

uv run uvicorn config.asgi:application --reload --port 8080 &
uv run mkdocs serve --dev-addr 127.0.0.1:8001 &

wait

