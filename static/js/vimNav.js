/**
 * Vim-style keyboard navigation for PersonalHub.
 *
 * Architecture
 * ────────────
 * Pure functions (isTypingContext, getCurrentSectionIndex, processKey) contain
 * all decision logic and are fully unit-testable without browser globals.
 *
 * init() wires everything together: reads config from the DOM, attaches a
 * keydown listener, and returns a destroy() for cleanup.
 *
 * The g-prefix mechanism is a two-state machine:
 *   idle  →[g pressed]→  gPending  →[second key or timeout]→  idle
 */


// ─── Pure utility functions (exported for testing) ───────────────────────────

/**
 * Returns true when the focused element is a text-entry context.
 * Used as a guard: vim shortcuts should never fire while the user is typing.
 *
 * We check tagName rather than instanceof because jsdom and real browsers may
 * use different class hierarchies, but tagName is always a plain string.
 *
 * @returns {boolean}
 */
export function isTypingContext() {
  const el = document.activeElement;
  if (!el || el === document.body || el === document.documentElement) return false;
  return (
    el.tagName === 'INPUT'    ||
    el.tagName === 'TEXTAREA' ||
    el.tagName === 'SELECT'   ||
    el.isContentEditable
  );
}

/**
 * Finds the index of the "current" section based on scroll position.
 *
 * Strategy: a section is "current" if its top edge is at or above the
 * viewport midpoint. We walk all sections and keep track of the last one
 * that satisfies this condition. This naturally handles the common case
 * where the user has scrolled partway through a section — the section
 * whose heading they last passed is the current one.
 *
 * @param {Element[]} sections
 * @param {number} [viewportHeight=window.innerHeight]
 * @returns {number}
 */
export function getCurrentSectionIndex(sections, viewportHeight = window.innerHeight) {
  if (!sections.length) return 0;
  const mid = viewportHeight / 2;
  let best = 0;
  sections.forEach((section, i) => {
    if (section.getBoundingClientRect().top <= mid) best = i;
  });
  return best;
}

/**
 * Factory for the mutable key-sequencer state.
 * Isolated into a factory so tests can get a clean state per test case
 * without module-level state leaking between runs.
 *
 * @returns {{ gPending: boolean, gTimer: ReturnType<typeof setTimeout> | null }}
 */
export function createState() {
  return { gPending: false, gTimer: null };
}

/**
 * Core key-processing function.
 *
 * Maps (key, current state, route map) → a command object describing what
 * should happen, or null if this key should be ignored.
 *
 * The only side effect here is the setTimeout that expires the g-prefix
 * window. Vitest's vi.useFakeTimers() intercepts this, making it safe to
 * test without real delays.
 *
 * @param {string} key             - event.key value
 * @param {{ gPending: boolean, gTimer: any }} state
 * @param {Record<string, string>} routes - letter → URL mapping
 * @param {number} [timeout=2000]   - ms before g-prefix expires
 * @returns {{ type: string, url?: string } | null}
 */
export function processKey(key, state, routes, timeout = 2000) {
  // ── Resolve a pending g-prefix ───────────────────────────────────────────
  if (state.gPending) {
    clearTimeout(state.gTimer);
    state.gPending = false;
    state.gTimer   = null;

    if (key === 'g') return { type: 'scrollTop' };
    if (key === 't') return { type: 'toggleTheme' };
    if (key === 'l') return { type: 'openLangDropdown' };

    const url = routes[key];
    if (url) return { type: 'navigate', url };

    // Unrecognised combo (e.g. gx): eat the keypress silently.
    // Returning null means executeCommand is never called, but the key's
    // browser default was already prevented in handleKeydown.
    return null;
  }

  // ── Single-key commands ──────────────────────────────────────────────────
  switch (key) {
    case 'j':  return { type: 'scrollDown'  };
    case 'k':  return { type: 'scrollUp'    };
    case 'G':  return { type: 'scrollBottom' };  // event.key is 'G' (uppercase) when Shift held
    case 'h':  return { type: 'prevSection' };
    case 'l':  return { type: 'nextSection' };
    case '?':  return { type: 'toggleModal' };
    case 'g':
      // Begin a g-prefix sequence. We return null immediately (no command),
      // then wait for the next keypress. A timer cleans up if nothing follows.
      state.gPending = true;
      state.gTimer   = setTimeout(() => {
        state.gPending = false;
        state.gTimer   = null;
      }, timeout);
      return null;

    default:
      return null;
  }
}


// ─── Private helpers ─────────────────────────────────────────────────────────

/**
 * Reads URL routes from data-vim-key attributes in the navbar links.
 * Django resolves the correct i18n-prefixed URL at render time;
 *
 * @returns {Record<string, string>}
 */
function readRoutes() {
  const get = key => document.querySelector(`a[data-vim-key="${key}"]`)?.href ?? '#';
  return {
    h: get('h'),
    a: get('a'),
    w: get('w'),
    p: get('p'),
    c: get('c'),
  };
}

// ─── Dropdown Navigation ─────────────────────────────────────────────────────────
/**
 * Moves focus between items in whichever dropdown is currently open using j/k.
 *
 * The focusable items are whatever Bootstrap itself would make keyboard-
 * navigable: any non-disabled button or anchor inside the open menu.
 * This mirrors Bootstrap's own arrow-key selector so j/k and arrows are
 * consistent in what they can reach.
 *
 * Returns true if the key was consumed, false if it should fall through.
 *
 * @param {string} key
 * @returns {boolean}
 */
