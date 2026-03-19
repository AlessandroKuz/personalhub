import pytest
from django.conf import settings
from django.test import AsyncClient
from django.urls import reverse
from django.utils import translation


# ── Helpers ──────────────────────────────────────────────────────────────────

async def _assert_page(
    async_client: AsyncClient,
    url: str,
    expected_template: str,
) -> None:
    """Reusable assertions for a single URL — status code and template."""
    response = await async_client.get(url)
    assert response.status_code == 200
    assert expected_template in [t.name for t in response.templates]


def _all_urls_for(url_name: str) -> list[str]:
    """
    Return the default URL + one prefixed URL per configured language.

    Example for url_name="core:home" with LANGUAGES=[("en","English"),("it","Italiano")]:
        ["/", "/en/", "/it/"]

    Why both?
    prefix_default_language=False means "/" is valid for EN.
    "/en/" is also valid and must not 404 — some users or crawlers
    will hit it directly, and it's the canonical URL for that language.
    """
    urls = [reverse(url_name)]  # default (no prefix)
    for code, _ in settings.LANGUAGES:
        with translation.override(code):
            urls.append(reverse(url_name))
    return urls

# ── HTTP contract ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize(
    "url_name, expected_template",
    [
        ("core:home", "core/home.html"),
        ("core:about", "core/about.html"),
        ("core:work", "core/work.html"),
        ("core:contact", "core/contact.html"),
    ],
)
async def test_core_views(
    async_client: AsyncClient,
    url_name: str,
    expected_template: str,
) -> None:
    """Assert each view returns 200 and the correct template for every language."""
    """
    Assert that each core page:
      - returns HTTP 200
      - renders the correct template
    for every configured language.
    """
    # Default language (EN) has no URL prefix due to prefix_default_language=False
    await _assert_page(async_client, reverse(url_name), expected_template)

    # Non-default languages get a URL prefix (/it/, /es/, ...)
    # /en/ is included for the sakes of consistency
    for language_code, _ in settings.LANGUAGES:
        # translation.override() makes reverse() return the prefixed URL correctly
        with translation.override(language_code):
            url = reverse(url_name)
        await _assert_page(async_client, url, expected_template)


async def test_nav_has_lang_options(
    home_content_per_language: dict[str, str],
) -> None:
    """
    Language switcher buttons have the lang-option class that
    main.js depends on. If this class is missing, the JS selector
    finds nothing and the switcher silently stops working.
    """
    for lang, html in home_content_per_language.items():
        assert 'class="lang-option"' in html or 'lang-option' in html, (
            f"lang-option class missing from nav [{lang}]"
        )

@pytest.mark.parametrize(
    "url_name, expected_template",
    [
        ("core:home",    "core/home.html"),
        ("core:about",   "core/about.html"),
        ("core:work",    "core/work.html"),
        ("core:contact", "core/contact.html"),
    ],
)
@pytest.mark.asyncio
async def test_core_views_return_200_and_correct_template(
    async_client: AsyncClient,
    url_name: str,
    expected_template: str,
) -> None:
    """Each core page returns 200 and the correct template for every language."""
    for url in _all_urls_for(url_name):
        await _assert_page(async_client, url, expected_template)


# ── Structural contract ───────────────────────────────────────────────────────
#
# These tests fetch the home page and assert specific strings are
# present in the HTML. We test structure, not copy — IDs and hrefs
# are stable; heading text changes constantly.
#
# We parametrize over languages here too: a section ID missing only
# in the Italian version would be a real bug worth catching.

@pytest.fixture
async def home_content_per_language(async_client: AsyncClient) -> dict[str, str]:
    """
    Fetch the home page for every language, return a dict of
    { language_code: decoded_html_content }.

    Fixture scope is "function" (default) — fresh per test.
    """
    results = {}
    for code, _ in settings.LANGUAGES:
        with translation.override(code):
            url = reverse("core:home")
        response = await async_client.get(url)
        results[code] = response.content.decode()
    return results


@pytest.mark.parametrize("section_id", [
    "hero",
    "about",
    "work",
    "projects",
    "process",
    "contact",
])
@pytest.mark.asyncio
async def test_home_has_required_sections(
    home_content_per_language: dict[str, str],
    section_id: str,
) -> None:
    """
    Every required section ID is present in the home page for all languages.
    These IDs are anchor targets — the nav and CTA buttons depend on them.
    """
    for lang, html in home_content_per_language.items():
        assert f'id="{section_id}"' in html, (
            f'Section id="{section_id}" missing from home page [{lang}]'
        )


@pytest.mark.parametrize("href", [
    "#work",
    "#contact",
])
@pytest.mark.asyncio
async def test_home_hero_has_cta_links(
    home_content_per_language: dict[str, str],
    href: str,
) -> None:
    """
    Hero CTA buttons link to the correct anchor targets on the same page.
    """
    for lang, html in home_content_per_language.items():
        assert f'href="{href}"' in html, (
            f'CTA href="{href}" missing from home page [{lang}]'
        )


@pytest.mark.asyncio
async def test_home_has_cursor_elements(
    home_content_per_language: dict[str, str],
) -> None:
    """
    Both cursor elements are present in the DOM.
    main.js looks these up by ID — if missing it exits silently
    and the custom cursor is broken with no visible error.
    """
    for lang, html in home_content_per_language.items():
        assert 'id="cursor-dot"'  in html, f"cursor-dot missing [{lang}]"
        assert 'id="cursor-ring"' in html, f"cursor-ring missing [{lang}]"

async def test_home_has_marquee(
    home_content_per_language: dict[str, str],
) -> None:
    """
    Marquee ticker is present in the DOM.
    main.js depends on id="marquee-track" to duplicate items —
    if missing the ticker shows only half the items before jumping.
    """
    for lang, html in home_content_per_language.items():
        assert 'id="marquee-track"' in html, (
            f"marquee-track missing from home page [{lang}]"
        )
