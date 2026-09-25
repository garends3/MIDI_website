"""Sitemap for search engines, served at /sitemap.xml."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .people_data import PEOPLE
from .news_data import NEWS


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return ["home", "people", "research", "publications"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "home" else 0.8


class PersonSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return [p["slug"] for p in PEOPLE]

    def location(self, slug):
        return reverse("person_detail", args=[slug])


class NewsSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return [n["slug"] for n in NEWS]

    def location(self, slug):
        return reverse("news_detail", args=[slug])


sitemaps = {
    "static": StaticViewSitemap,
    "people": PersonSitemap,
    "news": NewsSitemap,
}
