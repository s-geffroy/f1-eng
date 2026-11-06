#!/usr/bin/env python3
"""Croisement des résultats avec une seconde source : la base ouverte Jolpica (successeur d'Ergast,
https://api.jolpi.ca/ergast/f1/). Compare, course par course, le vainqueur, le deuxième, le troisième
et la première place de la grille de départ relevés sur formula1.com (_data/resultats.yml), puis,
pour chacun de ces pilotes, son écurie et, quand Jolpica le donne, son motoriste.
Écrit _data/croisement.yml : bilan par champ et chaque désaccord. Rien n'est corrigé : un désaccord
est signalé, on va voir les deux sources, on ne choisit pas en silence.
Usage : python3 -I outils/releve-jolpica.py <dossier-cache>   (après outils/releve-resultats.py)

Le dossier-cache reçoit les réponses de l'API (<annee>-<requete>.json) ; une réponse déjà présente
n'est pas redemandée. Il doit être hors du dépôt. L'API limite le débit : une requête par seconde
et demie au plus."""
import os, re, sys, json, time, unicodedata, urllib.request, urllib.error
import yaml

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE)
API = "https://api.jolpi.ca/ergast/f1"
# Requête Jolpica -> champ comparé. results/N : pilotes classés N-ièmes ; grid/1 : partis en tête.
REQUETES = {"results-1": "vainqueur", "results-2": "deuxieme", "results-3": "troisieme", "grid-1": "pole"}

# Écurie. Jolpica nomme le constructeur (constructorId) : « red_bull », « lotus-climax ». Le préfixe
# avant le tiret, soulignés changés en tirets, doit être l'identifiant de l'écurie du site, sans son
# année de distinction (alfa-romeo-1950 -> alfa-romeo). Correspondances de nom, pas de résultat :
ALIAS_JOLPICA = {"alfa": "alfa-romeo", "lotus": "team-lotus", "leyton": "leyton-house",
                 "larrousse": "lola-larrousse", "rb": "racing-bulls"}
# Écuries que le site distingue et que Jolpica réunit sous un seul constructeur.
MEME_CONSTRUCTEUR = {"frank-williams-racing-cars": "williams", "kick-sauber": "sauber"}
# Motoriste. Jolpica ne l'a pas en champ propre ; il n'apparaît qu'en suffixe du constructeur, pour
# quelques châssis des années 1950-1970 (« cooper-climax », « brabham-repco »). Le suffixe est
# alors l'identifiant du motoriste du site. Ailleurs, le motoriste n'est pas recoupé.

# Désaccords déjà examinés dans les deux sources : (saison, GP, champ) -> constat. Un désaccord absent
# d'ici est signalé à l'écran comme « à examiner ».
EXAMINES = {
    (1983, "Brazil", "troisieme"): "formula1.com laisse vacante la deuxième place de Keke Rosberg, "
        "disqualifié, et classe Niki Lauda troisième ; Jolpica fait remonter chacun d'un rang et classe "
        "Jacques Laffite troisième. Le site suit formula1.com.",
}

def telecharger(cache, annee, req):
    chemin = os.path.join(cache, f"{annee}-{req}.json")
    if not os.path.exists(chemin):
        url = f"{API}/{annee}/{req.replace('-', '/')}{'/results' if req.startswith('grid') else ''}.json?limit=100"
        for essai in range(6):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "f1-eng"}), timeout=60) as r:
                    open(chemin, "wb").write(r.read())
                break
            except urllib.error.HTTPError as e:
                # 429 : l'API demande de ralentir ; on attend de plus en plus longtemps avant de réessayer.
                if e.code != 429 or essai == 5:
                    raise
                time.sleep(30 * (essai + 1))
        time.sleep(1.5)
    return json.load(open(chemin, encoding="utf-8"))["MRData"]["RaceTable"]["Races"]

