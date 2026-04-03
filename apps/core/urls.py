from django.urls import path
from django.conf import settings

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("work/", views.work, name="work"),
    path("about/", views.about, name="about"),
    path("projects/", views.projects, name="projects"),
    path("contact/", views.contact, name="contact"),
]

if settings.DEBUG:
    urlpatterns += [
        path("__toast-preview__/", views.toast_preview, name="toast_preview"),
    ]
