from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("people/", views.people, name="people"),
    path("research/", views.research, name="research"),
    path("publications/", views.publications, name="publications"),
]