#!/usr/bin/env python3
"""Domination : périodes de domination des écuries, lignées, pilotes et motoristes, et leur
confrontation aux jalons de la chronologie, aux arrivées et départs d'ingénieurs et aux changements
de règlement. Lit _data/resultats.yml, _data/ecuries.yml, _data/chronologie.yml ; écrit
_data/domination.yml (chiffres communs aux deux langues, page /dossiers/domination/).
Usage : python3 outils/domination.py   (à relancer après outils/releve-resultats.py)

Une saison est « dominante » pour une entité si elle y est championne ou gagne au moins SEUIL des
Grands Prix. Les saisons dominantes d'une entité, séparées au plus par CREUX saison non dominante,
forment une période, classée en trois degrés :
  - saison : une seule saison dominante ;
  - domination : au moins DUO saisons dominantes ;
  - hegemonie : au moins MIN saisons dominantes, et robuste.
Les mêmes calculs sont refaits avec des seuils plus stricts (VARIANTES) : une période d'au moins MIN
saisons retrouvée dans toutes les variantes est dite robuste. Seules des variantes plus strictes
peuvent la rejeter (une variante plus lâche retrouve toujours tout) : la robustesse repose donc sur
deux épreuves, seuil à 50 % et aucune saison creuse. Les confrontations portent sur les périodes
d'au moins MIN saisons dominantes, robustes ou non (« longues »)."""
import os, sys, collections
import yaml

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE)
SEUIL, MIN, CREUX = 0.40, 3, 1
DUO = 2                      # seuil du degré « domination »
VARIANTES = [(0.50, 3, 1), (0.40, 3, 0)]
AVANT, APRES = 2, 3          # fenêtres des confrontations (saisons)
FENETRE_JALON = 2            # une domination longue « suit » un jalon si elle commence de Y à Y+2
FENETRE_REGLE = 1            # règlement dans l'année qui précède ou de l'année même
# Règlements d'autres catégories (Formule 2, Formule 3) : présents dans la chronologie pour leurs
# liens, mais ce ne sont pas des changements du règlement de la F1.
HORS_F1 = {"formule-500", "formule-2-1957", "formule-2-1600"}
# Même groupe propulseur sous trois noms : Honda le construit de 2021 à 2025, badgé RBPT à partir de 2022.
MEME_MOTEUR = {"rbpt": "honda", "honda-rbpt": "honda"}

R = yaml.safe_load(open("_data/resultats.yml", encoding="utf-8"))["saisons"]
E = yaml.safe_load(open("_data/ecuries.yml", encoding="utf-8"))
C = yaml.safe_load(open("_data/chronologie.yml", encoding="utf-8"))
ANNEES = [s["annee"] for s in R]
SAISONS = {s["annee"]: s for s in E["saisons"]}
NOM_ECURIE = {e["id"]: e["nom"] for e in E["ecuries"]}
NOM_MOTEUR = {m["id"]: m["nom"] for m in E["motoristes"]}
NOM_LIGNEE = {l["id"]: l["nom"] for l in E["lignees"]}

def lignee(ecurie, annee):
    for l in E["lignees"]:
        for s in l["segments"]:
            if s["ecurie"] == ecurie and s["de"] <= annee <= s["a"]:
                return l["id"]
    return None

def moteur(m):
    return MEME_MOTEUR.get(m, m)

def cle_ecurie(course):
    # Un gagnant sans fiche garde son nom (Mercedes-Benz 1954-1955, Watson à Indianapolis).
    return course.get("ecurie") or "~" + course["equipe"]

# --- Indicateurs par saison --------------------------------------------------------------------
# part[unite][annee][entite] = part des victoires ; champion[unite][annee] = entité championne
part = {u: {} for u in ("ecurie", "lignee", "pilote", "motoriste")}
victoires = {u: {} for u in part}
points = {u: {} for u in part}
champion = {u: {} for u in part}
for s in R:
    a, n = s["annee"], s["gp"]
    v = {u: collections.Counter() for u in part}
    for c in s["courses"]:
        ec = cle_ecurie(c)
        v["ecurie"][ec] += 1
        v["lignee"][lignee(c["ecurie"], a) if c.get("ecurie") else ec] += 1
        for pi in (c["vainqueur"], c.get("covainqueur")):
            if pi: v["pilote"][pi] += 1     # victoire partagée : comptée aux deux pilotes
        if c.get("motoriste"):
            v["motoriste"][moteur(c["motoriste"])] += 1
    for u in part:
        victoires[u][a] = dict(v[u])
        part[u][a] = {k: x / n for k, x in v[u].items()}
    sa = SAISONS[a]
    champion["pilote"][a] = sa.get("pilote")
    if sa.get("constructeurs"):
        champion["ecurie"][a] = sa["constructeurs"]
        champion["motoriste"][a] = moteur(s["constructeurs"][0].get("motoriste"))
    else:
        # Avant 1958, pas de titre constructeurs : l'écurie du champion du monde en tient lieu.
        champion["ecurie"][a] = sa.get("pilote_ecurie") or "~" + sa.get("pilote_equipe", "")
        ch = next(c for c in s["courses"] if cle_ecurie(c) == champion["ecurie"][a])
        champion["motoriste"][a] = moteur(ch.get("motoriste"))
    ce = champion["ecurie"][a]
    champion["lignee"][a] = lignee(ce, a) if not ce.startswith("~") else ce
    tot = sum(p["points"] for p in s["pilotes"])
    points["pilote"][a] = {p["pilote"]: p["points"] / tot for p in s["pilotes"]}
    if s.get("constructeurs"):
        tc = sum(c["points"] for c in s["constructeurs"])
        # Un constructeur classé sous plusieurs noms (Cooper Climax et Cooper Maserati) : points additionnés.
        pe = collections.Counter()
        for c in s["constructeurs"]:
            if c.get("ecurie"): pe[c["ecurie"]] += c["points"] / tc
        points["ecurie"][a] = dict(pe)

# --- Mesures complémentaires : poles, podiums, doublés, écart au deuxième -------------------------
# Elles décrivent une domination, elles ne la définissent pas : les degrés restent fondés sur les
# titres et les victoires. Une course sans grille ou sans podium publié sort du dénominateur.
def cles(c, a):
    """Entités créditées d'une place (vainqueur, podium, pole) : {unité: clé}."""
    ec = cle_ecurie(c)
    return {"ecurie": ec, "lignee": lignee(c["ecurie"], a) if c.get("ecurie") else ec,
            "pilote": c.get("vainqueur") or c.get("pilote"), "motoriste": moteur(c.get("motoriste"))}

poles = {u: {} for u in part}
podiums = {u: {} for u in part}
doubles = {u: {} for u in part}
gp_pole, gp_podium = {}, {}
for s in R:
    a = s["annee"]
    po, pd, db = ({u: collections.Counter() for u in part} for _ in range(3))
    gp_pole[a] = gp_podium[a] = 0
    for c in s["courses"]:
        if c.get("pole"):
            gp_pole[a] += 1
            for u, k in cles(c["pole"], a).items():
                if k: po[u][k] += 1
        if len(c.get("podium", [])) == 2:
            gp_podium[a] += 1
            places = [cles(c, a)] + [cles(p, a) for p in c["podium"]]
            for u in part:
                for pl in places:
                    if pl[u]: pd[u][pl[u]] += 1
                # Doublé : les deux premières places pour la même entité (sans objet pour un pilote).
                if u != "pilote" and places[0][u] and places[0][u] == places[1][u]:
                    db[u][places[0][u]] += 1
    for u in part:
        poles[u][a], podiums[u][a], doubles[u][a] = dict(po[u]), dict(pd[u]), dict(db[u])

def ecart_points(u, k, a):
    """Part des points de l'entité moins celle du meilleur des autres (négatif si battue)."""
    pts = points[u].get(a)
    if not pts or k not in pts:
        return None
    return pts[k] - max([v for x, v in pts.items() if x != k] or [0])

def mesures(u, k, annees):
    """Parts des poles, des places sur le podium et des doublés, écart au deuxième, indice composite."""
    n_po = sum(gp_pole[a] for a in annees)
    n_pd = sum(gp_podium[a] for a in annees)
    vic = sum(victoires[u][a].get(k, 0) for a in annees)
    gp = sum(next(s["gp"] for s in R if s["annee"] == a) for a in annees)
    m = {}
    if n_po:
        m["poles"] = round(sum(poles[u][a].get(k, 0) for a in annees) / n_po, 3)
    if n_pd:
        m["podiums"] = round(sum(podiums[u][a].get(k, 0) for a in annees) / (3 * n_pd), 3)
        if u != "pilote":
            m["doubles"] = round(sum(doubles[u][a].get(k, 0) for a in annees) / n_pd, 3)
    ec = [ecart_points(u, k, a) for a in annees]
    if ec and all(x is not None for x in ec):
        m["ecart"] = moyenne(ec)
    if "poles" in m and "podiums" in m:
        # Indice composite : moyenne simple des parts de victoires, de poles et de places sur le podium.
        m["indice"] = round((vic / gp + m["poles"] + m["podiums"]) / 3, 3)
    return m

def nom(u, k):
    if k.startswith("~"):
        return k[1:]
    return {"ecurie": NOM_ECURIE, "motoriste": NOM_MOTEUR, "lignee": NOM_LIGNEE}.get(u, {}).get(k, k)

# --- Détection ---------------------------------------------------------------------------------
def dominantes(u, k, seuil):
    return [a for a in ANNEES if champion[u].get(a) == k or part[u][a].get(k, 0) >= seuil]

def detecter(u, seuil, mini, creux):
    entites = {k for a in ANNEES for k in part[u][a]} | {champion[u][a] for a in ANNEES if champion[u].get(a)}
    out = []
    for k in entites:
        groupe = []
        for a in dominantes(u, k, seuil):
            if groupe and a - groupe[-1] > creux + 1:
                if len(groupe) >= mini: out.append((k, groupe))
                groupe = []
            groupe.append(a)
        if len(groupe) >= mini: out.append((k, groupe))
    return out

def recouvre(k, g, autres):
    return any(k == k2 and g[0] <= g2[-1] and g2[0] <= g[-1] for k2, g2 in autres)

ING_ECURIE = [(e["id"], i["id"], i.get("de"), i.get("a")) for e in E["ecuries"] for i in e.get("ingenieurs", [])]
JALONS = {j["id"]: j for j in C["jalons"]}
JALON_ECURIES = collections.defaultdict(list)
for e in E["ecuries"]:
    for j in e.get("jalons", []):
        JALON_ECURIES[j].append(e["id"])
REGLES = [x for x in C["contexte"] if x["categorie"] == "reglement" and x["id"] not in HORS_F1]

def regles_autour(annee):
    return [x["id"] for x in REGLES if annee - FENETRE_REGLE <= x["annee"] <= annee]

def moyenne(xs):
    return round(sum(xs) / len(xs), 3) if xs else None

def part_ecurie(ec, de, a):
    return moyenne([part["ecurie"][y].get(ec, 0) for y in range(de, a + 1) if y in part["ecurie"]])

