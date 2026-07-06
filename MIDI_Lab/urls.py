from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView

from website.sitemap import sitemaps

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('website.urls')),

    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
    ),

    path(
        'robots.txt',
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]