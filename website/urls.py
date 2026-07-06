from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path("", views.home, name="home"),
    path("people/", views.people, name="people"),
    path("research/", views.research, name="research"),
    path("publications/", views.publications, name="publications"),

    # People pages
    path("people/chantal-tax/", views.chantal_tax, name="chantal_tax"),
    path("people/christos-kanakis/", views.christos_kanakis, name="christos_kanakis"),
    path("people/jamila-guichelaar/", views.jamila_guichelaar, name="jamila_guichelaar"),
    path("people/leon-arends/", views.leon_arends, name="leon_arends"),
    path("people/phebe-groenheide/", views.phebe_groenheide, name="phebe_groenheide"),

    # News pages
    path("news/ismrm-2026/", views.ismrm_2026, name="ismrm_2026"),
    path("news/naturecom/", views.naturecom, name="naturecom"),
    path("news/vidi-chantal/", views.vidi_chantal, name="vidi_chantal"),
]