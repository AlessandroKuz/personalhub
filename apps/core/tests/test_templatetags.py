import pytest
from django.template import Context, Template
from django.test import RequestFactory

from apps.core.templatetags.hreflang_tags import hreflang_url


class TestHreflangTag:
    def test_returns_translated_url(self):
        rf = RequestFactory()
        request = rf.get("/en/about/")
        context = {"request": request}
        result = hreflang_url(context, "it")
        assert result == "/it/about/"

    def test_empty_when_no_request_in_context(self):
        context = {}
        result = hreflang_url(context, "it")
        assert result == ""

    @pytest.mark.parametrize(
        "path, lang, expected",
        [
            ("/en/", "it", "/it/"),
            ("/en/about/", "es", "/es/about/"),
            ("/en/work/", "de", "/de/work/"),
        ],
    )
    def test_various_paths_and_languages(self, path, lang, expected):
        rf = RequestFactory()
        request = rf.get(path)
        context = {"request": request}
        result = hreflang_url(context, lang)
        assert result == expected

    def test_renders_in_template(self):
        rf = RequestFactory()
        request = rf.get("/en/")
        template = Template("{% load hreflang_tags %}{% hreflang_url 'it' %}")
        rendered = template.render(Context({"request": request}))
        assert rendered == "/it/"
