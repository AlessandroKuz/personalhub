from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    priority = 0.9
    changefreq = "monthly"
    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return [
            "core:home",
            "core:about",
            "core:work",
            "core:projects",
            "core:contact",
        ]

    def location(self, item):
        return reverse(item)
