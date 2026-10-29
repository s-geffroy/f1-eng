#!/usr/bin/env python3
"""Hégémonies : périodes de domination des écuries, lignées, pilotes et motoristes, et leur
confrontation aux jalons de la chronologie, aux arrivées et départs d'ingénieurs et aux changements
de règlement. Lit _data/resultats.yml, _data/ecuries.yml, _data/chronologie.yml ; écrit
_data/hegemonies.yml (chiffres communs aux deux langues, page /dossiers/hegemonies/).
Usage : python3 outils/hegemonies.py   (à relancer après outils/releve-resultats.py)

Une saison est « dominante » pour une entité si elle y est championne ou gagne au moins SEUIL des
Grands Prix. Une hégémonie compte au moins MIN saisons dominantes, séparées au plus par CREUX
saison non dominante. Les mêmes calculs sont refaits avec des seuils plus stricts ou plus lâches
(VARIANTES) : une hégémonie retrouvée dans toutes les variantes est dite robuste."""
import os, collections
import yaml

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE)
SEUIL, MIN, CREUX = 0.40, 3, 1
VARIANTES = [(0.50, 3, 1), (0.40, 2, 1), (0.40, 3, 0)]
AVANT, APRES = 2, 3          # fenêtres des confrontations (saisons)
FENETRE_JALON = 2            # une hégémonie « suit » un jalon si elle commence de Y à Y+2
FENETRE_REGLE = 1            # règlement dans l'année qui précède ou de l'année même

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
        v["pilote"][c["vainqueur"]] += 1
        if c.get("motoriste"):
            v["motoriste"][c["motoriste"]] += 1
    for u in part:
        victoires[u][a] = dict(v[u])
        part[u][a] = {k: x / n for k, x in v[u].items()}
    sa = SAISONS[a]
    champion["pilote"][a] = sa.get("pilote")
    if sa.get("constructeurs"):
        champion["ecurie"][a] = sa["constructeurs"]
        champion["motoriste"][a] = s["constructeurs"][0].get("motoriste")
    else:
        # Avant 1958, pas de titre constructeurs : l'écurie du champion du monde en tient lieu.
        champion["ecurie"][a] = sa.get("pilote_ecurie") or "~" + sa.get("pilote_equipe", "")
        ch = next(c for c in s["courses"] if cle_ecurie(c) == champion["ecurie"][a])
        champion["motoriste"][a] = ch.get("motoriste")
    ce = champion["ecurie"][a]
    champion["lignee"][a] = lignee(ce, a) if not ce.startswith("~") else ce
    tot = sum(p["points"] for p in s["pilotes"])
    points["pilote"][a] = {p["pilote"]: p["points"] / tot for p in s["pilotes"]}
    if s.get("constructeurs"):
        tc = sum(c["points"] for c in s["constructeurs"])
        points["ecurie"][a] = {c["ecurie"]: c["points"] / tc for c in s["constructeurs"] if c.get("ecurie")}

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
REGLES = [x for x in C["contexte"] if x["categorie"] == "reglement"]

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

