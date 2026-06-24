# PersonalHub: Agent Instructions

## Project
Django 6.0 SSR portfolio. Python 3.14, uv, just. Bootstrap 5.3 SCSS + custom CSS tokens. HTMX 2.0. 5 languages (EN/IT/ES/DE/UK). PostgreSQL prod, SQLite dev.

## Commands
- `just install`: uv sync
- `just run`: uvicorn dev (reload .html/.css/.scss/.js)
- `just test`: pytest
- `just lint` / `just format`: ruff check/format
- `just migrate` / `just makemigrations`
- `just messages` / `just compile-messages` / `just i18n`
- `just compress`: SCSS/JS offline compilation
- `just ci`: lint + format check + test
- `just up`: docker compose build + up -d
- `just secret-key`: generate SECRET_KEY
- `uv run manage.py <command>`

## Structure
- `apps/core/`: home, about, work, contact views
- `apps/projects/`: portfolio (scaffolded)
- `apps/blog/`: blog (scaffolded)
- `config/settings/{base,dev,test,staging,prod}.py`
- `templates/`: base.html, components/_*.html, error pages
- `static/css/main.css`: tokens + custom CSS
- `static/css/home.css`: page styles
- `static/scss/custom.scss`: Bootstrap overrides
- `static/js/`: modular JS
- `locale/{en,it,es,de,uk}/`: translations
- `design-system/`: submodule (canonical design ref)

## Conventions
- Views: `async def` (error handlers: sync `def`)
- Templates: Django template lang, partials prefixed `_`
- i18n: `{% load i18n %}`, `{% trans %}`, `{% blocktrans %}`
- URLs: `i18n_patterns`, admin at `/stratos/`
- Ruff: py314, line-length 88, double quotes
- Tests: pytest, ASGI Django, `apps/*/tests/`, `asyncio_mode = auto`
- Git: no direct pushes to `main`. Pre-commit: ruff + djhtml + uv-lock
- Design: editorial/minimalist, DM Sans + JetBrains Mono, accent #275DAD, sharp 2px corners

## Auto-maintenance
- When you discover a project pattern, convention, or command not listed here, append it to the relevant section
- When the user gives preference feedback, incorporate it here
- Keep under 200 lines; if exceeded, split into `docs/agent/*.md` and reference via `opencode.json` instructions
- Never remove the Auto-maintenance section
