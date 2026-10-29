#!/usr/bin/env python3
"""Carte des usines (page des cartes) : projette le fond de carte et les lieux d'usine dans des panneaux
(zoom sur l'Angleterre, Europe, Amérique du Nord, Brésil, Japon, Afrique du Sud, Australie ; un panneau sans lieu n'est pas produit)
et écrit _data/carte_usines.yml, que lit _includes/carte-usines.html.

Usage : python3 outils/carte-usines.py <ne_50m_admin_0_countries.geojson>
Le fond vient de Natural Earth (domaine public), pays à 1:50 m, version 5.1.2 :
  https://raw.githubusercontent.com/nvkelso/natural-earth-vector/v5.1.2/geojson/ne_50m_admin_0_countries.geojson
Il n'est pas versionné ici ; seuls les tracés projetés et simplifiés le sont (dans le fichier produit).
Les lieux viennent de _data/usines-coordonnees.yml. À relancer si un lieu est ajouté."""
import json, math, os, sys
import yaml

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE)

# panneau : (identifiant, lon min, lon max, lat min, lat max, largeur en px)
# Un lieu va dans le premier panneau qui le contient, dans cet ordre de priorité : les zooms d'abord.
# Un panneau dessine un cadre à l'emplacement de chaque zoom qu'il contient. Ordre d'affichage : AFFICHAGE.
PANNEAUX = [
    ("londres", -0.85, 0.25, 51.15, 51.78, 560),
    ("italie-nord", 7.3, 12.6, 43.9, 45.95, 560),
    ("los-angeles", -118.6, -117.35, 33.3, 34.3, 420),
    ("angleterre", -2.35, 1.25, 50.55, 53.55, 560),
    ("europe", -9.5, 16.5, 36.5, 55.5, 640),
    ("amerique-nord", -124.0, -70.0, 25.0, 49.0, 640),
    ("bresil", -58.0, -38.0, -30.0, -15.0, 320),
    ("japon", 129.0, 145.0, 31.0, 41.0, 320),
    ("afrique-sud", 16.0, 33.5, -35.0, -22.0, 320),
    ("australie", 112.0, 155.0, -44.0, -10.0, 320),
]
AFFICHAGE = ["europe", "angleterre", "londres", "italie-nord", "amerique-nord", "los-angeles", "bresil", "japon", "afrique-sud", "australie"]
TAILLE = 10.5          # corps des étiquettes (px), pour l'estimation de leur largeur
CHASSE = 0.56          # largeur moyenne d'un caractère, en corps

def projeteur(lo0, lo1, la0, la1, largeur):
    kx = math.cos(math.radians((la0 + la1) / 2))
    echelle = largeur / ((lo1 - lo0) * kx)
    hauteur = (la1 - la0) * echelle
    return (lambda lon, lat: ((lon - lo0) * kx * echelle, (la1 - lat) * echelle)), round(hauteur)

def anneaux(geom):
    if geom["type"] == "Polygon":
        yield from geom["coordinates"]
    elif geom["type"] == "MultiPolygon":
        for poly in geom["coordinates"]:
            yield from poly

def fond(features, proj, lo0, lo1, la0, la1, largeur, hauteur):
    marge = 2.0
    morceaux = []
    for f in features:
        for anneau in anneaux(f["geometry"]):
            lons = [p[0] for p in anneau]; lats = [p[1] for p in anneau]
            if max(lons) < lo0 - marge or min(lons) > lo1 + marge or max(lats) < la0 - marge or min(lats) > la1 + marge:
                continue
            pts, dernier = [], None
            for lon, lat in anneau:
                x, y = proj(lon, lat)
                x = min(max(x, -40), largeur + 40); y = min(max(y, -40), hauteur + 40)   # rabat les points lointains au bord
                if dernier is None or abs(x - dernier[0]) + abs(y - dernier[1]) >= 0.8:
                    pts.append((x, y)); dernier = (x, y)
            if len(pts) >= 3:
                morceaux.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
    return "".join(morceaux)

