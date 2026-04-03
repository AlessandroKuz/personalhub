from dataclasses import dataclass

from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _


@dataclass
class Section:
    id: str
    label: str


async def home(request: HttpRequest) -> HttpResponse:
    section_list = [
        Section("hero", _("Introduction")),
        Section("about", _("About")),
        Section("work", _("Work")),
        Section("projects", _("Projects")),
        # Section("blog", _("Blog")),
        Section("process", _("Process")),
        Section("contact", _("Contact")),
    ]
    return render(
        request,
        "core/home.html",
        context={"section_list": section_list, "DEBUG": settings.DEBUG},
    )


async def about(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "coming_soon.html",
        {
            "page_title": _("About"),
            "page_icon": "bi-person-fill",
            "page_message": _(
                "I'm putting together a proper about page: background, the six "
                "languages, how I think about problems. The homepage "
                "introduction covers the essentials for now."
            ),
        },
    )
    # return render(request, "core/about.html", context={"DEBUG": settings.DEBUG})


async def work(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "coming_soon.html",
        {
            "page_title": _("Work"),
            "page_icon": "bi-briefcase-fill",
            "page_message": _(
                "A detailed breakdown of what I do and how I do it is coming: "
                "services, tools, and the approach behind the work. The "
                "homepage gives a summary in the meantime."
            ),
        },
    )
    # return render(request, "core/work.html", context={"DEBUG": settings.DEBUG})


async def projects(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "coming_soon.html",
        {
            "page_title": _("Projects"),
            "page_icon": "bi-code-slash",
            "page_message": _(
                "A curated showcase of my work is being put together: data "
                "pipelines, ML systems, and the web projects in between. "
                "The homepage gives a preview for now."
            ),
        },
    )


async def contact(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "coming_soon.html",
        {
            "page_title": _("Contact"),
            "page_icon": "bi-envelope-fill",
            "page_message": _(
                "This form is still being built. In the meantime, reach me "
                "directly at my email, I respond within 24 hours."
            ),
        },
    )
    # return render(request, "core/contact.html", context={"DEBUG": settings.DEBUG})


async def toast_preview(request: HttpRequest):
    messages.set_level(request, messages.DEBUG)  # enables DEBUG level (off by default)
    messages.debug(request, _("🐛 DEBUG — lowest level, hidden in production"))
    messages.info(request, _("ℹ️ INFO — general information"))
    messages.success(request, _("✅ SUCCESS — action completed"))
    messages.warning(request, _("⚠️ WARNING — something needs attention"))
    messages.error(request, _("❌ ERROR — something went wrong"))
    return redirect("/")  # or any page that extends base.html


async def gone(request: HttpRequest):
    return render(request, "410.html", status=410)


async def error_400(request: HttpRequest, exception=None):
    return TemplateResponse(request, "400.html", status=400)


async def error_403(request: HttpRequest, exception=None):
    return TemplateResponse(request, "403.html", status=403)


async def error_403_csrf(request: HttpRequest, reason: str = ""):
    return TemplateResponse(request, "403_csrf.html", {"reason": reason}, status=403)


async def error_404(request: HttpRequest, exception=None):
    return TemplateResponse(request, "404.html", status=404)


async def error_410(request: HttpRequest):
    return TemplateResponse(request, "410.html", status=410)


async def error_500(request: HttpRequest):
    return TemplateResponse(request, "500.html", status=500)
