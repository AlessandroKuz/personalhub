"""
Infrastructure-level tests for the Docker/production configuration.

These tests validate that your Django project is correctly configured
to run in the containerized production environment. They run inside
the container as part of CI or a pre-deploy check.

Run with:
docker compose -f docker-compose.prod.yml run --rm app \
pytest tests/test_docker_config.py
"""

import os

import pytest
from django.conf import settings

# ─── Configuration Sanity Checks ──────────────────────────────────────────────


class TestProductionSettings:
    """
    Validates that production settings are correctly loaded and sane.
    The goal is to catch misconfiguration before it causes a silent failure
    in a live environment.
    """

    def test_debug_is_false_in_production(self):
        """
        DEBUG=True in production leaks tracebacks, environment variables,
        and installed app details to anyone who triggers an error.
        """
        if os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.prod":
            assert settings.DEBUG is False, (
                "DEBUG must be False in production. Check your .env file."
            )

    def test_secret_key_is_set_and_not_default(self):
        """
        A weak or default SECRET_KEY compromises session security,
        CSRF tokens, and signed cookies.
        """
        assert settings.SECRET_KEY, "SECRET_KEY must not be empty."
        assert not settings.SECRET_KEY.startswith("django-insecure"), (
            "SECRET_KEY is using the insecure default. Set a real key in .env."
        )
        assert len(settings.SECRET_KEY) >= 50, (
            "SECRET_KEY should be at least 50 characters long."
        )

    def test_allowed_hosts_is_configured(self):
        """
        ALLOWED_HOSTS prevents HTTP Host header attacks. An empty list
        means Django rejects all requests in production.
        """
        if os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.prod":
            assert settings.ALLOWED_HOSTS, (
                "ALLOWED_HOSTS must contain at least one entry in production."
            )


# ─── Database Connectivity ────────────────────────────────────────────────────


class TestDatabaseConnectivity:
    """
    Validates that Django can reach and authenticate with the database.
    These tests rely on the db service being healthy (via health check
    and depends_on condition in docker-compose.prod.yml).
    """

    @pytest.mark.django_db
    def test_database_is_reachable(self):
        """
        Verifies a basic ORM query completes. If the database is unreachable,
        this fails with a connection error rather than a cryptic app error.
        """
        from django.contrib.auth.models import User

        # A simple count query — just proves the DB connection works.
        count = User.objects.count()
        assert isinstance(count, int)

    def test_database_engine_is_postgres_in_production(self):
        """
        Ensures the production settings are pointing at PostgreSQL, not SQLite.
        SQLite is for dev only — it lacks the concurrency guarantees needed
        for a web-facing production database.
        """
        if os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.prod":
            engine = settings.DATABASES["default"]["ENGINE"]
            assert "postgresql" in engine, (
                f"Expected PostgreSQL in production, got: {engine}"
            )


# ─── Static Files ─────────────────────────────────────────────────────────────


class TestStaticFiles:
    """
    WhiteNoise serves static files directly from Django. For this to work,
    collectstatic must have run and STATIC_ROOT must be populated.
    """

    def test_static_root_is_configured(self):
        assert settings.STATIC_ROOT, "STATIC_ROOT must be set for WhiteNoise to work."

    def test_whitenoise_is_in_middleware(self):
        """
        WhiteNoise must appear in MIDDLEWARE immediately after SecurityMiddleware.
        If it's missing or in the wrong position, static files won't be served.
        """
        middleware = settings.MIDDLEWARE
        assert any("whitenoise" in m.lower() for m in middleware), (
            "WhiteNoiseMiddleware is not in MIDDLEWARE. "
            "Add it directly after SecurityMiddleware."
        )


# ─── ASGI / Async Configuration ───────────────────────────────────────────────


class TestAsgiConfiguration:
    """
    Verifies the ASGI application is correctly configured and importable.
    A broken ASGI config means Uvicorn fails silently at startup.
    """

    def test_asgi_application_is_importable(self):
        """
        If this fails, Uvicorn will refuse to start. Better to catch it here.
        """
        try:
            from config.asgi import application

            assert application is not None
        except ImportError as e:
            pytest.fail(f"Could not import ASGI application: {e}")
