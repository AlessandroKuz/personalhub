from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect


async def home(request: HttpRequest) -> HttpResponse:
    return render(request, "core/home.html")


async def work(request: HttpRequest) -> HttpResponse:
    return render(request, "core/work.html")


async def about(request: HttpRequest) -> HttpResponse:
    return render(request, "core/about.html")


async def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "core/contact.html")


async def toast_preview(request):
    messages.set_level(request, messages.DEBUG)  # enables DEBUG level (off by default)
    messages.debug(request, "🐛 DEBUG — lowest level, hidden in production")
    messages.info(request, "ℹ️ INFO — general information")
    messages.success(request, "✅ SUCCESS — action completed")
    messages.warning(request, "⚠️ WARNING — something needs attention")
    messages.error(request, "❌ ERROR — something went wrong")
    return redirect("/")  # or any page that extends base.html