def cle(nom, homonymes=frozenset()):
    """Nom comparable : sans accents, sans casse, réduit au nom de famille (« Nino Farina » et
    « Giuseppe Farina » désignent le même pilote ; les prénoms varient d'une source à l'autre).
    Nom de famille porté par deux pilotes de la saison (Graham et Damon Hill, Michael et Ralf
    Schumacher) : l'initiale du prénom est ajoutée, pour qu'une inversion soit vue."""
    n = unicodedata.normalize("NFKD", nom).encode("ascii", "ignore").decode().lower()
    mots = [m for m in n.replace("-", " ").split() if m not in ("jr.", "jr", "sr.", "sr")]
    return f"{mots[-1]} {mots[0][0]}" if mots[-1] in homonymes and len(mots) > 1 else mots[-1]

def norm(t):
    return unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()

def ecurie_concorde(entree, cid, annee):
    """L'écurie du site (ou, pour un gagnant sans fiche, son nom formula1.com) et le constructeur
    Jolpica désignent-ils la même équipe ?"""
    base = cid.split("-")[0].replace("_", "-")
    base = ALIAS_JOLPICA.get(base, base)
    if not entree.get("ecurie"):
        return base in norm(entree.get("equipe", "")).replace("-", " ").split()
    e = re.sub(r"-\d{4}$", "", entree["ecurie"])
    return MEME_CONSTRUCTEUR.get(e, e) == base

