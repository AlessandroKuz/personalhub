import os

from django.utils.csp import CSP

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

# Caddy handles redirect, not Django, so it is disabled here
SECURE_SSL_REDIRECT = False

SECURE_HSTS_SECONDS = 300
# SECURE_HSTS_SECONDS = 15768000
# SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")

STATIC_ROOT = "/srv/personalhub/staticfiles"
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL  # noqa: F405

USE_X_FORWARDED_HOST = True
# behind reverse proxy / load balancer
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Might need to change in the future: Prevent JS from reading it via document.cookie
CSRF_COOKIE_HTTPONLY = True

SECURE_CSP = {
    "default-src": [CSP.NONE],
    "script-src": [CSP.SELF, CSP.NONCE, "https://cdn.jsdelivr.net"],
    "style-src": [
        CSP.SELF,
        CSP.NONCE,
        "https://cdn.jsdelivr.net",
        "https://fonts.googleapis.com",
        "'sha256-faU7yAF8NxuMTNEwVmBz+VcYeIoBQ2EMHW3WaVxCvnk='",
    ],
    "img-src": [CSP.SELF, "data:"],
    "connect-src": [CSP.SELF, "https://cdn.jsdelivr.net"],
    "font-src": [CSP.SELF, "https://fonts.gstatic.com", "https://cdn.jsdelivr.net"],
}
