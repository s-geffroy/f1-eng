#!/usr/bin/env python3
"""Fiches des écuries : une page par écurie de _data/ecuries.yml, dans les deux langues.
Usage : python3 outils/fiches-ecuries.py   (à relancer après toute modification des écuries)

Le contenu des fiches vient entièrement des données (gabarit _layouts/ecurie.html) : chaque fichier
de _ecuries/ et _teams/ ne porte que son titre, sa clé de tri, ses saisons et sa description. Les fichiers sans
écurie correspondante sont signalés, jamais supprimés (une URL publiée ne disparaît pas sans décision)."""
import os, sys
import yaml

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE)

def fusion(segs):
    """Segments triés par année, les segments contigus fusionnés (une écurie peut figurer dans plusieurs lignées)."""
    out = []
    for s in sorted(segs, key=lambda s: s["de"]):
        if out and s["de"] <= out[-1]["a"] + 1:
            out[-1]["a"] = max(out[-1]["a"], s["a"])
        else:
            out.append({"de": s["de"], "a": s["a"]})
    return out

def saisons(segs):
    return ", ".join(f"{s['de']}" if s["de"] == s["a"] else f"{s['de']}–{s['a']}" for s in fusion(segs))

def pluriel(segs, mot):
    f = fusion(segs)
    return mot if len(f) == 1 and f[0]["de"] == f[0]["a"] else mot + "s"

for lang, donnees, dossier in (("fr", "_data/ecuries.yml", "_ecuries"), ("en", "_data/en/ecuries.yml", "_teams")):
    E = yaml.safe_load(open(donnees, encoding="utf-8"))
    os.makedirs(dossier, exist_ok=True)
    ids = set()
    for e in E["ecuries"]:
        ids.add(e["id"])
        segs = [s for l in E["lignees"] for s in l["segments"] if s["ecurie"] == e["id"]]
        lignee = next(l for l in E["lignees"] if any(s["ecurie"] == e["id"] for s in l["segments"]))
        if lang == "fr":
            desc = f"{e['nom']} : écurie de Formule 1, {pluriel(segs, 'saison')} {saisons(segs)}"
            if len(lignee["segments"]) > 1:
                desc += f" ; lignée {lignee['nom']}"
        else:
            desc = f"{e['nom']}: Formula 1 team, {pluriel(segs, 'season')} {saisons(segs)}"
            if len(lignee["segments"]) > 1:
                desc += f"; lineage {lignee['nom']}"
        fm = {"title": e["nom"], "nom_tri": e["nom"].lower(), "saisons": saisons(segs), "description": desc + "."}
        texte = "---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, width=1000) + "---\n"
        chemin = f"{dossier}/{e['id']}.md"
        if not os.path.exists(chemin) or open(chemin, encoding="utf-8").read() != texte:
            open(chemin, "w", encoding="utf-8").write(texte)
    orphelins = sorted(f[:-3] for f in os.listdir(dossier) if f.endswith(".md") and f[:-3] not in ids)
    for o in orphelins:
        print(f"attention : {dossier}/{o}.md ne correspond plus à aucune écurie (à rediriger ou supprimer sur décision)", file=sys.stderr)
    print(f"{dossier} : {len(ids)} fiches")
