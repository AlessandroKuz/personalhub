"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # language switcher endpoint
]

# All user-facing URLs get language prefix: /en/... /it/...
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    # path('projects/', include('apps.projects.urls')),
    # path('blog/', include('apps.blog.urls')),
    prefix_default_language=True,  # /about/ works as well as /en/about/
)

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
    # Import is inside the if — critical. A top-level import would crash prod
    # because debug_toolbar is not in prod's INSTALLED_APPS.