def actives(ec):
    """Saisons disputées par une écurie (segments des lignées), bornées aux résultats relevés."""
    return sorted({y for l in E["lignees"] for s in l["segments"] if s["ecurie"] == ec
                   for y in range(s["de"], s["a"] + 1) if y in part["ecurie"]})

def degre(g, robuste):
    return "hegemonie" if len(g) >= MIN and robuste else "domination" if len(g) >= DUO else "saison"

dominations, saisons_dom, effectifs, liste_ecurie = {}, {}, {}, []
for u in part:
    base = detecter(u, SEUIL, 1, CREUX)
    variantes = [detecter(u, *v) for v in VARIANTES]
    hs = []
    # Saisons dominantes isolées : décrites brièvement, sans confrontation.
    saisons_dom[u] = [{"nom": nom(u, k), "annee": g[0], "titre": champion[u].get(g[0]) == k,
                       "part": round(part[u][g[0]].get(k, 0), 3), **({"id": k} if not k.startswith("~") else {}),
                       **mesures(u, k, [g[0]])}
                      for k, g in sorted(base, key=lambda x: (x[1][0], x[0])) if len(g) < DUO]
    for k, g in sorted(base, key=lambda x: (x[1][0], x[0])):
        if len(g) < DUO:
            continue
        debut, fin = g[0], g[-1]
        span = range(debut, fin + 1)
        vic = sum(victoires[u][a].get(k, 0) for a in span)
        gp = sum(next(s["gp"] for s in R if s["annee"] == a) for a in span)
        h = {"unite": u, "id": k.lstrip("~") if not k.startswith("~") else None, "nom": nom(u, k),
             "debut": debut, "fin": fin, "saisons": fin - debut + 1, "dominantes": len(g),
             "titres": sum(1 for a in span if champion[u].get(a) == k),
             "victoires": vic, "gp": gp, "part": round(vic / gp, 3),
             "part_max": round(max(part[u][a].get(k, 0) for a in span), 3),
             "longue": len(g) >= MIN,
             "robuste": len(g) >= MIN and all(recouvre(k, g, v) for v in variantes)}
        h["degre"] = degre(g, h["robuste"])
        if h["id"] is None: del h["id"]
        h.update(mesures(u, k, list(span)))
        if u in points and points[u]:
            pts = [points[u][a].get(k) for a in span if a in points[u]]
            if pts and all(p is not None for p in pts):
                h["points"] = moyenne(pts)
        # Associés : motoristes d'une écurie, écuries d'un pilote ou d'un motoriste.
        asso = collections.Counter()
        for a in span:
            for c in next(s for s in R if s["annee"] == a)["courses"]:
                cle = {"ecurie": cle_ecurie(c), "pilote": c["vainqueur"], "motoriste": moteur(c.get("motoriste")),
                       "lignee": lignee(c["ecurie"], a) if c.get("ecurie") else cle_ecurie(c)}[u]
                if cle == k or u == "pilote" and c.get("covainqueur") == k:
                    autre = moteur(c.get("motoriste")) if u in ("ecurie", "lignee") else cle_ecurie(c)
                    if autre: asso[autre] += 1
        h["associes"] = [x for x, _ in asso.most_common()]
        h["regles_debut"] = regles_autour(debut)
        h["regles_fin"] = [x["id"] for x in REGLES if fin <= x["annee"] <= fin + FENETRE_REGLE]
        if u == "ecurie" and not k.startswith("~") and h["longue"]:
            # Présents dans les trois saisons qui précèdent le début : arrivés avant, partis après.
            # Sans date de départ connue, la présence n'est sûre que pour une arrivée récente.
            h["ingenieurs"] = sorted({i for ec, i, de, a in ING_ECURIE if ec == k and de and de <= debut
                                      and (a is not None and a >= debut - 3 or a is None and de >= debut - 3)})
            h["ingenieurs_incertains"] = sorted({i for ec, i, de, a in ING_ECURIE if ec == k and de
                                                 and a is None and de < debut - 3} - set(h["ingenieurs"]))
            h["jalons"] = [j for j in JALON_ECURIES if k in JALON_ECURIES[j]
                           and debut - 3 <= JALONS[j]["annee"] <= fin]
            liste_ecurie.append((k, debut, fin))
        hs.append(h)
    # Rangée de la frise de l'accueil : la première dont la dernière période finit avant le début.
    fins = []
    for h in hs:
        r = next((i for i, f in enumerate(fins) if f < h["debut"]), len(fins))
        fins[r:r + 1] = [h["fin"]]
        h["rangee"] = r
    dominations[u] = hs
    effectifs[u] = {"saison": len(saisons_dom[u]), "domination": sum(h["degre"] == "domination" for h in hs),
                    "hegemonie": sum(h["degre"] == "hegemonie" for h in hs), "longue": sum(h["longue"] for h in hs)}

# Saisons les plus écrasantes : pour chaque saison, l'écurie et le pilote d'indice composite le plus
# élevé ; on garde les dix premiers (le classement ne dépend pas des degrés).
ecrasantes = {}
for u in ("ecurie", "pilote"):
    meilleures = []
    for a in ANNEES:
        cands = [(mesures(u, k, [a]), k) for k in part[u][a]]
        cands = [(m, k) for m, k in cands if "indice" in m]
        if cands:
            m, k = max(cands, key=lambda x: x[0]["indice"])
            meilleures.append({"annee": a, "nom": nom(u, k), **({"id": k} if not k.startswith("~") else {}),
                               "victoires": round(part[u][a][k], 3), **m})
    ecrasantes[u] = sorted(meilleures, key=lambda x: -x["indice"])[:10]

def debut_suit(ec, y):
    return any(e == ec and y <= d <= y + FENETRE_JALON for e, d, f in liste_ecurie)

def pendant(ec, y):
    return any(e == ec and d < y <= f for e, d, f in liste_ecurie)

# --- Confrontation 1 : jalons ------------------------------------------------------------------
# Deux jalons d'une même écurie la même année (Benetton 1993, McLaren 2009) ne font qu'un cas dans
# les études : la même saison serait sinon comptée deux fois.
jalons, obs, attendu, vus = [], [], [], set()
for jid, ecs in sorted(JALON_ECURIES.items(), key=lambda x: (JALONS[x[0]]["annee"], x[0])):
    j = JALONS[jid]
    y = j["annee"]
    for ec in ecs:
        statut = "pendant" if pendant(ec, y) else "ouvre" if debut_suit(ec, y) else "sans"
        jalons.append({"jalon": jid, "annee": y, "ecurie": ec, "avant": part_ecurie(ec, y - AVANT, y - 1),
                       "apres": part_ecurie(ec, y, y + APRES - 1), "statut": statut})
        if statut != "pendant" and (ec, y) not in vus:
            vus.add((ec, y))
            obs.append(statut == "ouvre")
            # Témoin : même écurie, n'importe quelle saison disputée hors domination longue.
            libres = [a for a in actives(ec) if not pendant(ec, a)]
            attendu.append(sum(debut_suit(ec, a) for a in libres) / len(libres))
jalons.sort(key=lambda x: (x["annee"], x["jalon"], x["ecurie"]))
sans_ecurie = sorted((j["id"] for j in C["jalons"] if j["id"] not in JALON_ECURIES), key=lambda i: JALONS[i]["annee"])

# --- Confrontation 2 : ingénieurs --------------------------------------------------------------
mouvements = []
for ec, ing, de, a in ING_ECURIE:
    act = actives(ec)
    if not act or de is None:
        continue
    # Fenêtres complètes seulement : une arrivée de 2025 n'a pas encore trois saisons de recul.
    if de > act[0] and de + APRES - 1 <= ANNEES[-1]:
        mouvements.append({"ingenieur": ing, "ecurie": ec, "type": "arrivee", "annee": de,
                           "avant": part_ecurie(ec, de - AVANT, de - 1), "apres": part_ecurie(ec, de, de + APRES - 1)})
    if a and a < act[-1] and a + APRES <= ANNEES[-1]:
        mouvements.append({"ingenieur": ing, "ecurie": ec, "type": "depart", "annee": a,
                           "avant": part_ecurie(ec, a - AVANT + 1, a), "apres": part_ecurie(ec, a + 1, a + APRES)})
mouvements.sort(key=lambda x: (x["annee"], x["ingenieur"], x["type"]))

def bilan(ms):
    d = [m["apres"] - m["avant"] for m in ms if m["avant"] is not None and m["apres"] is not None]
    return {"n": len(d), "hausse": sum(x > 0.05 for x in d), "baisse": sum(x < -0.05 for x in d),
            "stable": sum(abs(x) <= 0.05 for x in d), "ecart_moyen": moyenne(d)}

# Témoin : écart entre les mêmes fenêtres prises à n'importe quelle saison, pour les mêmes écuries.
temoin_ing = []
for ec in {m["ecurie"] for m in mouvements}:
    for y in actives(ec)[AVANT:]:
        av, ap = part_ecurie(ec, y - AVANT, y - 1), part_ecurie(ec, y, y + APRES - 1)
        temoin_ing.append(ap - av)

# --- Approfondissements ------------------------------------------------------------------------
# Profil des victoires autour des jalons (étude d'événement) : saisons Y-3 à Y+5, et le même
# profil pour la même écurie à une saison quelconque (témoin), pondéré comme les jalons.
K = list(range(-3, 6))

def profil(ec, y):
    act = set(actives(ec))
    return [part["ecurie"][y + k].get(ec, 0) if y + k in act else None for k in K]

def moyenne_profils(ps):
    return [moyenne([p[i] for p in ps if p[i] is not None]) for i in range(len(K))]

uniques = list({(j["ecurie"], j["annee"]): j for j in reversed(jalons)}.values())[::-1]
profils_j = [profil(j["ecurie"], j["annee"]) for j in uniques]
profils_t = []
for j in uniques:
    annees_j = {x["annee"] for x in jalons if x["ecurie"] == j["ecurie"]}
    ps = [profil(j["ecurie"], y) for y in actives(j["ecurie"]) if y not in annees_j]
    profils_t.append(moyenne_profils(ps) if ps else [None] * len(K))
etude = {"k": K, "jalons": moyenne_profils(profils_j), "temoin": moyenne_profils(profils_t),
         "n": len(uniques),
         "series": [{"jalon": j["jalon"], "ecurie": j["ecurie"], "annee": j["annee"], "valeurs": p}
                    for j, p in zip(uniques, profils_j)]}

def gain(ec, y):
    av, ap = part_ecurie(ec, y - AVANT, y - 1), part_ecurie(ec, y, y + APRES - 1)
    return None if av is None or ap is None else ap - av

gains_j = [gain(j["ecurie"], j["annee"]) for j in uniques]
gains_t = []
for j in uniques:
    annees_j = {x["annee"] for x in jalons if x["ecurie"] == j["ecurie"]}
    g = [gain(j["ecurie"], y) for y in actives(j["ecurie"])[AVANT:] if y not in annees_j]
    gains_t.append(moyenne([x for x in g if x is not None]))
