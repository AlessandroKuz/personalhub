import pytest
from django.conf import settings
from django.test import AsyncClient
from django.urls import reverse
from django.utils import translation


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


async def _assert_page(
    async_client: AsyncClient, url: str, expected_template: str
) -> None:
    """Reusable assertions for a single URL — status code and template."""
    response = await async_client.get(url)
    assert response.status_code == 200
    assert expected_template in [t.name for t in response.templates]
