from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("people/", views.people, name="people"),
    path("research/", views.research, name="research"),
    path("publications/", views.publications, name="publications"),
    path('people/<slug:slug>/', views.person_detail, name='person_detail'),
    path("news/ISMRM_2026.html", views.ISMRM_2026),
    path("news/NatureCom.html", views.news_natcom),
    path("news/Vidi_Chantal.html", views.news_vidi),
]