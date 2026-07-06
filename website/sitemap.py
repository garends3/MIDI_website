"""
SEO: proper Django sitemap definitions.

The previous sitemap.py accidentally duplicated views.py and defined view
functions instead of a Sitemap class, so it never produced a real
sitemap.xml. This file replaces it.

Wire this up in the project's urls.py (see the diff/instructions given
alongside this file).
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Person, ResearchTheme


from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.apps import apps


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["home", "people", "research", "publications"]

    def location(self, item):
        return reverse(item)


class PersonSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        Person = apps.get_model("website", "Person")
        return Person.objects.all()

    def location(self, obj):
        return reverse("person_detail", args=[obj.slug])


class ResearchThemeSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return []

    def location(self, obj):
        return reverse("home")


sitemaps = {
    "static": StaticViewSitemap,
    "people": PersonSitemap,
    "research": ResearchThemeSitemap,
}