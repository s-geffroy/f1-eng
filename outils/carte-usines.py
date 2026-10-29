#!/usr/bin/env python3
"""Cartes de la page « Cartes » : projette le fond (terres, frontières, fleuves, lacs, villes de repère,
quadrillage), les circuits et les lieux des sites dans des panneaux, et écrit _data/carte_usines.yml,
que lit _includes/carte-usines.html. Style « atlas » : les couleurs sont dans le CSS.

Usage : python3 outils/carte-usines.py <dossier Natural Earth>
Le dossier contient les couches Natural Earth au 1:10 m (domaine public), version 5.1.2, au format GeoJSON :
  ne_10m_land, ne_10m_admin_0_boundary_lines_land, ne_10m_rivers_lake_centerlines, ne_10m_lakes,
  ne_10m_populated_places_simple
  (https://raw.githubusercontent.com/nvkelso/natural-earth-vector/v5.1.2/geojson/<couche>.geojson)
Elles ne sont pas versionnées ici ; seuls les tracés projetés et simplifiés le sont (dans le fichier produit).
Lieux : _data/usines-coordonnees.yml ; circuits : _data/circuits.yml (facultatif). À relancer si l'un change."""
import json, math, os, sys
import yaml

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE)

# panneau : identifiant, lon min, lon max, lat min, lat max, largeur (px), pas du quadrillage (degrés),
# rang maximal des villes de repère (Natural Earth scalerank), rang maximal des fleuves
# Un lieu va dans le premier panneau qui le contient, dans cet ordre de priorité : les zooms d'abord.
PANNEAUX = [
    ("londres", -0.85, 0.25, 51.15, 51.78, 620, 0.25, 9, 12),
    ("italie-nord", 7.3, 12.6, 43.9, 45.95, 620, 1, 7, 12),
    ("los-angeles", -118.6, -117.35, 33.3, 34.3, 460, 0.25, 9, 12),
    ("angleterre", -2.35, 1.25, 50.55, 53.55, 620, 1, 7, 12),
    ("europe", -9.5, 20.5, 36.5, 55.5, 760, 5, 3, 7),
    ("amerique-nord", -124.0, -70.0, 18.5, 49.0, 720, 10, 2, 5),
    ("bresil", -58.0, -38.0, -30.0, -15.0, 360, 5, 3, 6),
    ("japon", 129.0, 145.0, 31.0, 41.0, 360, 5, 3, 6),
    ("afrique-sud", 16.0, 33.5, -35.0, -22.0, 360, 5, 3, 6),
    ("australie", 112.0, 155.0, -44.0, -10.0, 360, 10, 2, 5),
]
AFFICHAGE = ["europe", "angleterre", "londres", "italie-nord", "amerique-nord", "los-angeles", "bresil", "japon", "afrique-sud", "australie"]
TAILLE, CHASSE = 10.5, 0.56          # étiquettes des lieux : corps (px) et chasse moyenne d'un caractère
TAILLE_V, CHASSE_V = 8.5, 0.62       # villes et circuits, en petites capitales
TOLERANCE = 0.45                     # simplification des tracés (px)
# noms français des villes de repère, quand ils diffèrent
NOMS_FR = {"London": "Londres", "Turin": "Turin", "Munich": "Munich", "Cologne": "Cologne", "Brussels": "Bruxelles",
           "Vienna": "Vienne", "Venice": "Venise", "Florence": "Florence", "Genoa": "Gênes", "Naples": "Naples", "Rome": "Rome",
           "Lisbon": "Lisbonne", "Seville": "Séville", "Geneva": "Genève", "Basel": "Bâle", "Bologna": "Bologne",
           "Modena": "Modène", "Padua": "Padoue", "Verona": "Vérone", "Mantua": "Mantoue", "Copenhagen": "Copenhague",
           "Warsaw": "Varsovie", "The Hague": "La Haye", "Antwerp": "Anvers", "Edinburgh": "Édimbourg", "Dover": "Douvres",
           "Mexico City": "Mexico", "Sao Paulo": "São Paulo", "Cape Town": "Le Cap"}

def projeteur(lo0, lo1, la0, la1, largeur):
    kx = math.cos(math.radians((la0 + la1) / 2))
    echelle = largeur / ((lo1 - lo0) * kx)
    return (lambda lon, lat: ((lon - lo0) * kx * echelle, (la1 - lat) * echelle)), round((la1 - la0) * echelle)

