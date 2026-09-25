"""
News items, newest first. The home page shows the first three.

To add a news item:
  1. Add an entry at the TOP of NEWS (slug = template name, URL = /news/<slug>.html).
  2. Create website/templates/news/<slug>.html (copy an existing one).
  3. Put the image in website/static/images/.
"""

NEWS = [
    dict(slug="ISMRM_2026", label="Conference",
         title="Highlights from ISMRM 2026 in Cape Town",
         summary="Tatiana Nikolaeva's 28.2T OGSE abstract was nominated for the Best Power Pitch Award, "
                 "and we announced the upcoming Microstructure Challenge.",
         image="images/ISMRM_2026.jpg"),
    dict(slug="NatureCom", label="Publication",
         title="New paper in Communications Biology",
         summary="A self-supervised implicit neural representation method improves diffusion MRI estimation "
                 "of the Standard Model of white matter, especially at low signal-to-noise.",
         image="images/brain_poster.jpg"),
    dict(slug="Vidi_Chantal", label="Grant",
         title="NWO VIDI grant for ultra-high-field diffusion MRI",
         summary="MiDI Lab has been awarded an NWO VIDI grant to advance diffusion MRI research at 28.2T, "
                 "enabling new insights into tissue microstructure.",
         image="images/news3.svg"),
]

NEWS_BY_SLUG = {n["slug"]: n for n in NEWS}