etude["gain"] = moyenne([g for g in gains_j if g is not None])
etude["gain_temoin"] = moyenne([g for g in gains_t if g is not None])
etude["hausses"] = sum(g > 0.05 for g in gains_j if g is not None)

# Probabilité exacte d'au moins autant de dominations longues par le seul hasard (loi de Poisson binomiale,
# chaque jalon avec la probabilité de son écurie une saison quelconque).
dist = [1.0]
for p in attendu:
    dist = [a * (1 - p) + b * p for a, b in zip(dist + [0], [0] + dist)]
p_hasard = sum(dist[sum(obs):])

# Par voie de la chronologie.
voies = []
for v in C["voies"]:
    gs = [gain(j["ecurie"], j["annee"]) for j in jalons if JALONS[j["jalon"]]["voie"] == v["id"]]
    gs = [g for g in gs if g is not None]
    voies.append({"voie": v["id"], "n": len(gs), "gain": moyenne(gs), "hausses": sum(g > 0.05 for g in gs),
                  "ouvre": sum(1 for j in jalons if JALONS[j["jalon"]]["voie"] == v["id"] and j["statut"] == "ouvre")})

# Chaînes sourcées de la chronologie : un événement de contexte relié à un jalon porté par une écurie.
chaines = []
for x in C["contexte"]:
    for l in x.get("liens", []):
        jid = l.get("jalon")
        if not jid or l["mecanisme"] == "provoque":
            continue
        for ec in JALON_ECURIES.get(jid, []):
            if l["mecanisme"] == "ferme":
                # L'innovation disparaît : l'écurie qui la portait recule-t-elle ? (au plus tôt la saison
                # qui suit le jalon : un événement antérieur ne la ferme qu'ensuite)
                y = max(x["annee"], JALONS[jid]["annee"] + 1)
                if y not in actives(ec):
                    continue            # écurie disparue entre-temps : rien à mesurer
            elif x["annee"] > JALONS[jid]["annee"]:
                continue                # une cause ne peut suivre son effet
            else:
                y = JALONS[jid]["annee"]
            av, ap = part_ecurie(ec, y - AVANT, y - 1), part_ecurie(ec, y, y + APRES - 1)
            chaines.append({"evenement": x["id"], "categorie": x["categorie"], "annee_evenement": x["annee"],
                            "mecanisme": l["mecanisme"], "preuve": l["preuve"], "jalon": jid, "ecurie": ec,
                            "annee": y, "avant": av, "apres": ap,
                            "statut": "pendant" if pendant(ec, y) else "ouvre" if debut_suit(ec, y) else "sans"})
chaines.sort(key=lambda c: (c["mecanisme"] == "ferme", c["annee"], c["jalon"]))

# Ingénieurs : témoin apparié sur le niveau de départ (une écurie qui ne gagne rien ne peut que
# monter : c'est la régression vers la moyenne), et distinction des tiers du classement.
def tranche(x):
    return 0 if x == 0 else 1 if x <= 0.10 else 2 if x <= 0.30 else 3
temoin_tr = collections.defaultdict(list)
for ec in {e for l in E["lignees"] for s in l["segments"] for e in [s["ecurie"]]}:
    for y in actives(ec)[AVANT:]:
        av, ap = part_ecurie(ec, y - AVANT, y - 1), part_ecurie(ec, y, y + APRES - 1)
        temoin_tr[tranche(av)].append(ap - av)
TIERS = {}
for chemin in os.listdir("_ingenieurs"):
    fm = yaml.safe_load(open(f"_ingenieurs/{chemin}", encoding="utf-8").read().split("---\n")[1])
    TIERS[chemin[:-3]] = fm.get("tier") or "HC"

def poisson_binomiale(ps, k):
    """Probabilité d'au moins k succès quand chaque cas réussit avec sa propre probabilité."""
    d = [1.0]
    for p in ps:
        d = [a * (1 - p) + b * p for a, b in zip(d + [0], [0] + d)]
    return sum(d[k:])

def apparie(ms):
    d = [(m["apres"] - m["avant"], tranche(m["avant"])) for m in ms if m["avant"] is not None and m["apres"] is not None]
    ps = [sum(x > 0.05 for x in temoin_tr[t]) / len(temoin_tr[t]) for _, t in d]
    attendu_h = sum(ps)
    attendu_g = sum(sum(temoin_tr[t]) / len(temoin_tr[t]) for _, t in d)
    return {"n": len(d), "hausse": sum(x > 0.05 for x, _ in d), "hausse_attendue": round(attendu_h, 1),
            "gain": moyenne([x for x, _ in d]), "gain_attendu": round(attendu_g / len(d), 3) if d else None,
            "p": round(poisson_binomiale(ps, sum(x > 0.05 for x, _ in d)), 4)}

arrivees = [m for m in mouvements if m["type"] == "arrivee"]
groupes_ing = [
    {"groupe": "toutes", **apparie(arrivees)},
    {"groupe": "tier-a", **apparie([m for m in arrivees if TIERS.get(m["ingenieur"]) == "A"])},
    {"groupe": "tiers-b-c-d", **apparie([m for m in arrivees if TIERS.get(m["ingenieur"]) in ("B", "C", "D")])},
    {"groupe": "hc", **apparie([m for m in arrivees if TIERS.get(m["ingenieur"]) == "HC"])},
    {"groupe": "departs", **apparie([m for m in mouvements if m["type"] == "depart"])},
]

# Règlements : rebattent-ils les cartes ? Changement d'écurie en tête des victoires d'une saison à
# l'autre, selon qu'un changement de règlement de la chronologie s'applique cette saison-là.
def tete(a):
    return max(part["ecurie"][a], key=part["ecurie"][a].get)
regle_annee = {x["annee"] for x in REGLES}
chg = {"avec": [0, 0], "sans": [0, 0]}
for a in ANNEES[1:]:
    g = "avec" if a in regle_annee else "sans"
    chg[g][0] += tete(a) != tete(a - 1)
    chg[g][1] += 1
rebat = {g: {"changements": v[0], "saisons": v[1]} for g, v in chg.items()}
# Test exact de Fisher (unilatéral) : autant de changements de tête par le seul hasard ?
from math import comb
na, ka, ns, ks = chg["avec"][1], chg["avec"][0], chg["sans"][1], chg["sans"][0]
rebat["p"] = round(sum(comb(ka + ks, i) * comb(na + ns - ka - ks, na - i) for i in range(ka, min(na, ka + ks) + 1))
                   / comb(na + ns, na), 4)

# Jalons en amont : ceux qu'un événement de contexte « ouvre », « contourne » ou « transfère »,
# d'après les liens sourcés de la chronologie.
amont = {c["jalon"] for c in chaines if c["mecanisme"] != "ferme"}
amont_regle = {c["jalon"] for c in chaines if c["mecanisme"] != "ferme" and c["categorie"] == "reglement"}
ouvrants = sorted({j["jalon"] for j in jalons if j["statut"] == "ouvre"}, key=lambda i: JALONS[i]["annee"])
amont_bilan = {"jalons": len({j["jalon"] for j in jalons}), "avec_amont": len({j["jalon"] for j in jalons} & amont),
               "avec_regle": len({j["jalon"] for j in jalons} & amont_regle),
               "ouvrants": len(ouvrants), "ouvrants_amont": sum(j in amont for j in ouvrants),
               "ouvrants_regle": sum(j in amont_regle for j in ouvrants)}
# Probabilité d'autant d'ouvrants reliés à un règlement si chacun l'était comme un jalon quelconque.
q = amont_bilan["avec_regle"] / amont_bilan["jalons"]
amont_bilan["p"] = round(sum(comb(len(ouvrants), i) * q ** i * (1 - q) ** (len(ouvrants) - i)
                             for i in range(amont_bilan["ouvrants_regle"], len(ouvrants) + 1)), 3)

# --- Confrontation 3 : règlement ---------------------------------------------------------------
annees_regle = [a for a in ANNEES if regles_autour(a)]
debuts = [h for u in ("ecurie", "pilote", "motoriste") for h in dominations[u] if h["longue"]]

sortie = {
    "parametres": {"seuil": SEUIL, "min": MIN, "duo": DUO, "creux": CREUX, "avant": AVANT, "apres": APRES,
                   "fenetre_jalon": FENETRE_JALON, "fenetre_regle": FENETRE_REGLE,
                   "variantes": [{"seuil": s, "min": m, "creux": c} for s, m, c in VARIANTES],
                   "saisons": f"{ANNEES[0]}–{ANNEES[-1]}", "gp": sum(s["gp"] for s in R)},
    "effectifs": effectifs,
    "dominations": dominations,
    "saisons_dominantes": saisons_dom,
    "saisons_ecrasantes": ecrasantes,
    "jalons": jalons,
    "jalons_sans_ecurie": sans_ecurie,
    "temoin_jalons": {"n": len(obs), "ouvre": sum(obs), "attendu": round(sum(attendu), 1)},
    "etude_jalons": etude,
    "p_hasard": round(p_hasard, 3),
    "voies": voies,
    "chaines": chaines,
    "amont": amont_bilan,
    "ingenieurs_apparies": groupes_ing,
    "rebat": rebat,
    "ingenieurs": mouvements,
    "bilan_ingenieurs": {"arrivee": bilan([m for m in mouvements if m["type"] == "arrivee"]),
                         "depart": bilan([m for m in mouvements if m["type"] == "depart"]),
                         "temoin": {"n": len(temoin_ing), "hausse": sum(x > 0.05 for x in temoin_ing),
                                    "baisse": sum(x < -0.05 for x in temoin_ing)}},
    "temoin_reglement": {"annees": len(ANNEES), "avec_regle": len(annees_regle),
                         "debuts": len(debuts), "debuts_regle": sum(bool(h["regles_debut"]) for h in debuts),
                         "fins": sum(h["fin"] < ANNEES[-1] for h in debuts),
                         "fins_regle": sum(bool(h["regles_fin"]) for h in debuts if h["fin"] < ANNEES[-1])},
    # Domination saison par saison : écurie en tête des victoires (pour une frise ultérieure).
    "saisons": [{"annee": a, "gp": next(s["gp"] for s in R if s["annee"] == a),
                 "ecurie": max(part["ecurie"][a], key=part["ecurie"][a].get).lstrip("~"),
                 "part": round(max(part["ecurie"][a].values()), 3)} for a in ANNEES],
}
entete = ("# Dominations et confrontations, calculées par outils/domination.py depuis _data/resultats.yml,\n"
          "# _data/ecuries.yml et _data/chronologie.yml : ne pas modifier à la main, relancer le script.\n"
          "# part = part des Grands Prix gagnés ; points = part moyenne des points (écuries depuis 1958, pilotes) ;\n"
          "# degre = saison (1 saison dominante), domination (au moins duo), hegemonie (au moins min, robuste) ;\n"
          "# longue = au moins min saisons dominantes, robuste ou non : base des confrontations ;\n"
          "# poles, podiums (part des places), doubles : parts sur les courses dont la grille ou le podium est\n"
          "# publié ; ecart = part des points moins celle du meilleur des autres ; indice = moyenne des parts de\n"
          "# victoires, de poles et de places sur le podium ;\n"
          "# avant / apres = part moyenne des victoires de l'écurie dans les fenêtres de la confrontation.\n")
