# Personalhub — To-Do

Legend:

- `[P0]` Phase 0: Simple Landing page website
- `[P1]` Phase 1: Complete website with dedicated details pages
- `[P2]` Phase 2: Website with dynamic projects section
- `[P3]` Phase 3: Website with dynamic blog section
- `[P4]` Phase 4: Clean code and SEO optimizations
- `[P5]` Phase 5: LLM-ChatBot to talk about the content

---

## 🎨 Design & CSS Foundation `[P0]` ← Start here

- [x] Finalise design tokens in `static/css/main.css`
      — `--accent`, `--bg`, `--surface`, `--text`, `--muted`, `--border`, `--mono`
      for both `[data-theme="light"]` and `[data-theme="dark"]`
- [x] Confirm `data-theme` / `data-bs-theme` parity across all custom tokens
- [x] Lock in font duo: DM Sans + JetBrains Mono
      — add Google Fonts `<link>` to `base.html` (or self-host in `static/`)
- [x] Add custom lagging cursor (dot + ring, `mix-blend-mode`) to `main.js`
- [x] Scroll reveal — Intersection Observer fade-in on section enter (no library)

---

## 🧩 Components `[P0]`

- [x] `_footer.html` — copyright, socials, easter egg, back-to-top
- [x] `_nav.html` — brand, true-centered links, lang switcher, theme toggle,
      scroll effect
- [ ] `_cta.html` — reusable "get in touch" block, used at the bottom of every page

---

## ⚙️ JavaScript `[P0]`

- [x] `themeInit.js` — flash prevention, sets `data-bs-theme` before first paint
- [x] `theme.js` — toggle logic, icon sync, localStorage persistence
- [x] `main.js` — consolidate all: navbar scroll, navbar height offset,
      lang switcher, tooltip init, cursor effect, scroll reveal

---

## 🏠 `home.html` — Primary Document `[P0]`

> `home.html` is the main experience. Every other content page is an
> **expanded version** of its corresponding section here.

- [x] Write tests first (`apps/core/tests/test_views.py`)
      — hero renders, each section `id` is present, CTA is included
- [x] **Hero section**
      — name + title, status card (pulsing green dot + availability line),
        tag cloud, subtle entrance animation
- [x] **Marquee ticker strip** — stack / tools scrolling banner
- [x] **About section** (`id="about"`)
      — 2–3 sentence TLDR, "Read more →" links to `/about/`
- [x] **Work / Skills section** (`id="work"`)
      — 3-col skills grid (grouped by domain), "See full CV →" links to `/work/`
- [x] **Projects section** (`id="projects"`)
      — featured project card + 2 preview cards (static placeholders for now),
        "All projects →" links to `/projects/` (Phase 2)
- [x] **Process section** — 4-step "how I work" strip
- [x] **Contact section** (`id="contact"`)
      — include `_cta.html`, cal.com link, social links
- [x] Review content inside each section

---

## 📄 Custom Error pages - [P1]

> Each page should cover the corresponding error code.

- [ ] Write tests first
- [ ] 400 error pages
  - [ ] 404 page
  - [ ] ...
- [ ] 500 error pages

---

## 📄 Content Pages — Expanded Versions `[P1]`

> Each page expands on its home.html section.
> They share the same design language but go deeper.

### `about.html` — Full About

- [ ] Write tests first
- [ ] Full personal bio — background, ML/AI focus, builder mentality
- [ ] Human languages spoken (EN, IT, ES, DE)
- [ ] Interests / what I'm currently building
- [ ] Include `_cta.html` at the bottom

### `work.html` — Full CV

- [ ] Write tests first
- [ ] Full skills breakdown — grouped by domain (ML/AI, Backend, DevOps, Tools)
- [ ] Career timeline — education + work experience (CSS only, no model needed)
- [ ] CV download — PDF served from `static/`, button with `bi-download` icon
- [ ] Include `_cta.html` at the bottom

### `contact.html` — Full Contact

- [ ] Write tests first — `test_views.py` + `test_forms.py`
- [ ] `ContactForm` Django form class — name, email, message, validation
- [ ] HTMX form submission — no full page reload
      - `partials/_contact_form.html` — form + inline validation errors
      - `partials/_contact_success.html` — post-submit confirmation
- [ ] Email sending — console backend in dev, SMTP in prod (`.env` controlled)
- [ ] cal.com scheduling embed / link
- [ ] Social links — GitHub, LinkedIn, YouTube

---

### 🌍 i18n `[P1]`

> QA step.

- [ ] Mark all template strings with `{% trans %}` / `{% blocktrans %}`
      once content is written (do this last, before release)
- [ ] `makemessages -l it` → fill translations → `compilemessages`
- [ ] Smoke-test both `/` (EN) and `/it/` (IT) routes end-to-end

---

### 🔒 SEO, Accessibility & Performance `[P1 wrap-up]`

- [ ] `robots.txt` — served from `static/`
- [ ] `sitemap.xml` — via `django.contrib.sitemaps`
- [ ] Verify Open Graph tags on each page (use opengraph.xyz)
- [ ] Lighthouse audit — target 95+ on Performance, Accessibility, Best Practices
- [ ] All images have `alt` text
- [ ] All icon-only interactive elements have `aria-label`
- [ ] Keyboard navigation works end-to-end (Tab through navbar, form, footer)

---

## 🗃️ Phase 2 — Projects App `[P2]`

- [ ] Write model tests first (`apps/projects/tests/test_models.py`)
- [ ] `Tag` model — name, slug
- [ ] `Project` model — title, slug, description, body, tags (M2M),
      github_url, live_url, featured, created_at
