import pytest
from django.conf import settings
from django.urls import reverse
from django.utils import translation


@pytest.mark.parametrize(
    "url_name, expected_url",
    [
        ("core:home", "/"),
        ("core:about", "/about/"),
        ("core:work", "/work/"),
        ("core:contact", "/contact/"),
    ],
)
# tests are synchronous — there's no HTTP request, no async, just reverse() calls.
def test_core_urls_resolve(url_name: str, expected_url: str) -> None:
    """Assert each URL name resolves to the correct path for every language."""
    for language_code, _ in settings.LANGUAGES:
        with translation.override(language_code):
            assert reverse(url_name) == f"/{language_code}{expected_url}"