open("_data/domination.yml", "w", encoding="utf-8").write(
    entete + yaml.safe_dump(sortie, allow_unicode=True, sort_keys=False, width=1000))
for u, n in effectifs.items():
    print(f"{u} : {n['saison']} saisons isolées, {n['domination']} dominations, {n['hegemonie']} hégémonies "
          f"({n['longue']} périodes longues)")

# --- Graphiques (SVG en ligne, inclus par le dossier ; couleurs et polices du site) ---------------
TEXTES = {
    "fr": {"pc": " %", "x": "Saisons par rapport au jalon", "y": "Part des Grands Prix gagnés",
           "jalon": "saison du jalon", "s1": "Écurie qui innove", "s2": "Même écurie,", "s2b": "saison quelconque",
           "t1": "Part des victoires autour d'un jalon technique",
           "d1": "Moyenne sur {n} jalons : l'écurie qui innove passe d'environ {a} à {b} des victoires, puis revient à son niveau habituel en quatre saisons ; le témoin reste stable.",
           "t2": "Écuries en hausse après un mouvement d'ingénieur : observé et attendu",
           "d2": "Part des cas où la part des victoires de l'écurie monte de plus de 5 points, comparée au témoin apparié sur le niveau de départ.",
           "obs": "observé", "att": "attendu (témoin apparié)",
           "g": {"toutes": "Toutes les arrivées", "tier-a": "Arrivées, Tier A", "tiers-b-c-d": "Arrivées, Tiers B à D",
                 "hc": "Arrivées, hors classement", "departs": "Départs"}},
    "en": {"pc": "%", "x": "Seasons relative to the milestone", "y": "Share of Grands Prix won",
           "jalon": "milestone season", "s1": "Innovating team", "s2": "Same team,", "s2b": "any season",
           "t1": "Share of wins around a technical milestone",
           "d1": "Average over {n} milestones: the innovating team goes from about {a} to {b} of wins, then returns to its usual level within four seasons; the control stays flat.",
           "t2": "Teams improving after an engineer's move: observed and expected",
           "d2": "Share of cases where the team's share of wins rises by more than 5 points, compared with the control matched on the starting level.",
           "obs": "observed", "att": "expected (matched control)",
           "g": {"toutes": "All arrivals", "tier-a": "Arrivals, Tier A", "tiers-b-c-d": "Arrivals, Tiers B to D",
                 "hc": "Arrivals, unranked", "departs": "Departures"}},
}
STYLE = ("<style>.dm-t{font-family:var(--titre);font-size:14px;fill:var(--mine)}"
         ".dm-f{font-family:var(--titre);font-size:15px;font-weight:600;fill:var(--graphite)}"
         ".dm-g{stroke:#e1e5e7;stroke-width:1}.dm-a{stroke:var(--trait);stroke-width:1}"
         ".dm-1{stroke:#1f5fa8;fill:none;stroke-width:2;stroke-linejoin:round}"
         ".dm-2{stroke:#8e979d;fill:none;stroke-width:2;stroke-dasharray:6 4}"
         ".dm-p1{fill:#1f5fa8;stroke:#fff;stroke-width:2}.dm-p2{fill:#fff;stroke:#8e979d;stroke-width:2}"
         ".dm-l{stroke:#c2c9cc;stroke-width:2}</style>")

def pct(x, lang):
    return f"{round(x * 100)}{TEXTES[lang]['pc']}"

def svg_etude(lang):
    L, W, Hh = TEXTES[lang], 560, 300
    g, d, h, b = 52, 150, 20, 50
    xs = lambda i: g + i * (W - g - d) / (len(K) - 1)
    ys = lambda v: Hh - b - v / 0.35 * (Hh - b - h)
    o = [f'<svg class="graphique" viewBox="0 0 {W} {Hh}" role="img" aria-labelledby="dm-e-t dm-e-d">',
         f'<title id="dm-e-t">{L["t1"]}</title>',
         f'<desc id="dm-e-d">{L["d1"].format(n=etude["n"], a=pct(etude["jalons"][2], lang), b=pct(etude["jalons"][4], lang))}</desc>', STYLE]
    for v in (0, 0.1, 0.2, 0.3):
        o.append(f'<line class="dm-g" x1="{g}" x2="{W - d}" y1="{ys(v):.1f}" y2="{ys(v):.1f}"/>'
                 f'<text class="dm-t" x="{g - 8}" y="{ys(v) + 5:.1f}" text-anchor="end">{pct(v, lang)}</text>')
    for i, k in enumerate(K):
        o.append(f'<text class="dm-t" x="{xs(i):.1f}" y="{Hh - b + 20}" text-anchor="middle">{k:+d}</text>'.replace("+0", "0"))
    x0 = xs(K.index(0))
    o.append(f'<line class="dm-a" x1="{x0:.1f}" x2="{x0:.1f}" y1="{h}" y2="{Hh - b}"/>'
             f'<text class="dm-t" x="{x0 + 6:.1f}" y="{Hh - b - 8}">{L["jalon"]}</text>')
    o.append(f'<text class="dm-t" x="{(g + W - d) / 2:.1f}" y="{Hh - 8}" text-anchor="middle">{L["x"]}</text>')
    o.append(f'<text class="dm-t" transform="translate(14 {(h + Hh - b) / 2:.1f}) rotate(-90)" text-anchor="middle">{L["y"]}</text>')
    for cle, cl, pc in (("temoin", "dm-2", "dm-p2"), ("jalons", "dm-1", "dm-p1")):
        pts = [(xs(i), ys(v)) for i, v in enumerate(etude[cle])]
        o.append(f'<polyline class="{cl}" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}"/>')
        for (x, y), k, v in zip(pts, K, etude[cle]):
            lib = L["s1"] if cle == "jalons" else f'{L["s2"]} {L["s2b"]}'
            o.append(f'<circle class="{pc}" cx="{x:.1f}" cy="{y:.1f}" r="4"><title>{lib}, {k:+d} : {pct(v, lang)}</title></circle>'.replace("+0 :", "0 :"))
    xe = W - d + 10
    ip = max(range(len(K)), key=lambda i: etude["jalons"][i])
    o.append(f'<text class="dm-f" x="{xs(ip) + 10:.1f}" y="{ys(etude["jalons"][ip]) - 8:.1f}">{L["s1"]}</text>')
    yt = ys(etude["temoin"][-1]) - 24
    o.append(f'<text class="dm-t" x="{xe}" y="{yt:.1f}">{L["s2"]}</text><text class="dm-t" x="{xe}" y="{yt + 16:.1f}">{L["s2b"]}</text>')
    o.append("</svg>")
    return "".join(o)

def svg_ingenieurs(lang):
    L, W = TEXTES[lang], 560
    g, d, h, pas = 230, 40, 46, 40
    Hh = h + pas * len(groupes_ing) + 34
    xs = lambda v: g + v * (W - g - d)
    o = [f'<svg class="graphique" viewBox="0 0 {W} {Hh}" role="img" aria-labelledby="dm-i-t dm-i-d">',
         f'<title id="dm-i-t">{L["t2"]}</title><desc id="dm-i-d">{L["d2"]}</desc>', STYLE,
         f'<circle class="dm-p1" cx="{g + 6}" cy="16" r="5"/><text class="dm-t" x="{g + 16}" y="21">{L["obs"]}</text>',
         f'<circle class="dm-p2" cx="{g + 110}" cy="16" r="5"/><text class="dm-t" x="{g + 120}" y="21">{L["att"]}</text>']
    for v in (0, 0.25, 0.5, 0.75, 1):
        o.append(f'<line class="dm-g" x1="{xs(v):.1f}" x2="{xs(v):.1f}" y1="{h - 10}" y2="{Hh - 30}"/>'
                 f'<text class="dm-t" x="{xs(v):.1f}" y="{Hh - 10}" text-anchor="middle">{pct(v, lang)}</text>')
    for i, gr in enumerate(groupes_ing):
        y = h + pas * i + pas / 2
        ob, at = gr["hausse"] / gr["n"], gr["hausse_attendue"] / gr["n"]
        o.append(f'<text class="dm-t" x="{g - 12}" y="{y + 5:.1f}" text-anchor="end">{L["g"][gr["groupe"]]} ({gr["n"]})</text>')
        o.append(f'<line class="dm-l" x1="{xs(at):.1f}" x2="{xs(ob):.1f}" y1="{y:.1f}" y2="{y:.1f}"/>')
        o.append(f'<circle class="dm-p2" cx="{xs(at):.1f}" cy="{y:.1f}" r="5"><title>{L["att"]} : {pct(at, lang)}</title></circle>')
        o.append(f'<circle class="dm-p1" cx="{xs(ob):.1f}" cy="{y:.1f}" r="5"><title>{L["obs"]} : {pct(ob, lang)} ({gr["hausse"]}/{gr["n"]})</title></circle>')
        lx, anc = (xs(ob) + 10, "start") if ob >= at else (xs(ob) - 10, "end")
        o.append(f'<text class="dm-f" x="{lx:.1f}" y="{y + 5:.1f}" text-anchor="{anc}">{pct(ob, lang)}</text>')
    o.append("</svg>")
    return "".join(o)

os.makedirs("_includes/domination", exist_ok=True)
for lang in TEXTES:
    open(f"_includes/domination/etude-jalons-{lang}.svg", "w", encoding="utf-8").write(svg_etude(lang) + "\n")
    open(f"_includes/domination/ingenieurs-{lang}.svg", "w", encoding="utf-8").write(svg_ingenieurs(lang) + "\n")

# --- Compteur de domination des écuries (fiches) ----------------------------------------------
# Indice composite saison par saison, à l'échelle de la lignée (l'usine sous tous ses noms), sur
# 0-100 absolu : 100 = toutes les victoires, toutes les poles et tout le podium. Un cadran donne la
# meilleure saison, une courbe la suite des saisons, avec titres, dominations, jalons et seuil.
EN = yaml.safe_load(open("_data/en/ecuries.yml", encoding="utf-8"))
CEN = yaml.safe_load(open("_data/en/chronologie.yml", encoding="utf-8"))
NOMS = {"fr": {e["id"]: e["nom"] for e in E["ecuries"]}, "en": {e["id"]: e["nom"] for e in EN["ecuries"]}}
JALONS_L = {"fr": {j["id"]: j["titre"] for j in C["jalons"]}, "en": {j["id"]: j["titre"] for j in CEN["jalons"]}}

def indice(u, k, a):
    return mesures(u, k, [a]).get("indice")

