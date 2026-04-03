# config/settings/test.py
from .base import *  # noqa: F401, F403

TESTING = True
# ─────────────────────────────────────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────────────────────────────────────

# A fixed, arbitrary key — no rotation needed, nothing real is at stake.
SECRET_KEY = "test-only-secret-key-do-not-use-in-production"

# THIS IS THE MOST IMPORTANT TEST OVERRIDE.
# With DEBUG=True, Django short-circuits your error handlers and renders its
# own yellow debug page. Error views (handler400, handler404, etc.) only execute
# when DEBUG=False. Every test in this suite depends on this being False.
DEBUG = False

# Django's test client sends requests with Host: testserver by default.
# With DEBUG=False, the SecurityMiddleware validates the Host header against
# ALLOWED_HOSTS and returns 400 if it doesn't match — which would silently
# break every single test. "testserver" must be here.
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]


# ─────────────────────────────────────────────────────────────────────────────
# PASSWORD HASHING
# ─────────────────────────────────────────────────────────────────────────────

# Django's default hasher (PBKDF2 with 870,000 iterations as of Django 5)
# is intentionally slow — that's the point in production. In tests, every
# User.objects.create_user() call pays this cost. MD5PasswordHasher skips
# the key-stretching entirely. It's cryptographically terrible and perfect
# for tests: no real secrets, maximum speed.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


# ─────────────────────────────────────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────────────────────────────────────

# :memory: means SQLite creates the entire database in RAM. No file I/O, no
# cleanup between runs. The tradeoff: you can't inspect the DB after a failed
# test, but for a test suite this is a non-issue.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


# ─────────────────────────────────────────────────────────────────────────────
# MIGRATIONS
# ─────────────────────────────────────────────────────────────────────────────


# By default, pytest-django runs all migrations before the test suite starts.
# For a project with many migrations, this can add several seconds. This class
# tricks Django into thinking every app has no migrations module, so it creates
# tables directly from model definitions (via CREATE TABLE) instead.
#
# WARNING: This means your migration files are NOT tested. You should
# occasionally run your test suite without this override to verify migrations
# are in sync with your models. A CI step like `manage.py migrate --check`
# covers this separately.
class DisableMigrations:
    def __contains__(self, item: str) -> bool:
        return True  # "any_app_name" in MIGRATION_MODULES → True

    def __getitem__(self, item: str) -> None:
        return None  # return None = no migrations module for this app


MIGRATION_MODULES = DisableMigrations()


# ─────────────────────────────────────────────────────────────────────────────
# EMAIL
# ─────────────────────────────────────────────────────────────────────────────

# Captures emails in a Python list (django.core.mail.outbox) instead of
# hitting an SMTP server. Lets you assert on email content without any network.
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


# ─────────────────────────────────────────────────────────────────────────────
# STATIC FILES
# ─────────────────────────────────────────────────────────────────────────────

# WhiteNoise (your production static file server) adds manifest hashing and
# compression. None of that is relevant in tests. The base StaticFilesStorage
# is dead simple and requires no collectstatic step.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────────────────────

# Silence everything. Test output should only contain test results.
# If a test fails and you need to debug, temporarily set disable_existing_loggers
# to False and add a StreamHandler to root.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {},
    "root": {"handlers": []},
}


# ─────────────────────────────────────────────────────────────────────────────
# CSRF
# ─────────────────────────────────────────────────────────────────────────────

# The CSRF failure view is a Django setting, not a urls.py variable.
# This routes Django's CSRF middleware to your custom 403_csrf view
# rather than Django's built-in one. We define it here (and in base.py
# once it exists) so the test suite can verify it works.
CSRF_FAILURE_VIEW = "apps.core.views.error_403_csrf"
