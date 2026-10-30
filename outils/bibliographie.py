#!/usr/bin/env python3
"""Bibliographie : toutes les sources citées par le site, dédoublonnées par URL et regroupées par
éditeur, avec les pages qui les citent. Lit le front matter des collections et les sources de
_data/*.yml ; écrit _data/bibliographie.yml et _data/en/bibliographie.yml (pages /sources/ et
/en/sources/). Usage : python3 outils/bibliographie.py   (à relancer après tout ajout de source)

Les pages de résultats course par course de formula1.com (_data/resultats.yml, 1950-2025) ne sont
pas listées une à une : elles forment un jeu de données, présenté comme tel en tête de page."""
import os, re, glob, collections
from urllib.parse import urlsplit
import yaml

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE)

# Éditeur d'après le domaine ; un domaine absent est affiché tel quel.
EDITEURS = {
    "motorsportmagazine.com": "Motor Sport Magazine", "formula1.com": "Formula 1",
    "grandprix.com": "GrandPrix.com", "autosport.com": "Autosport", "en.wikipedia.org": "Wikipedia",
    "fr.wikipedia.org": "Wikipedia (fr)", "it.wikipedia.org": "Wikipedia (it)", "de.wikipedia.org": "Wikipedia (de)",
    "commons.wikimedia.org": "Wikimedia Commons", "the-race.com": "The Race", "racefans.net": "RaceFans",
    "fia.com": "FIA", "goodwood.com": "Goodwood", "motorsport.com": "Motorsport.com",
    "theguardian.com": "The Guardian", "nytimes.com": "The New York Times", "bbc.co.uk": "BBC",
    "bbc.com": "BBC", "telegraph.co.uk": "The Telegraph", "independent.co.uk": "The Independent",
    "racecar-engineering.com": "Racecar Engineering", "lequipe.fr": "L'Équipe", "imeche.org": "IMechE",
    "ims.com": "Indianapolis Motor Speedway", "indianapolismotorspeedway.com": "Indianapolis Motor Speedway",
    "jolpi.ca": "Jolpica", "openstreetmap.org": "OpenStreetMap", "mclaren.com": "McLaren",
    "ferrari.com": "Ferrari", "williamsf1.com": "Williams", "redbullracing.com": "Red Bull Racing",
    "mercedesamgf1.com": "Mercedes-AMG F1", "statsf1.com": "StatsF1", "oldracingcars.com": "OldRacingCars",
    "forix.autosport.com": "Forix (Autosport)", "8w.forix.com": "8W (Forix)", "archive.org": "Internet Archive",
    "web.archive.org": "Internet Archive", "youtube.com": "YouTube", "pirelli.com": "Pirelli",
    "forix.com": "Forix (Autosport)", "global.honda": "Honda", "crash.net": "Crash.net",
    "f1technical.net": "F1Technical", "pitpass.com": "Pitpass", "skysports.com": "Sky Sports",
    "planetf1.com": "PlanetF1", "speedcafe.com": "Speedcafe", "lotuscars.com": "Lotus Cars",
    "classicteamlotus.co.uk": "Classic Team Lotus", "bmwgroup.com": "BMW Group",
    "group.renault.com": "Groupe Renault", "espn.com": "ESPN", "communicationskw.podbean.com": "Beyond the Grid (podcast)",
}
AUTRES = 3                                         # un éditeur de moins de AUTRES sources va dans « autres »

MOIS = {"janvier": "January", "février": "February", "mars": "March", "avril": "April", "mai": "May",
        "juin": "June", "juillet": "July", "août": "August", "septembre": "September", "octobre": "October",
        "novembre": "November", "décembre": "December"}
PAYS = {"France": "French", "Belgique": "Belgian", "Monaco": "Monaco", "Allemagne": "German", "Italie": "Italian",
        "Grande-Bretagne": "British", "Espagne": "Spanish", "Pays-Bas": "Dutch", "Suisse": "Swiss"}

