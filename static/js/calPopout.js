// static/js/calPopout.js
// Initialises the Cal.com popup embed and keeps its theme in sync
// with the site's data-bs-theme attribute in real time.
// Cal's ui() communicates with the iframe via postMessage, so changes
// reach an already-open popup immediately — no reopen needed.

(function (C, A, L) {
  let p = function (a, ar) { a.q.push(ar); };
  let d = C.document;
  C.Cal = C.Cal || function () {
    let cal = C.Cal; let ar = arguments;
    if (!cal.loaded) {
      cal.ns = {};
      cal.q = cal.q || [];
      d.head.appendChild(d.createElement("script")).src = A;
      cal.loaded = true;
    }
    if (ar[0] === L) {
      const api = function () { p(api, arguments); };
      const namespace = ar[1];
      api.q = api.q || [];
      if (typeof namespace === "string") {
        cal.ns[namespace] = cal.ns[namespace] || api;
        p(cal.ns[namespace], ar);
        p(cal, ["initNamespace", namespace]);
      } else p(cal, ar);
      return;
    }
    p(cal, ar);
  };
})(window, "https://app.cal.com/embed/embed.js", "init");

Cal("init", "30min", { origin: "https://app.cal.com" });

var _calTrigger = document.getElementById("cal-trigger");

function _getCalTheme() {
  return document.documentElement.getAttribute("data-bs-theme") || "dark";
}

// Updates the button's data-cal-config so Cal reads the correct theme when
// constructing a new iframe. Must NOT be called while the popup is open —
// Cal watches this attribute and reinitialises if it changes mid-session.
function _syncCalConfig() {
  if (!_calTrigger) return;
  _calTrigger.setAttribute("data-cal-config", JSON.stringify({
    layout: "month_view",
    useSlotsViewOnSmallScreen: "true",
    theme: _getCalTheme(),
  }));
}

// Sends theme to the live open iframe via postMessage.
function _syncCalUi() {
  Cal.ns["30min"]("ui", {
    hideEventTypeDetails: false,
    layout: "month_view",
    theme: _getCalTheme(),
  });
}

// Set initial state.
_syncCalConfig();
_syncCalUi();

// Refresh config right before Cal opens the popup so new iframes always get
// the current theme. Our listener runs before Cal's (Cal's script loads async).
// Also mark the popup as open so vimNav can suppress shortcuts.
if (_calTrigger) {
  _calTrigger.addEventListener("click", function () {
    _syncCalConfig();
    _syncCalUi();
    document.documentElement.dataset.calOpen = "1";
  });
}

// Clear the open flag when Cal closes the popup (covers X button, backdrop
// click, and Escape — all paths fire __closeIframe internally).
Cal.ns["30min"]("on", {
  action: "__closeIframe",
  callback: function () {
    delete document.documentElement.dataset.calOpen;
  },
});

// Forward theme changes to the live iframe via postMessage only.
// Do NOT touch data-cal-config here — mutating it while the popup is open
// triggers Cal's own observer and breaks the live update.
new MutationObserver(function (mutations) {
  mutations.forEach(function (mutation) {
    if (mutation.attributeName === "data-bs-theme") {
      _syncCalUi();
      // Firefox doesn't repaint iframe canvas when parent color-scheme changes dynamically.
      // Delay one rAF so Cal's postMessage lands before we flush the compositor layer.
      requestAnimationFrame(function () {
        var calIframe = document.querySelector('iframe[src*="cal.com"]');
        if (calIframe) {
          calIframe.style.opacity = "0.9999";
          requestAnimationFrame(function () { calIframe.style.opacity = ""; });
        }
      });
    }
  });
}).observe(document.documentElement, {
  attributes: true,
  attributeFilter: ["data-bs-theme"],
});