function handleDropdownNav(key) {
  if (key !== 'j' && key !== 'k') return false;

  const menu = document.querySelector('.dropdown-menu.show');
  if (!menu) return false;

  // Same selector Bootstrap uses internally for its own arrow-key handling —
  // keeps j/k and ↑/↓ consistent in what they can reach.
  const FOCUSABLE = 'button:not(:disabled), a:not(.disabled)[href]';
  const options   = Array.from(menu.querySelectorAll(FOCUSABLE));
  if (!options.length) return false;

  const current = options.indexOf(document.activeElement);

  if (key === 'j') {
    options[(current + 1) % options.length].focus();
  } else {
    options[current <= 0 ? options.length - 1 : current - 1].focus();
  }

  return true;
}

// ─── init() ──────────────────────────────────────────────────────────────────

/**
 * Bootstraps vim-nav. Reads config from the DOM, attaches the keydown
 * listener, and fires the first-visit toast. Returns a destroy() for cleanup.
 *
 * @param {{ scrollStep?: number, gTimeout?: number }} [options]
 * @param {number} options.scrollStep - Fraction of viewport to scroll per j/k (default 0.15)
 * @param {number} options.gTimeout   - ms before g-prefix expires (default 2000)
 * @returns {{ destroy: () => void }}
 */
export function init({ scrollStep = 0.15, gTimeout = 2000 } = {}) {
  const state  = createState();
  const routes = readRoutes();

  // Live query every time — sections may not exist on all pages
  const getSections = () => Array.from(document.querySelectorAll('section'));
  const getModal    = () => document.getElementById('keyboardShortcutsModal');

  // ── Command executor (all side effects live here) ────────────────────────
  function executeCommand(cmd) {
    const step = Math.round(window.innerHeight * scrollStep);

    switch (cmd.type) {

      case 'scrollDown':
        window.scrollBy({ top: step, behavior: 'smooth' });
        break;

      case 'scrollUp':
        window.scrollBy({ top: -step, behavior: 'smooth' });
        break;

      case 'scrollBottom':
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        break;

      case 'scrollTop':
        window.scrollTo({ top: 0, behavior: 'smooth' });
        break;

      case 'prevSection': {
        const sections = getSections();
        const idx      = getCurrentSectionIndex(sections);
        sections[Math.max(0, idx - 1)]?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        break;
      }

      case 'nextSection': {
        const sections = getSections();
        const idx      = getCurrentSectionIndex(sections);
        sections[Math.min(sections.length - 1, idx + 1)]?.scrollIntoView({
          behavior: 'smooth',
          block: 'start',
        });
        break;
      }

      case 'toggleTheme':
        // Delegate to the existing button — single source of truth,
        // no duplicated theme logic here.
        document.getElementById('theme-toggle')?.click();
        break;

      case 'openLangDropdown': {
        const btn = document.getElementById('lang-dropdown-btn');
        if (!btn) return;
        window.bootstrap?.Dropdown.getOrCreateInstance(btn).show();
        // Shift focus into the first option so arrow keys work immediately.
        requestAnimationFrame(() => {
          document.querySelector('.lang-menu .lang-option')?.focus();
        });
        break;
      }

      case 'navigate':
        // Guard against '#' fallback (page not built yet in current phase)
        if (cmd.url && cmd.url !== '#') window.location.assign(cmd.url);
        break;

      case 'toggleModal': {
        const el = getModal();
        if (!el) return;
        // Bootstrap 5 lazy-initialises modals; getOrCreateInstance is idempotent
        window.bootstrap?.Modal.getOrCreateInstance(el).toggle();
        break;
      }
    }
  }

  // ── Keydown handler ──────────────────────────────────────────────────────

  // Keys whose browser defaults we want to suppress
  const INTERCEPTED = new Set(['j', 'k', 'G', 'h', 'l', 'g']);

  function handleKeydown(e) {
    // ── Guard: modified keypress (Ctrl+l = clear address bar, Cmd+k, etc.) ─
    if (e.ctrlKey || e.altKey || e.metaKey) return;

    // ── Guard: user is typing in a form field ────────────────────────────
    if (isTypingContext()) return;

    // ── Escape: cancel pending g-sequence; Bootstrap handles modal close ──
    if (e.key === 'Escape') {
      clearTimeout(state.gTimer);
      state.gPending = false;
      state.gTimer   = null;
      return; // let event propagate — Bootstrap's modal listens for it too
    }

    // ── ? always toggles the modal, regardless of whether it's open ───────
    // This must come before the "modal open" guard below so ? can close it.
    if (e.key === '?') {
      e.preventDefault();
      executeCommand({ type: 'toggleModal' });
      return;
    }

    // ── Guard: open modal or dropdown  ───────────────────────────────────
    // ── Dropdown open: only j/k navigate options, everything else suppressed ──
    if (document.querySelector('.dropdown-menu.show')) {
      if (handleDropdownNav(e.key)) e.preventDefault();
      return;
    }

    // ── Modal open: suppress everything (? and Escape handled above already) ──
    if (document.querySelector('.modal.show')) return;

    // Prevent browser defaults for our intercepted keys before processing
    if (INTERCEPTED.has(e.key)) e.preventDefault();

    const cmd = processKey(e.key, state, routes, gTimeout);
    if (cmd) executeCommand(cmd);
  }

  window.addEventListener('keydown', handleKeydown);

  // ── Cleanup ──────────────────────────────────────────────────────────────
  return {
    destroy() {
      window.removeEventListener('keydown', handleKeydown);
      clearTimeout(state.gTimer);
    },
  };
}
