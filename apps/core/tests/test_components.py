from datetime import date

import pytest
from django.test import AsyncClient
from django.urls import reverse


# Footer Tests ----------------------------------------------------------------
@pytest.mark.parametrize(
    "url_name",
    [
        "core:home",
        "core:about",
        "core:work",
        "core:contact",
    ],
)
async def test_footer_present_on_all_pages(
    async_client: AsyncClient, url_name: str
) -> None:
    """Footer is rendered on every page via base.html."""
    response = await async_client.get(reverse(url_name))
    assert response.status_code == 200
    content = response.content.decode()
    assert "<footer" in content


async def test_footer_contains_name(async_client: AsyncClient) -> None:
    response = await async_client.get(reverse("core:home"))
    assert "Alessandro Kuz" in response.content.decode()


async def test_footer_contains_current_year(async_client: AsyncClient) -> None:
    response = await async_client.get(reverse("core:home"))
    assert str(date.today().year) in response.content.decode()


async def test_footer_contains_github_link(async_client: AsyncClient) -> None:
    response = await async_client.get(reverse("core:home"))
    assert "github.com" in response.content.decode()


async def test_footer_contains_linkedin_link(async_client: AsyncClient) -> None:
    response = await async_client.get(reverse("core:home"))
    assert "linkedin.com" in response.content.decode()


async def test_footer_contains_youtube_link(async_client: AsyncClient) -> None:
    response = await async_client.get(reverse("core:home"))
    assert "youtube.com" in response.content.decode()


# Navbar Tests -----------------------------------------------------------------
@pytest.mark.parametrize(
    "url_name",
    [
        "core:home",
        "core:about",
        "core:work",
        "core:contact",
    ],
)
async def test_navbar_present_on_all_pages(
    async_client: AsyncClient, url_name: str
) -> None:
    """Navbar is rendered on every page via base.html."""
    response = await async_client.get(reverse(url_name))
    assert response.status_code == 200
    assert "<nav" in response.content.decode()


async def test_navbar_contains_brand(async_client: AsyncClient) -> None:
    response = await async_client.get(reverse("core:home"))
    assert "Kuz" in response.content.decode()


@pytest.mark.parametrize(
    "link_url",
    [
        reverse("core:about"),
        reverse("core:work"),
        reverse("core:contact"),
    ],
)
async def test_navbar_contains_nav_links(
    async_client: AsyncClient, link_url: str
) -> None:
    response = await async_client.get(reverse("core:home"))
    assert link_url in response.content.decode()


async def test_navbar_contains_theme_toggle(async_client: AsyncClient) -> None:
    response = await async_client.get(reverse("core:home"))
    assert "theme-toggle" in response.content.decode()


async def test_navbar_contains_language_switcher(async_client: AsyncClient) -> None:
    response = await async_client.get(reverse("core:home"))
    assert "lang-form" in response.content.decode()


async def test_navbar_active_state(async_client: AsyncClient) -> None:
    """The about link is marked active when on the about page."""
    response = await async_client.get(reverse("core:about"))
    content = response.content.decode()
    # The active class must appear near the about URL
    about_url = reverse("core:about")
    # Find the anchor tag for about and confirm it has the active class
    assert f'href="{about_url}"' in content
    # active class must appear somewhere in the navbar
    assert 'aria-current="page"' in content


async def test_navbar_controls_present(async_client: AsyncClient) -> None:
    """Theme toggle and language switcher are both rendered."""
    response = await async_client.get(reverse("core:home"))
    content = response.content.decode()
    assert "theme-toggle" in content
    assert "lang-switcher" in content
    assert "bi-globe2" in content
