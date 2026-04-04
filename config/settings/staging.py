import os

from .base import *  # noqa: F401, F403

DEBUG = False

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

SECURE_SSL_REDIRECT = False
SECURE_HSTS_PRELOAD = False
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")

STATIC_ROOT = "/srv/personalhub/staticfiles"
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL  # noqa: F405

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
