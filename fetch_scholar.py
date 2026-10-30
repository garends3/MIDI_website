"""
Update the Publications page from Chantal Tax's Google Scholar profile.

Run locally (Google blocks requests from cloud servers):

    venv_website\\Scripts\\activate
    pip install requests beautifulsoup4
    python fetch_scholar.py

Then commit db.sqlite3 and push.

What it does
- Reads every entry on the Scholar profile (100 per page, a few requests only).
- Adds new entries and updates existing ones (matched on Scholar ID, or on title
  for entries that came from the old PubMed script).
- Removes publications that are not on the Scholar profile, so the website
  mirrors the profile. Use --keep-old to skip this step.

Note: Scholar's list view shortens long author lists (they end in "...").
"""
import argparse
import os
import random
import re
import sys
import time

import django
import requests
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MIDI_Lab.settings")
django.setup()

from website.models import Publication  # noqa: E402

SCHOLAR_USER = "glzYhDgAAAAJ"  # Chantal Tax
BASE = "https://scholar.google.com"
PAGE_SIZE = 100
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def norm_title(title):
    """Lower-case, letters/digits only – used to match PubMed rows to Scholar rows."""
    return re.sub(r"[^a-z0-9]", "", (title or "").lower())


def parse_page(html):
    """Return a list of publication dicts from one Scholar profile page."""
    soup = BeautifulSoup(html, "html.parser")
    if soup.find(id="gsc_a_b") is None:
        raise RuntimeError(
            "Google Scholar did not return the publication list "
            "(probably a CAPTCHA or rate limit). Wait a while and try again."
        )

    pubs = []
    for row in soup.select("tr.gsc_a_tr"):
        a = row.select_one("a.gsc_a_at")
        if a is None:
            continue
        href = a.get("href", "")
        m = re.search(r"citation_for_view=([^&]+)", href)
        scholar_id = m.group(1) if m else None

        grays = row.select("div.gs_gray")
        authors = grays[0].get_text(strip=True) if len(grays) > 0 else ""
        venue = grays[1].get_text(" ", strip=True) if len(grays) > 1 else ""
        venue = re.sub(r",?\s*(19|20)\d{2}$", "", venue).strip(" ,")  # drop year at end

        year_el = row.select_one("td.gsc_a_y span")
        year_txt = year_el.get_text(strip=True) if year_el else ""
        year = int(year_txt) if year_txt.isdigit() else None

        pubs.append({
            "scholar_id": scholar_id,
            "title": a.get_text(strip=True),
            "authors": authors,
            "journal": venue,
            "year": year,
            "link": BASE + href.replace("&amp;", "&") if href else "",
        })
    return pubs


def fetch_all():
    session = requests.Session()
    session.headers.update(HEADERS)
    pubs, start = [], 0
    while True:
        url = (f"{BASE}/citations?hl=en&user={SCHOLAR_USER}"
               f"&view_op=list_works&sortby=pubdate&cstart={start}&pagesize={PAGE_SIZE}")
        resp = session.get(url, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f"Google Scholar returned HTTP {resp.status_code}. Try again later.")
        page = parse_page(resp.text)
        pubs.extend(page)
        print(f"  page {start // PAGE_SIZE + 1}: {len(page)} entries")
        if len(page) < PAGE_SIZE:
            break
        start += PAGE_SIZE
        time.sleep(random.uniform(4, 8))  # be polite, avoid CAPTCHAs
    return pubs


def sync(pubs, keep_old=False):
    existing = list(Publication.objects.all())
    by_key = {p.pmid: p for p in existing if p.pmid}
    by_title = {}
    for p in existing:
        by_title.setdefault(norm_title(p.title), p)

    kept_ids, added, updated = set(), 0, 0
    for d in pubs:
        key = f"scholar:{d['scholar_id']}" if d["scholar_id"] else None
        obj = by_key.get(key) or by_title.get(norm_title(d["title"]))
        if obj and obj.pk in kept_ids:
            obj = None  # two Scholar entries with the same title: keep both
        if obj is None:
            obj = Publication()
            added += 1
        else:
            updated += 1
        obj.pmid = key
        obj.title = d["title"][:500]
        obj.authors = d["authors"]
        obj.journal = d["journal"][:500]
        obj.year = d["year"]
        obj.link = d["link"]
        obj.save()
        kept_ids.add(obj.pk)

    removed = 0
    if not keep_old:
        stale = Publication.objects.exclude(pk__in=kept_ids)
        removed = stale.count()
        stale.delete()

    print(f"Done: {added} added, {updated} updated, {removed} removed "
          f"({Publication.objects.count()} publications in database).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keep-old", action="store_true",
                    help="don't delete publications that aren't on the Scholar profile")
    args = ap.parse_args()

    print(f"Fetching Google Scholar profile {SCHOLAR_USER} ...")
    try:
        pubs = fetch_all()
    except Exception as e:
        print(f"ERROR: {e}\nDatabase not changed.")
        sys.exit(1)

    if len(pubs) < 10:
        print(f"Only {len(pubs)} entries found – looks wrong, so the database was not changed.")
        sys.exit(1)

    sync(pubs, keep_old=args.keep_old)


if __name__ == "__main__":
    main()