def titre_en(t):
    """Titre anglais d'une source des données sans version anglaise (chassis, pneus, technologies) :
    guillemets et mentions françaises traduits, le titre cité restant tel quel."""
    t = re.sub(r"«\s*(.*?)\s*»", r"“\1”", t)
    t = re.sub(r"compte rendu du Grand Prix (?:de |d'|du )(\S+)(?: (\d{4}))?",
               lambda m: f"{m.group(2) + ' ' if m.group(2) else ''}{PAYS.get(m.group(1), m.group(1))} Grand Prix report", t)
    t = re.sub(r"résultats de l'Indianapolis 500 (\d{4})", r"\1 Indianapolis 500 results", t)
    t = re.sub(r"saison (\d{4}) de F1", r"\1 F1 season", t)
    for a, b in (("tableau des engagés", "entry list"), ("articles étiquetés", "tagged articles"),
                 ("base de données", "database"), ("fiche équipe", "team page"), ("résultats", "results"),
                 ("(tableau “", "(table “"), ("Wikipédia", "Wikipedia (fr)")):
        t = t.replace(a, b)
    t = re.sub(r"\b(" + "|".join(MOIS) + r")\b", lambda m: MOIS[m.group(1)], t)
    return t

def cle_url(url):
    """URL normalisée pour le dédoublonnage : sans protocole, sans « www. », sans barre finale."""
    return re.sub(r"^https?://(www\.)?", "", url).rstrip("/").lower()

def editeur(url):
    hote = urlsplit(url).hostname or url
    hote = hote.removeprefix("www.")
    if hote in EDITEURS:
        return EDITEURS[hote]
    parties = hote.split(".")
    for i in range(1, len(parties) - 1):
        if ".".join(parties[i:]) in EDITEURS:
            return EDITEURS[".".join(parties[i:])]
    return hote

def front_matter(chemin):
    texte = open(chemin, encoding="utf-8").read()
    if not texte.startswith("---\n"):
        return {}
    return yaml.safe_load(texte.split("---\n", 2)[1]) or {}

# langue -> collections (dossier, préfixe d'URL) et fichiers de données (fichier, page, ancre)
LANGUES = {
    "fr": {"sortie": "_data/bibliographie.yml", "titre_cle": "titre",
           "collections": [("_ingenieurs", "/ingenieurs/"), ("_voitures", "/voitures/"), ("_dossiers", "/dossiers/")],
           "donnees": "_data", "pages": {"ecuries": "/ecuries/", "glossaire": "/glossaire/", "chronologie": "/chronologie/",
                                          "lignees": "/lignees/", "circuits": "/cartes/", "chassis": "/dossiers/domination/",
                                          "pneus": "/dossiers/domination/", "technologies": "/dossiers/domination/"},
           "noms": {"ecuries": "Écuries", "glossaire": "Glossaire", "chronologie": "Chronologie", "lignees": "Lignées",
                    "circuits": "Cartes", "chassis": "Domination (châssis)", "pneus": "Domination (pneus)",
                    "technologies": "Domination (technologies)"}},
    "en": {"sortie": "_data/en/bibliographie.yml", "titre_cle": "titre_en",
           "collections": [("_engineers", "/en/engineers/"), ("_cars", "/en/cars/"), ("_features", "/en/features/")],
           "donnees": "_data/en", "pages": {"ecuries": "/en/teams/", "glossaire": "/en/glossary/", "chronologie": "/en/timeline/",
                                             "lignees": "/en/lineages/", "circuits": "/en/maps/", "chassis": "/en/features/domination/",
                                             "pneus": "/en/features/domination/", "technologies": "/en/features/domination/"},
           "noms": {"ecuries": "Teams", "glossaire": "Glossary", "chronologie": "Timeline", "lignees": "Lineages",
                    "circuits": "Maps", "chassis": "Dominance (chassis)", "pneus": "Dominance (tyres)",
                    "technologies": "Dominance (technologies)"}},
}
# Fichiers de données sans version anglaise : lus dans _data/ pour les deux langues.
COMMUNS = ("circuits", "chassis", "pneus", "technologies")

