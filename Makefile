# ══════════════════════════════════════════════════════════════════════════════
# PersonalHub — Makefile
# ══════════════════════════════════════════════════════════════════════════════
#
# Usage:   make <target>
# Help:    make                        (default goal prints this help)
# Args:    make <target> ARGS="..."    (pass extra flags to targets that support it)
# Dry run: make <target> --dry-run
#
# Requires: GNU Make 4.0+, uv, docker, docker compose v2
# ══════════════════════════════════════════════════════════════════════════════


# ── Variables ─────────────────────────────────────────────────────────────────

UV      := uv
RUN     := $(UV) run
MANAGE  := $(RUN) manage.py
DC      := docker compose
SERVICE := web

CYAN  := \033[36m
RESET := \033[0m

# All supported locales. Add a new code here and `make messages` picks it up.
LANGUAGES := en it es de

# Extra arguments forwarded to targets that support them.
# Usage: make migrate ARGS="--run-syncdb"
ARGS :=


# ── Phony Targets ─────────────────────────────────────────────────────────────

.PHONY: help \
        install upgrade \
        run runserver shell \
        check migrate makemigrations migration createsuperuser \
        messages message compile-messages i18n \
        compress static lint lint-fix format \
        test test-verbose test-coverage ci \
        build up down logs ps exec deploy \
        secret-key reset-db urls \
        clean


# ── Default Goal ──────────────────────────────────────────────────────────────

.DEFAULT_GOAL := help


# ── Help ──────────────────────────────────────────────────────────────────────
# Self-documenting: grep extracts lines matching "target: ## description" and
# awk formats them into a table. This is the standard Makefile help pattern.

help:
	@echo ""
	@echo "  PersonalHub — available targets"
	@echo "  ────────────────────────────────────────────────────────────"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-22s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "  Pass extra flags via ARGS: make migrate ARGS=\"--run-syncdb\""
	@echo "  Dry-run any target: make <target> --dry-run"
	@echo ""


# ── Dependencies ──────────────────────────────────────────────────────────────

install: ## Install all dependencies from uv.lock (reproducible environment)
	$(UV) sync

upgrade: ## Upgrade all dependencies to latest compatible versions and update uv.lock
	$(UV) sync --upgrade
	@echo "→ uv.lock has been updated. Review the diff before committing."


# ── Development Server ────────────────────────────────────────────────────────

run: ## Start the ASGI dev server via Uvicorn — watches Python, HTML, CSS, SCSS, JS
	$(RUN) uvicorn config.asgi:application --reload \
		--reload-include "*.html" \
		--reload-include "*.css" \
		--reload-include "*.scss" \
		--reload-include "*.js"

runserver: ## Start Django's synchronous WSGI dev server — use for browser error debugger
	$(MANAGE) runserver $(ARGS)

shell: ## Open an interactive Django Python shell — accepts ARGS="-i ipython"
	$(MANAGE) shell $(ARGS)


# ── Django Management ─────────────────────────────────────────────────────────

check: ## Run Django system checks — accepts ARGS="--deploy"
	$(MANAGE) check $(ARGS)

migrate: ## Apply all pending migrations — accepts ARGS="--run-syncdb"
	$(MANAGE) migrate $(ARGS)

makemigrations: ## Detect model changes and generate migration files — accepts ARGS="--merge"
	$(MANAGE) makemigrations $(ARGS)

migration: ## Generate a named migration — usage: make migration ARGS="add_slug_to_post"
	$(MANAGE) makemigrations --name $(ARGS)

createsuperuser: ## Interactively create a Django admin superuser
	$(MANAGE) createsuperuser


# ── i18n ──────────────────────────────────────────────────────────────────────
# Note the $$ in the for-loop: Make consumes single $ for its own variable
# expansion, so $$ is needed to pass a literal $ to the shell.

messages: ## Extract translatable strings into .po files for all configured languages
	@for lang in $(LANGUAGES); do \
		echo "→ Extracting messages for $$lang..."; \
		$(MANAGE) makemessages -l $$lang --ignore="site/*" --ignore="docs/*" --ignore=".venv/*"; \
	done

message: ## Extract strings for one language — usage: make message ARGS="de"
	$(MANAGE) makemessages -l $(ARGS) --ignore="site/*" --ignore="docs/*" --ignore=".venv/*"

compile-messages: ## Compile all .po files into binary .mo files
	$(MANAGE) compilemessages

i18n: messages compile-messages ## Full i18n refresh: extract then compile


# ── Static Files & Linting ────────────────────────────────────────────────────

compress: ## Compile and bundle SCSS/JS via django-compressor — accepts ARGS="--force"
	$(MANAGE) compress $(ARGS)

static: ## Collect static files into STATIC_ROOT — accepts ARGS="--clear"
	$(MANAGE) collectstatic --no-input $(ARGS)

# $(if $(ARGS),$(ARGS),.) means: use ARGS if provided, otherwise default to "."
# This mirrors the `if args == "" { "." } else { args }` behaviour in the justfile.
lint: ## Run Ruff linter — accepts a path via ARGS, defaults to scanning everything
	$(RUN) ruff check $(if $(ARGS),$(ARGS),.)

lint-fix: ## Run Ruff linter and automatically apply all safe fixes
	$(RUN) ruff check --fix .

format: ## Run Ruff formatter — accepts a path via ARGS, defaults to formatting everything
	$(RUN) ruff format $(if $(ARGS),$(ARGS),.)


# ── Testing ───────────────────────────────────────────────────────────────────

test: ## Run the full test suite — accepts ARGS="-x", ARGS="apps/core/tests.py"
	$(RUN) pytest $(ARGS)

test-verbose: ## Run the full test suite with verbose output — accepts same ARGS as test
	$(RUN) pytest -v $(ARGS)

test-coverage: ## Run tests and display a per-file line coverage report
	$(RUN) pytest --cov=. --cov-report=term-missing

ci: ## Run lint + format check + full test suite — pre-push safety net
	$(RUN) ruff check .
	$(RUN) ruff format --check .
	$(RUN) pytest


# ── Deployment (Docker) ───────────────────────────────────────────────────────

build: ## (Re)build Docker images — run after changing Dockerfile or dependencies
	$(DC) build

up: ## Build images and start all containers in the background
	$(DC) up -d --build

down: ## Stop and remove all containers (named volumes are preserved)
	$(DC) down

logs: ## Stream live logs — accepts a service name via ARGS: make logs ARGS="web"
	$(DC) logs -f $(ARGS)

ps: ## Show the status and port bindings of all containers
	$(DC) ps

exec: ## Open an interactive bash shell inside the running web container
	$(DC) exec $(SERVICE) /bin/bash

deploy: build ## Full deployment: build, restart, migrate, compile, compress, collect static
	$(DC) up -d


# ── Utils ─────────────────────────────────────────────────────────────────────

secret-key: ## Generate a cryptographically strong SECRET_KEY — copy output into .env
	$(RUN) python -c "import secrets; print(secrets.token_urlsafe(50))"

# $(MAKE) instead of make ensures flags from the parent invocation propagate correctly.
# read syntax differs from bash's read -r: both prompt and consume a line from stdin.
reset-db: ## Wipe and recreate the local SQLite database from scratch (dev only)
	@echo "⚠️  This will DELETE your local database. Press Enter to continue or Ctrl+C to abort."; \
	read confirm; \
	rm -f db.sqlite3; \
	$(MAKE) migrate; \
	echo "→ Database reset complete."

urls: ## Print all registered URL patterns (requires django-extensions)
	$(MANAGE) show_urls


# ── Cleanup ───────────────────────────────────────────────────────────────────

clean: ## Remove Python bytecode caches (__pycache__, .pyc) and compiled translations (.mo)
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.mo" -delete
	@echo "→ Workspace cleaned."
