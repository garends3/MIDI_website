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


class StaticViewSitemap(Sitemap):
    """Core static pages that don't map to a single model."""
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        # Add any other name= routes from urls.py here as the site grows
        return ["home", "people", "research", "publications"]

    def location(self, item):
        return reverse(item)


class PersonSitemap(Sitemap):
    """
    Individual people pages.

    NOTE: `person_detail` currently renders a static template named after
    a `slug` URL parameter (e.g. /people/jane-doe/ -> people/jane-doe.html),
    but the Person model has no `slug` field to generate that URL from.
    To include real people pages in the sitemap, add:

        slug = models.SlugField(max_length=200, unique=True, blank=True)

    to the Person model (and populate it, e.g. via save() override or a
    migration/data script from `name`). Once that field exists, this class
    will work as written.
    """
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Person.objects.exclude(slug__isnull=True).exclude(slug__exact="") \
            if hasattr(Person, "slug") else Person.objects.none()

    def location(self, obj):
        return reverse("person_detail", args=[obj.slug])


class ResearchThemeSitemap(Sitemap):
    """
    Placeholder for research theme pages. Currently /research/ shows all
    themes on one page rather than individual theme URLs. If you later add
    per-theme detail pages, wire them here the same way as PersonSitemap.
    """
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ResearchTheme.objects.none()  # no detail URL exists yet

    def location(self, obj):
        return reverse("home")


sitemaps = {
    "static": StaticViewSitemap,
    "people": PersonSitemap,
}