def douglas_peucker(pts, tol):
    if len(pts) < 3:
        return pts
    garde, pile = [False] * len(pts), [(0, len(pts) - 1)]
    garde[0] = garde[-1] = True
    while pile:
        a, b = pile.pop()
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1e-9
        imax, dmax = None, tol
        for i in range(a + 1, b):
            d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / n
            if d > dmax:
                imax, dmax = i, d
        if imax is not None:
            garde[imax] = True
            pile += [(a, imax), (imax, b)]
    return [p for p, g in zip(pts, garde) if g]

def simplifier_anneau(pts, tol):
    """Douglas-Peucker sur un anneau fermé : on le coupe au point le plus éloigné du premier, et l'on simplifie
    chaque moitié (sur l'anneau entier, le segment de référence serait de longueur nulle)."""
    if len(pts) < 4:
        return pts
    k = max(range(len(pts)), key=lambda i: (pts[i][0] - pts[0][0]) ** 2 + (pts[i][1] - pts[0][1]) ** 2)
    a = douglas_peucker(pts[:k + 1], tol)
    b = douglas_peucker(pts[k:] + [pts[0]], tol)
    return a[:-1] + b[:-1]

def decouper_polygone(pts, x0, y0, x1, y1):
    """Sutherland-Hodgman contre le rectangle [x0,x1]×[y0,y1]."""
    def couper(pts, dedans, inter):
        out = []
        for i, p in enumerate(pts):
            q = pts[i - 1]
            if dedans(p):
                if not dedans(q):
                    out.append(inter(q, p))
                out.append(p)
            elif dedans(q):
                out.append(inter(q, p))
        return out
    def ix(xc):
        return lambda a, b: (xc, a[1] + (b[1] - a[1]) * (xc - a[0]) / ((b[0] - a[0]) or 1e-9))
    def iy(yc):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (yc - a[1]) / ((b[1] - a[1]) or 1e-9), yc)
    for dedans, inter in ((lambda p: p[0] >= x0, ix(x0)), (lambda p: p[0] <= x1, ix(x1)),
                          (lambda p: p[1] >= y0, iy(y0)), (lambda p: p[1] <= y1, iy(y1))):
        if not pts:
            break
        pts = couper(pts, dedans, inter)
    return pts

def decouper_ligne(pts, x0, y0, x1, y1):
    """Morceaux d'une ligne à l'intérieur du rectangle (le rectangle a une marge hors du dessin)."""
    morceaux, cur = [], []
    for p in pts:
        if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
            cur.append(p)
        else:
            if len(cur) >= 2:
                morceaux.append(cur)
            cur = []
    if len(cur) >= 2:
        morceaux.append(cur)
    return morceaux

