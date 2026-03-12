from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


async def home(request: HttpRequest) -> HttpResponse:
    return render(request, "core/home.html")


async def work(request: HttpRequest) -> HttpResponse:
    return render(request, "core/work.html")


async def about(request: HttpRequest) -> HttpResponse:
    return render(request, "core/about.html")


async def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "core/contact.html")
