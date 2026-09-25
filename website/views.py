# Create your views here.
from django.shortcuts import render
from .models import Person, ResearchTheme, Publication, PhDThesis

def home(request):
    themes = ResearchTheme.objects.all()
    people = Person.objects.all()
    return render(request, "website/home.html", {
        "themes": themes,
        "people": people[:4],  # show only some
        "meta_title": "MiDI Lab \u2013 Diffusion MRI & Microstructure Imaging Research",
        "meta_description": "MiDI Lab at UMC Utrecht researches diffusion MRI and MRI gradient hardware. Explore our people, research themes, and publications, and learn how to collaborate with us.",
    })

def people(request):
    people = Person.objects.all().order_by("role")
    return render(request, "website/people.html", {
        "people": people,
        "meta_title": "People \u2013 MiDI Lab",
        "meta_description": "Meet the researchers of MiDI Lab at UMC Utrecht: our group lead, postdocs, PhD students, and alumni working on diffusion MRI and microstructure imaging.",
    })

def research(request):
    themes = ResearchTheme.objects.all()
    return render(request, "website/research.html", {
        "themes": themes,
        "meta_title": "Research \u2013 MiDI Lab",
        "meta_description": "MiDI Lab's research spans diffusion MRI with plug-and-play gradient inserts, multi-modal microscopy validation of tissue microstructure, and flow MRI for aneurysm detection.",
    })

def person_detail(request, slug):
    return render(request, f"people/{slug}.html")

def ISMRM_2026(request):
    return render(request, "news/ISMRM_2026.html")

def news_natcom(request):
    return render(request, "news/NatureCom.html")

def news_vidi(request):
    return render(request, "news/Vidi_Chantal.html")


def publications(request):
    """
    Display all publications and PhD theses stored in the database, grouped by year.
    """
    # Fetch publications from the database
    pubs = Publication.objects.all().order_by('-year')

    # Group publications by year
    journal_articles = {}
    for pub in pubs:
        year = pub.year if pub.year else "Unknown"
        journal_articles.setdefault(year, []).append({
            "title": pub.title,
            "authors": pub.authors,
            "journal": pub.journal,
            "link": pub.link
        })

    # Sort years descending
    for year in journal_articles:
        journal_articles[year] = sorted(
            journal_articles[year],
            key=lambda x: x.get("date", "")
        )

    # Fetch PhD theses from the database
    phd_theses_qs = PhDThesis.objects.all().order_by('-year')
    phd_theses = []
    for thesis in phd_theses_qs:
        phd_theses.append({
            "title": thesis.title,
            "author": thesis.author,
            "university": thesis.university,
            "year": thesis.year,
            "link": thesis.link
        })

    return render(request, "website/publications.html", {
        "journal_articles": journal_articles,
        "phd_theses": phd_theses
    })

