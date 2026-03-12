// ── HTMX ──────────────────────────────────────────────────
document.body.addEventListener('htmx:configRequest', (event) => {
    if (event.detail.verb !== 'get') {
        event.detail.headers['X-CSRFToken'] =
            document.querySelector('meta[name="csrf-token"]').content;
    }
});

// ── Bootstrap tooltips ────────────────────────────────────
// // Initialises tooltips on a given root element (document by default).
// Called on first load AND after every HTMX swap so dynamically
// injected tooltips are always wired up.
function initTooltips(root = document) {
    root.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
        // Avoid double-initialising if tooltip already exists on element
        if (!bootstrap.Tooltip.getInstance(el)) {
            new bootstrap.Tooltip(el);
        }
    });
}

document.addEventListener('DOMContentLoaded', () => initTooltips());

// Re-init only inside the swapped fragment, not the whole document
document.body.addEventListener('htmx:afterSwap', (e) => initTooltips(e.detail.elt));

// ── Navbar scroll effect ──────────────────────────────────
(function () {
    var nav = document.getElementById('main-nav');
    if (!nav) return;
    window.addEventListener('scroll', function () {
        nav.classList.toggle('scrolled', window.scrollY > 0);
    }, { passive: true });
})();

// ── Shortcuts listeners ───────────────────────────────────
(function () {
  let keyBuffer = '';
  let bufferTimeout;

  document.addEventListener('keydown', (e) => {
      // Don't trigger shortcuts if user is typing in an input field
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      // Clear existing timeout
      if (bufferTimeout) clearTimeout(bufferTimeout);

      // Vim Scrolling
      if (e.key === 'j') {
          window.scrollBy({ top: 100, behavior: 'smooth' });
          keyBuffer = ''; // Reset buffer for single keys
      } else if (e.key === 'k') {
          window.scrollBy({ top: -100, behavior: 'smooth' });
          keyBuffer = '';
      } else if (e.key === 'l') {
          window.scrollBy({ left: -100, behavior: 'smooth' });
          keyBuffer = '';
      } else if (e.key === 'h') {
          window.scrollBy({ left: 100, behavior: 'smooth' });
          keyBuffer = '';
      }

      // main 'g' navigation logic
      else if (e.key.toLowerCase() === 'g' || (e.shiftKey && e.key === 'G')) {
          keyBuffer += e.key;

          // Check for sequences
          if (keyBuffer === 'gg') { 
              window.scrollTo({ top: 0, behavior: 'smooth' });
              keyBuffer = ''; 
          } else if (keyBuffer === 'G') {  // Single Shift+G
              window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
              keyBuffer = '';
          }
          // Keep buffer to max 2 chars (e.g., for gg)
          if (keyBuffer.length > 2) keyBuffer = keyBuffer.slice(-2);
      }
      else {
          keyBuffer = ''; // Reset if other keys are pressed
      }

      // Clear buffer after 1.5 seconds if sequence isn't completed
      bufferTimeout = setTimeout(() => { keyBuffer = ''; }, 1500);
  });
})();

// ── Anchor links: close mobile menu then scroll ───────────
// Delegated to #navbarContent so any anchor link added via
// HTMX swap inside the navbar is automatically handled.
(function () {
    const navContent = document.getElementById('navbarContent');
    if (!navContent) return;

    navContent.addEventListener('click', e => {
        const link = e.target.closest('a[href^="#"]');
        if (!link) return;

        e.preventDefault();
        const targetId = link.getAttribute('href');
        const collapse = bootstrap.Collapse.getInstance(navContent);

        if (collapse) {
            navContent.addEventListener(
                'hidden.bs.collapse',
                () => document.querySelector(targetId)?.scrollIntoView({ behavior: 'smooth' }),
                { once: true }
            );
            collapse.hide();
        } else {
            document.querySelector(targetId)?.scrollIntoView({ behavior: 'smooth' });
        }
    });
})();

// ── Language switcher ─────────────────────────────────────
// Delegated to #lang-switcher. The navbar is never HTMX-swapped
// but delegation is consistent and avoids any boot-order issues.
(function () {
    const switcher = document.getElementById('lang-switcher');
    if (!switcher) return;

    switcher.addEventListener('click', e => {
        const btn = e.target.closest('[data-lang]');
        if (!btn) return;

        document.getElementById('lang-input').value = btn.dataset.lang;
        document.getElementById('lang-form').submit();
    });
})();

