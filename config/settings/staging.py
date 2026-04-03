# config/settings/prod.py
import os

from .base import *  # noqa: F401, F403

DEBUG = False
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "OPTIONS": {
            "prepare_threshold": 100,
        },
    }
}

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# pre-compiles everything at deploy time, no runtime compilation
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

# This is handled directly with Cloudflare
# The alternative is to do it here
SECURE_SSL_REDIRECT = False
# SECURE_HSTS_SECONDS = 1

STATIC_ROOT = "/srv/personalhub/staticfiles"
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL
