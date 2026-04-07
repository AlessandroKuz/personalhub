# Current To-dos

- [ ] aggiungere questo alla creazione del db in produzione:
  - `python manage.py shell -c "from django.contrib.sites.models import Site; Site.objects.update_or_create(id=1, defaults={'domain': 'alessandrokuz.com', 'name': 'Alessandro Kuz'})"`

## SEO

### 🔴 Fondamenta (Critiche)

- [x] HTTPS attivo sul dominio principale
- [ ] Meta tag description in ogni pagina
- [ ] Meta tag title univoco per ogni pagina
- [x] Tag canonical per evitare contenuti duplicati
- [x] Favicon stack completo (SVG + ICO + apple-touch-icon)
- [x] meta name="robots" content="index, follow"
- [x] Creare e servire robots.txt con riferimento alla sitemap
- [x] Installare django.contrib.sitemaps e generare sitemap.xml
- [x] Inviare sitemap.xml a Google Search Console
- [ ] Richiedere l'indicizzazione delle pagine principali da Search Console

### 🟠 Struttura & Internazionalizzazione

- [x] Struttura URL con prefissi lingua (/en/, /it/, ...)
- [x] prefix_default_language=False per l'inglese
- [x] og:locale dinamico per lingua
- [x] og:locale:alternate per tutte le lingue (senza duplicati)
- [x] Nessun redirect automatico forzato per paese
- [x] Aggiungere hreflang tag per tutte le lingue in base.html
- [x] Creare il custom template tag hreflang_url
- [x] Aggiungere hreflang x-default puntando alla versione EN
- [x] Includere le versioni multilingua nella sitemap

### 🟡 Open Graph & Social

- [x] og:title, og:description, og:type, og:url, og:site_name
- [ ] og:image dinamico per lingua (og-card-{lang}.png)
- [x] og:image:width, og:image:height, og:image:type, og:image:alt
- [x] Twitter/X card completa (summary_large_image)
- [ ] Generare le OG card per tutte le lingue (og-card-it.png, og-card-de.png, ...)
- [ ] Aggiungere og:updated_time per velocizzare il refresh delle preview sui social
- [x] Aggiungere meta name="color-scheme" content="light dark"

### 🟢 Structured Data (JSON-LD)

- [x] Aggiungere schema Person con name, url, jobTitle, sameAs
- [x] Aggiungere description tradotta con {% blocktrans %} al JSON-LD
- [x] Includere GitHub, LinkedIn, YouTube in sameAs
- [x] Aggiungere nonce CSP al tag JSON-LD

### 🔵 Autorità & Identità

- [ ] Usare lo strumento pubblico di rimozione per deindexare alessandrokuz.info
- [ ] Rimuovere la proprietà .info non verificata da Search Console
- [x] Verificare che alessandrokuz.com sia la proprietà principale in Search Console
- [ ] Monitorare le query di ricerca per il proprio nome dopo 48–72 ore

### ⚪ Performance Tecnica

- [ ] Misurare le Core Web Vitals con PageSpeed Insights
- [ ] Convertire le immagini pesanti in formato WebP
- [ ] Verificare che tutte le immagini abbiano attributo alt descrittivo
- [x] Abilitare la compressione Gzip/Brotli sul server (Caddy lo fa automaticamente)
- [ ] Verificare i tempi di risposta del server (target: sotto i 200ms TTFB)
- [ ] Lazy loading per immagini sotto la piega (loading="lazy")

### ⬛ Contenuto & Long-term

- [ ] Aggiornare regolarmente la sezione progetti con nuovi lavori
- [ ] Scrivere articoli tecnici o un blog (aumenta le pagine indicizzate e l'autorità)
- [ ] Contribuire a progetti open source che linkano al tuo sito (link building)
- [x] Assicurarsi che GitHub, LinkedIn, YouTube abbiano il link a alessandrokuz.com nella bio
- [ ] Monitorare la Search Console ogni 2–4 settimane per errori di copertura