hegemonies, courtes, liste_ecurie = {}, {}, []
for u in part:
    base = detecter(u, SEUIL, MIN, CREUX)
    variantes = [detecter(u, *v) for v in VARIANTES]
    hs = []
    for k, g in sorted(base, key=lambda x: (x[1][0], x[0])):
        debut, fin = g[0], g[-1]
        span = range(debut, fin + 1)
        vic = sum(victoires[u][a].get(k, 0) for a in span)
        gp = sum(next(s["gp"] for s in R if s["annee"] == a) for a in span)
        h = {"unite": u, "id": k.lstrip("~") if not k.startswith("~") else None, "nom": nom(u, k),
             "debut": debut, "fin": fin, "saisons": fin - debut + 1, "dominantes": len(g),
             "titres": sum(1 for a in span if champion[u].get(a) == k),
             "victoires": vic, "gp": gp, "part": round(vic / gp, 3),
             "part_max": round(max(part[u][a].get(k, 0) for a in span), 3),
             "robuste": all(recouvre(k, g, v) for v in variantes)}
        if h["id"] is None: del h["id"]
        if u in points and points[u]:
            pts = [points[u][a].get(k) for a in span if a in points[u]]
            if pts and all(p is not None for p in pts):
                h["points"] = moyenne(pts)
        # Associés : motoristes d'une écurie, écuries d'un pilote ou d'un motoriste.
        asso = collections.Counter()
        for a in span:
            for c in next(s for s in R if s["annee"] == a)["courses"]:
                cle = {"ecurie": cle_ecurie(c), "pilote": c["vainqueur"], "motoriste": c.get("motoriste"),
                       "lignee": lignee(c["ecurie"], a) if c.get("ecurie") else cle_ecurie(c)}[u]
                if cle == k:
                    autre = c.get("motoriste") if u in ("ecurie", "lignee") else cle_ecurie(c)
                    if autre: asso[autre] += 1
        h["associes"] = [x for x, _ in asso.most_common()]
        h["regles_debut"] = regles_autour(debut)
        h["regles_fin"] = [x["id"] for x in REGLES if fin <= x["annee"] <= fin + FENETRE_REGLE]
        if u == "ecurie" and not k.startswith("~"):
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
    hegemonies[u] = hs
    # Dominations de deux saisons seulement : hors hégémonie, mais citées par le dossier.
    courtes[u] = [{"nom": nom(u, k), "debut": g[0], "fin": g[-1], "titres": sum(1 for a in g if champion[u].get(a) == k),
                   **({"id": k} if not k.startswith("~") else {})}
                  for k, g in sorted(detecter(u, SEUIL, 2, CREUX), key=lambda x: (x[1][0], x[0]))
                  if not recouvre(k, g, base)]

def debut_suit(ec, y):
    return any(e == ec and y <= d <= y + FENETRE_JALON for e, d, f in liste_ecurie)

def pendant(ec, y):
    return any(e == ec and d < y <= f for e, d, f in liste_ecurie)

# --- Confrontation 1 : jalons ------------------------------------------------------------------
jalons, obs, attendu = [], [], []
for jid, ecs in JALON_ECURIES.items():
    j = JALONS[jid]
    y = j["annee"]
    for ec in ecs:
        statut = "pendant" if pendant(ec, y) else "ouvre" if debut_suit(ec, y) else "sans"
        jalons.append({"jalon": jid, "annee": y, "ecurie": ec, "avant": part_ecurie(ec, y - AVANT, y - 1),
                       "apres": part_ecurie(ec, y, y + APRES - 1), "statut": statut})
        if statut != "pendant":
            obs.append(statut == "ouvre")
            # Témoin : même écurie, n'importe quelle saison disputée hors hégémonie.
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

profils_j = [profil(j["ecurie"], j["annee"]) for j in jalons]
profils_t = []
for j in jalons:
    annees_j = {x["annee"] for x in jalons if x["ecurie"] == j["ecurie"]}
    ps = [profil(j["ecurie"], y) for y in actives(j["ecurie"]) if y not in annees_j]
    profils_t.append(moyenne_profils(ps) if ps else [None] * len(K))
etude = {"k": K, "jalons": moyenne_profils(profils_j), "temoin": moyenne_profils(profils_t),
         "n": len(jalons),
         "series": [{"jalon": j["jalon"], "ecurie": j["ecurie"], "annee": j["annee"], "valeurs": p}
                    for j, p in zip(jalons, profils_j)]}

def gain(ec, y):
    av, ap = part_ecurie(ec, y - AVANT, y - 1), part_ecurie(ec, y, y + APRES - 1)
    return None if av is None or ap is None else ap - av

gains_j = [gain(j["ecurie"], j["annee"]) for j in jalons]
gains_t = []
for j in jalons:
    annees_j = {x["annee"] for x in jalons if x["ecurie"] == j["ecurie"]}
    g = [gain(j["ecurie"], y) for y in actives(j["ecurie"])[AVANT:] if y not in annees_j]
    gains_t.append(moyenne([x for x in g if x is not None]))
