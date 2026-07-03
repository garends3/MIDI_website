from Bio import Entrez
import time
import os
import django

# Set up Django environment for standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taxlab_website.settings")
django.setup()

from website.models import Publication

# Configure Entrez
Entrez.email = "G.C.Arends-3@umcutrecht.nl"  # change to your email
Entrez.api_key = "232b1a9b82ac417d126745752812b305bf08"  # optional but recommended

def fetch_pubmed_ids(name, retmax=200):
    """Search PubMed for articles by an author name, return list of PMIDs."""
    handle = Entrez.esearch(db="pubmed",
                            term=f"{name}[Author]",
                            retmax=retmax)
    result = Entrez.read(handle)
    handle.close()
    return result["IdList"]

def fetch_pubmed_details(pmids):
    """Fetch article metadata (title, authors, journal, year) for a list of PMIDs."""
    if not pmids:
        return []
    ids_str = ",".join(pmids)
    handle = Entrez.efetch(db="pubmed", id=ids_str,
                           rettype="xml", retmode="text")
    records = Entrez.read(handle)
    handle.close()
    return records.get("PubmedArticle", [])

def parse_article(article):
    """Extract relevant info from a PubMed XML article dict."""
    medline = article.get("MedlineCitation", {})
    pmid = medline.get("PMID", "")
    article_data = medline.get("Article", {})
    
    title = article_data.get("ArticleTitle", "No title")
    journal = article_data.get("Journal", {}).get("Title", "No journal")

    # Year extraction
    year = None
    try:
        year_str = article_data.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {}).get("Year")
        if year_str:
            year = int(year_str)
    except Exception:
        year = None

    # Authors
    authors_list = []
    for auth in article_data.get("AuthorList", []):
        name = f"{auth.get('LastName','')} {auth.get('ForeName','')}".strip()
        if name:
            authors_list.append(name)
    authors_str = ", ".join(authors_list)

    link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

    return {
        "pmid": pmid,
        "title": title,
        "authors": authors_str,
        "journal": journal,
        "year": year,
        "link": link
    }

def import_publications_for_author(author_name):
    pmids = fetch_pubmed_ids(author_name)
    print(f"Found {len(pmids)} PMIDs for {author_name}")

    articles = fetch_pubmed_details(pmids)

    for article in articles:
        data = parse_article(article)
        pub, created = Publication.objects.update_or_create(
            pmid=str(data["pmid"]),          # use pmid from parsed data
            defaults={
                "title": data["title"],
                "authors": data["authors"],
                "journal": data.get("journal", ""),
                "year": data.get("year"),
                "link": data.get("link", "")
            }
        )
        if created:
            print(f"Added {data['pmid']}: {data['title']}")
        else:
            print(f"Updated {data['pmid']}: {data['title']}")

        time.sleep(0.34)  # stay within NCBI rate limits

if __name__ == "__main__":
    # Example: you can pass multiple authors here
    authors = ["Tax CMW", "Chantal MW Tax"]
    
    for author in authors:
        import_publications_for_author(author)