# Seuil calibré : la valeur d'indice qui sépare le mieux les saisons dominantes des autres
# (indice de Youden : sensibilité + spécificité - 1, maximal), sur toutes les saisons de lignée.
obs_l = []
def saisons_lignee(lid):
    return sorted({y for l in E["lignees"] if l["id"] == lid for s in l["segments"]
                   for y in range(s["de"], s["a"] + 1) if y in part["lignee"]})
for l in E["lignees"]:
    for a in saisons_lignee(l["id"]):
        x = indice("lignee", l["id"], a)
        if x is not None:
            dom = champion["lignee"].get(a) == l["id"] or part["lignee"][a].get(l["id"], 0) >= SEUIL
            obs_l.append((x, dom))
def youden(t):
    p = [x >= t for x, d in obs_l if d]
    n = [x < t for x, d in obs_l if not d]
    return sum(p) / len(p) + sum(n) / len(n) - 1
SEUIL_INDICE = max((round(t / 100, 2) for t in range(1, 100)), key=youden)
sortie_compteur = {"seuil": SEUIL_INDICE, "youden": round(youden(SEUIL_INDICE), 3),
                   "saisons": len(obs_l), "dominantes": sum(d for _, d in obs_l),
                   "au_dessus": sum(x >= SEUIL_INDICE for x, _ in obs_l),
                   "dominantes_au_dessus": sum(x >= SEUIL_INDICE and d for x, d in obs_l),
                   "lignees": {}}

TXT = {"fr": {"t": "Compteur de domination de la lignée {n}", "rec": "Meilleure saison", "seuil": "seuil",
              "d": "Indice composite saison par saison, sur 100 : moyenne des parts de victoires, de poles et de places sur le podium. Meilleure saison : {b} en {y}, {v}.",
              "titre": "titre", "dom": "domination", "heg": "hégémonie", "aucune": "aucune saison mesurée"},
       "en": {"t": "Dominance gauge of the {n} lineage", "rec": "Best season", "seuil": "threshold",
              "d": "Composite index season by season, out of 100: average share of wins, poles and podium places. Best season: {b} in {y}, {v}.",
              "titre": "title", "dom": "dominance", "heg": "hegemony", "aucune": "no season measured"}}
CS = ("<style>.cp-t{font-family:var(--titre);font-size:13px;fill:var(--mine)}"
      ".cp-v{font-family:var(--titre);font-size:30px;font-weight:700;fill:var(--graphite)}"
      ".cp-f{font-family:var(--titre);font-size:13px;font-weight:600;fill:var(--graphite)}"
      ".cp-g{stroke:#e1e5e7;stroke-width:1}.cp-a{stroke:var(--trait);stroke-width:1}"
      ".cp-c{stroke:#1f5fa8;fill:none;stroke-width:2;stroke-linejoin:round}"
      ".cp-p{fill:#1f5fa8}.cp-ti{fill:#c8102e;stroke:#fff;stroke-width:1.5}"
      ".cp-s{stroke:#c8102e;stroke-width:1.5;stroke-dasharray:5 4}"
      ".cp-dom{fill:#1f5fa8;opacity:.08}.cp-heg{fill:#1f5fa8;opacity:.18}"
      ".cp-j{fill:var(--graphite)}.cp-n{fill:#eef1f2;stroke:#fff;stroke-width:1}"
      ".cp-arc{fill:none;stroke:#e1e5e7;stroke-width:14}.cp-arcv{fill:none;stroke:#1f5fa8;stroke-width:14}"
      ".cp-ai{stroke:var(--graphite);stroke-width:3;stroke-linecap:round}</style>")

def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def ecurie_de(lid, a):
    return next((s["ecurie"] for l in E["lignees"] if l["id"] == lid for s in l["segments"] if s["de"] <= a <= s["a"]), None)

def cadran_g(cx, cy, r, v, lignes, record=None, fragile=False, taille=1.0):
    """Cadran 0-100 (groupe SVG) : arc rempli jusqu'à v, aiguille, repère rouge du seuil calibré,
    trait fin pour un record (meilleure saison d'une période), valeur au centre, lignes de légende.
    fragile : arc en tirets (domination qui n'est pas une hégémonie)."""
    import math
    ang = lambda x: math.pi * (1 - min(max(x, 0), 1))
    pt = lambda x, rr: (cx + rr * math.cos(ang(x)), cy - rr * math.sin(ang(x)))
    ep = max(6, round(14 * taille))
    x0, y0 = pt(0, r); x1, y1 = pt(1, r); xv, yv = pt(v, r)
    o = [f'<path class="cp-arc" style="stroke-width:{ep}" d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}"/>',
         f'<path class="cp-arcv" style="stroke-width:{ep}{";stroke-dasharray:6 3" if fragile else ""}" '
         f'd="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {xv:.1f},{yv:.1f}"/>']
    for t in range(0, 101, 10):
        a1, a2 = pt(t / 100, r - ep), pt(t / 100, r - ep - (8 if t % 50 == 0 else 4) * taille)
        o.append(f'<line class="cp-a" x1="{a1[0]:.1f}" y1="{a1[1]:.1f}" x2="{a2[0]:.1f}" y2="{a2[1]:.1f}"/>')
        if t % 50 == 0 and taille >= 0.8:
            tx, ty = pt(t / 100, r - ep - 20 * taille)
            o.append(f'<text class="cp-t" x="{tx:.1f}" y="{ty + 4:.1f}" text-anchor="middle">{t}</text>')
    s1, s2 = pt(SEUIL_INDICE, r - ep / 2 - 2), pt(SEUIL_INDICE, r + ep / 2 + 3)
    o.append(f'<line class="cp-s" style="stroke-dasharray:none;stroke-width:3" x1="{s1[0]:.1f}" y1="{s1[1]:.1f}" x2="{s2[0]:.1f}" y2="{s2[1]:.1f}"/>')
    if record is not None:
        q1, q2 = pt(record, r - ep / 2 - 2), pt(record, r + ep / 2 + 3)
        o.append(f'<line class="cp-ai" style="stroke-width:2" x1="{q1[0]:.1f}" y1="{q1[1]:.1f}" x2="{q2[0]:.1f}" y2="{q2[1]:.1f}"/>')
    ax, ay = pt(v, r - ep - 10 * taille)
    o.append(f'<line class="cp-ai" style="stroke-width:{max(2, 3 * taille):.1f}" x1="{cx}" y1="{cy}" x2="{ax:.1f}" y2="{ay:.1f}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{max(3, 6 * taille):.1f}" class="cp-j"/>')
    o.append(f'<text class="cp-v" style="font-size:{round(30 * taille)}px" x="{cx}" y="{cy + 34 * taille:.1f}" text-anchor="middle">{round(v * 100)}</text>')
    for i, l in enumerate(lignes):
        fs = "" if taille >= 0.8 else ' style="font-size:11px"'
        o.append(f'<text class="{"cp-f" if i == 0 and len(lignes) > 1 else "cp-t"}"{fs} x="{cx}" y="{cy + 34 * taille + 15 * (i + 1) + 2:.1f}" text-anchor="middle">{l}</text>')
    return "".join(o)

def svg_compteur(lid, lang):
    import math
    L, nl = TXT[lang], {"fr": NOM_LIGNEE, "en": {l["id"]: l["nom"] for l in EN["lignees"]}}[lang][lid]
    ans = saisons_lignee(lid)
    vals = {a: indice("lignee", lid, a) for a in ans}
    mes = [a for a in ans if vals[a] is not None]
    uid = f"cp-{lid}-{lang}"
    if not mes:
        return None
    best = max(mes, key=lambda a: vals[a])
    bn = NOMS[lang].get(ecurie_de(lid, best), nl)
    v100 = lambda x: round(x * 100)
    desc = L["d"].format(b=esc(bn), y=best, v=v100(vals[best]))
    # Cadran : demi-cercle 0-100, aiguille sur la meilleure saison, repère du seuil.
    cadran = (f'<svg class="graphique compteur-cadran" viewBox="0 0 220 170" role="img" aria-labelledby="{uid}-ct">'
              f'<title id="{uid}-ct">{L["rec"]} : {esc(bn)} {best}, {v100(vals[best])} / 100</title>{CS}'
              + cadran_g(110, 112, 86, vals[best], [f'{L["rec"]} : {esc(bn)} {best}']) + "</svg>")
    # Courbe : indice saison par saison sur l'axe des années de la lignée.
    W, Hh, g, d, h, b = 640, 250, 40, 14, 14, 62
    a0, a1_ = ans[0], ans[-1]
    # Axe d'au moins dix saisons, centré sur la lignée : une écurie d'une saison reste lisible.
    m0 = (a0 + a1_) / 2
    x0a, x1a = min(a0, m0 - 5), max(a1_, m0 + 5)
    x0a, x1a = x0a - 0.5, x1a + 0.5
    span = x1a - x0a
    xs = lambda a: g + (a - x0a) / span * (W - g - d)
    ys = lambda x: Hh - b - x * (Hh - b - h)
    o = [f'<svg class="graphique compteur-courbe" viewBox="0 0 {W} {Hh}" role="img" aria-labelledby="{uid}-t {uid}-d">',
         f'<title id="{uid}-t">{L["t"].format(n=esc(nl))}</title><desc id="{uid}-d">{desc}</desc>', CS]
    demi = 0.5 * (W - g - d) / span
    for p in dominations["lignee"]:
        if p.get("id") == lid:
            cl = "cp-heg" if p["degre"] == "hegemonie" else "cp-dom"
            lib = L["heg"] if p["degre"] == "hegemonie" else L["dom"]
            o.append(f'<rect class="{cl}" x="{xs(p["debut"]) - demi:.1f}" y="{h}" width="{xs(p["fin"]) - xs(p["debut"]) + 2 * demi:.1f}" height="{Hh - b - h}"><title>{lib}, {p["debut"]}–{p["fin"]}</title></rect>')
    for v in (0, 0.25, 0.5, 0.75, 1):
        o.append(f'<line class="cp-g" x1="{g}" x2="{W - d}" y1="{ys(v):.1f}" y2="{ys(v):.1f}"/>'
                 f'<text class="cp-t" x="{g - 6}" y="{ys(v) + 4:.1f}" text-anchor="end">{round(v * 100)}</text>')
    o.append(f'<line class="cp-s" x1="{g}" x2="{W - d}" y1="{ys(SEUIL_INDICE):.1f}" y2="{ys(SEUIL_INDICE):.1f}"/>'
             f'<text class="cp-t" x="{W - d}" y="{ys(SEUIL_INDICE) - 5:.1f}" text-anchor="end">{L["seuil"]} {v100(SEUIL_INDICE)}</text>')
    pas = 10 if span > 25 else 2
    for a in range(int(x0a) + 1 + (-(int(x0a) + 1)) % pas, int(x1a) + 1, pas):
        o.append(f'<text class="cp-t" x="{xs(a):.1f}" y="{Hh - b + 16}" text-anchor="middle">{a}</text>')
    # Courbe brisée sur les saisons sans mesure.
    tr, cur = [], []
    for a in ans:
        if vals[a] is None:
            if cur: tr.append(cur); cur = []
        else:
            cur.append((xs(a), ys(vals[a])))
    if cur: tr.append(cur)
    for c in tr:
        o.append(f'<polyline class="cp-c" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in c)}"/>')
    for a in mes:
        ti = champion["lignee"].get(a) == lid
        nm = esc(NOMS[lang].get(ecurie_de(lid, a), nl))
        o.append(f'<circle class="{"cp-ti" if ti else "cp-p"}" cx="{xs(a):.1f}" cy="{ys(vals[a]):.1f}" r="{5 if ti else 2.5}">'
                 f'<title>{a}, {nm} : {v100(vals[a])}{" · " + L["titre"] if ti else ""}</title></circle>')
    # Bande des noms successifs, puis jalons portés par les écuries de la lignée.
    yb = Hh - b + 24
    segs = [s for l in E["lignees"] if l["id"] == lid for s in l["segments"]]
    for s in segs:
        de, a_ = max(s["de"], a0), min(s["a"], a1_)
        if de > a_:
            continue
        x1s, x2s = xs(de) - demi, xs(a_) + demi
        nm = esc(NOMS[lang].get(s["ecurie"], s["ecurie"]).split(" (")[0])
        o.append(f'<rect class="cp-n" x="{x1s:.1f}" y="{yb}" width="{x2s - x1s:.1f}" height="16"><title>{nm}, {s["de"]}–{s["a"]}</title></rect>')
        if x2s - x1s > 7 * len(nm):
            o.append(f'<text class="cp-t" x="{(x1s + x2s) / 2:.1f}" y="{yb + 12}" text-anchor="middle">{nm}</text>')
    ecs = {s["ecurie"] for s in segs}
    for jid, eclist in JALON_ECURIES.items():
        y = JALONS[jid]["annee"]
        if ecs & set(eclist) and a0 <= y <= a1_ and any(s["ecurie"] in eclist and s["de"] <= y <= s["a"] for s in segs):
            xj, yj = xs(y), yb + 22
            o.append(f'<path class="cp-j" d="M{xj:.1f},{yj} l-5,9 h10 z"><title>{y} : {esc(JALONS_L[lang].get(jid, jid))}</title></path>')
    o.append("</svg>")
    sortie_compteur["lignees"][lid] = {"meilleure": best, "indice": round(vals[best], 3)}
    return cadran, "".join(o)

