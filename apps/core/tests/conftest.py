import pytest


@pytest.fixture
def trigger_urlconf(settings):
    # Swap ROOT_URLCONF for the duration of any test that requests this
    # fixture. pytest-django's `settings` fixture handles teardown
    # automatically — no manual cleanup needed.
    settings.ROOT_URLCONF = "config.urls_test"
