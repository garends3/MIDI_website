from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("people/", views.people, name="people"),
    path("research/", views.research, name="research"),
    path("publications/", views.publications, name="publications"),
    path("people/<slug:slug>/", views.person_detail, name="person_detail"),
    # Existing news URLs end in .html; kept as-is so old links keep working.
    path("news/<str:slug>.html", views.news_detail, name="news_detail"),
]