# --- Ingénieurs : la domination de leur écurie pendant leur présence ---------------------------
# Saisons sûres seulement : de « de » à « a ». Un séjour sans date de fin (ou sans début) reste hors
# du compte, faute de savoir quand l'ingénieur est parti : il est dénombré à part.
ING_NOMS = {}
for chemin in os.listdir("_ingenieurs"):
    fm = yaml.safe_load(open(f"_ingenieurs/{chemin}", encoding="utf-8").read().split("---\n")[1])
    ING_NOMS[chemin[:-3]] = fm.get("nom_complet") or fm.get("title") or chemin[:-3]
sejours = collections.defaultdict(set)
non_dates = collections.Counter()
for ec, ing, de, a in ING_ECURIE:
    if de is None or a is None:
        non_dates[ing] += 1
        continue
    for y in range(max(de, ANNEES[0]), min(a, ANNEES[-1]) + 1):
        sejours[ing].add((y, ec))
def suites_ing(ss, seuil, creux):
    """Suites de saisons où une écurie de l'ingénieur domine (titre ou seuil des victoires)."""
    dom = sorted({y for y, ec in ss if champion["ecurie"].get(y) == ec or part["ecurie"][y].get(ec, 0) >= seuil})
    out, g = [], []
    for y in dom:
        if g and y - g[-1] > creux + 1:
            out.append(g); g = []
        g.append(y)
    return out + ([g] if g else []), dom

ing_dom = []
for ing, ss in sejours.items():
    suites, dom = suites_ing(ss, SEUIL, CREUX)
    vals = [x for x in (mesures("ecurie", ec, [y]).get("indice") for y, ec in ss) if x is not None]
    if not vals:
        continue
    # Degré de sa plus longue suite de saisons dominantes, mêmes règles que pour une écurie :
    # une hégémonie doit se retrouver dans les deux variantes plus strictes.
    plus = max(suites, key=len) if suites else []
    robuste = len(plus) >= MIN and all(
        any(len(v) >= m and v[0] <= plus[-1] and plus[0] <= v[-1] for v in suites_ing(ss, sv, cv)[0])
        for sv, m, cv in VARIANTES)
    best = max(ss, key=lambda x: mesures("ecurie", x[1], [x[0]]).get("indice") or 0)
    ing_dom.append({"id": ing, "nom": ING_NOMS.get(ing, ing), "saisons": len({y for y, _ in ss}),
                    "dominantes": len(dom), "titres": sum(1 for y, ec in ss if champion["ecurie"].get(y) == ec),
                    "indice_moyen": round(sum(vals) / len(vals), 3),
                    "meilleure": {"annee": best[0], "ecurie": best[1],
                                  "indice": mesures("ecurie", best[1], [best[0]]).get("indice")},
                    "plus_longue": [plus[0], plus[-1]] if plus else None,
                    "degre": ("hegemonie" if robuste else "domination" if len(plus) >= DUO
                              else "saison" if plus else None),
                    "sejours_non_dates": non_dates.get(ing, 0)})
ing_dom.sort(key=lambda x: (-x["dominantes"], -x["indice_moyen"]))
sortie_ing = {"ingenieurs": ing_dom, "non_dates": sum(non_dates.values()),
              "ingenieurs_partiels": sum(1 for i in ing_dom if i["sejours_non_dates"])}

# --- Visuels « compteur » du dossier --------------------------------------------------------------
TXT_D = {"fr": {"f1_t": "Le compteur de la F1, 1950-2025",
                "f1_d": "Pour chaque saison, l'indice composite de l'écurie la plus forte, sur 100. Les bandes marquent les hégémonies d'écurie ; les tirets rouges, le seuil calibré.",
                "y": "Indice de l'écurie la plus forte", "seuil": "seuil", "tb_t": "Tableau de bord des dominations longues",
                "tb_d": "Un cadran par domination d'au moins trois saisons : l'aiguille donne l'indice moyen de la période, le trait noir sa meilleure saison, le repère rouge le seuil. Arc en tirets : domination qui n'est pas une hégémonie.",
                "heg": "hégémonie", "dom": "domination", "ing_t": "Le compteur des ingénieurs",
                "ing_d": "Indice moyen des écuries pendant la présence de l'ingénieur, pour les douze ingénieurs dont l'écurie a dominé le plus de saisons.",
                "sd": "saisons dominantes"},
         "en": {"f1_t": "The F1 gauge, 1950-2025",
                "f1_d": "For each season, the composite index of the strongest team, out of 100. Bands mark team hegemonies; red dashes, the calibrated threshold.",
                "y": "Index of the strongest team", "seuil": "threshold", "tb_t": "Dashboard of long dominance",
                "tb_d": "One dial per period of at least three dominant seasons: the needle gives the period's average index, the black mark its best season, the red mark the threshold. Dashed arc: dominance that is not a hegemony.",
                "heg": "hegemony", "dom": "dominance", "ing_t": "The engineers' gauge",
                "ing_d": "Average index of the teams while the engineer was present, for the twelve engineers whose team dominated the most seasons.",
                "sd": "dominant seasons"}}
NOMS_U = {"fr": {"pilote": {}, "motoriste": NOM_MOTEUR},
          "en": {"pilote": {}, "motoriste": {m["id"]: m["nom"] for m in EN["motoristes"]}}}

def nom_u(u, k, lang):
    if u in ("ecurie", "lignee"):
        return NOMS[lang].get(k, nom(u, k)).split(" (")[0]
    return NOMS_U[lang][u].get(k, nom(u, k))

# Saison par saison : l'écurie d'indice le plus élevé.
tete_indice = []
for a in ANNEES:
    c = [(mesures("ecurie", k, [a]).get("indice"), k) for k in set(part["ecurie"][a]) | set(poles["ecurie"][a])]
    c = [x for x in c if x[0] is not None]
    if c:
        v, k = max(c)
        tete_indice.append({"annee": a, "ecurie": k.lstrip("~"), "indice": round(v, 3)})

def svg_f1(lang):
    L = TXT_D[lang]
    W, Hh, g, d, h, b = 640, 300, 44, 14, 30, 34
    a0, a1 = ANNEES[0] - 0.5, ANNEES[-1] + 0.5
    xs = lambda a: g + (a - a0) / (a1 - a0) * (W - g - d)
    ys = lambda v: Hh - b - v * (Hh - b - h)
    o = [f'<svg class="graphique" viewBox="0 0 {W} {Hh}" role="img" aria-labelledby="cf-t-{lang} cf-d-{lang}">',
         f'<title id="cf-t-{lang}">{L["f1_t"]}</title><desc id="cf-d-{lang}">{L["f1_d"]}</desc>', CS]
    for i, p_ in enumerate(x for x in dominations["ecurie"] if x["degre"] == "hegemonie"):
        x1, x2 = xs(p_["debut"] - 0.5), xs(p_["fin"] + 0.5)
        nm = esc(nom_u("ecurie", p_["id"], lang))
        o.append(f'<rect class="cp-heg" x="{x1:.1f}" y="{h}" width="{x2 - x1:.1f}" height="{Hh - b - h}"><title>{nm}, {p_["debut"]}–{p_["fin"]}</title></rect>')
        o.append(f'<text class="cp-t" x="{(x1 + x2) / 2:.1f}" y="{h - 6 - 12 * (i % 2)}" text-anchor="middle">{nm}</text>')
    for v in (0, 0.25, 0.5, 0.75, 1):
        o.append(f'<line class="cp-g" x1="{g}" x2="{W - d}" y1="{ys(v):.1f}" y2="{ys(v):.1f}"/>'
                 f'<text class="cp-t" x="{g - 6}" y="{ys(v) + 4:.1f}" text-anchor="end">{round(v * 100)}</text>')
    o.append(f'<line class="cp-s" x1="{g}" x2="{W - d}" y1="{ys(SEUIL_INDICE):.1f}" y2="{ys(SEUIL_INDICE):.1f}"/>'
             f'<text class="cp-t" x="{W - d}" y="{ys(SEUIL_INDICE) + 14:.1f}" text-anchor="end">{L["seuil"]} {round(SEUIL_INDICE * 100)}</text>')
    for a in range(1950, 2030, 10):
        o.append(f'<text class="cp-t" x="{xs(a):.1f}" y="{Hh - b + 18}" text-anchor="middle">{a}</text>')
    o.append(f'<polyline class="cp-c" points="{" ".join(f"{xs(t["annee"]):.1f},{ys(t["indice"]):.1f}" for t in tete_indice)}"/>')
    for t in tete_indice:
        nm = esc(nom_u("ecurie", t["ecurie"], lang))
        o.append(f'<circle class="cp-p" cx="{xs(t["annee"]):.1f}" cy="{ys(t["indice"]):.1f}" r="3"><title>{t["annee"]}, {nm} : {round(t["indice"] * 100)}</title></circle>')
    o.append("</svg>")
    return "".join(o)

