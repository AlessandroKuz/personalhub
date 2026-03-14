# Alessandro Kuz | PersonalHub | Portfolio

> **[SHORT DESCRIPTION — e.g. "A clean, fast, server-rendered personal portfolio built for performance and clarity."]**

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)](https://djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![HTMX](https://img.shields.io/badge/HTMX-2.0-3D72D7)](https://htmx.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live](https://img.shields.io/badge/Live-alessandrokuz.com-success)](https://alessandrokuz.com)

---

## Overview

I'm **Alessandro Kuz** — AI/ML Engineer, Data Scientist, and Builder. This project is my own digital place, a personal website and professional portfolio. It serves as a central hub for showcasing projects, skills, and career background, and as a direct point of contact for recruiters, collaborators, and clients; That is the reason why I called it "PersonalHub".

The site is built on a deliberately minimal but slick stack: server-rendered Django templates, HTMX for targeted partial-page updates, and Bootstrap 5 for layout — no JavaScript framework, no build pipeline, no client-side routing. The result is a fast, accessible, and fully indexable website with a small operational footprint.

**Live site:** [alessandrokuz.com](https://alessandrokuz.com)

---

## Features

- **Light / dark theme** with flash-free initialization and `localStorage` persistence
- **Fully responsive** layout across mobile, tablet, and desktop
- **Internationalisation (i18n)** with English (default) and Italian (more to come), via Django's i18n framework with clean URL prefixes (`/it/about/`)
- **HTMX-powered interactions** — partial page updates without a single-page application
- **Contact form** with server-side validation and HTMX submission (no full page reload)
- **Sticky frosted-glass navbar** with true-centred navigation links and scroll transition
- **Fully responsive** layout built on Bootstrap 5's grid, with mobile-first breakpoints
- **Accessibility-first** — semantic HTML, `aria` attributes, skip-to-content link, keyboard navigability (via Vim-like motions)
- **Dockerised deployment** with separate development and production Compose configurations
- **Zero build step** — no webpack, no Node, no asset pipeline
- **MkDocs documentation** for the project itself, available at `docs.alessandrokuz.com`

---

## Tech Stack

| Layer              | Technology                              | Purpose                                        |
| ------------------ | --------------------------------------- | ---------------------------------------------- |
| Language           | Python 3.14                             | Runtime                                        |
| Framework          | Django 6.0                              | Routing, views, templating, ORM                |
| Interactivity      | HTMX 2.0                                | Partial DOM updates without a JS framework     |
| CSS framework      | Bootstrap 5.3                           | Responsive layout and components               |
| ASGI server        | Uvicorn                                 | Async request handling                         |
| Static files       | WhiteNoise                              | Zero-config static file serving                |
| Package manager    | uv                                      | Dependency management and virtual environments |
| Linter / formatter | Ruff                                    | Code quality                                   |
| Testing            | pytest + pytest-django + pytest-asyncio | TDD test suite                                 |
| Reverse proxy      | Caddy                                   | TLS termination and automatic HTTPS            |
| Containerisation   | Docker + Compose                        | Reproducible environments                      |
| Documentation      | MkDocs Material                         | Project reference docs                         |

---

## Project Structure

> "The tree below is sorted by logical grouping, not alphabetically — directories and files are ordered by purpose and dependency to make the architecture easier to read at a glance."
>

```bash
personalhub/
│
├── config/                     # Project config — NOT an app
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py             # Shared settings across all environments
│   │   ├── dev.py              # Development overrides (SQLite, console email, debug toolbar)
│   │   └── prod.py             # Production overrides (PostgreSQL, HTTPS headers, security settings)
│   ├── urls.py                 # Root URL dispatcher with i18n_patterns
│   ├── asgi.py                 # ASGI entry point (uvicorn target)
│   └── wsgi.py
│
├── apps/
│   ├── core/                   # Phase 1: home, about, work, contact
│   ├── projects/               # Phase 2: Project + Tag models
│   └── blog/                   # Phase 3: Post model, writing interface
│
├── templates/
│   ├── base.html               # Master layout — extended by all pages
│   ├── components/             # _nav.html, _footer.html, _cta.html
│   └── partials/               # HTMX response fragments
│
├── static/
│   ├── css/     # Design tokens and custom styles
│   ├── js/      # Navbar, Theme & language switches, tooltips, ...
│   └── img/
│
├── locale/                     # i18n .po / .mo translation files
├── docs/                       # MkDocs source — architecture and decisions
├── docs/                       # MkDocs source (you are here)
├── site/                       # MkDocs build output (gitignored)
├── scripts/
│   └── dev.sh                  # Launches Django + MkDocs simultaneously
│
├── manage.py                   # Django CLI entry point
├── mkdocs.yml                  # MkDocs configuration
├── pyproject.toml              # uv: dependencies + tool config (ruff, etc.)
├── uv.lock                     # Committed lockfile — guarantees reproducible installs
├── .python-version             # Pins Python 3.14 — read by uv and mise
├── Dockerfile                  # Production image definition
├── docker-compose.yml          # Dev environment
├── docker-compose.prod.yml     # Production environment
├── .env                        # Secret values — gitignored
└── .env.example                # Committed template for .env

```

---

## Local Development Setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/) — Python version and package management
- Docker (optional, for running the full production stack locally)

### 1. Clone and install

```bash
git clone https://github.com/AlessandroKuz/personalhub.git
cd personalhub
```

```bash
cp .env.example .env
# Edit .env and set at minimum:
#   SECRET_KEY=
#   DJANGO_SETTINGS_MODULE=config.settings.dev
```

```bash
uv sync
```

**Generating a secret key:**

```bash
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Run migrations - Initialize db

```bash
uv run python manage.py migrate
```

### 3. Start the development servers

The included script starts both the Django/Uvicorn server and the MkDocs documentation server simultaneously. A single `Ctrl+C` shuts both down cleanly.

```bash
./scripts/dev.sh
```

Alternatively, run each separately:

```bash
# Application — http://127.0.0.1:8080
uv run uvicorn config.asgi:application --reload --port 8080

# Documentation — http://127.0.0.1:8001
uv run mkdocs serve --dev-addr 127.0.0.1:8001
```

### 4. Run the test suite

```bash
uv run pytest -v
```

With coverage:

```bash
uv run pytest --cov=apps --cov-report=term-missing
```

---

## Environment Variables

Copy `.env.example` to `.env` and populate the following:

```env
# Django
SECRET_KEY=<your-secret-key>
DJANGO_SETTINGS_MODULE=config.settings.dev
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (production only — dev uses SQLite)
POSTGRES_DB=personalhub
POSTGRES_USER=personalhub
POSTGRES_PASSWORD=<your-db-password>

# Email (production)
EMAIL_HOST=<smtp-host>
EMAIL_PORT=587
EMAIL_HOST_USER=<your-email>
EMAIL_HOST_PASSWORD=<your-email-password>
```

---

## Deployment

The production stack runs as three Docker services — the Django application, PostgreSQL, and Caddy — defined in `docker-compose.prod.yml`. Caddy handles TLS certificate provisioning and renewal automatically via Let's Encrypt.

### First deploy

```bash
# On the production host
git clone https://github.com/AlessandroKuz/personalhub.git
cd personalhub

cp .env.example .env
# Fill in all production values, set DJANGO_SETTINGS_MODULE=config.settings.prod

docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec web uv run python manage.py migrate
docker compose -f docker-compose.prod.yml exec web uv run python manage.py createsuperuser
```

### Subsequent deploys

```bash
git pull
docker compose -f docker-compose.prod.yml build web
docker compose -f docker-compose.prod.yml up -d
# Run migrations if the update includes model changes:
docker compose -f docker-compose.prod.yml exec web uv run python manage.py migrate
```

### Hosting

The site is hosted on a VPS behind Caddy. An alternative zero-cost configuration using a home server and Cloudflare Tunnel is documented in [`docs/infrastructure/hosting.md`](docs/infrastructure/hosting.md) — no port forwarding required, the home IP never appears in DNS.

---

## Customization

### Personal information

Content lives directly in the templates under `templates/` and `apps/core/templates/core/` (Django convention tbh). Update the following to make the site your own:

- `templates/base.html` — brand name, social links
- `templates/components/_nav.html` — brand name, social links
- `templates/components/_footer.html` — name, social links (GitHub, LinkedIn, YouTube), copyright
- `templates/components/_cta.html` — email, scheduling link, social handles components

And inside the `core` app:

- `templates/core/home.html` — TLDR version of all the pages

- `templates/core/about.html` — bio, background, languages, interests

- `templates/core/work.html` — skills, career timeline, CV download

- `templates/core/contact.html` — email, scheduling link, social handles

### Design tokens

All colours are defined as CSS custom properties in `static/css/main.css`. Light and dark variants are set in a single place:

```css
:root {
    --accent: #275DAD;   /* Change this one value to re-theme the entire site */
    /* ... */
}
[data-theme="dark"] {
    --accent: #4a8fd4;
    /* ... */
}
```

### Internationalisation

To add a language, add its code to `LANGUAGES` in `config/settings/base.py`, then run:

```bash
uv run python manage.py makemessages -l <LANG_CODE>
# for example for English: uv run python manage.py makemessages -l en
# Edit the generated .po file in locale//LC_MESSAGES/django.po
uv run python manage.py compilemessages
```

---

## Screenshots

| Light mode                                                 | Dark mode                                                |
| ---------------------------------------------------------- | -------------------------------------------------------- |
| ![Light mode screenshot](docs/assets/screenshot-light.png) | ![Dark mode screenshot](docs/assets/screenshot-dark.png) |

---

## What's Next

### Phase 2 — Projects Showcase

The `apps/projects` application will introduce dynamic project cards driven by Django models. Each project will have a title, description, tags, GitHub link, and optional live URL. Tag-based filtering will be implemented with HTMX — clicking a tag updates the project grid without a page reload. Content will be managed through Django's admin interface.

### Phase 3 — Blog

The `apps/blog` application will add a writing and publishing interface. Posts will be written in Markdown with a live server-side preview powered by a WebSocket connection — the ASGI foundation is already in place for this. Posts will support draft and published states, managed through a lightweight custom editor or the Django admin.

### Phase 4 — Polish & Performance

With core functionality in place, this phase focuses on elevating the production quality of the site across three dimensions: visual refinement, performance, and SEO. Animations and micro-interactions will be tightened, the design system will be audited for consistency across all pages and themes, and accessibility will be validated. On the performance side, static assets will be audited with Lighthouse, images will be served in modern formats with appropriate sizing, and Core Web Vitals will be measured and optimised. SEO groundwork — canonical URLs, structured data and a generated sitemap — will also be completed in this phase.

### Phase 5 — AI Assistant

The `apps/chat` application will introduce a context-aware AI assistant capable of answering questions about my background, projects, skills and work. The assistant will be powered by a Retrieval-Augmented Generation (RAG) pipeline: site content, project descriptions, and CV data will be embedded and stored in a vector database, retrieved at query time to ground the model's responses in accurate, up-to-date information. The interface will be a minimal chat widget, streamed over a WebSocket connection using the ASGI infrastructure already in place. The goal is not a generic chatbot, but a focused, honest assistant that represents me accurately — and declines gracefully when it doesn't know the answer.
Partially inspired by [Ignacio Figueroa's Portfolio](https://ignaciofigueroa.vercel.app/).

---

## Developer Documentation

Full architecture documentation — settings split, URL structure, ASGI rationale, HTMX patterns, deployment guide — is available at:

```bash
uv run mkdocs serve --dev-addr 127.0.0.1:8001
```

Or browse the `docs/` directory directly.

---

## Testing & TDD

This project follows a **Test-Driven Development** approach — tests are written before implementation, not after. The discipline of writing a failing test first ensures that every piece of production code has a clear, testable purpose and that the entire codebase remains refactorable with confidence.

### Stack

| Package | Role |
|---|---|
| `pytest` | Test runner — plain `assert`, rich failure output |
| `pytest-django` | Django integration — `async_client`, `db` fixtures, settings wiring |
| `pytest-asyncio` | Native `async def` test support (required for async views) |
| `pytest-cov` | Coverage reporting |

`asyncio_mode = "auto"` is set in `pyproject.toml`, meaning every `async def test_*` function runs on the event loop without any decorator. Given that all views in this project are async, this eliminates significant boilerplate.

### Running the test suite

```bash
# Run all tests
uv run pytest

# Verbose output (show individual test names)
uv run pytest -v

# Run a specific app
uv run pytest apps/core/

# Run with coverage report
uv run pytest --cov=apps --cov-report=term-missing
```

### Structure

Tests live **inside each app**, co-located with the code they test. This is the Django convention: when an app is removed, its tests go with it — no orphaned test files pointing at deleted code.

```
apps/
└── core/
    └── tests/
        ├── __init__.py
        ├── test_urls.py      # URL resolution + i18n prefix correctness
        ├── test_views.py     # HTTP status codes + template assertions
        ├── test_navbar.py    # Navbar rendered on all pages, controls present
        └── test_footer.py    # Footer rendered on all pages, content assertions
```

### The Red → Green → Refactor cycle

No production code in this repository was written without a failing test that justified it. The workflow is:

1. **Red** — write a test that describes the desired behaviour; confirm it fails
2. **Green** — write the minimum code to make it pass
3. **Refactor** — improve the implementation; tests confirm nothing broke

For detailed rationale, patterns, and the full test inventory see the [Testing & TDD documentation](docs/testing/tdd.md).

---

## Contributing

This is a personal portfolio project and is not open to general feature contributions. That said, the following are welcome and appreciated:

- **Bug reports** — if you spot a broken layout, a template rendering issue, or unexpected behaviour, please open an issue with your browser, OS, and a clear description of what you expected vs. what you saw.
- **Accessibility feedback** — if you encounter any barrier navigating the site with assistive technology, please open an issue. Accessibility is treated as a first-class concern in this project.
- **Security disclosures** — please do not open a public issue for security vulnerabilities. Contact me directly at [akuzcontact@gmail.com](mailto:akuzcontact@gmail.com) with a description of the issue.
- If you are forking this project as a base for your own portfolio, you are welcome to do so under the terms of the licence below. A mention or backlink is appreciated but not required.

---

## License

This project is licensed under the **MIT Licence**. You are free to use, copy, modify, and distribute it, provided the original copyright notice is retained.

[Click to View - MIT LICENSE](LICENSE.md)

---

## Contact

**Alessandro Kuz** — AI/ML Engineer, Data Scientist & Builder

| Channel | Link |
| --- | --- |
| Website | [alessandrokuz.com](https://alessandrokuz.com) |
| Email | [akuzcontact@gmail.com](mailto:akuzcontact@gmail.com) |
| LinkedIn | [linkedin.com/in/alessandrokuz](https://linkedin.com/in/alessandrokuz) |
| GitHub | [github.com/alessandrokuz](https://github.com/alessandrokuz) |
| Schedule a call | [cal.com/alessandrokuz](https://cal.com/alessandrokuz) |

---

## Acknowledgements

This project makes use of the following open-source tools and would not exist without the work of their respective communities.

- [Django](https://www.djangoproject.com/) — the web framework doing the heavy lifting
- [HTMX](https://htmx.org/) — hypermedia-driven interactivity without a JavaScript framework
- [Bootstrap 5](https://getbootstrap.com/) — layout, components, and responsive utilities
- [uv](https://github.com/astral-sh/uv) — fast Python package and project management
- [Caddy](https://caddyserver.com/) — automatic HTTPS and reverse proxy
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) — developer documentation
- [Cloudflare](https://cloudflare.com/) — Domain Name, DDoS protection, Docs hosting
