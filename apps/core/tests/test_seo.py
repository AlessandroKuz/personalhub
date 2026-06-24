from django.test import AsyncClient
from django.urls import reverse

from apps.core.sitemaps import StaticSitemap


class TestStaticSitemapClass:
    def test_items_returns_all_core_urls(self):
        sm = StaticSitemap()
        assert sm.items() == [
            "core:home",
            "core:about",
            "core:work",
            "core:projects",
            "core:contact",
        ]

    def test_properties(self):
        sm = StaticSitemap()
        assert sm.priority == 0.9
        assert sm.changefreq == "monthly"
        assert sm.i18n is True
        assert sm.alternates is True
        assert sm.x_default is True

    def test_location_resolves_via_reverse(self):
        sm = StaticSitemap()
        for item in sm.items():
            url = sm.location(item)
            assert url.startswith("/")
            assert len(url) > 1 or item == "core:home"


class TestSitemapEndpoint:
    async def test_returns_200(self, async_client: AsyncClient):
        response = await async_client.get("/sitemap.xml")
        assert response.status_code == 200

    async def test_content_type(self, async_client: AsyncClient):
        response = await async_client.get("/sitemap.xml")
        assert response["Content-Type"] == "application/xml"

    async def test_contains_urls(self, async_client: AsyncClient):
        response = await async_client.get("/sitemap.xml")
        response.render()
        content = response.content.decode()
        assert "<urlset" in content
        assert "<url>" in content
        assert "<loc>" in content

    async def test_includes_all_core_pages(self, async_client: AsyncClient):
        response = await async_client.get("/sitemap.xml")
        response.render()
        content = response.content.decode()
        for url_name in StaticSitemap().items():
            path = reverse(url_name)
            assert path in content, f"{path} not found in sitemap"

    async def test_includes_alternate_hreflang_links(self, async_client: AsyncClient):
        response = await async_client.get("/sitemap.xml")
        response.render()
        content = response.content.decode()
        assert 'rel="alternate"' in content
        assert "hreflang=" in content
        assert "x-default" in content


class TestHealthEndpoint:
    async def test_returns_200(self, async_client: AsyncClient):
        response = await async_client.get("/health/")
        assert response.status_code == 200

    async def test_returns_ok(self, async_client: AsyncClient):
        response = await async_client.get("/health/")
        content = response.content.decode()
        assert content == "ok"


class TestRobotsTxt:
    async def test_returns_200(self, async_client: AsyncClient):
        response = await async_client.get("/robots.txt")
        assert response.status_code == 200

    async def test_content_type(self, async_client: AsyncClient):
        response = await async_client.get("/robots.txt")
        assert response["Content-Type"] == "text/plain"

    async def test_contains_sitemap_directive(self, async_client: AsyncClient):
        response = await async_client.get("/robots.txt")
        content = response.content.decode()
        assert "Sitemap:" in content

    async def test_contains_sitemap_url(self, async_client: AsyncClient):
        response = await async_client.get("/robots.txt")
        content = response.content.decode()
        assert "sitemap.xml" in content