def svg_tableau(u, lang):
    L = TXT_D[lang]
    ps = [x for x in dominations[u] if x["longue"]]
    par_ligne, W, cw, ch = 4, 640, 160, 150
    lignes_n = (len(ps) + par_ligne - 1) // par_ligne
    Hh = lignes_n * ch + 6
    o = [f'<svg class="graphique" viewBox="0 0 {W} {Hh}" role="img" aria-labelledby="tb-{u}-t-{lang} tb-{u}-d-{lang}">',
         f'<title id="tb-{u}-t-{lang}">{L["tb_t"]}</title><desc id="tb-{u}-d-{lang}">{L["tb_d"]}</desc>', CS]
    for i, p_ in enumerate(ps):
        cx, cy = cw * (i % par_ligne) + cw / 2, ch * (i // par_ligne) + 72
        k = p_.get("id") or p_["nom"]
        rec = max((mesures(u, k, [a]).get("indice") or 0) for a in range(p_["debut"], p_["fin"] + 1))
        nm = esc(nom_u(u, k, lang) if p_.get("id") else p_["nom"])
        if u == "pilote":
            nm = esc(p_["nom"].split(" ")[-1])
        deg = L["heg"] if p_["degre"] == "hegemonie" else L["dom"]
        o.append(f'<g><title>{esc(p_["nom"])}, {p_["debut"]}–{p_["fin"]} · {deg} · {round(p_["indice"] * 100)} / 100</title>')
        o.append(cadran_g(cx, cy, 58, p_["indice"], [f"{nm}", f'{p_["debut"]}–{p_["fin"]} · {deg}'],
                          record=rec, fragile=p_["degre"] != "hegemonie", taille=0.62))
        o.append("</g>")
    o.append("</svg>")
    return "".join(o)

def svg_ingenieurs_cp(lang):
    L = TXT_D[lang]
    ps = ing_dom[:12]
    par_ligne, W, cw, ch = 4, 640, 160, 150
    Hh = ((len(ps) + par_ligne - 1) // par_ligne) * ch + 6
    o = [f'<svg class="graphique" viewBox="0 0 {W} {Hh}" role="img" aria-labelledby="ti-t-{lang} ti-d-{lang}">',
         f'<title id="ti-t-{lang}">{L["ing_t"]}</title><desc id="ti-d-{lang}">{L["ing_d"]}</desc>', CS]
    for i, p_ in enumerate(ps):
        cx, cy = cw * (i % par_ligne) + cw / 2, ch * (i // par_ligne) + 72
        nm = esc(p_["nom"].split(" ")[-1])
        o.append(f'<g><title>{esc(p_["nom"])} · {p_["dominantes"]} {L["sd"]} / {p_["saisons"]} · {round(p_["indice_moyen"] * 100)} / 100</title>')
        o.append(cadran_g(cx, cy, 58, p_["indice_moyen"], [nm, f'{p_["dominantes"]} {L["sd"]}'],
                          record=p_["meilleure"]["indice"], taille=0.62))
        o.append("</g>")
    o.append("</svg>")
    return "".join(o)

for lang in ("fr", "en"):
    open(f"_includes/domination/compteur-f1-{lang}.svg", "w", encoding="utf-8").write(svg_f1(lang) + "\n")
    for u in ("ecurie", "pilote", "motoriste"):
        open(f"_includes/domination/tableau-{u}-{lang}.svg", "w", encoding="utf-8").write(svg_tableau(u, lang) + "\n")
    open(f"_includes/domination/ingenieurs-compteur-{lang}.svg", "w", encoding="utf-8").write(svg_ingenieurs_cp(lang) + "\n")
sortie_compteur["tete_indice"] = tete_indice
sortie_compteur["ingenieurs"] = sortie_ing

# --- Domination technique : part des victoires de chaque technologie ---------------------------
# _data/technologies.yml (saisi à la main, sourcé) : pour chaque technologie, des ères par défaut
# (tous les gagnants l'ont, ou aucun) et, pendant la fenêtre de transition, un classement explicite
# de chaque écurie gagnante (« des » : adoption en cours de saison ; « victoires_sans » : courses
# gagnées sans elle). Une victoire non classée arrête le script : on complète, on ne devine pas.
TECH = yaml.safe_load(open("_data/technologies.yml", encoding="utf-8"))["technologies"] \
    if os.path.exists("_data/technologies.yml") else []

def avec_tech(t, a, c, rang):
    """La voiture gagnante de la course c (rang-ième de la saison a) a-t-elle la technologie t ?"""
    ec = cle_ecurie(c).lstrip("~")
    for x in t.get("cas", []):
        if x["annee"] == a and x["ecurie"] == ec and x.get("equipe", c["equipe"]) == c["equipe"]:
            if x["valeur"] == "incertain":
                return None
            if c["gp"] in (x.get("victoires_sans") or []):
                return False
            if x.get("des"):
                gps = [k["gp"] for k in next(s for s in R if s["annee"] == a)["courses"]]
                if x["des"] not in gps:
                    sys.exit(f"technologies : {t['id']} {a} {ec} : GP « {x['des']} » inconnu")
                return x["valeur"] == "oui" and rang >= gps.index(x["des"])
            return x["valeur"] == "oui"
    for d in t.get("defaut", []):
        if d["de"] <= a <= d["a"]:
            return d["valeur"] == "oui"
    sys.exit(f"technologies : {t['id']} : victoire non classée ({a}, {c['gp']}, {c['equipe']})")

techno = []
for t in TECH:
    serie, pionnier, premiere = [], None, None
    for s in R:
        a = s["annee"]
        oui = inc = 0
        gagnants = set()
        for i, c in enumerate(s["courses"]):
            v = avec_tech(t, a, c, i)
            if v is None:
                inc += 1
            elif v:
                oui += 1
                gagnants.add(cle_ecurie(c).lstrip("~"))
                if premiere is None:
                    premiere, pionnier = (a, c["gp"]), cle_ecurie(c).lstrip("~")
        serie.append({"annee": a, "part": round(oui / s["gp"], 3), "ecuries": sorted(gagnants),
                      **({"incertaines": inc} if inc else {})})
    if premiere is None:
        continue
    apres = [x for x in serie if x["annee"] >= premiere[0]]
    # Exclusivité : saisons, depuis la première victoire, où le pionnier est seul à gagner avec elle.
    excl = 0
    for x in apres:
        if x["ecuries"] and x["ecuries"] != [pionnier]:
            break
        excl += 1
    seuil50 = next((x["annee"] for x in apres if x["part"] >= 0.5), None)
    seuil90 = next((x["annee"] for x in apres if x["part"] >= 0.9), None)
    dom_p = next((h for h in dominations["ecurie"] if h.get("id") == pionnier
                  and premiere[0] - 1 <= h["debut"] <= premiere[0] + FENETRE_JALON), None)
    jal = JALONS.get(t.get("jalon"), {})
    techno.append({"id": t["id"], "jalon": t.get("jalon"), "annee_jalon": jal.get("annee"),
                   "premiere": {"annee": premiere[0], "gp": premiere[1], "ecurie": pionnier},
                   "exclusivite": excl, "a50": seuil50, "a90": seuil90,
                   "delai50": seuil50 - premiere[0] if seuil50 else None,
                   "delai90": seuil90 - premiere[0] if seuil90 else None,
                   "domination_pionnier": ({"debut": dom_p["debut"], "fin": dom_p["fin"], "degre": dom_p["degre"]}
                                           if dom_p else None),
                   "serie": serie})
sortie_compteur["technologies"] = techno

TXT_T = {"fr": {"t": "La diffusion des technologies : part des victoires", "pc": " %",
                "d": "Pour chaque technologie, la part des Grands Prix gagnés par des voitures qui l'utilisent, saison par saison. Trait vertical : le jalon de la chronologie. Fond : les saisons où le pionnier est seul à gagner avec elle.",
                "seul": "pionnier seul"},
         "en": {"t": "The spread of technologies: share of wins", "pc": "%",
                "d": "For each technology, the share of Grands Prix won by cars using it, season by season. Vertical line: the timeline milestone. Background: the seasons when the pioneer alone wins with it.",
                "seul": "pioneer alone"}}

def svg_techno(lang):
    L = TXT_T[lang]
    noms = {t["id"]: (t["nom"] if lang == "fr" else t.get("nom_en", t["nom"])) for t in TECH}
    par_ligne, W, cw, ch = 3, 640, 640 / 3, 150
    Hh = ((len(techno) + par_ligne - 1) // par_ligne) * ch + 4
    o = [f'<svg class="graphique" viewBox="0 0 {W} {Hh:.0f}" role="img" aria-labelledby="tt-t-{lang} tt-d-{lang}">',
         f'<title id="tt-t-{lang}">{L["t"]}</title><desc id="tt-d-{lang}">{L["d"]}</desc>', CS]
    for i, t in enumerate(techno):
        ox, oy = cw * (i % par_ligne), ch * (i // par_ligne)
        g, d, h, b = ox + 30, ox + cw - 10, oy + 26, oy + ch - 26
        a0 = min(t["premiere"]["annee"], t["annee_jalon"] or 9999) - 3
        a1 = max(a0 + 12, (t["a90"] or t["premiere"]["annee"]) + 3)
        a1 = min(a1, ANNEES[-1])
        xs = lambda a: g + (a - a0) / (a1 - a0) * (d - g)
        ys = lambda v: b - v * (b - h)
        o.append(f'<text class="cp-f" x="{g}" y="{oy + 16}">{esc(noms[t["id"]])}</text>')
        if t["exclusivite"]:
            x1, x2 = xs(t["premiere"]["annee"] - 0.5), xs(t["premiere"]["annee"] + t["exclusivite"] - 0.5)
            o.append(f'<rect class="cp-dom" style="opacity:.18" x="{x1:.1f}" y="{h}" width="{x2 - x1:.1f}" height="{b - h}"><title>{L["seul"]}</title></rect>')
        for v in (0, 0.5, 1):
            o.append(f'<line class="cp-g" x1="{g}" x2="{d}" y1="{ys(v):.1f}" y2="{ys(v):.1f}"/>'
                     f'<text class="cp-t" style="font-size:10px" x="{g - 4}" y="{ys(v) + 3:.1f}" text-anchor="end">{round(v * 100)}</text>')
        if t["annee_jalon"] and a0 <= t["annee_jalon"] <= a1:
            o.append(f'<line class="cp-a" style="stroke-width:1.5" x1="{xs(t["annee_jalon"]):.1f}" x2="{xs(t["annee_jalon"]):.1f}" y1="{h}" y2="{b}"/>')
        pas = 5 if a1 - a0 > 12 else 2
        for a in range(a0 + (-a0) % pas, a1 + 1, pas):
            o.append(f'<text class="cp-t" style="font-size:10px" x="{xs(a):.1f}" y="{b + 13}" text-anchor="middle">{a}</text>')
        pts = [(xs(x["annee"]), ys(x["part"]), x) for x in t["serie"] if a0 <= x["annee"] <= a1]
        o.append(f'<polyline class="cp-c" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y, _ in pts)}"/>')
        for x, y, e in pts:
            o.append(f'<circle class="cp-p" cx="{x:.1f}" cy="{y:.1f}" r="2.5"><title>{e["annee"]} : {round(e["part"] * 100)}{L["pc"]}</title></circle>')
    o.append("</svg>")
    return "".join(o)

if techno:
    for lang in ("fr", "en"):
        open(f"_includes/domination/technologies-{lang}.svg", "w", encoding="utf-8").write(svg_techno(lang) + "\n")

# --- Pneumatiques : la domination des manufacturiers ----------------------------------------------
# _data/pneus.yml (saisi à la main, sourcé) : monopoles (un seul fournisseur imposé) et, hors
# monopole, le manufacturier de chaque écurie qui a gagné ou signé une pole. Les saisons de monopole
# sont hors concours : elles ne comptent ni comme dominantes ni comme creuses (elles coupent une suite).
PN = yaml.safe_load(open("_data/pneus.yml", encoding="utf-8")) if os.path.exists("_data/pneus.yml") else None
MARQUES = ["Pirelli", "Firestone", "Dunlop", "Goodyear", "Michelin", "Bridgestone"]   # ordre fixe des couleurs

def pneus_de(a, c, gp, role="victoire"):
    """Manufacturier de la voiture c (role : victoire ou pole) au GP gp de la saison a."""
    for m in PN["monopoles"]:
        if m["de"] <= a <= m["a"]:
            return m["pneus"]
    ec = cle_ecurie(c).lstrip("~")
    for x in PN["cas"]:
        if x["annee"] == a and x["ecurie"].lstrip("~") == ec and x.get("equipe", c["equipe"]) == c["equipe"]:
            for e in x.get("exceptions") or []:
                if e["gp"] == gp and e.get("pour", role) == role:
                    return e["pneus"]
            m = x["pneus"]
            gps = [k["gp"] for k in next(s for s in R if s["annee"] == a)["courses"]]
            for ch in x.get("changements") or []:
                if ch["des"] not in gps:
                    sys.exit(f"pneus : {a} {ec} : GP « {ch['des']} » inconnu")
                if gps.index(gp) >= gps.index(ch["des"]):
                    m = ch["pneus"]
            return m
    sys.exit(f"pneus : écurie non classée ({a}, {gp}, {c['equipe']})")

pneus_out = None
if PN:
    mono = {a for m in PN["monopoles"] for a in range(m["de"], m["a"] + 1)}
    pn_saisons, pv, pp, pch = [], {}, {}, {}
    for s in R:
        a = s["annee"]
        v, po = collections.Counter(), collections.Counter()
        for c in s["courses"]:
            v[pneus_de(a, c, c["gp"])] += 1
            if c.get("pole"):
                po[pneus_de(a, c["pole"], c["gp"], "pole")] += 1
        pv[a] = {k: x / s["gp"] for k, x in v.items()}
        pp[a] = {k: x / s["gp"] for k, x in po.items()}
        # Manufacturier du champion : celui de l'écurie championne (avant 1958, de l'écurie du champion).
        ce = champion["ecurie"][a]
        cc = next((c for c in s["courses"] if cle_ecurie(c) == ce), None) or \
             next((c["pole"] for c in s["courses"] if c.get("pole") and cle_ecurie(c["pole"]) == ce), None)
        pch[a] = pneus_de(a, cc, next(k["gp"] for k in s["courses"] if cle_ecurie(k) == ce or
                                      (k.get("pole") and cle_ecurie(k["pole"]) == ce))) if cc else None
        pn_saisons.append({"annee": a, "monopole": a in mono, "victoires": {k: round(x, 3) for k, x in sorted(pv[a].items())},
                           "poles": {k: round(x, 3) for k, x in sorted(pp[a].items())}, "champion": pch[a]})
    def suites_pn(seuil, creux):
        out = {}
        for m in {k for a in pv for k in pv[a]}:
            dom = [a for a in ANNEES if a not in mono and (pch[a] == m or pv[a].get(m, 0) >= seuil)]
            g, res = [], []
            for a in dom:
                # Une saison de monopole entre deux saisons dominantes coupe la suite.
                if g and (a - g[-1] > creux + 1 or any(y in mono for y in range(g[-1] + 1, a))):
                    res.append(g); g = []
                g.append(a)
            out[m] = res + ([g] if g else [])
        return out
    base = suites_pn(SEUIL, CREUX)
    var = [suites_pn(sv, cv) for sv, _, cv in VARIANTES]
    periodes = []
    for m, gs in base.items():
        for g in gs:
            rob = len(g) >= MIN and all(any(len(x) >= MIN and x[0] <= g[-1] and g[0] <= x[-1] for x in v.get(m, [])) for v in var)
            span = [a for a in range(g[0], g[-1] + 1) if a not in mono]
            periodes.append({"pneus": m, "debut": g[0], "fin": g[-1], "dominantes": len(g),
                             "titres": sum(1 for a in span if pch[a] == m),
                             "victoires": round(sum(pv[a].get(m, 0) for a in span) / len(span), 3),
                             "poles": round(sum(pp[a].get(m, 0) for a in span) / len(span), 3),
                             "degre": "hegemonie" if rob else "domination" if len(g) >= DUO else "saison"})
    periodes.sort(key=lambda x: (x["debut"], x["pneus"]))
    pneus_out = {"monopoles": [{"de": m["de"], "a": m["a"], "pneus": m["pneus"], "nature": m["nature"]} for m in PN["monopoles"]],
                 "periodes": periodes, "saisons": pn_saisons}
    sortie_compteur["pneus"] = pneus_out

TXT_P = {"fr": {"t": "Les manufacturiers de pneus : part des victoires, 1950-2025", "pc": " %", "mono": "monopole",
                "d": "Pour chaque saison, la part des Grands Prix gagnés sur chaque marque de pneus. Hachures : les saisons de fournisseur unique.",
                "autres": "Autres"},
         "en": {"t": "Tyre manufacturers: share of wins, 1950-2025", "pc": "%", "mono": "monopoly",
                "d": "For each season, the share of Grands Prix won on each tyre brand. Hatching: single-supplier seasons.",
                "autres": "Others"}}
COUL_P = dict(zip(MARQUES + ["Autres"], ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6"]))

def svg_pneus(lang):
    L = TXT_P[lang]
    W, Hh, g, d, h, b = 640, 290, 40, 14, 44, 30
    a0, a1 = ANNEES[0] - 0.5, ANNEES[-1] + 0.5
    bw = (W - g - d) / (a1 - a0)
    xs = lambda a: g + (a - a0) * bw
    ys = lambda v: Hh - b - v * (Hh - b - h)
    o = [f'<svg class="graphique" viewBox="0 0 {W} {Hh}" role="img" aria-labelledby="pn-t-{lang} pn-d-{lang}">',
         f'<title id="pn-t-{lang}">{L["t"]}</title><desc id="pn-d-{lang}">{L["d"]}</desc>', CS,
         '<defs><pattern id="pn-h" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<line x1="0" y1="0" x2="0" y2="5" stroke="#ffffff" stroke-width="1.6" opacity=".7"/></pattern></defs>']
    # Légende : une case par marque, dans l'ordre fixe, libellés à l'encre du texte.
    lx = g
    for m in MARQUES + ["Autres"]:
        nm = L["autres"] if m == "Autres" else m
        o.append(f'<rect x="{lx}" y="8" width="10" height="10" rx="2" fill="{COUL_P[m]}"/><text class="cp-t" x="{lx + 14}" y="17">{nm}</text>')
        lx += 22 + 7.2 * len(nm)
    for v in (0, 0.5, 1):
        o.append(f'<line class="cp-g" x1="{g}" x2="{W - d}" y1="{ys(v):.1f}" y2="{ys(v):.1f}"/>'
                 f'<text class="cp-t" x="{g - 6}" y="{ys(v) + 4:.1f}" text-anchor="end">{round(v * 100)}</text>')
    for x in pneus_out["saisons"]:
        a, y = x["annee"], ys(0)
        parts = {}
        for m, v in x["victoires"].items():
            parts[m if m in MARQUES else "Autres"] = parts.get(m if m in MARQUES else "Autres", 0) + v
        for m in MARQUES + ["Autres"]:
            v = parts.get(m, 0)
            if not v:
                continue
            hgt = v * (Hh - b - h)
            nm = L["autres"] if m == "Autres" else m
            o.append(f'<rect x="{xs(a) - bw / 2 + 0.6:.1f}" y="{y - hgt + 0.6:.1f}" width="{bw - 1.2:.1f}" height="{max(hgt - 1.2, 0.5):.1f}" fill="{COUL_P[m]}">'
                     f'<title>{a}, {nm} : {round(v * 100)}{L["pc"]}{" · " + L["mono"] if x["monopole"] else ""}</title></rect>')
            if x["monopole"]:
                o.append(f'<rect x="{xs(a) - bw / 2 + 0.6:.1f}" y="{y - hgt + 0.6:.1f}" width="{bw - 1.2:.1f}" height="{max(hgt - 1.2, 0.5):.1f}" fill="url(#pn-h)" pointer-events="none"/>')
            y -= hgt
    for a in range(1950, 2030, 10):
        o.append(f'<text class="cp-t" x="{xs(a):.1f}" y="{Hh - b + 18}" text-anchor="middle">{a}</text>')
    o.append("</svg>")
    return "".join(o)

if pneus_out:
    for lang in ("fr", "en"):
        open(f"_includes/domination/pneus-{lang}.svg", "w", encoding="utf-8").write(svg_pneus(lang) + "\n")

os.makedirs("_includes/compteur", exist_ok=True)
for f in os.listdir("_includes/compteur"):
    os.remove(os.path.join("_includes/compteur", f))
for l in E["lignees"]:
    for lang in ("fr", "en"):
        r = svg_compteur(l["id"], lang)
        if r:
            open(f"_includes/compteur/{l['id']}-{lang}.svg", "w", encoding="utf-8").write(
                f'<div class="compteur">{r[0]}{r[1]}</div>\n')
open("_data/compteur.yml", "w", encoding="utf-8").write(
    "# Compteur de domination des lignées, calculé par outils/domination.py : ne pas modifier à la main.\n"
    "# seuil = valeur d'indice (0-1) qui sépare le mieux les saisons dominantes (titre ou SEUIL des victoires)\n"
    "# des autres, au sens de l'indice de Youden ; lignees = meilleure saison de chaque lignée mesurée.\n"
    + yaml.safe_dump(sortie_compteur, allow_unicode=True, sort_keys=False, width=1000))
print(f"compteur : seuil {SEUIL_INDICE} (Youden {sortie_compteur['youden']}), {len(sortie_compteur['lignees'])} lignées")