etude["gain"] = moyenne([g for g in gains_j if g is not None])
etude["gain_temoin"] = moyenne([g for g in gains_t if g is not None])
etude["hausses"] = sum(g > 0.05 for g in gains_j if g is not None)

# Probabilité exacte d'au moins autant d'hégémonies par le seul hasard (loi de Poisson binomiale,
# chaque jalon avec la probabilité de son écurie une saison quelconque).
dist = [1.0]
for p in attendu:
    dist = [a * (1 - p) + b * p for a, b in zip(dist + [0], [0] + dist)]
p_hasard = sum(dist[sum(obs):])

# Par voie de la chronologie.
voies = []
for v in C["voies"]:
    gs = [g for j, g in zip(jalons, gains_j) if JALONS[j["jalon"]]["voie"] == v["id"] and g is not None]
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

# --- Confrontation 3 : règlement ---------------------------------------------------------------
annees_regle = [a for a in ANNEES if regles_autour(a)]
debuts = [h for u in ("ecurie", "pilote", "motoriste") for h in hegemonies[u]]

sortie = {
    "parametres": {"seuil": SEUIL, "min": MIN, "creux": CREUX, "avant": AVANT, "apres": APRES,
                   "fenetre_jalon": FENETRE_JALON, "fenetre_regle": FENETRE_REGLE,
                   "variantes": [{"seuil": s, "min": m, "creux": c} for s, m, c in VARIANTES],
                   "saisons": f"{ANNEES[0]}–{ANNEES[-1]}", "gp": sum(s["gp"] for s in R)},
    "hegemonies": hegemonies,
    "courtes": courtes,
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
entete = ("# Hégémonies et confrontations, calculées par outils/hegemonies.py depuis _data/resultats.yml,\n"
          "# _data/ecuries.yml et _data/chronologie.yml : ne pas modifier à la main, relancer le script.\n"
          "# part = part des Grands Prix gagnés ; points = part moyenne des points (écuries depuis 1958, pilotes) ;\n"
          "# avant / apres = part moyenne des victoires de l'écurie dans les fenêtres de la confrontation.\n")
open("_data/hegemonies.yml", "w", encoding="utf-8").write(
    entete + yaml.safe_dump(sortie, allow_unicode=True, sort_keys=False, width=1000))
for u, hs in hegemonies.items():
    print(f"{u} : {len(hs)} hégémonies, dont {sum(h['robuste'] for h in hs)} robustes")

# --- Graphiques (SVG en ligne, inclus par le dossier ; couleurs et polices du site) ---------------
TEXTES = {
    "fr": {"pc": " %", "x": "Saisons par rapport au jalon", "y": "Part des Grands Prix gagnés",
           "jalon": "saison du jalon", "s1": "Écurie qui innove", "s2": "Même écurie,", "s2b": "saison quelconque",
           "t1": "Part des victoires autour d'un jalon technique",
           "d1": "Moyenne sur {n} jalons : l'écurie qui innove passe d'environ {a} à {b} des victoires, puis revient à son niveau en quatre saisons ; le témoin reste plat.",
           "t2": "Écuries en hausse après un mouvement d'ingénieur, observé et attendu",
           "d2": "Part des cas où la part des victoires de l'écurie monte de plus de 5 points, comparée au témoin apparié sur le niveau de départ.",
           "obs": "observé", "att": "attendu (témoin apparié)",
           "g": {"toutes": "Toutes les arrivées", "tier-a": "Arrivées, Tier A", "tiers-b-c-d": "Arrivées, Tiers B à D",
                 "hc": "Arrivées, hors classement", "departs": "Départs"}},
    "en": {"pc": "%", "x": "Seasons relative to the milestone", "y": "Share of Grands Prix won",
           "jalon": "milestone season", "s1": "Innovating team", "s2": "Same team,", "s2b": "any season",
           "t1": "Share of wins around a technical milestone",
           "d1": "Average over {n} milestones: the innovating team goes from about {a} to {b} of wins, then returns to its level within four seasons; the control stays flat.",
           "t2": "Teams improving after an engineer's move, observed and expected",
           "d2": "Share of cases where the team's share of wins rises by more than 5 points, compared with the control matched on the starting level.",
           "obs": "observed", "att": "expected (matched control)",
           "g": {"toutes": "All arrivals", "tier-a": "Arrivals, Tier A", "tiers-b-c-d": "Arrivals, Tiers B to D",
                 "hc": "Arrivals, unranked", "departs": "Departures"}},
}
STYLE = ("<style>.hg-t{font-family:var(--titre);font-size:14px;fill:var(--mine)}"
         ".hg-f{font-family:var(--titre);font-size:15px;font-weight:600;fill:var(--graphite)}"
         ".hg-g{stroke:#e1e5e7;stroke-width:1}.hg-a{stroke:var(--trait);stroke-width:1}"
         ".hg-1{stroke:#1f5fa8;fill:none;stroke-width:2;stroke-linejoin:round}"
         ".hg-2{stroke:#8e979d;fill:none;stroke-width:2;stroke-dasharray:6 4}"
         ".hg-p1{fill:#1f5fa8;stroke:#fff;stroke-width:2}.hg-p2{fill:#fff;stroke:#8e979d;stroke-width:2}"
         ".hg-l{stroke:#c2c9cc;stroke-width:2}</style>")

def pct(x, lang):
    return f"{round(x * 100)}{TEXTES[lang]['pc']}"

def svg_etude(lang):
    L, W, Hh = TEXTES[lang], 560, 300
    g, d, h, b = 52, 150, 20, 50
    xs = lambda i: g + i * (W - g - d) / (len(K) - 1)
    ys = lambda v: Hh - b - v / 0.35 * (Hh - b - h)
    o = [f'<svg class="graphique" viewBox="0 0 {W} {Hh}" role="img" aria-labelledby="hg-e-t hg-e-d">',
         f'<title id="hg-e-t">{L["t1"]}</title>',
         f'<desc id="hg-e-d">{L["d1"].format(n=etude["n"], a=pct(etude["jalons"][2], lang), b=pct(etude["jalons"][4], lang))}</desc>', STYLE]
    for v in (0, 0.1, 0.2, 0.3):
        o.append(f'<line class="hg-g" x1="{g}" x2="{W - d}" y1="{ys(v):.1f}" y2="{ys(v):.1f}"/>'
                 f'<text class="hg-t" x="{g - 8}" y="{ys(v) + 5:.1f}" text-anchor="end">{pct(v, lang)}</text>')
    for i, k in enumerate(K):
        o.append(f'<text class="hg-t" x="{xs(i):.1f}" y="{Hh - b + 20}" text-anchor="middle">{k:+d}</text>'.replace("+0", "0"))
    x0 = xs(K.index(0))
    o.append(f'<line class="hg-a" x1="{x0:.1f}" x2="{x0:.1f}" y1="{h}" y2="{Hh - b}"/>'
             f'<text class="hg-t" x="{x0 + 6:.1f}" y="{Hh - b - 8}">{L["jalon"]}</text>')
    o.append(f'<text class="hg-t" x="{(g + W - d) / 2:.1f}" y="{Hh - 8}" text-anchor="middle">{L["x"]}</text>')
    o.append(f'<text class="hg-t" transform="translate(14 {(h + Hh - b) / 2:.1f}) rotate(-90)" text-anchor="middle">{L["y"]}</text>')
    for cle, cl, pc in (("temoin", "hg-2", "hg-p2"), ("jalons", "hg-1", "hg-p1")):
        pts = [(xs(i), ys(v)) for i, v in enumerate(etude[cle])]
        o.append(f'<polyline class="{cl}" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}"/>')
        for (x, y), k, v in zip(pts, K, etude[cle]):
            lib = L["s1"] if cle == "jalons" else f'{L["s2"]} {L["s2b"]}'
            o.append(f'<circle class="{pc}" cx="{x:.1f}" cy="{y:.1f}" r="4"><title>{lib}, {k:+d} : {pct(v, lang)}</title></circle>'.replace("+0 :", "0 :"))
    xe = W - d + 10
    ip = max(range(len(K)), key=lambda i: etude["jalons"][i])
    o.append(f'<text class="hg-f" x="{xs(ip) + 10:.1f}" y="{ys(etude["jalons"][ip]) - 8:.1f}">{L["s1"]}</text>')
    yt = ys(etude["temoin"][-1]) - 24
    o.append(f'<text class="hg-t" x="{xe}" y="{yt:.1f}">{L["s2"]}</text><text class="hg-t" x="{xe}" y="{yt + 16:.1f}">{L["s2b"]}</text>')
    o.append("</svg>")
    return "".join(o)

def svg_ingenieurs(lang):
    L, W = TEXTES[lang], 560
    g, d, h, pas = 230, 40, 46, 40
    Hh = h + pas * len(groupes_ing) + 34
    xs = lambda v: g + v * (W - g - d)
    o = [f'<svg class="graphique" viewBox="0 0 {W} {Hh}" role="img" aria-labelledby="hg-i-t hg-i-d">',
         f'<title id="hg-i-t">{L["t2"]}</title><desc id="hg-i-d">{L["d2"]}</desc>', STYLE,
         f'<circle class="hg-p1" cx="{g + 6}" cy="16" r="5"/><text class="hg-t" x="{g + 16}" y="21">{L["obs"]}</text>',
         f'<circle class="hg-p2" cx="{g + 110}" cy="16" r="5"/><text class="hg-t" x="{g + 120}" y="21">{L["att"]}</text>']
    for v in (0, 0.25, 0.5, 0.75, 1):
        o.append(f'<line class="hg-g" x1="{xs(v):.1f}" x2="{xs(v):.1f}" y1="{h - 10}" y2="{Hh - 30}"/>'
                 f'<text class="hg-t" x="{xs(v):.1f}" y="{Hh - 10}" text-anchor="middle">{pct(v, lang)}</text>')
    for i, gr in enumerate(groupes_ing):
        y = h + pas * i + pas / 2
        ob, at = gr["hausse"] / gr["n"], gr["hausse_attendue"] / gr["n"]
        o.append(f'<text class="hg-t" x="{g - 12}" y="{y + 5:.1f}" text-anchor="end">{L["g"][gr["groupe"]]} ({gr["n"]})</text>')
        o.append(f'<line class="hg-l" x1="{xs(at):.1f}" x2="{xs(ob):.1f}" y1="{y:.1f}" y2="{y:.1f}"/>')
        o.append(f'<circle class="hg-p2" cx="{xs(at):.1f}" cy="{y:.1f}" r="5"><title>{L["att"]} : {pct(at, lang)}</title></circle>')
        o.append(f'<circle class="hg-p1" cx="{xs(ob):.1f}" cy="{y:.1f}" r="5"><title>{L["obs"]} : {pct(ob, lang)} ({gr["hausse"]}/{gr["n"]})</title></circle>')
        lx, anc = (xs(ob) + 10, "start") if ob >= at else (xs(ob) - 10, "end")
        o.append(f'<text class="hg-f" x="{lx:.1f}" y="{y + 5:.1f}" text-anchor="{anc}">{pct(ob, lang)}</text>')
    o.append("</svg>")
    return "".join(o)

os.makedirs("_includes/hegemonies", exist_ok=True)
for lang in TEXTES:
    open(f"_includes/hegemonies/etude-jalons-{lang}.svg", "w", encoding="utf-8").write(svg_etude(lang) + "\n")
    open(f"_includes/hegemonies/ingenieurs-{lang}.svg", "w", encoding="utf-8").write(svg_ingenieurs(lang) + "\n")
