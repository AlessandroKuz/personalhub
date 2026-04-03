# ══════════════════════════════════════════════════════════════════════════════
# PersonalHub — justfile
# ══════════════════════════════════════════════════════════════════════════════
#
# Usage:   just <recipe>
# Help:    just          (lists all recipes with their comments)
# Dry run: just --dry-run <recipe>
#
# Install just on Arch: sudo pacman -S just
# Install just on Debian/Ubuntu: sudo apt install just
# Requires: just, uv, docker, docker compose v2
# ══════════════════════════════════════════════════════════════════════════════


# ── Variables ─────────────────────────────────────────────────────────────────
# just variables use := and are interpolated with {{ }} in recipes.
# No $ escaping needed — shell commands use $ freely without conflicts.

uv      := "uv"
run     := uv + " run"
manage  := run + " manage.py"
dc      := "docker compose"
service := "web"

# Languages for i18n - All supported locales. Add a new code here and `just messages` picks it up.
langs := "en it es de"


# ── Default: list all recipes ──────────────────────────────────────────────────
# Running bare `just` lists all recipes and their doc-comments automatically.
# No grep/awk trick needed — this is built into just.

# List all recipes — run `just` with no arguments to invoke this
default:
    @just --list --list-heading $'PersonalHub - available recipes:\n'


# ── Dependencies ──────────────────────────────────────────────────────────────

# Install all dependencies from uv.lock (reproducible environment)
install:
    {{ uv }} sync

# Upgrade all dependencies to latest compatible versions and update uv.lock
upgrade:
    {{ uv }} sync --upgrade
    @echo "→ uv.lock has been updated. Review the diff before committing."


# ── Development Server ────────────────────────────────────────────────────────

# Start the ASGI dev server via uvicorn (auto-reloads on file changes)
run:
    {{ run }} uvicorn config.asgi:application --reload \
        --reload-include "*.html" \
        --reload-include "*.css" \
        --reload-include "*.scss" \
        --reload-include "*.js"

# Start Django's built-in WSGI dev server — synchronous only, use for quick checks
# or when you need Django's interactive error debugger in the browser
runserver *args:
    {{ manage }} runserver {{ args }}

# Open an interactive Django Python shell
shell *args:
    {{ manage }} shell {{ args }}


# ── Django Management ─────────────────────────────────────────────────────────

# Run Django's built-in system checks (catches configuration errors early)
check *args:
    {{ manage }} check {{ args }}

# Apply all pending database migrations
migrate *args:
    {{ manage }} migrate {{ args }}

# Detect model changes and generate new migration files
makemigrations *args:
    {{ manage }} makemigrations {{ args }}

# Generate a new migration with an explicit name (usage: just migration add_slug_to_post)
migration name:
    {{ manage }} makemigrations --name {{ name }}

# Interactively create a new Django admin superuser
createsuperuser:
    {{ manage }} createsuperuser


# ── i18n ──────────────────────────────────────────────────────────────────────
# The shebang line #!/usr/bin/env bash tells just to run this recipe in bash,
# giving us a real shell with proper for-loop support.
# Without it, just uses sh, which works too, but bash is more explicit.

# Extract all translatable strings into .po files (runs for all configured languages)
messages:
    #!/usr/bin/env bash
    set -euo pipefail
    for lang in {{ langs }}; do
        echo "→ Extracting messages for $lang..."
        {{ manage }} makemessages -l $lang
    done

# Extract translatable strings for a single language (usage: just message de)
message lang:
    {{ manage }} makemessages -l {{ lang }}

# Compile all .po translation files into binary .mo files Django reads at runtime
compile-messages:
    {{ manage }} compilemessages

# Full i18n refresh: extract new strings then immediately compile everything
i18n: messages compile-messages


# ── Static Files & Linting ────────────────────────────────────────────────────

# Pre-compress and bundle SCSS/JS assets via django-compressor
compress *args:
    {{ manage }} compress {{ args }}

# Collect and compress static files (required before each production deploy)
static *args:
    {{ manage }} collectstatic --no-input {{ args }}

# Run Ruff linter — reports issues without modifying files
lint *args:
    {{ run }} ruff check {{ if args == "" { "." } else { args } }}

# Run Ruff linter and automatically fix all auto-fixable issues
lint-fix:
    {{ run }} ruff check --fix .

# Run Ruff formatter — reformats source code according to style rules
format *args:
    {{ run }} ruff format {{ if args == "" { "." } else { args } }}


# ── Testing ───────────────────────────────────────────────────────────────────

# Run the full test suite
test *args:
    {{ run }} pytest {{ args }}

# Run the full test suite with verbose output (shows each test name)
test-verbose *args:
    {{ run }} pytest -v {{ args }}

# Run tests and display a per-file line coverage report
test-coverage:
    {{ run }} pytest --cov=. --cov-report=term-missing

# Run lint + format check + full test suite — your pre-push safety net
ci:
    {{ run }} ruff check .
    {{ run }} ruff format --check .
    {{ run }} pytest


# ── Deployment (Docker) ───────────────────────────────────────────────────────
# Docker is used exclusively for deployment. There is one compose file.
# All commands here operate on docker-compose.yml.

# Build Docker images (run after changing Dockerfile or adding dependencies)
build:
    {{ dc }} build

# Build images and start all containers in the background
up:
    {{ dc }} up -d --build

# Stop and remove all containers (named volumes are preserved)
down:
    {{ dc }} down

# Stream live logs from all running containers (Ctrl+C to stop)
logs *args:
    {{ dc }} logs -f {{ args }}

# Show the status and port bindings of all containers
ps:
    {{ dc }} ps

# Open an interactive bash shell inside the running web container
exec:
    {{ dc }} exec {{ service }} /bin/bash

# Full deployment cycle: rebuild images, restart containers, migrate, compile translations
deploy: build
    {{ dc }} up -d
    {{ dc }} exec {{ service }} {{ manage }} migrate
    {{ dc }} exec {{ service }} {{ manage }} compilemessages
    {{ dc }} exec {{ service }} {{ manage }} compress --force
    {{ dc }} exec {{ service }} {{ manage }} collectstatic --no-input
    {{ dc }} logs -f {{ service }}


# ── Utils ─────────────────────────────────────────────────────────────────────

# Generate a new cryptographically strong SECRET_KEY value (copy into your .env)
secret-key:
    {{ run }} python -c "import secrets; print(secrets.token_urlsafe(50))"

# Wipe and recreate the local SQLite database from scratch (dev only — irreversible)
reset-db:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "⚠️  This will DELETE your local database. Press Enter to continue or Ctrl+C to abort."
    read -r
    rm -f db.sqlite3
    just migrate
    echo "→ Database reset complete."

# Print all registered URL patterns (requires django-extensions)
urls:
    {{ manage }} show_urls


# ── Cleanup ───────────────────────────────────────────────────────────────────

# Remove Python bytecode caches and compiled translation files
clean:
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -name "*.pyc" -delete
    find . -name "*.mo" -delete
    @echo "→ Workspace cleaned."
