"""
Single source of truth for lab members.

To add a person:
  1. Add an entry to PEOPLE below (slug = URL part, e.g. /people/jane-doe/).
  2. Put their photo in website/static/people/ (square-ish, ~800px is plenty).
  3. Create website/templates/people/<slug>.html (copy an existing profile).
The People page, profile header, sitemap and search-engine data all use this list.
"""

GROUPS = [
    ("pi", "Principal Investigator"),
    ("postdoc", "Postdoctoral Researchers"),
    ("phd", "PhD Candidates"),
]

PEOPLE = [
    # --- Principal investigator -------------------------------------------
    dict(slug="chantal-tax", name="Chantal Tax", group="pi",
         role="Associate Professor", photo="chantal_tax.png",
         email="C.M.W.Tax@umcutrecht.nl",
         keywords=["Diffusion MRI", "Gradient inserts", "Tractography"],
         description="Chantal Tax is Associate Professor at UMC Utrecht and leads MiDI Lab, "
                     "developing diffusion MRI methods from gradient hardware to quantitative modelling."),

    # --- Postdocs -----------------------------------------------------------
    dict(slug="tatiana-nikolaeva", name="Tatiana Nikolaeva", group="postdoc",
         role="Postdoctoral Researcher", photo="tatiana_nikolaeva.png",
         email="T.Nikolaeva@umcutrecht.nl", keywords=[],
         description="Tatiana Nikolaeva is a postdoctoral researcher at MiDI Lab, Department of Radiology, "
                     "UMC Utrecht, the High Precision Imaging Group and the Image Sciences Institute."),
    dict(slug="rico-singer", name="Rico Singer", group="postdoc",
         role="Postdoctoral Researcher", photo="rico_singer.jpeg", email="",
         keywords=["Ultra-high-field MRI", "CEST MRI", "MR spectroscopy", "Multimodal imaging",
                   "Neurodegenerative diseases"],
         description="Rico Singer is a postdoctoral researcher at MiDI Lab, UMC Utrecht, developing advanced "
                     "and multimodal MRI methods to study rare neurodegenerative diseases."),

    # --- PhD candidates -----------------------------------------------------
    dict(slug="leon-arends", name="Leon Arends", group="phd",
         role="PhD Candidate", photo="leon_arends.jpeg",
         email="G.C.Arends-3@umcutrecht.nl",
         keywords=["MRI physics", "Diffusion MRI", "Gradient inserts"],
         description="Leon Arends is a PhD candidate at MiDI Lab, UMC Utrecht, using plug-and-play gradient "
                     "inserts for high-performance diffusion MRI of the brain and breast."),
    dict(slug="christos-kanakis", name="Christos Kanakis", group="phd",
         role="PhD Candidate", photo="christos_kanakis.jpg", email="ck@cerebriu.com",
         keywords=["Machine learning", "Diffusion MRI", "Prostate cancer", "dMRI preprocessing"],
         description="Christos Kanakis is a PhD candidate at MiDI Lab, UMC Utrecht, and Cerebriu, developing "
                     "automated diffusion MRI preprocessing, quality control and detection for prostate cancer."),
    dict(slug="paula-del-popolo", name="Paula del Popolo", group="phd",
         role="PhD Candidate", photo="paula_del_popolo.jpg",
         email="M.P.DelPopolo-2@umcutrecht.nl",
         keywords=["Diffusion MRI", "Physics-informed machine learning", "Tissue microstructure",
                   "Sequence optimisation"],
         description="Paula del Popolo is a PhD candidate at MiDI Lab, UMC Utrecht, working on forward "
                     "modelling of diffusion MRI to probe tissue microstructure."),
    dict(slug="jiaxin-zhang", name="Jiaxin Zhang", group="phd",
         role="PhD Candidate", photo="jiaxin_zhang.jpg", email="J.Zhang-3@umcutrecht.nl",
         keywords=["Deep learning", "Intracranial aneurysms", "Segmentation", "Hemodynamic analysis",
                   "Vascular imaging"],
         description="Jiaxin Zhang is a PhD candidate at MiDI Lab, UMC Utrecht, developing deep learning "
                     "segmentation of intracranial arteries and aneurysms and 4D Flow MRI hemodynamic analysis."),
    dict(slug="jamila-guichelaar", name="Jamila Guichelaar", group="phd",
         role="PhD Candidate", photo="jamila_guichelaar.jpg",
         email="C.J.Guichelaar-2@umcutrecht.nl", keywords=[],
         description="Jamila Guichelaar is a PhD candidate at MiDI Lab, Department of Radiology, UMC Utrecht."),
    dict(slug="phebe-groenheide", name="Phebe Groenheide", group="phd",
         role="PhD Candidate", photo="phebe_groenheide.jpg",
         email="P.J.Groenheide@umcutrecht.nl",
         keywords=["MRA", "CTA", "Intracranial aneurysms"],
         description="Phebe Groenheide is a PhD candidate at UMC Utrecht developing image-based prediction of "
                     "intracranial aneurysm instability within the Aneurysm@Risk project."),
    dict(slug="jeroen-de-groot", name="Jeroen de Groot", group="phd",
         role="PhD Candidate", photo="jeroen_de_groot.jpg",
         email="J.T.J.deGroot-34@umcutrecht.nl",
         keywords=["Time-dependent diffusion MRI", "Microstructure"],
         description="Jeroen de Groot is a PhD candidate at MiDI Lab, UMC Utrecht, using time-dependent "
                     "diffusion MRI to characterize tumour microstructure."),
    dict(slug="dominique-weltevreden", name="Dominique Weltevreden", group="phd",
         role="PhD Candidate", photo="dominique_weltevreden.jpg", email="",
         keywords=["Ultrasound", "Machine learning", "Developmental neuroscience"],
         description="Dominique Weltevreden is a PhD candidate at Utrecht University and MiDI Lab, UMC Utrecht, "
                     "applying ultrasound, MRI and normative modelling to early brain development."),
    dict(slug="vittoria-cappozzo", name="Vittoria Cappozzo", group="phd",
         role="PhD Candidate", photo="vittoria_cappozzo.jpg", email="V.Cappozzo@umcutrecht.nl",
         keywords=["Diffusion MRI", "Imaging biomarkers", "Paediatric oncology", "Sarcoma"],
         description="Vittoria Cappozzo is a PhD candidate at MiDI Lab, UMC Utrecht, developing diffusion MRI "
                     "biomarkers of tumour microstructure for paediatric rhabdomyosarcoma and Ewing sarcoma."),
]

ALUMNI = [
    ("PhD", ["Anouk Versteeg"]),
    ("Master's students", ["Joris Harbers"]),
]

PEOPLE_BY_SLUG = {p["slug"]: p for p in PEOPLE}


def grouped_people():
    """[(heading, [person, ...]), ...] in display order."""
    return [(title, [p for p in PEOPLE if p["group"] == key]) for key, title in GROUPS]


# How a member appears in PubMed author lists ("Surname Initial"), where the
# default (last word of the name + first initial) would be wrong.
PUBMED_NAMES = {
    "leon-arends": "Arends G",
    "paula-del-popolo": "Del Popolo M",
    "jeroen-de-groot": "de Groot J",
}


def author_patterns():
    """'Surname Initial' prefixes used to highlight lab members in author lists."""
    out = []
    for p in PEOPLE:
        if p["slug"] in PUBMED_NAMES:
            out.append(PUBMED_NAMES[p["slug"]])
        else:
            first, last = p["name"].split()[0], p["name"].split()[-1]
            out.append(f"{last} {first[0]}")
    return out
