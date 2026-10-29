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
    if de > act[0] and de <= ANNEES[-1]:
        mouvements.append({"ingenieur": ing, "ecurie": ec, "type": "arrivee", "annee": de,
                           "avant": part_ecurie(ec, de - AVANT, de - 1), "apres": part_ecurie(ec, de, de + APRES - 1)})
    if a and a < act[-1] and a < ANNEES[-1]:
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