def chemin(morceaux, ferme):
    return "".join("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in m) + ("Z" if ferme else "") for m in morceaux)

def geometries(f):
    g = f["geometry"]
    if g is None:
        return []
    t, c = g["type"], g["coordinates"]
    return {"Polygon": [c], "MultiPolygon": c, "LineString": [[c]], "MultiLineString": [[l] for l in c]}.get(t, [])

def couche(features, proj, bbox_geo, cadre, ferme, filtre=lambda f: True):
    lo0, lo1, la0, la1 = bbox_geo
    m = 1.0
    out = []
    for f in features:
        if not filtre(f):
            continue
        for poly in geometries(f):
            for anneau in poly:
                lons = [p[0] for p in anneau]; lats = [p[1] for p in anneau]
                if max(lons) < lo0 - m or min(lons) > lo1 + m or max(lats) < la0 - m or min(lats) > la1 + m:
                    continue
                pts = [proj(p[0], p[1]) for p in anneau]
                if ferme:
                    pts = decouper_polygone(pts, *cadre)
                    pts = simplifier_anneau(pts, TOLERANCE) if len(pts) >= 3 else []
                    if len(pts) >= 3:
                        out.append(pts)
                else:
                    for morceau in decouper_ligne(pts, *cadre):
                        morceau = douglas_peucker(morceau, TOLERANCE)
                        if len(morceau) >= 2:
                            out.append(morceau)
    return chemin(out, ferme)

def graticule(proj, lo0, lo1, la0, la1, pas):
    morceaux = []
    lon = math.ceil(lo0 / pas) * pas
    while lon <= lo1 + 1e-9:
        morceaux.append([proj(lon, la0), proj(lon, la1)]); lon += pas
    lat = math.ceil(la0 / pas) * pas
    while lat <= la1 + 1e-9:
        morceaux.append([proj(lo0, lat), proj(lo1, lat)]); lat += pas
    return chemin(morceaux, False)

class Placeur:
    """Étiquettes sans chevauchement : huit directions, plusieurs distances ; au-delà de la première, un trait de rappel."""
    DIRS = [(1, 0, "start"), (-1, 0, "end"), (0, -1, "middle"), (0, 1, "middle"),
            (1, -1, "start"), (1, 1, "start"), (-1, -1, "end"), (-1, 1, "end")]
    def __init__(self, largeur, hauteur, points):
        self.l, self.h = largeur, hauteur
        self.pris = [(x - 5, y - 5, 10, 10) for x, y in points]
    def libre(self, r):
        return (0 <= r[0] and r[0] + r[2] <= self.l and 0 <= r[1] and r[1] + r[3] <= self.h and
                all(r[0] + r[2] <= q[0] or q[0] + q[2] <= r[0] or r[1] + r[3] <= q[1] or q[1] + q[3] <= r[1] for q in self.pris))
    def placer(self, x, y, texte, taille, chasse, rayons=(8, 20, 34), obligatoire=True):
        w, h = len(texte) * taille * chasse, taille
        for rayon in rayons:
            for ux, uy, ancre in self.DIRS:
                ax, ay = x + ux * rayon, y + uy * rayon * 0.8
                x0 = ax if ancre == "start" else ax - w if ancre == "end" else ax - w / 2
                y0 = ay - h / 2 if uy == 0 else (ay - h if uy < 0 else ay)
                r = (x0, y0, w, h)
                if self.libre(r):
                    self.pris.append(r)
                    d = {"ancre": ancre, "dx": round(ax - x, 1), "dy": round(y0 + h * 0.82 - y, 1)}
                    if rayon > rayons[0]:
                        d["trait"] = [round(ax - x, 1), round(ay - y, 1)]
                    return d
        if not obligatoire:
            return None
        r = (x + 8, y - h / 2, w, h); self.pris.append(r)
        return {"ancre": "start", "dx": 8, "dy": round(h * 0.32, 1)}

def charger(dossier, nom):
    return json.load(open(os.path.join(dossier, nom + ".geojson"), encoding="utf-8"))["features"]

def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        sys.exit(__doc__)
    ne = sys.argv[1]
    terres, frontieres = charger(ne, "ne_10m_land"), charger(ne, "ne_10m_admin_0_boundary_lines_land")
    fleuves, lacs, villes = charger(ne, "ne_10m_rivers_lake_centerlines"), charger(ne, "ne_10m_lakes"), charger(ne, "ne_10m_populated_places_simple")
    lieux = yaml.safe_load(open("_data/usines-coordonnees.yml", encoding="utf-8"))
    circuits = yaml.safe_load(open("_data/circuits.yml", encoding="utf-8")) if os.path.exists("_data/circuits.yml") else []
    def panneau_de(lon, lat):
        return next((p[0] for p in PANNEAUX if p[1] <= lon <= p[2] and p[3] <= lat <= p[4]), None)
    place = {l["id"]: panneau_de(l["lon"], l["lat"]) for l in lieux}
    for l in lieux:
        if place[l["id"]] is None:
            print(f"attention : {l['id']} hors de tous les panneaux", file=sys.stderr)
    sortie = {"panneaux": []}
    for pid, lo0, lo1, la0, la1, largeur, pas, rang_v, rang_f in sorted(PANNEAUX, key=lambda p: AFFICHAGE.index(p[0])):
        if pid not in place.values():
            continue
        proj, hauteur = projeteur(lo0, lo1, la0, la1, largeur)
        cadre = (-15, -15, largeur + 15, hauteur + 15)
        bbox = (lo0, lo1, la0, la1)
        pan = {"id": pid, "largeur": largeur, "hauteur": hauteur,
               "graticule": graticule(proj, lo0, lo1, la0, la1, pas),
               "terre": couche(terres, proj, bbox, cadre, True),
               "lacs": couche(lacs, proj, bbox, cadre, True, lambda f: (f["properties"].get("scalerank") or 0) <= rang_f),
               "fleuves": couche(fleuves, proj, bbox, cadre, False,
                                 lambda f: (f["properties"].get("scalerank") or 0) <= rang_f and f["properties"].get("featurecla") != "Lake Centerline"),
               "frontieres": couche(frontieres, proj, bbox, cadre, False)}
        # 1. lieux des sites : prioritaires
        pts = [(l, *proj(l["lon"], l["lat"])) for l in lieux if place[l["id"]] == pid]
        circ = [(c, *proj(c["lon"], c["lat"])) for c in circuits if panneau_de(c["lon"], c["lat"]) == pid]
        placeur = Placeur(largeur, hauteur, [(x, y) for _, x, y in pts] + [(x, y) for _, x, y in circ])
        pan["points"] = []
        for l, x, y in sorted(pts, key=lambda t: (t[1], t[2])):
            p = {"lieu": l["id"], "x": round(x, 1), "y": round(y, 1)}
            p.update(placeur.placer(x, y, l["nom"], TAILLE, CHASSE))
            pan["points"].append(p)
        # 2. circuits : étiquette si la place le permet
        pan["circuits"] = []
        for c, x, y in sorted(circ, key=lambda t: (t[1], t[2])):
            p = {"circuit": c["id"], "x": round(x, 1), "y": round(y, 1)}
            e = placeur.placer(x, y, max(c["etiquette"], c["etiquette_en"], key=len).upper(), TAILLE_V, CHASSE_V, rayons=(7, 16), obligatoire=False)
            if e:
                p.update(e)
            pan["circuits"].append(p)
        # 3. villes de repère : seulement si leur point et leur nom tiennent sans rien gêner
        pan["villes"] = []
        candidats = sorted((v for v in villes if v["properties"]["scalerank"] <= rang_v
                            and lo0 <= v["geometry"]["coordinates"][0] <= lo1 and la0 <= v["geometry"]["coordinates"][1] <= la1),
                           key=lambda v: (v["properties"]["scalerank"], -(v["properties"].get("pop_max") or 0)))
        for v in candidats:
            x, y = proj(*v["geometry"]["coordinates"][:2])
            if not placeur.libre((x - 3, y - 3, 6, 6)) or any(abs(x - q["x"]) < 12 and abs(y - q["y"]) < 12 for q in pan["points"]):
                continue
            nom_en = v["properties"]["name"]; nom_fr = NOMS_FR.get(nom_en, nom_en)
            e = placeur.placer(x, y, max(nom_fr, nom_en, key=len).upper(), TAILLE_V, CHASSE_V, rayons=(5,), obligatoire=False)
            if e:
                placeur.pris.append((x - 3, y - 3, 6, 6))
                pan["villes"].append({"nom": nom_fr, "nom_en": nom_en, "x": round(x, 1), "y": round(y, 1), **e})
        # cadres des zooms contenus dans ce panneau (un zoom inclus dans un autre zoom n'a pas son propre cadre)
        pan["cadres"] = []
        for zid, a0, a1, b0, b1, *_ in PANNEAUX:
            if zid != pid and zid in place.values() and lo0 <= a0 and a1 <= lo1 and la0 <= b0 and b1 <= la1:
                x0, y0 = proj(a0, b1); x1, y1 = proj(a1, b0)
                pan["cadres"].append({"zoom": zid, "x": round(x0, 1), "y": round(y0, 1), "l": round(x1 - x0, 1), "h": round(y1 - y0, 1)})
        pan["cadres"] = [c for c in pan["cadres"] if not any(
            o is not c and o["x"] <= c["x"] and o["y"] <= c["y"] and c["x"] + c["l"] <= o["x"] + o["l"] and c["y"] + c["h"] <= o["y"] + o["h"]
            for o in pan["cadres"])]
        sortie["panneaux"].append(pan)
    entete = ("# Cartes : produit par outils/carte-usines.py (ne pas modifier a la main).\n"
              "# Fond : Natural Earth 1:10 m (domaine public) ; lieux : _data/usines-coordonnees.yml ; circuits : _data/circuits.yml.\n")
    open("_data/carte_usines.yml", "w", encoding="utf-8").write(entete + yaml.safe_dump(sortie, allow_unicode=True, sort_keys=False, width=100000))
    taille = os.path.getsize("_data/carte_usines.yml") // 1024
    print({p["id"]: (len(p["points"]), len(p["circuits"]), len(p["villes"])) for p in sortie["panneaux"]}, f"{taille} Ko")

main()
