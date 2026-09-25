import re

from django.http import Http404
from django.shortcuts import render
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .models import ResearchTheme, Publication, PhDThesis
from .people_data import PEOPLE_BY_SLUG, ALUMNI, grouped_people, author_patterns
from .news_data import NEWS, NEWS_BY_SLUG


def home(request):
    return render(request, "website/home.html", {
        "news": NEWS[:3],
        "n_people": len(PEOPLE_BY_SLUG),
        "n_publications": Publication.objects.count(),
        "meta_title": "MiDI Lab – Diffusion MRI & Microstructure Imaging | UMC Utrecht",
        "meta_description": "MiDI Lab at UMC Utrecht develops diffusion MRI methods, from plug-and-play "
                            "gradient inserts and ultra-high-field MRI to microstructure modelling, "
                            "microscopy validation and flow MRI.",
    })


def people(request):
    return render(request, "website/people.html", {
        "groups": grouped_people(),
        "alumni": ALUMNI,
        "meta_title": "People – MiDI Lab, UMC Utrecht",
        "meta_description": "Meet the researchers of MiDI Lab at UMC Utrecht: our group lead, postdocs, "
                            "PhD candidates and alumni working on diffusion MRI and microstructure imaging.",
    })


def person_detail(request, slug):
    person = PEOPLE_BY_SLUG.get(slug)
    if person is None:
        raise Http404("Unknown person")
    return render(request, f"people/{slug}.html", {
        "person": person,
        "meta_title": f"{person['name']} – {person['role']} | MiDI Lab, UMC Utrecht",
        "meta_description": person["description"],
        "og_type": "profile",
        "og_image": f"people/{person['photo']}",
    })


def research(request):
    return render(request, "website/research.html", {
        "themes": ResearchTheme.objects.all(),
        "meta_title": "Research – MiDI Lab, UMC Utrecht",
        "meta_description": "MiDI Lab's research spans diffusion MRI with plug-and-play gradient inserts, "
                            "multi-modal microscopy validation of tissue microstructure, and flow MRI of "
                            "intracranial aneurysms.",
    })


_AUTHOR_RE = None


def _highlight_authors(authors):
    """Escape an author string and bold the lab members in it."""
    global _AUTHOR_RE
    if _AUTHOR_RE is None:
        alts = "|".join(re.escape(a) for a in sorted(author_patterns(), key=len, reverse=True))
        _AUTHOR_RE = re.compile(rf"(^|, )((?:{alts})[^,]*)", re.IGNORECASE)
    return mark_safe(_AUTHOR_RE.sub(r"\1<strong>\2</strong>", escape(authors)))


PREPRINT_SERVERS = {"arxiv", "biorxiv", "medrxiv", "research square"}


def _is_preprint(pub):
    return (pub.journal or "").strip().lower() in PREPRINT_SERVERS


def publications(request):
    pubs = list(Publication.objects.all().order_by("-year", "-pmid"))
    # Hide a preprint when the peer-reviewed version is also listed.
    published_titles = {p.title.lower().rstrip(". ") for p in pubs if not _is_preprint(p)}
    pubs = [p for p in pubs if not (_is_preprint(p) and p.title.lower().rstrip(". ") in published_titles)]

    journal_articles = {}
    for pub in pubs:
        journal_articles.setdefault(pub.year or "Other", []).append({
            "title": pub.title,
            "authors": _highlight_authors(pub.authors),
            "journal": pub.journal,
            "year": pub.year,
            "link": pub.link,
        })

    return render(request, "website/publications.html", {
        "journal_articles": journal_articles,
        "n_articles": sum(len(v) for v in journal_articles.values()),
        "phd_theses": PhDThesis.objects.all().order_by("-year"),
        "meta_title": "Publications – MiDI Lab, UMC Utrecht",
        "meta_description": "Journal articles and PhD theses from MiDI Lab at UMC Utrecht on diffusion MRI, "
                            "tissue microstructure, gradient hardware and quantitative MRI.",
    })


def news_detail(request, slug):
    item = NEWS_BY_SLUG.get(slug)
    if item is None:
        raise Http404("Unknown news item")
    return render(request, f"news/{slug}.html", {
        "item": item,
        "meta_title": f"{item['title']} – MiDI Lab news",
        "meta_description": item["summary"],
        "og_type": "article",
        "og_image": item["image"],
    })