for lang, L in LANGUES.items():
    sources = {}                                   # url -> {titre, editeur, pages: {url: titre}}

    def ajouter(titre, url, page_url, page_titre):
        if not (isinstance(url, str) and url.startswith("http")):
            return
        s = sources.setdefault(cle_url(url), {"titre": titre or url, "url": url, "pages": {}})
        s["pages"].setdefault((page_url, page_titre), None)

    for dossier, prefixe in L["collections"]:
        for f in sorted(glob.glob(f"{dossier}/*.md")):
            fm = front_matter(f)
            page = prefixe + os.path.basename(f)[:-3] + "/"
            for s in fm.get("sources") or []:
                ajouter(s.get("titre"), s.get("url"), page, fm.get("title", page))

    for cle, page in L["pages"].items():
        base = "_data" if cle in COMMUNS else L["donnees"]
        donnees = yaml.safe_load(open(f"{base}/{cle}.yml", encoding="utf-8"))
        nom_page = L["noms"][cle]

        def parcourir(x, ancre, intitule):
            if isinstance(x, dict):
                if cle == "ecuries" and "id" in x and "voitures" in x:      # fiche d'écurie
                    ancre, intitule = f"{x['id']}/", x["nom"]
                elif cle == "ecuries" and "id" in x and "nom" in x and ("segments" in x or "usines" in x):
                    ancre, intitule = "", x["nom"]          # lignée (usines, souffleries) ou motoriste
                elif cle == "ecuries" and "annee" in x and "pilote" in x:   # titres de la saison
                    ancre, intitule = "", ("saison " if lang == "fr" else "season ") + str(x["annee"])
                elif cle == "glossaire" and "terme" in x:
                    ancre, intitule = f"#{x['id']}", x["terme"]
                elif cle == "chronologie" and "annee" in x and "titre" in x and "id" in x:
                    ancre, intitule = f"#{'c' if 'categorie' in x else 'j'}-{x['id']}", f"{x['annee']}, {x['titre']}"
                elif cle == "circuits" and "lat" in x:
                    ancre, intitule = "", x.get("nom_en" if lang == "en" else "nom")
                elif cle == "technologies" and "defaut" in x:
                    ancre, intitule = "", x.get("nom_en" if lang == "en" else "nom")
                elif cle == "chassis" and "modeles" in x:
                    ancre, intitule = "", f"{x['annee']}, {x.get('equipe', '')}"
                elif cle == "lignees" and "etapes" in x:
                    ancre, intitule = f"#{x['id']}", x["nom"]
                if isinstance(x.get("url"), str) and ("titre" in x or "titre_en" in x):
                    t = x.get(L["titre_cle"]) or (titre_en(x["titre"]) if lang == "en" and cle in COMMUNS else x.get("titre"))
                    ajouter(t, x["url"], page + ancre,
                            nom_page + (f" : {intitule}" if intitule and lang == "fr" else f": {intitule}" if intitule else ""))
                for v in x.values():
                    parcourir(v, ancre, intitule)
            elif isinstance(x, list):
                for v in x:
                    parcourir(v, ancre, intitule)
        parcourir(donnees, "", "")

    groupes = collections.defaultdict(list)
    for s in sources.values():
        url = s["url"]
        groupes[editeur(url)].append({"titre": s["titre"], "url": url,
                                      "pages": [{"url": u, "titre": t} for u, t in sorted(s["pages"], key=lambda p: p[1].lower())]})
    def tri(t):
        return re.sub(r"[«»“”\"'‘’]", "", t).lower()
    autres = [s for v in groupes.values() if len(v) < AUTRES for s in v]
    editeurs = sorted(({"nom": nom, "n": len(v), "sources": sorted(v, key=lambda s: tri(s["titre"]))}
                       for nom, v in groupes.items() if len(v) >= AUTRES), key=lambda e: (-e["n"], e["nom"].lower()))
    editeurs.append({"nom": "Autres éditeurs" if lang == "fr" else "Other publishers", "autres": True,
                     "n": len(autres), "sources": sorted(autres, key=lambda s: tri(s["titre"]))})
    sortie = {"total": len(sources), "editeurs_total": len(groupes),
              "citations": sum(len(s["pages"]) for s in sources.values()), "editeurs": editeurs}
    entete = ("# Bibliographie générée par outils/bibliographie.py : ne pas modifier à la main, relancer le script.\n"
              if lang == "fr" else "# Bibliography generated by outils/bibliographie.py: do not edit by hand, rerun the script.\n")
    with open(L["sortie"], "w", encoding="utf-8") as f:
        f.write(entete)
        yaml.safe_dump(sortie, f, allow_unicode=True, sort_keys=False, width=1000)
    print(f"{lang} : {len(sources)} sources, {len(editeurs)} éditeurs -> {L['sortie']}")
