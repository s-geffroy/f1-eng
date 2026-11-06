#!/usr/bin/env python3
"""Relevé des résultats officiels (formula1.com) : vainqueur, podium et poleman de chaque Grand Prix,
points des constructeurs et des pilotes, saisons 1950-2025. Écrit _data/resultats.yml.
Usage : python3 -I outils/releve-resultats.py <dossier-cache>

Le dossier-cache reçoit les pages téléchargées (<annee>-races.html, -team.html, -drivers.html, et
pour chaque course courses/<annee>-<id>-race-result.html et -starting-grid.html) ; une page déjà
présente n'est pas retéléchargée. Il doit être hors du dépôt : ce sont des données
externes, jamais versionnées.

Chaque nom d'équipe de formula1.com (« Châssis Moteur ») est rapporté à une écurie de
_data/ecuries.yml (désambiguïsée par l'année) et à un motoriste. Un nom inconnu arrête le script :
on complète la table CHASSIS ou MOTEURS, on ne devine pas. Les gagnants sans fiche (constructeurs
des 500 miles d'Indianapolis) sont gardés sous leur nom, sans identifiant."""
import os, re, sys, html, time, urllib.request, urllib.error
import yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # pour outils/commun.py (python3 -I)
import commun

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE)
ANNEES = range(commun.PREMIERE_SAISON, commun.DERNIERE_SAISON + 1)
BASE = "https://www.formula1.com"

