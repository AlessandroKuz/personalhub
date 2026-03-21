/* ============================================================
   PERSONALHUB — main.js
   Loaded just before </body> — DOM is fully parsed at this point.
   theme.js and themeInit.js run separately (see base.html).

   Sections:
     1.  Custom cursor
     2.  Navbar scroll + height offset
     3.  Language switcher
     4.  Bootstrap tooltips
     5.  Scroll reveal (IntersectionObserver)
   ============================================================ */


/* ── 1. CUSTOM CURSOR ───────────────────────────────────────── */
/* Dot snaps to mouse instantly via mousemove.
   Ring lags behind via a lerp (linear interpolation) loop
   running on requestAnimationFrame.

   Lerp formula: current += (target - current) * factor
   factor = 0.12 → ring reaches ~70% of the distance each frame
   at 60fps this gives a ~8 frame lag — perceptible but smooth.

   Both elements are hidden on touch devices via CSS
   (media: pointer coarse) so the RAF loop is the only cost
   on desktop.                                                  */

(function () {
  var dot  = document.getElementById('cursor-dot');
  var ring = document.getElementById('cursor-ring');

  if (!dot || !ring) return;

  var mx = 0, my = 0;   /* mouse target position */
  var rx = 0, ry = 0;   /* ring current position (lerped) */

  /* Dot follows instantly */
  document.addEventListener('mousemove', function (e) {
    mx = e.clientX;
    my = e.clientY;
    dot.style.left = mx + 'px';
    dot.style.top  = my + 'px';
  });

  /* Ring lags via RAF loop */
  (function animateRing() {
    rx += (mx - rx) * 0.12;
    ry += (my - ry) * 0.12;
    ring.style.left = rx + 'px';
    ring.style.top  = ry + 'px';
    requestAnimationFrame(animateRing);
  })();

  /* Expand both elements when hovering interactive targets */
  document.querySelectorAll(
    'a, button, .project-card, .skill-col, [data-bs-toggle], select, input, textarea'
  ).forEach(function (el) {
    el.addEventListener('mouseenter', function () {
      document.body.classList.add('cursor-hover');
    });
    el.addEventListener('mouseleave', function () {
      document.body.classList.remove('cursor-hover');
    });
  });
})();


/* ── 2. NAVBAR SCROLL + HEIGHT OFFSET ──────────────────────── */
/* scroll: adds .scrolled class at 60px for frosted glass effect.

   height offset: reads the navbar's actual rendered height and
   applies it as body padding-top so content isn't hidden behind
   the sticky navbar. Re-measures on resize because the navbar
   can be taller on mobile (two-row layout when toggler is shown).

   Why not a hardcoded value?
   The navbar height changes at breakpoints — adding the toggler
   row on mobile makes it taller. A hardcoded value would either
   clip content on mobile or add too much space on desktop.      */

(function () {
  var nav = document.getElementById('main-nav');
  if (!nav) return;

  /* Scroll state */
  function updateNav() {
    nav.classList.toggle('scrolled', window.scrollY > 10);
  }

  /* Run once immediately — handles direct anchor links
     and any page that loads mid-scroll                 */
  updateNav();

  /* Then keep updating on scroll */
  window.addEventListener('scroll', updateNav, { passive: true });
})();


/* ── 3. LANGUAGE SWITCHER ───────────────────────────────────── */
/* The visible dropdown is decorative — clicking a .lang-option
   writes its data-lang value into the hidden form input and
   submits the form via POST to Django's set_language view.

   Why a hidden form instead of fetch()?
   set_language is a Django view that sets a session cookie and
   redirects. A standard form POST handles this correctly with
   zero extra code. A fetch() call would need to handle the
   redirect manually and re-render the page anyway.             */

(function () {
  var input = document.getElementById('lang-input');
  var form  = document.getElementById('lang-form');
  var label = document.getElementById('lang-current');

  if (!input || !form) return;

  document.querySelectorAll('.lang-option').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var lang = btn.dataset.lang;
      input.value = lang;
      /* Update trigger label instantly — feels responsive before
         the page reloads on form submit                         */
      if (label) label.textContent = lang.toUpperCase();
      form.submit();
    });
  });
})();


/* ── 4. BOOTSTRAP TOOLTIPS ──────────────────────────────────── */
/* Bootstrap tooltips are opt-in — they don't initialise from
   data attributes alone, querySelectorAll + new Tooltip() is
   required. We wait for DOMContentLoaded as a safety net even
   though this script is already at end of body.                */

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
    new bootstrap.Tooltip(el);
  });
});


/* ── 5. SCROLL REVEAL ───────────────────────────────────────── */
/* Elements with class .reveal start at opacity:0 + translateY(28px)
   (set in main.css). When they enter the viewport, the observer
   adds .visible which transitions them to opacity:1 + translateY(0).

   threshold: 0.15 → element must be 15% visible before triggering.
   This prevents reveal firing the instant a pixel enters the viewport
   which looks like a glitch on fast scrolls.

   once: true equivalent — we disconnect the element after it's
   revealed so the observer isn't tracking hundreds of already-
   visible elements on long pages.                              */

(function () {
  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);   /* stop watching once revealed */
        }
      });
    },
    { threshold: 0.15 }
  );

  document.querySelectorAll('.reveal').forEach(function (el) {
    observer.observe(el);
  });
})();

/* ── 6. MARQUEE ─────────────────────────────────────────────────
   Duplication + precise pixel offset = seamless loop.

   Why pixels instead of -50%?
   translateX(-50%) is relative to the track's total width.
   If original items don't perfectly fill the container,
   -50% doesn't land where the first item started — causing
   a visible jump on reset.

   Measuring the original items' exact scrollWidth before
   duplication gives us the precise offset to animate to.
   The reset from that offset to 0 is pixel-perfect.
   ──────────────────────────────────────────────────────────── */

(function () {
  var track = document.getElementById('marquee-track');
  if (!track) return;

  /* Measure original width BEFORE duplication */
  var originalWidth = track.scrollWidth;

  /* Duplicate all children for seamless loop */
  Array.from(track.children).forEach(function (item) {
    track.appendChild(item.cloneNode(true));
  });

  /* Set the exact pixel offset as a CSS custom property.
     The keyframe animates to var(--marquee-offset) so
     the reset is always mathematically exact.            */
  track.style.setProperty('--marquee-offset', '-' + originalWidth + 'px');

  /* Pause on hover */
  var wrap = track.closest('.marquee-wrap');
  if (wrap) {
    wrap.addEventListener('mouseenter', function () {
      track.classList.add('paused');
    });
    wrap.addEventListener('mouseleave', function () {
      track.classList.remove('paused');
    });
  }

  /* Respect reduced motion */
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    track.style.animationPlayState = 'paused';
  }
})();