def placer(points, largeur, hauteur):
    """Étiquette de chaque point : on essaie huit directions, à trois distances croissantes, et l'on garde la
    première position qui ne chevauche ni une autre étiquette ni un point. Au-delà de la première distance,
    un trait relie l'étiquette à son point (champ « trait »)."""
    pris = [(p["x"] - 5, p["y"] - 5, 10, 10) for p in points]
    def libre(r):
        return (0 <= r[0] and r[0] + r[2] <= largeur and 0 <= r[1] and r[1] + r[3] <= hauteur and
                all(r[0] + r[2] <= q[0] or q[0] + q[2] <= r[0] or r[1] + r[3] <= q[1] or q[1] + q[3] <= r[1] for q in pris))
    # (dx, dy) unitaires et ancre du texte
    directions = [(1, 0, "start"), (-1, 0, "end"), (0, -1, "middle"), (0, 1, "middle"),
                  (1, -1, "start"), (1, 1, "start"), (-1, -1, "end"), (-1, 1, "end")]
    for p in sorted(points, key=lambda p: (p["x"], p["y"])):
        w, h = len(p["nom"]) * TAILLE * CHASSE, TAILLE
        choix = None
        for rayon in (8, 20, 34):
            for ux, uy, ancre in directions:
                ax, ay = p["x"] + ux * rayon, p["y"] + uy * rayon * 0.8      # point d'accroche de l'étiquette
                x0 = ax if ancre == "start" else ax - w if ancre == "end" else ax - w / 2
                y0 = ay - h / 2 if uy == 0 else (ay - h if uy < 0 else ay)
                r = (x0, y0, w, h)
                if libre(r):
                    choix = (ancre, ax - p["x"], y0 + h * 0.82 - p["y"], rayon > 8, ax - p["x"], ay - p["y"], r); break
            if choix: break
        if choix is None:
            r = (p["x"] + 8, p["y"] - h / 2, w, h)
            choix = ("start", 8, h * 0.32, False, 8, 0, r)
        p["ancre"], p["dx"], p["dy"] = choix[0], round(choix[1], 1), round(choix[2], 1)
        if choix[3]:
            p["trait"] = [round(choix[4], 1), round(choix[5], 1)]
        pris.append(choix[6])

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    features = json.load(open(sys.argv[1], encoding="utf-8"))["features"]
    lieux = yaml.safe_load(open("_data/usines-coordonnees.yml", encoding="utf-8"))
    sortie = {"panneaux": []}
    place = {}
    for l in lieux:
        for pid, lo0, lo1, la0, la1, _ in PANNEAUX:
            if lo0 <= l["lon"] <= lo1 and la0 <= l["lat"] <= la1:
                place[l["id"]] = pid
                break
    for pid, lo0, lo1, la0, la1, largeur in sorted(PANNEAUX, key=lambda p: AFFICHAGE.index(p[0])):
        if pid not in place.values():
            continue
        proj, hauteur = projeteur(lo0, lo1, la0, la1, largeur)
        pan = {"id": pid, "largeur": largeur, "hauteur": hauteur, "fond": fond(features, proj, lo0, lo1, la0, la1, largeur, hauteur), "points": []}
        for l in lieux:
            if place.get(l["id"]) == pid:
                x, y = proj(l["lon"], l["lat"])
                pan["points"].append({"lieu": l["id"], "nom": l["nom"], "x": round(x, 1), "y": round(y, 1)})
        placer(pan["points"], largeur, hauteur)
        for p in pan["points"]:
            del p["nom"]
        # cadres des zooms contenus dans ce panneau (et qui ont des lieux)
        pan["cadres"] = []
        for zid, a0, a1, b0, b1, _ in PANNEAUX:
            if zid != pid and zid in place.values() and lo0 <= a0 and a1 <= lo1 and la0 <= b0 and b1 <= la1:
                x0, y0 = proj(a0, b1); x1, y1 = proj(a1, b0)
                pan["cadres"].append({"zoom": zid, "x": round(x0, 1), "y": round(y0, 1), "l": round(x1 - x0, 1), "h": round(y1 - y0, 1)})
        # un zoom déjà contenu dans un autre zoom du même panneau n'a pas son propre cadre (Londres dans l'Angleterre)
        boites = {c["zoom"]: c for c in pan["cadres"]}
        pan["cadres"] = [c for c in pan["cadres"] if not any(
            o is not c and o["x"] <= c["x"] and o["y"] <= c["y"] and c["x"] + c["l"] <= o["x"] + o["l"] and c["y"] + c["h"] <= o["y"] + o["h"]
            for o in boites.values())]
        sortie["panneaux"].append(pan)
    for l in lieux:
        if l["id"] not in place:
            print(f"attention : {l['id']} hors de tous les panneaux", file=sys.stderr)
    entete = ("# Carte des usines : produit par outils/carte-usines.py (ne pas modifier a la main).\n"
              "# Fond : Natural Earth, pays 1:50 m (domaine public) ; lieux : _data/usines-coordonnees.yml.\n")
    open("_data/carte_usines.yml", "w", encoding="utf-8").write(entete + yaml.safe_dump(sortie, allow_unicode=True, sort_keys=False, width=100000))
    print({p["id"]: (p["largeur"], p["hauteur"], len(p["points"]), len(p["fond"])) for p in sortie["panneaux"]})

main()