# Préfixe du nom formula1.com -> [(de, a, écurie)] ; écurie None = gagnant sans fiche sur le site.
CHASSIS = {
    "AGS": [(0, 9999, "ags")], "ATS": [(0, 9999, "ats-1978")],
    "Alfa Romeo Racing": [(2019, 2023, "alfa-romeo")],
    "Alfa Romeo": [(1950, 1951, "alfa-romeo-1950"), (1979, 1985, "alfa-romeo-1979"), (2019, 2023, "alfa-romeo")],
    "AlphaTauri": [(0, 9999, "alphatauri")], "Alpine": [(0, 9999, "alpine")],
    "Arrows": [(0, 9999, "arrows")], "Aston Martin": [(2021, 2026, "aston-martin")],
    "BAR": [(0, 9999, "bar")], "BRP": [(0, 9999, "brp")], "BRM": [(0, 9999, "brm")],
    "Benetton": [(0, 9999, "benetton")], "Brabham": [(0, 9999, "brabham")],
    "Brawn": [(0, 9999, "brawn")], "Caterham": [(0, 9999, "caterham")],
    "Cooper": [(0, 9999, "cooper")], "Dallara": [(0, 9999, "dallara")],
    "Eagle": [(0, 9999, "eagle")], "Ensign": [(0, 9999, "ensign")],
    "Epperly": [(0, 9999, None)], "Ferrari": [(0, 9999, "ferrari")],
    "Fittipaldi": [(0, 9999, "fittipaldi")], "Footwork": [(0, 9999, "footwork")],
    "Force India": [(0, 9999, "force-india")],
    "Frank Williams Racing Cars/Williams": [(0, 9999, "frank-williams-racing-cars")],
    "HRT": [(0, 9999, "hrt")], "Haas F1 Team": [(0, 9999, "haas")], "Haas": [(0, 9999, "haas")],
    "Hesketh": [(0, 9999, "hesketh")], "Hill": [(0, 9999, "hill")],
    "Honda": [(1964, 1968, "honda-1964"), (2006, 2008, "honda")],
    "Iso Marlboro": [(0, 9999, "iso-marlboro")], "Jaguar": [(0, 9999, "jaguar")],
    "Jordan": [(0, 9999, "jordan")], "Kick Sauber": [(0, 9999, "kick-sauber")],
    "Kurtis Kraft": [(0, 9999, "kurtis-kraft")], "Kuzma": [(0, 9999, None)],
    "Lancia": [(1954, 1955, "lancia"), (1956, 1956, "ferrari")], "Connaught": [(0, 9999, "connaught")],
    "Larrousse": [(0, 9999, "larrousse")], "Leyton House": [(0, 9999, "leyton-house")],
    "Ligier": [(0, 9999, "ligier")],
    "Lola": [(1962, 1986, "lola"), (1987, 1991, "lola-larrousse")],
    "Lotus": [(1958, 1994, "team-lotus"), (2010, 2011, "lotus-racing"), (2012, 2015, "lotus-f1")],
    "MF1": [(0, 9999, "midland")], "MRT": [(0, 9999, "manor")],
    "March": [(0, 9999, "march")], "Marussia": [(0, 9999, "marussia")],
    "Maserati": [(0, 9999, "maserati")], "Matra": [(0, 9999, "matra")],
    "McLaren": [(0, 9999, "mclaren")], "Mclaren": [(0, 9999, "mclaren")],
    "Mercedes-Benz": [(1954, 1955, "mercedes-1954")], "Mercedes": [(2010, 2026, "mercedes")],
    "Minardi": [(0, 9999, "minardi")], "Onyx": [(0, 9999, "onyx")],
    "Osella": [(0, 9999, "osella")], "Parnelli": [(0, 9999, "parnelli")],
    "Penske": [(0, 9999, "penske")], "Porsche": [(0, 9999, "porsche")],
    "Prost": [(0, 9999, "prost")], "RB": [(0, 9999, "rb")], "RBR": [(0, 9999, "red-bull")],
    "STR": [(0, 9999, "toro-rosso")], "Racing Bulls": [(0, 9999, "racing-bulls")],
    "Racing Point": [(0, 9999, "racing-point")], "Red Bull Racing": [(0, 9999, "red-bull")],
    "Red Bull": [(0, 9999, "red-bull")],
    "Renault": [(1977, 1985, "renault-1977"), (2002, 2011, "renault"), (2016, 2020, "renault")],
    "Rial": [(0, 9999, "rial")],
    "Sauber": [(1993, 2005, "sauber"), (2006, 2009, "bmw-sauber"), (2010, 2018, "sauber")],
    "Scuderia Toro Rosso": [(0, 9999, "toro-rosso")], "Shadow": [(0, 9999, "shadow")],
    "Spyker": [(0, 9999, "spyker")], "Stewart": [(0, 9999, "stewart")],
    "Super Aguri": [(0, 9999, "super-aguri")], "Surtees": [(0, 9999, "surtees")],
    "Tecno": [(0, 9999, "tecno")], "Theodore": [(0, 9999, "theodore")],
    "Toleman": [(0, 9999, "toleman")], "Toro Rosso": [(0, 9999, "toro-rosso")],
    "Toyota": [(0, 9999, "toyota")], "Tyrrell": [(0, 9999, "tyrrell")],
    "Vanwall": [(0, 9999, "vanwall")], "Venturi": [(0, 9999, "venturi")],
    "Virgin": [(0, 9999, "virgin")], "Watson": [(0, 9999, None)],
    "Williams": [(1978, 2026, "williams")], "Wolf": [(0, 9999, "wolf")],
    "Zakspeed": [(0, 9999, "zakspeed")],
}
# Suffixe moteur du nom formula1.com -> motoriste de _data/ecuries.yml.
MOTEURS = {
    "Ford": "ford", "Cosworth": "cosworth", "Climax": "climax", "BRM": "brm", "Honda": "honda",
    "Honda RBPT": "honda-rbpt", "RBPT": "rbpt", "TAG Heuer": "tag-heuer", "TAG": "tag",
    "Mugen Honda": "mugen-honda", "Mercedes": "mercedes", "Aramco Mercedes": "mercedes",
    "BWT Mercedes": "mercedes", "Offenhauser": "offenhauser", "Repco": "repco",
    "Weslake": "weslake", "Serenissima": "serenissima", "Castellotti": "castellotti",
    "Megatron": "megatron", "Supertec": "supertec", "Playlife": "playlife", "Petronas": "petronas",
    "Mecachrome": "mecachrome", "Asiatech": "asiatech", "Acer": "acer", "Hart": "hart",
    "Judd": "judd", "Ilmor": "ilmor", "Yamaha": "yamaha", "Lamborghini": "lamborghini",
    "Peugeot": "peugeot", "Matra": "matra", "Alfa Romeo": "alfa-romeo", "Ferrari": "ferrari",
    "Renault": "renault", "BMW": "bmw", "Toyota": "toyota", "Maserati": "maserati",
    "Bristol": "bristol", "Alta": "alta", "OSCA": "osca", "JAP": "jap", "Lea-Francis": "lea-francis",
    "Borgward": "borgward", "Novi": "novi", "Cummins": "cummins",
}
# Erreurs d'équipe de formula1.com, corrigées à la source : (saison, GP, rôle) -> nom d'équipe juste.
# Argentine 1955 : González part en pole sur Ferrari 625 (formula1.com écrit « Lancia »).
# Brésil 1983 : Rosberg part en pole sur Williams FW08C à moteur Ford (la grille écrit « Williams
# Honda », moteur qu'il n'a qu'à la dernière course) ; disqualifié, il manque à la page de la course.
# Argentine 1975 : Jarier part en pole sur Shadow DN5 à moteur Ford (la grille écrit « Shadow Matra »,
# moteur de la DN7 de fin de saison) ; non partant, il manque à la page de la course.
CORRECTIONS = {(1955, "Argentina", "pole"): "Ferrari", (1983, "Brazil", "pole"): "Williams Ford",
               (1975, "Argentina", "pole"): "Shadow Ford"}
