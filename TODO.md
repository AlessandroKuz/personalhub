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

## GDPR and Privacy pages `[P1 wrap-up]`

- [ ] Research what GDPR rules are there for site visitors
- [ ] US-based CDNs are not GDPR compliant, serve via staticfiles
  - [ ] Google
  - [ ] Bootstrap
    - [ ] Bootstrap CSS
    - [ ] Bootstrap JS
    - [ ] Bootstrap ICONS
- [ ] Add `legal` app with needed pages
- [ ] Create dedicated pages

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

---

## EU Deployment checklist

Here is a comprehensive EU compliance checklist organized by regulatory sector. The scope of each regulation scales with your site's size and functionality — items marked **⚠️ if applicable** only trigger depending on your features.

***

### 🔐 1. GDPR — Data Protection

The foundational regulation. Applies to any site that processes personal data of EU residents. [drupfan](https://drupfan.com/en/blog/how-to-make-your-website-gdpr-compliant)

**Data & Legal Basis**

- [ ] Identify every piece of personal data you collect (names, emails, IPs, cookies, etc.)
- [ ] Define a lawful basis for each (consent, contract, legitimate interest, legal obligation) [cookieyes](https://www.cookieyes.com/blog/gdpr-checklist-for-websites/)
- [ ] Apply **data minimization** — don't collect more than you need [onlinehashcrack](https://www.onlinehashcrack.com/guides/best-practices/gdpr-compliance-2025-essential-checklist.php)
- [ ] Document your data processing activities (even a simple spreadsheet works)

**Transparency**

- [ ] Publish a **Privacy Policy** accessible from every page (footer link)
- [ ] State: what you collect, why, how long you keep it, who you share it with [drupfan](https://drupfan.com/en/blog/how-to-make-your-website-gdpr-compliant)
- [ ] Disclose all **third-party processors** (CDNs, Google Fonts, email providers, etc.)
- [ ] Name yourself as data controller with a contact address

**User Rights**

- [ ] Provide a way for users to request **access, correction, deletion** of their data [cookieyes](https://www.cookieyes.com/blog/gdpr-checklist-for-websites/)
- [ ] Respond to data subject requests within **30 days**
- [ ] Allow withdrawal of consent as easily as it was given

**Security & Breaches**

- [ ] Use HTTPS/TLS across the entire site
- [ ] Report data breaches to your national DPA (Italy: *Garante*) within **72 hours** [onlinehashcrack](https://www.onlinehashcrack.com/guides/best-practices/gdpr-compliance-2025-essential-checklist.php)
- [ ] Store passwords with strong hashing (bcrypt/argon2) — never plaintext
- [ ] Apply **Privacy by Design**: don't store what you don't need from the start

**Cross-Border Transfers**

- [ ] If sending data outside the EU/EEA, use Standard Contractual Clauses (SCCs) or verify the third party is covered by an adequacy decision [onlinehashcrack](https://www.onlinehashcrack.com/guides/best-practices/gdpr-compliance-2025-essential-checklist.php)

***

### 🍪 2. ePrivacy Directive — Cookies & Tracking

Applies on top of GDPR specifically for cookies, local storage, and tracking. [osano](https://www.osano.com/articles/eu-cookie-law)

**Cookie Consent**

- [ ] No non-essential cookies/trackers before explicit consent — no pre-ticked boxes [osano](https://www.osano.com/articles/eu-cookie-law)
- [ ] Show a **cookie banner** on first visit with clear Accept / Reject options
- [ ] Allow users to change or withdraw consent at any time (e.g. a "Cookie settings" link in the footer) [cookieinformation](https://cookieinformation.com/what-is-the-eprivacy-directive/)
- [ ] Log and store consent records

**Essential vs. Non-Essential**

- [ ] Essential cookies (session auth, CSRF tokens, security) are **exempt** from consent [cookieinformation](https://cookieinformation.com/what-is-the-eprivacy-directive/)
- [ ] localStorage used purely for UI preferences (e.g. theme) is generally considered essential — no consent needed, but **disclose it** in your privacy policy [cookieinformation](https://cookieinformation.com/regulations/the-eprivacy-directive/)
- [ ] Analytics, advertising, and third-party tracking cookies are **non-essential** → require opt-in

**Cookie Policy**

- [ ] Publish a **Cookie Policy** (can be part of your Privacy Policy) listing every cookie, its purpose, duration, and provider

***

### ♿ 3. European Accessibility Act (EAA)

In force since **June 28, 2025** — applies to businesses offering digital services in the EU. [beespoke](https://www.beespoke.it/en/website-accessibility-compliance-2025)

> **Note:** Micro-enterprises (< 10 employees, < €2M turnover) are **exempt** from the EAA. As a freelancer/solo developer this likely doesn't apply to you yet, but it's good practice. [ogd-solutions](https://ogd-solutions.com/blog/eaa-compliance-in-2025-what-the-european-accessibility-act-means-for-your-website)

- [ ] All images have **alt text**
- [ ] Full **keyboard navigation** support (no mouse required)
- [ ] Sufficient **color contrast** ratios (WCAG AA minimum: 4.5:1 for text) [digife](https://www.digife.it/en/european-accessibility-act-2025-your-site-is-truly-accessible/)
- [ ] Semantic HTML structure (headings, landmarks, ARIA roles) [digife](https://www.digife.it/en/european-accessibility-act-2025-your-site-is-truly-accessible/)
- [ ] Forms have clear labels and error messages
- [ ] Publish an **Accessibility Statement** on your site [ogd-solutions](https://ogd-solutions.com/blog/eaa-compliance-in-2025-what-the-european-accessibility-act-means-for-your-website)
- [ ] Target **WCAG 2.1 Level AA** as your compliance baseline

***

### 📜 4. Legal Pages & Notices

Required by EU/Italian law depending on site type. [openforest](https://www.openforest.co/articles/terms-conditions-website-legal-requirements)

| Page | Required For | Notes |
|---|---|---|
| **Privacy Policy** | All sites processing any EU user data | GDPR Art. 13/14 |
| **Cookie Policy** | Any site using cookies | ePrivacy Directive |
| **Terms & Conditions** | E-commerce, SaaS, user accounts | Legally mandatory for online sales  [openforest](https://www.openforest.co/articles/terms-conditions-website-legal-requirements) |
| **Imprint / Legal Notice** | Commercial/business sites (Italy: *note legali*) | VAT number, registered address |
| **Accessibility Statement** | EAA scope (see above) |  [ogd-solutions](https://ogd-solutions.com/blog/eaa-compliance-in-2025-what-the-european-accessibility-act-means-for-your-website) |

***

### 🛒 5. E-Commerce Rules *(if selling anything)*

Only relevant if you take payments or sell products/services. [openforest](https://www.openforest.co/articles/terms-conditions-website-legal-requirements)

- [ ] Display **full pricing including VAT**
- [ ] Provide a clear **14-day right of withdrawal** (cooling-off period)
- [ ] Publish returns and refund procedures
- [ ] Show your business's legal name, address, VAT number before purchase
- [ ] Send an **order confirmation** email after purchase
- [ ] Do not use **dark patterns** (fake urgency, hidden fees, manipulative UX) — banned by DSA [shma.co](https://www.shma.co.uk/our-thoughts/eu-digital-services-act-what-businesses-need-to-know-after-first-non-compliance-decision/)

***

### 🌐 6. Digital Services Act (DSA)

Applies to all online services, but obligations scale with size. [digital-strategy.ec.europa](https://digital-strategy.ec.europa.eu/en/policies/digital-services-act)

- [ ] **Small/personal sites**: minimal obligations — just no dark patterns and no illegal content
- [ ] **Online platforms with user content** (comments, uploads, marketplace): must have a content reporting mechanism and terms of service [en.wikipedia](https://en.wikipedia.org/wiki/Digital_Services_Act)
- [ ] **Very large platforms** (45M+ EU users): full DSA obligations — not relevant to personal sites [youtube](https://www.youtube.com/watch?v=_fm_-NfI03g)

***

### 🔒 7. Security (NIS2 Directive)

NIS2 primarily targets essential/important sector entities, not personal or small portfolio sites. However, good-practice security hygiene is expected regardless: [medialaws](https://www.medialaws.eu/rivista/the-new-nis-ii-directive-and-its-impact-on-small-and-medium-enterprises-smes-initial-considerations/)

- [ ] HTTPS everywhere (TLS 1.2+)
- [ ] Keep dependencies (Django, libraries) up to date
- [ ] Use strong, unique passwords and MFA for admin accounts [dataguard](https://www.dataguard.com/nis2/requirements/)
- [ ] Set up basic rate limiting and CSRF protection (Django handles much of this by default)
- [ ] Regular backups of any data you do store

***

### 📧 8. Email & Marketing *(if applicable)*

- [ ] Never send marketing emails without **explicit prior opt-in**
- [ ] Every marketing email must include an **easy unsubscribe** link
- [ ] Honor unsubscribe requests immediately
- [ ] Store proof of consent with timestamp

***

### 🇮🇹 Italy-Specific Note

Italy's *Garante* enforces GDPR strictly and has issued additional national guidelines, especially around cookies and Google services. The Garante specifically found **Google Fonts loaded via Google CDN to be non-compliant** in cases brought before Italian courts  — self-hosting fonts is the cleanest fix, as mentioned earlier. [pandectes](https://pandectes.io/blog/italys-privacy-guidelines-what-you-need-to-know/)
