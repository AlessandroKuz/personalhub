// static/js/theme.js
// Handles theme toggle. Loaded just before </body> — DOM is already ready.
// themeInit.js already set the correct initial data-theme on <html>,
// so the first job here is just syncing the icon to match.

(function () {
    var html   = document.documentElement;
    var toggle = document.getElementById('theme-toggle');
    var icon   = document.getElementById('theme-icon');

    // ── Apply a theme ────────────────────────────────────────
    function applyTheme(theme) {
        html.setAttribute('data-theme',    theme);
        html.setAttribute('data-bs-theme', theme);  // Bootstrap utilities
        localStorage.setItem('theme', theme);
        syncIcon(theme);
    }

    // ── Keep icon in sync with current theme ─────────────────
    // Sun  = you are in dark mode  (click to go light)
    // Moon = you are in light mode (click to go dark)
    function syncIcon(theme) {
        if (!icon) return;
        icon.className = (theme === 'dark')
            ? 'bi bi-sun-fill'
            : 'bi bi-moon-stars-fill';
    }

    // ── Initialise icon to match whatever themeInit.js set ───
    syncIcon(html.getAttribute('data-theme') || 'dark');

    // ── Wire up the toggle button ─────────────────────────────
    if (toggle) {
        toggle.addEventListener('click', function () {
            var current = html.getAttribute('data-theme') || 'dark';
            applyTheme(current === 'dark' ? 'light' : 'dark');
        });
    }
})();

