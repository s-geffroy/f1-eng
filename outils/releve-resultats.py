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
on complète la table CHASSIS ou MOTEURS, on ne devine pas. Les gagnants sans fiche (Mercedes-Benz
1954-1955, constructeurs des 500 miles d'Indianapolis) sont gardés sous leur nom, sans identifiant."""
import os, re, sys, html, time, urllib.request, urllib.error
import yaml

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE)
ANNEES = range(1950, 2026)
BASE = "https://www.formula1.com"

# Préfixe du nom formula1.com -> [(de, a, écurie)] ; écurie None = gagnant sans fiche sur le site.
CHASSIS = {
    "AGS": [(0, 9999, "ags")], "ATS": [(0, 9999, "ats-1978")],
    "Alfa Romeo Racing": [(2019, 2023, "alfa-romeo")],
    "Alfa Romeo": [(1950, 1985, "alfa-romeo-1979"), (2019, 2023, "alfa-romeo")],
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
    "Larrousse": [(0, 9999, "larrousse")], "Leyton House": [(0, 9999, "leyton-house")],
    "Ligier": [(0, 9999, "ligier")],
    "Lola": [(1962, 1986, "lola"), (1987, 1991, "lola-larrousse")],
    "Lotus": [(1958, 1994, "team-lotus"), (2010, 2011, "lotus-racing"), (2012, 2015, "lotus-f1")],
    "MF1": [(0, 9999, "midland")], "MRT": [(0, 9999, "manor")],
    "March": [(0, 9999, "march")], "Marussia": [(0, 9999, "marussia")],
    "Maserati": [(0, 9999, "maserati")], "Matra": [(0, 9999, "matra")],
    "McLaren": [(0, 9999, "mclaren")], "Mclaren": [(0, 9999, "mclaren")],
    "Mercedes-Benz": [(0, 9999, None)], "Mercedes": [(2010, 2026, "mercedes")],
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
# Suffixes qui ne sont pas un moteur (commanditaire) : moteur pris dans la fiche.
COMMANDITAIRES = {"Sahara"}
# Gagnants sans fiche : motoriste connu par le nom seul.
MOTEUR_SANS_FICHE = {"Mercedes-Benz": "mercedes"}

def telecharger_course(cache, url, page):
    """Page d'une course (race-result, starting-grid) ; None si formula1.com ne la publie pas."""
    annee, ident = re.search(r"/results/(\d+)/races/(\d+)/", url).groups()
    chemin = os.path.join(cache, "courses", f"{annee}-{ident}-{page}.html")
    if not os.path.exists(chemin):
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        req = urllib.request.Request(url.replace("/race-result", "/" + page), headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                contenu = r.read()
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
            contenu = b""          # page absente : mémorisée vide, pour ne pas la redemander
        open(chemin, "wb").write(contenu)
        time.sleep(0.5)
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
            out[int(l[0])] = (pilote(l[2]), equipe(l[3], annee, strict=False))
    return out

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
        req = urllib.request.Request(f"{BASE}/en/results/{annee}/{page}", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            open(chemin, "wb").write(r.read())
        time.sleep(0.5)
    return open(chemin, encoding="utf-8").read()

def lignes(texte):
    out = []
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", texte, re.S):
        cellules = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)
        out.append([" ".join(html.unescape(re.sub("<[^>]+>", " ", c)).split()) for c in cellules])
    return out[1:]

def pilote(nom):
    # Code à trois lettres accolé au nom, apostrophe comprise (« Pat O'Connor O'C »).
    return re.sub(r"\s+[A-Z][A-Z']{2}$", "", nom)

E = yaml.safe_load(open("_data/ecuries.yml", encoding="utf-8"))
MOT = {m["id"] for m in E["motoristes"]}
FICHES = {e["id"]: e for e in E["ecuries"]}

class Inconnu(Exception):
    pass

def equipe(nom, annee, strict=True):
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
        liens = [re.search(rf'href="(/en/results/{annee}/races/[^"]+/race-result)"', r).group(1) for r in rangs]
        gp = []
        for i, l in enumerate(lignes(t)):
            if gp and BASE + liens[i] == gp[-1]["url"]:
                assert pilote(l[2]) != gp[-1]["vainqueur"] and equipe(l[3], annee)[2] == gp[-1]["equipe"], (annee, l)
                gp[-1]["covainqueur"] = pilote(l[2])
                continue
            ec, mot, nom = equipe(l[3], annee)
            assert mot is None or mot in MOT, (annee, mot)
            # Le drapeau répète le nom du pays : « Flag of Great Britain Great Britain ».
            pays = l[0][len("Flag of "):] if l[0].startswith("Flag of ") else l[0]
            moitie = pays[: len(pays) // 2].strip()
            course = {"gp": moitie if moitie == pays[len(pays) // 2:].strip() else pays,
                      "vainqueur": pilote(l[2]), "equipe": nom}
            if ec: course["ecurie"] = ec
            if mot: course["motoriste"] = mot
            course["url"] = BASE + liens[i]
            # Podium et grille : pages de la course. La pole est la première place de la grille de
            # départ publiée (après pénalités éventuelles), pas forcément le meilleur temps.
            res = classe(cache, course["url"], "race-result", annee)
            if res:
                if res.get(1, ("",))[0] not in (course["vainqueur"], course.get("covainqueur")):
                    print(f"attention : {annee} {course['gp']}, vainqueur « {course['vainqueur']} » mais "
                          f"première place « {res.get(1, ('?',))[0]} » sur la page de la course")
                # Place gardée explicitement : une place peut rester vide (Brésil 1983, deuxième disqualifié).
                course["podium"] = [place(res[k], k) for k in (2, 3) if k in res]
            grille = classe(cache, course["url"], "starting-grid", annee)
            if grille and 1 in grille:
                course["pole"] = place(grille[1])
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
            if float(l[4]) > 0:
                p = {"pilote": pilote(l[1]), "points": float(l[4])}
                ec = equipe(l[3], annee, strict=False)[0] if l[3] else None
                if ec: p["ecurie"] = ec
                pil.append(p)
        s["pilotes"] = pil
        s["sources"] = [f"{BASE}/en/results/{annee}/{p}" for p in (("races", "team", "drivers") if annee >= 1958 else ("races", "drivers"))]
        saisons.append(s)
    entete = ("# Résultats officiels par saison (1950-2025), relevés sur formula1.com par\n"
              "# outils/releve-resultats.py : ne pas modifier à la main, relancer le script.\n"
              "# courses : vainqueur de chaque Grand Prix (equipe = nom formula1.com, ecurie et motoriste =\n"
              "#   identifiants de _data/ecuries.yml, absents pour un gagnant sans fiche), url = résultat de la course.\n"
              "#   covainqueur : second pilote d'une victoire partagée (une seule course, créditée aux deux pilotes).\n"
              "#   podium : deuxième et troisième avec leur place (première ligne d'un équipage partagé) ; pole : première place de\n"
              "#   la grille de départ publiée. Absents quand formula1.com ne publie pas la page de la course.\n"
              "# constructeurs (depuis 1958) et pilotes : points au classement final ; sources : classements.\n"
              "# Les 500 miles d'Indianapolis (1950-1960) comptent au championnat et figurent donc ici.\n")
    texte = entete + yaml.safe_dump({"saisons": saisons}, allow_unicode=True, sort_keys=False, width=1000)
    open("_data/resultats.yml", "w", encoding="utf-8").write(texte)
    print(f"_data/resultats.yml : {len(saisons)} saisons, {sum(s['gp'] for s in saisons)} Grands Prix")

main()