# Coquilles de libellé de formula1.com, rectifiées avant tout rapprochement.
LIBELLES = {"Lanica Ferrari": "Lancia Ferrari"}
# Suffixes qui ne sont pas un moteur (commanditaire) : moteur pris dans la fiche.
COMMANDITAIRES = {"Sahara"}
# Gagnants sans fiche : motoriste connu par le nom seul.
MOTEUR_SANS_FICHE = {}

# Premières places que la page de la course attribue à un autre pilote que la liste des courses,
# examinées dans les deux pages : (saison, GP) -> constat. Un autre désaccord arrête le script.
VAINQUEURS_EXAMINES = {}

def obtenir(url, chemin, absente_ok=False):
    """Télécharge url dans chemin (cache). Erreur 429 ou 5xx, coupure réseau : nouvel essai, de plus en
    plus tard. 404 avec absente_ok : page mémorisée vide. Écriture par fichier temporaire puis
    os.replace : un arrêt en cours de route ne laisse pas dans le cache une page tronquée, qui serait
    relue comme bonne au passage suivant."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for essai in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                contenu = r.read()
            break
        except urllib.error.HTTPError as e:
            if e.code == 404 and absente_ok:
                contenu = b""      # page absente : mémorisée vide, pour ne pas la redemander
                break
            if (e.code != 429 and e.code < 500) or essai == 5:
                sys.exit(f"{url} : erreur HTTP {e.code}")
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if essai == 5:
                sys.exit(f"{url} : {e}")
        time.sleep(10 * (essai + 1))
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin + ".tmp", "wb") as f:
        f.write(contenu)
    os.replace(chemin + ".tmp", chemin)
    time.sleep(0.5)

def telecharger_course(cache, url, page):
    """Page d'une course (race-result, starting-grid) ; None si formula1.com ne la publie pas."""
    annee, ident = re.search(r"/results/(\d+)/races/(\d+)/", url).groups()
    chemin = os.path.join(cache, "courses", f"{annee}-{ident}-{page}.html")
    if not os.path.exists(chemin):
        obtenir(url.replace("/race-result", "/" + page), chemin, absente_ok=True)
    return open(chemin, encoding="utf-8").read() or None

def classe(cache, url, page, annee):
    """Lignes classées d'une page de course : [(position, pilote, (écurie, motoriste, nom))].
    Un équipage partagé occupe plusieurs lignes à la même position : seule la première est gardée."""
    t = telecharger_course(cache, url, page)
    if t is None:
        return None
    out = {}
    for l in lignes(t):
        if len(l) >= 4 and l[0].isdigit() and int(l[0]) not in out:
            out[int(l[0])] = (pilote(l[2], annee), equipe(l[3], annee, strict=False))
    return out

