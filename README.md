# Alessandro Kuz · PersonalHub · Portfolio

> *"A clean, fast, server-rendered personal portfolio built for performance and clarity."*

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)](https://djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![HTMX](https://img.shields.io/badge/HTMX-2.0-3D72D7)](https://htmx.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](/LICENSE.md)
[![Live](https://img.shields.io/badge/Live-alessandrokuz.com-success)](https://alessandrokuz.com)

My Personal website and portfolio (**Alessandro Kuz**), Data Scientist and AI/ML Engineer.
Built with Django, HTMX and Bootstrap 5. No JS framework, no build step. Just server-rendered HTML.
**→ [alessandrokuz.com](https://alessandrokuz.com)**

---

## Features

| | |
|---|---|
| Light/dark theme | Flash-free init via inline `<script>`, `localStorage` persistence |
| Internationalisation | EN (default), IT, ES, DE, UK via i18n URL prefixes |
| HTMX interactions | Partial page updates, contact form submission, toast notifications |
| Responsive | Bootstrap 5 grid, mobile-first breakpoints, single column at 992px |
| Accessibility | Semantic HTML, `aria` attributes, skip link, Vim keyboard nav, respects `prefers-reduced-motion` |
| Custom design system | Two-font stack (DM Sans + JetBrains Mono), single blue accent, sharp 2px corners, 1px hairline grids |
| Security | CSP headers, HSTS, secure cookies, rate-limit middleware, max scores on Security Headers and Mozilla Observatory |
| SEO | hreflang, Open Graph, JSON-LD Person schema, sitemap.xml, robots.txt |
| Dockerised | Multi-stage build, Compose for production (Django + PostgreSQL + Caddy with auto TLS) |
| Zero build step | No webpack, no Node, no asset pipeline |

---

## Quick Start

```bash
git clone https://github.com/AlessandroKuz/personalhub.git && cd personalhub
cp .env.example .env          # edit SECRET_KEY + DJANGO_SETTINGS_MODULE=config.settings.dev
uv sync                       # install deps from uv.lock
uv run python manage.py migrate
./scripts/dev.sh              # launches Django + MkDocs docs simultaneously
```

Or individually:
```bash
uv run uvicorn config.asgi:application --reload --port 8080   # app
uv run mkdocs serve --dev-addr 127.0.0.1:8001                   # docs
```

---

## Project Structure

```
config/          settings (base/dev/test/staging/prod), urls, ASGI/WSGI entrypoints
apps/
├── core/        home, about, work, contact
├── projects/    scaffolded (Project + Tag models)
├── blog/        scaffolded (Post model, Markdown authoring)
└── chat/        planned (RAG chatbot)
templates/       base.html, components (_nav, _footer, _cta), HTMX partials
static/          CSS, JS (vanilla), images
docs/            MkDocs submodule, architecture, decisions, design system
```

---

## Roadmap

| Phase | Status |
|---|---|
| **P0** Landing page | Done: hero, about, skills, projects grid, process, contact |
| **P1** Detail pages | Partial: core app wired, detail views placeholder, contact form not implemented |
| **P2** Dynamic Projects | Scaffolded: models commented out |
| **P3** Blog | Scaffolded: models commented out |
| **P4** Production Polish | In progress: sitemap, hreflang, JSON-LD done; Lighthouse/CWV, GDPR, structured JSON logging, rate-limiting pending |
| **P5** AI Chat | Not started: RAG pipeline planned |

---

## Design System

Editorial/minimalist aesthetic: terminal UI meets editorial prose. Two-font system (DM Sans for reading, JetBrains Mono for interface), single accent `#275DAD`, sharp 2px corners, 1px hairline grid technique. Full spec: [`design-system/`](design-system/readme.md).

---

## Key Commands

| Command | Action |
|---|---|
| `just install` | Sync environment from uv.lock |
| `just run` | Start ASGI dev server (mirrors production) |
| `just test` | Run full test suite |
| `just ci` | Lint + format check + tests |
| `just deploy` | Build + deploy Docker stack |
| `just reset-db` | Wipe dev SQLite (irreversible) |

Pass extra args naturally: `just test apps/core/tests.py -x`.

---

## Environment Variables

Copy `.env.example`. Minimum required:

```env
SECRET_KEY=<generate with `uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`>
DJANGO_SETTINGS_MODULE=config.settings.dev
```

Prod also needs `POSTGRES_*`, `EMAIL_*`, `ALLOWED_HOSTS`. See `.env.example`.

---

## Deployment

```bash
docker compose up -d --build
docker compose exec web uv run python manage.py migrate
```

Production stack: Django/Uvicorn + PostgreSQL + Caddy (auto TLS via Let's Encrypt and Cloudflare origin certs). Hosted on a Hetzner VPS. Home server option in `docs/infrastructure/hosting.md` if you prefer a zero-cost setup.

---

## Testing

TDD approach: tests come before code, not after. Pytest with pytest-django and pytest-asyncio. `asyncio_mode = "auto"` means async tests run without extra decorators. Tests live inside each app, not in a separate top-level directory.

```bash
uv run pytest -v
uv run pytest --cov=apps --cov-report=term-missing
```

---

## License

**MIT**. Use, copy, modify, distribute. Just keep the copyright notice.

**Alessandro Kuz** · [alessandrokuz.com](https://alessandrokuz.com) · [contact@alessandrokuz.com](mailto:contact@alessandrokuz.com) · [GitHub](https://github.com/alessandrokuz) · [LinkedIn](https://linkedin.com/in/alessandrokuz)
