#!/usr/bin/env python3
"""Croisement des résultats avec une seconde source : la base ouverte Jolpica (successeur d'Ergast,
https://api.jolpi.ca/ergast/f1/). Compare, course par course, le vainqueur, le deuxième, le troisième
et la première place de la grille de départ relevés sur formula1.com (_data/resultats.yml).
Écrit _data/croisement.yml : bilan par champ et chaque désaccord. Rien n'est corrigé : un désaccord
est signalé, on va voir les deux sources, on ne choisit pas en silence.
Usage : python3 -I outils/releve-jolpica.py <dossier-cache>   (après outils/releve-resultats.py)

Le dossier-cache reçoit les réponses de l'API (<annee>-<requete>.json) ; une réponse déjà présente
n'est pas redemandée. Il doit être hors du dépôt. L'API limite le débit : une requête par seconde
et demie au plus."""
import os, sys, json, time, unicodedata, urllib.request
import yaml

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE)
API = "https://api.jolpi.ca/ergast/f1"
# Requête Jolpica -> champ comparé. results/N : pilotes classés N-ièmes ; grid/1 : partis en tête.
REQUETES = {"results-1": "vainqueur", "results-2": "deuxieme", "results-3": "troisieme", "grid-1": "pole"}

def telecharger(cache, annee, req):
    chemin = os.path.join(cache, f"{annee}-{req}.json")
    if not os.path.exists(chemin):
        url = f"{API}/{annee}/{req.replace('-', '/')}{'/results' if req.startswith('grid') else ''}.json?limit=100"
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "f1-eng"}), timeout=60) as r:
            open(chemin, "wb").write(r.read())
        time.sleep(1.5)
    return json.load(open(chemin, encoding="utf-8"))["MRData"]["RaceTable"]["Races"]

def cle(nom):
    """Nom comparable : sans accents, sans casse, réduit au nom de famille (« Nino Farina » et
    « Giuseppe Farina » désignent le même pilote ; les prénoms varient d'une source à l'autre)."""
    n = unicodedata.normalize("NFKD", nom).encode("ascii", "ignore").decode().lower()
    mots = [m for m in n.replace("-", " ").split() if m not in ("jr.", "jr", "sr.", "sr")]
    return mots[-1]

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    cache = sys.argv[1]
    os.makedirs(cache, exist_ok=True)
    R = yaml.safe_load(open("_data/resultats.yml", encoding="utf-8"))["saisons"]
    bilan = {c: {"concordants": 0, "desaccords": 0, "absents": 0} for c in REQUETES.values()}
    desaccords, saisons_ecartees = [], []
    for s in R:
        a = s["annee"]
        j = {c: {int(x["round"]): x for x in telecharger(cache, a, req)} for req, c in REQUETES.items()}
        manches = sorted(j["vainqueur"])
        if len(manches) != s["gp"]:
            # Calendriers différents : la correspondance par ordre ne vaudrait rien.
            saisons_ecartees.append({"annee": a, "formula1": s["gp"], "jolpica": len(manches)})
            continue
        for course, rnd in zip(s["courses"], manches):
            f1 = {"vainqueur": [course["vainqueur"]] + ([course["covainqueur"]] if course.get("covainqueur") else []),
                  "deuxieme": [p["pilote"] for p in course.get("podium", []) if p["place"] == 2],
                  "troisieme": [p["pilote"] for p in course.get("podium", []) if p["place"] == 3],
                  "pole": [course["pole"]["pilote"]] if course.get("pole") else []}
            for c in REQUETES.values():
                jo = j[c].get(rnd)
                noms_j = [f'{x["Driver"]["givenName"]} {x["Driver"]["familyName"]}' for x in jo["Results"]] if jo else []
                if not f1[c] or not noms_j:
                    bilan[c]["absents"] += 1
                elif {cle(n) for n in f1[c]} & {cle(n) for n in noms_j}:
                    bilan[c]["concordants"] += 1
                else:
                    bilan[c]["desaccords"] += 1
                    desaccords.append({"annee": a, "gp": course["gp"], "champ": c, "formula1": " / ".join(f1[c]),
                                       "jolpica": " / ".join(noms_j), "url": course["url"]})
    entete = ("# Croisement formula1.com / Jolpica (successeur d'Ergast), calculé par outils/releve-jolpica.py :\n"
              "# ne pas modifier à la main. Comparaison par nom de famille, sans accents ; une course comptée\n"
              "# concordante si un pilote est commun aux deux sources (équipages partagés). absents = champ manquant\n"
              "# dans l'une des sources. Un désaccord est signalé, jamais corrigé ici.\n")
    sortie = {"source": API, "bilan": bilan, "saisons_ecartees": saisons_ecartees, "desaccords": desaccords}
    open("_data/croisement.yml", "w", encoding="utf-8").write(
        entete + yaml.safe_dump(sortie, allow_unicode=True, sort_keys=False, width=1000))
    for c, b in bilan.items():
        print(f"{c} : {b['concordants']} concordants, {b['desaccords']} désaccords, {b['absents']} absents")
    if saisons_ecartees:
        print(f"saisons écartées (calendriers différents) : {saisons_ecartees}")

main()
