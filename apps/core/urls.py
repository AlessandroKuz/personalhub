from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("work/", views.work, name="work"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("__toast-preview__/", views.toast_preview, name="toast_preview"),
]