- [ ] Migrations + Django admin registration
- [ ] Write view tests first (`apps/projects/tests/test_views.py`)
- [ ] `project_list` async view — full page + HTMX partial branch
- [ ] `project_detail` async view
- [ ] `partials/_project_grid.html` — HTMX fragment for tag-filtered grid
- [ ] `partials/_project_card.html` — single card partial
- [ ] Tag filter buttons — `hx-get`, `hx-target`, `hx-push-url`
- [ ] Replace static project placeholders on `home.html` with live DB query
- [ ] Seed initial data — fixture or management command

---

### 🌍 i18n translations for projects `[P2]`

- [ ] Handle translations for each language in each model

---

## 📝 Phase 3 — Blog App `[P3]`

- [ ] Write model tests first (`apps/blog/tests/test_models.py`)
- [ ] `Post` model — title, slug, body (Markdown source), status
      (draft / published), published_at, created_at, updated_at
- [ ] Markdown rendering — rendered in view, passed as safe HTML to template
- [ ] Django admin for Post
- [ ] `post_list` + `post_detail` async views
- [ ] Post card partial
- [ ] Lightweight custom writing interface (not just admin)
- [ ] EasyMDE editor — CDN, no build step
- [ ] WebSocket live Markdown preview — Django Channels (ASGI already set up)
- [ ] RSS feed — `django.contrib.syndication`

---

### 🌍 i18n translations for articles `[P3]`

- [ ] Handle translations for each article
- [ ] Make sure all images wont contain "hardcoded" text

---

## 🐳 Docker & Infrastructure

- [ ] `Dockerfile` — finalise: uv install, collectstatic, Uvicorn entrypoint
- [ ] `docker-compose.yml` — dev: volume mounts, SQLite, live reload
- [ ] `docker-compose.prod.yml` — web + PostgreSQL + Caddy
- [ ] `Caddyfile` — reverse proxy to `web:8000`, auto-HTTPS via Let's Encrypt
- [ ] `.env.example` — document every required variable
- [ ] Confirm `CompressedManifestStaticFilesStorage` is in `prod.py` only ✅

---

## 🚀 Deployment — Two Options (decide before going live)

- [x] Register domain + add to Cloudflare

### Option A — Home Server + Cloudflare Tunnel (€0/mo)

- [ ] Create Tunnel in Cloudflare Zero Trust dashboard
- [ ] Add `cloudflared` service to `docker-compose.prod.yml`
- [ ] Point DNS to tunnel (Cloudflare handles automatically)
- [ ] First deploy checklist (see `docs/infrastructure/deployment.md`)

### Option B — Hetzner VPS CX22/23 (~€4/mo)

- [ ] Provision CX22/23 (2 vCPU, 4GB RAM, 40GB SSD)
- [ ] Configure DNS → VPS IP (optionally via Cloudflare proxy)
- [ ] SSH hardening — disable password auth, `ufw` firewall
- [ ] Clone repo, fill `.env`, `docker compose -f docker-compose.prod.yml up -d`
- [ ] First deploy checklist (see `docs/infrastructure/deployment.md`)

### Common to both

- [ ] DB backup — `pg_dump` via cron, stored off-host (Backblaze B2 free tier)
- [ ] Confirm HTTPS, HSTS, and all security headers via securityheaders.com
- [ ] Cloudflare R2 as an alternative to Backblaze B2 for DB
      backups — S3-compatible API, zero egress fees (unlike S3), generous free tier.
      Worth evaluating since you're already in the Cloudflare ecosystem

---

## 📚 Documentation (MkDocs)

- [x] Fill all stub `.md` files — most are currently empty skeletons
- [ ] `frontend/design-system.md` — final token values, font choices
- [ ] `frontend/components.md` — footer, navbar, CTA patterns with examples
- [ ] `testing/tdd.md` — update test inventory as new tests are added ✅
- [ ] `decisions.md` — add: sticky-top rationale, Bootstrap-first CSS approach,
      page architecture decision (home = primary, others = expanded)
- [x] `mkdocs.yml` — add `repo_url` + `repo_name` once repo is public
- [x] Cloudflare Pages for docs.alessandrokuz.com

---

## 🔒 Occasional check - SEO, Accessibility & Performance `[P1 to P5]`

- [ ] `robots.txt` — served from `static/`
- [ ] `sitemap.xml` — via `django.contrib.sitemaps`
- [ ] Verify Open Graph tags on each page (use opengraph.xyz)
- [ ] Lighthouse audit — target 95+ on Performance, Accessibility, Best Practices
- [ ] All images have `alt` text
- [ ] All icon-only interactive elements have `aria-label`
- [ ] Keyboard navigation works end-to-end (Tab through navbar, form, footer)

---

## Cloudflare-specific setup

- [ ] Set SSL/TLS mode to "Full (strict)" in Cloudflare dashboard — not just "Full".
      Full (strict) requires a valid certificate on the origin server;
      without it Cloudflare accepts self-signed certs and you're vulnerable to origin impersonation
- [ ] Install a Cloudflare Origin Certificate on the server (via Caddy or manually) — this is a cert
      issued by Cloudflare specifically for the Cloudflare→origin leg, valid for 15 years, free, no renewal
- [ ] Enable Cloudflare Web Analytics — privacy-friendly, no cookie banner needed,
      free, zero JS performance cost compared to Google Analytics
- [ ] Consider Cloudflare Email Routing for the contact form — forwards form submissions to your real inbox
      without exposing your email address or needing an SMTP server. Free tier, zero infrastructure