def equipes_course(cache, url, annee):
    """Équipe de chaque pilote sur la page de résultats de la course, abandons compris."""
    t = telecharger_course(cache, url, "race-result")
    return {pilote(l[2], annee): equipe(l[3], annee, strict=False) for l in lignes(t or "") if len(l) >= 4}

def place(p, rang=None):
    """Entrée « place, pilote, équipe, écurie, motoriste » d'une position, sans champ vide."""
    nom, (ec, mot, eq) = p
    d = ({"place": rang} if rang else {}) | {"pilote": nom, "equipe": eq}
    if ec: d["ecurie"] = ec
    if mot: d["motoriste"] = mot
    return d

def telecharger(cache, annee, page):
    chemin = os.path.join(cache, f"{annee}-{page}.html")
    if not os.path.exists(chemin):
        obtenir(f"{BASE}/en/results/{annee}/{page}", chemin)
    return open(chemin, encoding="utf-8").read()

def lignes(texte):
    out = []
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", texte, re.S):
        cellules = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)
        out.append([" ".join(html.unescape(re.sub("<[^>]+>", " ", c)).split()) for c in cellules])
    return out[1:]

# Noms que formula1.com écrit sans leurs accents, rétablis d'après Jolpica (même nom, accents mis à part).
ACCENTS = {
    "Andre Pilette": "André Pilette", "Antonio Pizzonia": "Antônio Pizzonia", "Elie Bayol": "Élie Bayol",
    "Eric Bernard": "Éric Bernard", "Erik Comas": "Érik Comas", "Esteban Gutierrez": "Esteban Gutiérrez",
    "Eugene Chaboud": "Eugène Chaboud", "Francois Cevert": "François Cevert", "Jean-Eric Vergne": "Jean-Éric Vergne",
    "Jose Froilan Gonzalez": "José Froilán González", "Jyrki Jarvilehto": "Jyrki Järvilehto",
    "Luis Perez-Sala": "Luis Pérez-Sala", "Marc Gene": "Marc Gené", "Mauricio Gugelmin": "Maurício Gugelmin",
    "Mika Hakkinen": "Mika Häkkinen", "Nico Hulkenberg": "Nico Hülkenberg", "Nyck De Vries": "Nyck de Vries",
    "Onofre Marimon": "Onofre Marimón", "Paul Frere": "Paul Frère", "Pedro Rodriguez": "Pedro Rodríguez",
    "Philippe Etancelin": "Philippe Étancelin", "Rene Arnoux": "René Arnoux", "Ricardo Rodriguez": "Ricardo Rodríguez",
    "Sebastien Bourdais": "Sébastien Bourdais", "Sebastien Buemi": "Sébastien Buemi", "Sergio Perez": "Sergio Pérez",
}

# Homonymes que formula1.com écrit sous le même nom : (nom, première saison, dernière) -> nom distinct.
# Le site compte les pilotes par leur nom (outils/domination.py) ; Nelson Piquet fils (2008-2009, driverId
# Jolpica piquet_jr) serait sinon confondu avec son père (1978-1991). outils/releve-jolpica.py vérifie
# que chaque nom répond à un seul pilote.
HOMONYMES = {("Nelson Piquet", 2008, 2009): "Nelson Piquet Jr."}

def pilote(nom, annee):
    # Code à trois lettres accolé au nom, apostrophe comprise (« Pat O'Connor O'C »).
    nom = re.sub(r"\s+[A-Z][A-Z']{2}$", "", nom)
    nom = ACCENTS.get(nom, nom)
    return next((v for (n, de, a), v in HOMONYMES.items() if n == nom and de <= annee <= a), nom)

E = yaml.safe_load(open("_data/ecuries.yml", encoding="utf-8"))
MOT = {m["id"] for m in E["motoristes"]}
FICHES = {e["id"]: e for e in E["ecuries"]}