def homonymes(saison):
    """Noms de famille portés par plusieurs pilotes de la saison (classement et courses)."""
    noms = {p["pilote"] for p in saison.get("pilotes", [])}
    for c in saison["courses"]:
        noms |= {c["vainqueur"], c.get("covainqueur") or c["vainqueur"]} | {p["pilote"] for p in c.get("podium", [])}
        if c.get("pole"): noms.add(c["pole"]["pilote"])
    par_nom = {}
    for n in noms:
        par_nom.setdefault(cle(n), set()).add(n)
    return frozenset(k for k, v in par_nom.items() if len(v) > 1)

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    cache = sys.argv[1]
    os.makedirs(cache, exist_ok=True)
    R = yaml.safe_load(open("_data/resultats.yml", encoding="utf-8"))["saisons"]
    bilan = {c: {"concordants": 0, "desaccords": 0, "absents": 0} for c in REQUETES.values()}
    # Écurie et motoriste : seulement là où le pilote concorde (sinon on comparerait deux voitures).
    bilan["ecurie"] = {"concordants": 0, "desaccords": 0}
    bilan["motoriste"] = {"concordants": 0, "desaccords": 0, "non_renseignes": 0}
    desaccords, saisons_ecartees = [], []
    for s in R:
        a = s["annee"]
        j = {c: {int(x["round"]): x for x in telecharger(cache, a, req)} for req, c in REQUETES.items()}
        manches = sorted(j["vainqueur"])
        h = homonymes(s)
        if len(manches) != s["gp"]:
            # Calendriers différents : la correspondance par ordre ne vaudrait rien.
            saisons_ecartees.append({"annee": a, "formula1": s["gp"], "jolpica": len(manches)})
            continue
        for course, rnd in zip(s["courses"], manches):
            f1 = {"vainqueur": [course["vainqueur"]] + ([course["covainqueur"]] if course.get("covainqueur") else []),
                  "deuxieme": [p["pilote"] for p in course.get("podium", []) if p["place"] == 2],
                  "troisieme": [p["pilote"] for p in course.get("podium", []) if p["place"] == 3],
                  "pole": [course["pole"]["pilote"]] if course.get("pole") else []}
            voiture = {"vainqueur": course, "pole": course.get("pole") or {}}
            for p in course.get("podium", []):
                voiture.setdefault({2: "deuxieme", 3: "troisieme"}[p["place"]], p)
            for c in REQUETES.values():
                jo = j[c].get(rnd)
                noms_j = [f'{x["Driver"]["givenName"]} {x["Driver"]["familyName"]}' for x in jo["Results"]] if jo else []
                if not f1[c] or not noms_j:
                    bilan[c]["absents"] += 1
                elif {cle(n, h) for n in f1[c]} & {cle(n, h) for n in noms_j}:
                    bilan[c]["concordants"] += 1
                    communs = {cle(n, h) for n in f1[c]}
                    cids = sorted({x["Constructor"]["constructorId"] for x in jo["Results"]
                                   if cle(f'{x["Driver"]["givenName"]} {x["Driver"]["familyName"]}', h) in communs})
                    v = voiture[c]
                    if any(ecurie_concorde(v, cid, a) for cid in cids):
                        bilan["ecurie"]["concordants"] += 1
                    else:
                        bilan["ecurie"]["desaccords"] += 1
                        desaccords.append({"annee": a, "gp": course["gp"], "champ": f"ecurie ({c})",
                                           "formula1": v.get("ecurie") or v.get("equipe", ""),
                                           "jolpica": " / ".join(cids), "url": course["url"]})
                    moteurs = {cid.split("-", 1)[1] for cid in cids if "-" in cid}
                    if not moteurs or not v.get("motoriste"):
                        bilan["motoriste"]["non_renseignes"] += 1
                    elif v["motoriste"] in moteurs:
                        bilan["motoriste"]["concordants"] += 1
                    else:
                        bilan["motoriste"]["desaccords"] += 1
                        desaccords.append({"annee": a, "gp": course["gp"], "champ": f"motoriste ({c})",
                                           "formula1": v["motoriste"], "jolpica": " / ".join(sorted(moteurs)),
                                           "url": course["url"]})
                else:
                    bilan[c]["desaccords"] += 1
                    desaccords.append({"annee": a, "gp": course["gp"], "champ": c, "formula1": " / ".join(f1[c]),
                                       "jolpica": " / ".join(noms_j), "url": course["url"]})
    entete = ("# Croisement formula1.com / Jolpica (successeur d'Ergast), calculé par outils/releve-jolpica.py :\n"
              "# ne pas modifier à la main. Comparaison par nom de famille, sans accents (avec l'initiale du prénom\n"
              "# quand deux pilotes de la saison portent le même nom) ; une course comptée\n"
              "# concordante si un pilote est commun aux deux sources (équipages partagés). absents = champ manquant\n"
              "# dans l'une des sources. ecurie et motoriste : comparés là où le pilote concorde ; motoriste\n"
              "# non_renseignes = Jolpica ne le donne pas (hors suffixes « -climax », « -repco »... des années\n"
              "# 1950-1970). Un désaccord est signalé, jamais corrigé ici ; examine = constat après lecture des\n"
              "# deux sources (table EXAMINES du script).\n")
    for d in desaccords:
        if (d["annee"], d["gp"], d["champ"]) in EXAMINES:
            d["examine"] = EXAMINES[(d["annee"], d["gp"], d["champ"])]
    sortie = {"source": API, "bilan": bilan, "saisons_ecartees": saisons_ecartees, "desaccords": desaccords}
    with open("_data/croisement.yml.tmp", "w", encoding="utf-8") as f:
        f.write(entete + yaml.safe_dump(sortie, allow_unicode=True, sort_keys=False, width=1000))
    os.replace("_data/croisement.yml.tmp", "_data/croisement.yml")
    for c, b in bilan.items():
        print(f"{c} : " + ", ".join(f"{n} {k.replace('_', ' ')}" for k, n in b.items()))
    for d in desaccords:
        if "examine" not in d:
            print(f"à examiner : {d['annee']} {d['gp']}, {d['champ']} : formula1.com {d['formula1']}, "
                  f"Jolpica {d['jolpica']}")
    if saisons_ecartees:
        print(f"saisons écartées (calendriers différents) : {saisons_ecartees}")

main()
