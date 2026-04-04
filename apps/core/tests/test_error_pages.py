from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import Http404
from django.test import AsyncRequestFactory

from apps.core.views import (
    error_400,
    error_403,
    error_403_csrf,
    error_404,
    error_410,
    error_500,
)

factory = AsyncRequestFactory()


class TestErrorViewsUnit:
    def test_400_status(self):
        request = factory.get("/")
        response = error_400(request, exception=SuspiciousOperation())
        assert response.status_code == 400

    def test_400_template(self):
        request = factory.get("/")
        response = error_400(request, exception=SuspiciousOperation())
        response.render()
        assert response.template_name == "400.html"

    def test_403_status(self):
        request = factory.get("/")
        response = error_403(request, exception=PermissionDenied())
        assert response.status_code == 403

    def test_403_template(self):
        request = factory.get("/")
        response = error_403(request, exception=PermissionDenied())
        response.render()
        assert response.template_name == "403.html"

    def test_403_csrf_status(self):
        request = factory.get("/")
        response = error_403_csrf(request, reason="CSRF token missing.")
        assert response.status_code == 403

    def test_403_csrf_template(self):
        request = factory.get("/")
        response = error_403_csrf(request, reason="CSRF token missing.")
        response.render()
        assert response.template_name == "403_csrf.html"

    def test_403_csrf_reason_in_context(self):
        reason = "CSRF cookie not set."
        request = factory.get("/")
        response = error_403_csrf(request, reason=reason)
        assert response.context_data["reason"] == reason

    def test_404_status(self):
        request = factory.get("/")
        response = error_404(request, exception=Http404())
        assert response.status_code == 404

    def test_404_template(self):
        request = factory.get("/")
        response = error_404(request, exception=Http404())
        response.render()
        assert response.template_name == "404.html"

    def test_410_status(self):
        request = factory.get("/")
        response = error_410(request)
        assert response.status_code == 410

    def test_410_template(self):
        request = factory.get("/")
        response = error_410(request)
        response.render()
        assert response.template_name == "410.html"

    def test_500_status(self):
        request = factory.get("/")
        response = error_500(request)
        assert response.status_code == 500

    def test_500_template(self):
        request = factory.get("/")
        response = error_500(request)
        response.render()
        assert response.template_name == "500.html"
