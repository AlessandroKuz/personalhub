# Snippets — Sessioni recenti

Tutto implementato. Da usare per rework docs.

---

## Focus system

**File**: `static/css/main.css:69-82`
**Dettaglio**: `:focus-visible` globale con outline 2px solid `--accent`, offset 2px. Sostituisce box-shadow Bootstrap su `.btn`. Scrollspy wrapper soppresso (`[data-bs-spy="scroll"]:focus-visible { outline: none }`).

---

## Skip link

**File**: `templates/base.html:161`, `static/css/main.css:84-103`
**Dettaglio**: Link "Skip to main content" — slide-in bar da sopra, sfondo accent, mono uppercase. Visibile solo a focus.

---

## Scrollspy UX refactor

**File**: `static/css/main.css:557-637`
**Dettaglio**: Dot nav laterale ridisegnata. `.nav-link` padding 8px (area cliccabile 24×24px). `.dot` 8px base, 12px active (via width/height, non transform — anello outline resta equidistante). Label allineata `right: calc(100% + 2px)`. Anello focus via `outline: 2px solid var(--accent)` + offset 2px. Zero animazioni sul ring (swap istantaneo). Nav gap ridotto a 0.
**Decisioni**: Outline > box-shadow per ring. Width/height > transform per consistenza anello. Transizione rifiutata.
**Edge case**: `border` + `box-shadow` causava gap visivo in animazione → scartato.

---

## Keyboard-nav mode (`data-kb-nav`)

**File**: `static/js/main.js:239-259`, `static/css/main.css:676-751`
**Dettaglio**: JS imposta `data-kb-nav` su `<html>` a keydown (Tab/Enter/Frecce/Escape/Spazio). CSS sopprime tutti gli `:hover` mentre è attivo. Rimozione immediata su `mousemove`/`mousedown` — nessun debounce. Cursore custom nascosto (`display: none`) in KB mode, `* { cursor: auto !important }`.
**Edge case**: Mouse su card 1, Tab sulla stessa card → `:focus-visible` perdeva contro `html[data-kb-nav] .card:hover` per specificità (1,1,1 vs 0,2,1). Fix: `:not(:focus-visible):not(:focus)` su ogni regola data-kb-nav, così elemento focalizzato non subisce hover suppression.
**Decisioni**: No debounce (utente notò hover non tornava con 400ms delay). Cursore nascosto per segnalare cambio modalità.

---

## Custom cursor

**File**: `static/css/main.css:220-280+`
**Dettaglio**: Due elementi fixed: `#cursor-dot` (6px, accent, transition width/height) e `#cursor-ring` (40px, bordo accent). Nascosti in KB mode.

---

## Skill-col hover/focus-visible parity

**File**: `static/css/home.css:370-452`
**Dettaglio**: Ogni effetto hover (background, view-link opacity, skill-tag bordo/colore) replicato su `:focus-visible`. `outline-offset: -1px`.
**Edge case**: `::after` accent bar rimosso da focus (clash con outline).

---

## Project-card hover/focus-visible parity

**File**: `static/css/home.css:485-535`
**Dettaglio**: Stessa logica skill-col. `overflow: hidden` rimosso. Bg change e project-link opacity su hover e focus-visible. `::after` accent bar solo su mouse hover.

---

## Contact link padding

**File**: `static/css/home.css:830`
**Dettaglio**: `.contact-link` padding `1.1rem 1rem`.

---

## Scrollspy tabindex rimosso

**File**: `apps/core/templates/core/home.html:30`
**Dettaglio**: `tabindex="0"` rimosso dal div scrollspy — Bootstrap 5.3 non serve.

---

## Vim navigation (vimNav.js)

**File**: `static/js/vimNav.js`
**Dettaglio**: State machine per `j`/`k` navigazione tra sezioni scrollabili. `getCurrentSectionIndex()` usa midpoint scroll. Listener keydown escluso su input/textarea/select.