class Inconnu(Exception):
    pass

def equipe(nom, annee, strict=True):
    nom = LIBELLES.get(nom, nom)
    try:
        return _equipe(nom, annee)
    except Inconnu as e:
        if strict:
            sys.exit(str(e))
        return None, None, nom

def _equipe(nom, annee):
    """(écurie, motoriste, nom) pour un nom formula1.com et une saison. strict=False : None si inconnu
    (équipe d'un pilote au classement, souvent un petit constructeur des années 1950)."""
    for prefixe in sorted(CHASSIS, key=len, reverse=True):
        if nom == prefixe or nom.startswith(prefixe + " "):
            ec = next((e for de, a, e in CHASSIS[prefixe] if de <= annee <= a), "?")
            if ec == "?":
                raise Inconnu(f"{annee} : « {nom} » hors des années connues pour « {prefixe} »")
            reste = nom[len(prefixe):].strip()
            if ec is None:
                return None, MOTEURS.get(reste) or MOTEUR_SANS_FICHE.get(nom), nom
            if ec not in FICHES:
                raise Inconnu(f"{annee} : écurie « {ec} » absente de _data/ecuries.yml")
            if reste and reste not in COMMANDITAIRES:
                if reste not in MOTEURS:
                    raise Inconnu(f"{annee} : moteur « {reste} » inconnu (dans « {nom} »)")
                return ec, MOTEURS[reste], nom
            # Nom sans moteur : celui de la fiche pour l'année, s'il est unique.
            m = {x["motoriste"] for x in FICHES[ec].get("moteurs", []) if x["de"] <= annee <= x["a"]}
            return ec, (m.pop() if len(m) == 1 else None), nom
    raise Inconnu(f"{annee} : équipe « {nom} » inconnue (compléter CHASSIS)")

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    cache = sys.argv[1]
    os.makedirs(cache, exist_ok=True)
    saisons = []
    for annee in ANNEES:
        t = telecharger(cache, annee, "races")
        # Le lien de la course est lu dans sa propre ligne : une victoire partagée (France 1951,
        # Argentine 1956, Grande-Bretagne 1957) occupe deux lignes pour une seule course.
        rangs = re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S)[1:]
        liens = [re.search(rf'href="(/en/results/{annee}/races/[^"]+/race-result)"', r) for r in rangs]
        if not all(liens):
            sys.exit(f"{annee} : ligne de la liste des courses sans lien de résultat (mise en page de formula1.com changée ?)")
        liens = [m.group(1) for m in liens]
        gp = []
        for i, l in enumerate(lignes(t)):
            if gp and BASE + liens[i] == gp[-1]["url"]:
                if pilote(l[2], annee) == gp[-1]["vainqueur"] or equipe(l[3], annee)[2] != gp[-1]["equipe"]:
                    sys.exit(f"{annee} : victoire partagée incohérente (même pilote, ou autre équipe) : {l}")
                gp[-1]["covainqueur"] = pilote(l[2], annee)
                continue
            ec, mot, nom = equipe(l[3], annee)
            if mot is not None and mot not in MOT:
                sys.exit(f"{annee} : motoriste « {mot} » absent de _data/ecuries.yml (dans « {nom} »)")
            # Le drapeau répète le nom du pays : « Flag of Great Britain Great Britain ».
            pays = l[0][len("Flag of "):] if l[0].startswith("Flag of ") else l[0]
            moitie = pays[: len(pays) // 2].strip()
            course = {"gp": moitie if moitie == pays[len(pays) // 2:].strip() else pays,
                      "vainqueur": pilote(l[2], annee), "equipe": nom}
            if ec: course["ecurie"] = ec
            if mot: course["motoriste"] = mot
            course["url"] = BASE + liens[i]
            # Podium et grille : pages de la course. La pole est la première place de la grille de
            # départ publiée (après pénalités éventuelles), pas forcément le meilleur temps.
            res = classe(cache, course["url"], "race-result", annee)
            if res:
                if res.get(1, ("",))[0] not in (course["vainqueur"], course.get("covainqueur")) \
                        and (annee, course["gp"]) not in VAINQUEURS_EXAMINES:
                    sys.exit(f"{annee} {course['gp']} : vainqueur « {course['vainqueur']} » mais première place "
                             f"« {res.get(1, ('?',))[0]} » sur la page de la course ; examiner les deux pages, puis "
                             "consigner le constat dans VAINQUEURS_EXAMINES")
                # Place gardée explicitement : une place peut rester vide (Brésil 1983, deuxième disqualifié).
                course["podium"] = [place(res[k], k) for k in (2, 3) if k in res]
            grille = classe(cache, course["url"], "starting-grid", annee)
            if grille and 1 in grille:
                # L'équipe affichée sur la grille est parfois fausse (Lotus 49 « Lotus Climax » en 1967,
                # March de Stewart « Tyrrell » en 1970…) : quand la page de la course donne au même
                # pilote une autre écurie ou un autre moteur, c'est elle qui fait foi.
                eq = equipes_course(cache, course["url"], annee).get(grille[1][0])
                if eq and eq[:2] != grille[1][1][:2]:
                    grille[1] = (grille[1][0], eq)
                course["pole"] = place(grille[1])
                if (annee, course["gp"], "pole") in CORRECTIONS:
                    course["pole"] = place((grille[1][0], equipe(CORRECTIONS[annee, course["gp"], "pole"], annee)))
            gp.append(course)
        s = {"annee": annee, "gp": len(gp), "courses": gp}
        if annee >= 1958:
            cons = []
            for l in lignes(telecharger(cache, annee, "team")):
                ec, mot, nom = equipe(l[1], annee)
                c = {"equipe": nom, "points": float(l[2])}
                if ec: c["ecurie"] = ec
                if mot: c["motoriste"] = mot
                cons.append(c)
            s["constructeurs"] = cons
        pil = []
        for l in lignes(telecharger(cache, annee, "drivers")):
            # Pilote exclu du championnat (Schumacher 1997 : « DSQ ») : hors classement.
            if l[0].isdigit() and float(l[4]) > 0:
                p = {"pilote": pilote(l[1], annee), "points": float(l[4])}
                ec = equipe(l[3], annee, strict=False)[0] if l[3] else None
                if ec: p["ecurie"] = ec
                pil.append(p)
        s["pilotes"] = pil
        s["sources"] = [f"{BASE}/en/results/{annee}/{p}" for p in (("races", "team", "drivers") if annee >= 1958 else ("races", "drivers"))]
        saisons.append(s)
    entete = (f"# Résultats officiels par saison ({commun.PREMIERE_SAISON}-{commun.DERNIERE_SAISON}), relevés sur formula1.com par\n"
              "# outils/releve-resultats.py : ne pas modifier à la main, relancer le script.\n"
              "# courses : vainqueur de chaque Grand Prix (equipe = nom formula1.com, ecurie et motoriste =\n"
              "#   identifiants de _data/ecuries.yml, absents pour un gagnant sans fiche), url = résultat de la course.\n"
              "#   covainqueur : second pilote d'une victoire partagée (une seule course, créditée aux deux pilotes).\n"
              "#   podium : deuxième et troisième avec leur place (première ligne d'un équipage partagé) ; pole : première place de\n"
              "#   la grille de départ publiée. Absents quand formula1.com ne publie pas la page de la course.\n"
              "# constructeurs (depuis 1958) et pilotes : points au classement final ; sources : classements.\n"
              "# Les 500 miles d'Indianapolis (1950-1960) comptent au championnat et figurent donc ici.\n")
    texte = entete + yaml.safe_dump({"saisons": saisons}, allow_unicode=True, sort_keys=False, width=1000)
    with open("_data/resultats.yml.tmp", "w", encoding="utf-8") as f:
        f.write(texte)
    os.replace("_data/resultats.yml.tmp", "_data/resultats.yml")
    print(f"_data/resultats.yml : {len(saisons)} saisons, {sum(s['gp'] for s in saisons)} Grands Prix")

main()
