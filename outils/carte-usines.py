#!/usr/bin/env python3
"""Carte des usines (page des écuries) : projette le fond de carte et les lieux d'usine dans trois panneaux
(Europe, zoom sur l'Angleterre, Caroline du Nord) et écrit _data/carte_usines.yml, que lit
_includes/carte-usines.html.

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
PANNEAUX = [
    ("europe", -6.5, 15.0, 42.6, 55.2, 640),
    ("angleterre", -2.35, 1.25, 50.55, 53.55, 560),
    ("amerique", -84.5, -75.0, 33.0, 37.5, 280),
]
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
    """Étiquette de chaque point : à droite, à gauche, au-dessus ou au-dessous, sans chevaucher les autres."""
    pris = [(p["x"] - 4, p["y"] - 4, 8, 8) for p in points]
    def libre(r):
        return (0 <= r[0] and r[0] + r[2] <= largeur and 0 <= r[1] and r[1] + r[3] <= hauteur and
                all(r[0] + r[2] <= q[0] or q[0] + q[2] <= r[0] or r[1] + r[3] <= q[1] or q[1] + q[3] <= r[1] for q in pris))
    for p in sorted(points, key=lambda p: p["x"]):
        w, h = len(p["nom"]) * TAILLE * CHASSE, TAILLE
        essais = [("start", 7, 3.5, (p["x"] + 6, p["y"] - h / 2, w, h)),
                  ("end", -7, 3.5, (p["x"] - 6 - w, p["y"] - h / 2, w, h)),
                  ("middle", 0, -7, (p["x"] - w / 2, p["y"] - 6 - h, w, h)),
                  ("middle", 0, 14, (p["x"] - w / 2, p["y"] + 6, w, h)),
                  ("start", 6, -6, (p["x"] + 5, p["y"] - 6 - h, w, h)),
                  ("start", 6, 13, (p["x"] + 5, p["y"] + 5, w, h)),
                  ("end", -6, -6, (p["x"] - 5 - w, p["y"] - 6 - h, w, h)),
                  ("end", -6, 13, (p["x"] - 5 - w, p["y"] + 5, w, h))]
        choix = next((e for e in essais if libre(e[3])), essais[0])
        p["ancre"], p["dx"], p["dy"] = choix[0], choix[1], choix[2]
        pris.append(choix[3])

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    features = json.load(open(sys.argv[1], encoding="utf-8"))["features"]
    lieux = yaml.safe_load(open("_data/usines-coordonnees.yml", encoding="utf-8"))
    sortie = {"panneaux": []}
    for pid, lo0, lo1, la0, la1, largeur in PANNEAUX:
        proj, hauteur = projeteur(lo0, lo1, la0, la1, largeur)
        pan = {"id": pid, "largeur": largeur, "hauteur": hauteur, "fond": fond(features, proj, lo0, lo1, la0, la1, largeur, hauteur), "points": []}
        for l in lieux:
            dans = lo0 <= l["lon"] <= lo1 and la0 <= l["lat"] <= la1
            # l'Europe ne montre pas les lieux du zoom sur l'Angleterre (un cadre y renvoie)
            if pid == "europe" and PANNEAUX[1][1] <= l["lon"] <= PANNEAUX[1][2] and PANNEAUX[1][3] <= l["lat"] <= PANNEAUX[1][4]:
                dans = False
            if dans:
                x, y = proj(l["lon"], l["lat"])
                pan["points"].append({"lieu": l["id"], "nom": l["nom"], "x": round(x, 1), "y": round(y, 1)})
        placer(pan["points"], largeur, hauteur)
        for p in pan["points"]:
            del p["nom"]
        if pid == "europe":
            _, a0, a1, b0, b1, _ = PANNEAUX[1]
            x0, y0 = proj(a0, b1); x1, y1 = proj(a1, b0)
            pan["cadre"] = {"x": round(x0, 1), "y": round(y0, 1), "l": round(x1 - x0, 1), "h": round(y1 - y0, 1)}
        sortie["panneaux"].append(pan)
    places = {p["lieu"] for pan in sortie["panneaux"] for p in pan["points"]}
    for l in lieux:
        if l["id"] not in places:
            print(f"attention : {l['id']} hors des trois panneaux", file=sys.stderr)
    entete = ("# Carte des usines : produit par outils/carte-usines.py (ne pas modifier a la main).\n"
              "# Fond : Natural Earth, pays 1:50 m (domaine public) ; lieux : _data/usines-coordonnees.yml.\n")
    open("_data/carte_usines.yml", "w", encoding="utf-8").write(entete + yaml.safe_dump(sortie, allow_unicode=True, sort_keys=False, width=100000))
    print({p["id"]: (p["largeur"], p["hauteur"], len(p["points"]), len(p["fond"])) for p in sortie["panneaux"]})

main()
