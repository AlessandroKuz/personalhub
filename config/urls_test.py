# Test-only URL conf. Extends the real routing with endpoints that
# intentionally trigger specific error conditions. Never imported in
# production — only referenced via the `trigger_urlconf` fixture in
# apps/core/tests/conftest.py.

from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.urls import path

from config.urls import handler400, handler403, handler404, handler500  # noqa: F401
from config.urls import urlpatterns as real_urlpatterns


async def _trigger_400(request):
    raise SuspiciousOperation("intentional bad request for testing")


async def _trigger_403(request):
    raise PermissionDenied("intentional permission denied for testing")


async def _trigger_500(request):
    raise RuntimeError("intentional server error for testing")


urlpatterns = real_urlpatterns + [
    path("_test/400/", _trigger_400),
    path("_test/403/", _trigger_403),
    path("_test/500/", _trigger_500),
]
