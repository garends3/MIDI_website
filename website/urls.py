"""
URL configuration for taxlab_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView

from ..website.sitemap import sitemaps  # sitemap.py content replaced - was a broken duplicate of views.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),

    # SEO: real sitemap.xml (was broken before - see website/sitemaps.py)
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
    ),

    # SEO: robots.txt pointing crawlers at the sitemap.
    # Create templates/robots.txt (see robots.txt file provided alongside this).
    path(
        'robots.txt',
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]