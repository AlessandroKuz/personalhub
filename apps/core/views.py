from dataclasses import dataclass

from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
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


async def work(request: HttpRequest) -> HttpResponse:
    return render(request, "core/work.html", context={"DEBUG": settings.DEBUG})


async def about(request: HttpRequest) -> HttpResponse:
    return render(request, "core/about.html", context={"DEBUG": settings.DEBUG})


async def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "core/contact.html", context={"DEBUG": settings.DEBUG})


async def toast_preview(request):
    messages.set_level(request, messages.DEBUG)  # enables DEBUG level (off by default)
    messages.debug(request, _("🐛 DEBUG — lowest level, hidden in production"))
    messages.info(request, _("ℹ️ INFO — general information"))
    messages.success(request, _("✅ SUCCESS — action completed"))
    messages.warning(request, _("⚠️ WARNING — something needs attention"))
    messages.error(request, _("❌ ERROR — something went wrong"))
    return redirect("/")  # or any page that extends base.html
