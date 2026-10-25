#!/usr/bin/env python3
"""Contrôle du site avant publication : ce que GitHub Pages refuserait (ou publierait cassé)
sans message visible ici. Usage : python3 outils/verifier.py   (code de sortie 1 si erreur).

Vérifie : YAML des données et de la config ; front matter de toutes les pages ; champs des
entrées (classées ou hors classement) ; cibles des {% link %} et {% include %} ; identifiants
cités par les données (entrées, termes, lignées) ; ancres du glossaire citées dans les textes ;
fichiers d'images ; correspondance des entrées entre langues."""
import os, re, sys, glob
import yaml

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE)
erreurs, avertissements = [], []
err = erreurs.append
warn = avertissements.append

# langue -> (collection d'entrées, collection de dossiers, dossier de données, préfixe du glossaire)
LANGUES = {
    "fr": ("_ingenieurs", "_dossiers", "_data", "/glossaire/#"),
    "en": ("_engineers", "_features", "_data/en", "/en/glossary/#"),
}

def charger_yaml(chemin):
    try:
        return yaml.safe_load(open(chemin, encoding="utf-8"))
    except Exception as e:
        err(f"{chemin} : YAML invalide ({str(e).splitlines()[0]})")
        return None

def front_matter(chemin):
    texte = open(chemin, encoding="utf-8").read()
    if not texte.startswith("---\n"):
        return None, texte
    try:
        _, fm, corps = texte.split("---\n", 2)
    except ValueError:
        err(f"{chemin} : front matter non refermé")
        return None, texte
    try:
        return (yaml.safe_load(fm) or {}), corps
    except Exception as e:
        err(f"{chemin} : front matter invalide ({str(e).splitlines()[0]})")
        return None, corps

# 1. données et configuration
for f in ["_config.yml"] + glob.glob("_data/**/*.yml", recursive=True):
    charger_yaml(f)

# 2. toutes les pages du site (hors dossiers exclus)
EXCLUS = ("_site", "deck", "outils", "specs", "node_modules", ".git", "vendor")
pages = [p for p in glob.glob("**/*.*", recursive=True)
         if p.endswith((".md", ".html")) and not p.startswith(EXCLUS) and p not in ("README.md", "CLAUDE.md")]
corps_par_page = {}
for p in pages:
    fm, corps = front_matter(p)
    corps_par_page[p] = (fm, corps)

# 3. liens et inclusions Liquid
for p, (fm, corps) in corps_par_page.items():
    for cible in re.findall(r"\{%\s*link\s+(\S+)\s*%\}", corps):
        if not os.path.exists(cible):
            err(f"{p} : lien vers un fichier absent ({cible})")
    for inc in re.findall(r"\{%\s*include\s+(\S+)", corps):
        if not os.path.exists(f"_includes/{inc}"):
            err(f"{p} : inclusion absente (_includes/{inc})")
for p in glob.glob("_layouts/*.html") + glob.glob("_includes/*.html"):
    for inc in re.findall(r"\{%-?\s*include\s+(\S+)", open(p, encoding="utf-8").read()):
        if not os.path.exists(f"_includes/{inc}"):
            err(f"{p} : inclusion absente (_includes/{inc})")

# 4. par langue : entrées, données, ancres
ids_par_langue = {}
for lang, (coll, coll_doss, rep_data, prefixe_gloss) in LANGUES.items():
    if not os.path.isdir(coll):
        if lang != "fr":
            warn(f"{lang} : collection {coll} absente")
        continue
    ids = {f[:-3] for f in os.listdir(coll) if f.endswith(".md")}
    ids_par_langue[lang] = ids
    gloss = charger_yaml(f"{rep_data}/glossaire.yml") if os.path.exists(f"{rep_data}/glossaire.yml") else []
    chrono = charger_yaml(f"{rep_data}/chronologie.yml") if os.path.exists(f"{rep_data}/chronologie.yml") else {}
    lignees = charger_yaml(f"{rep_data}/lignees.yml") if os.path.exists(f"{rep_data}/lignees.yml") else []
    ids_gloss = {t["id"] for t in (gloss or [])}
    ids_lignees = {l["id"] for l in (lignees or [])}

    for f in sorted(os.listdir(coll)):
        chemin = f"{coll}/{f}"
        fm, corps = corps_par_page.get(chemin, (None, ""))
        if fm is None:
            continue
        for champ in ("title", "nom_complet", "nom_tri", "accroche", "domaine", "image"):
            if not fm.get(champ):
                err(f"{chemin} : champ « {champ} » manquant")
        classe = [k for k in ("rang", "tier", "score", "confiance") if fm.get(k) is not None]
        if classe and len(classe) != 4:
            err(f"{chemin} : entrée classée incomplète (rang, tier, score, confiance : {classe})")
        for v in fm.get("voir_aussi") or []:
            if v not in ids:
                err(f"{chemin} : voir_aussi « {v} » inconnu")
        for l in fm.get("lignees") or []:
            if l not in ids_lignees:
                err(f"{chemin} : lignée « {l} » inconnue")
        for img in [fm.get("image"), (fm.get("portrait") or {}).get("fichier")]:
            if img and not os.path.exists(img.lstrip("/")):
                err(f"{chemin} : image absente ({img})")
        for ancre in re.findall(re.escape(prefixe_gloss) + r"([a-z0-9-]+)", corps):
            if ancre not in ids_gloss:
                err(f"{chemin} : ancre de glossaire inconnue (#{ancre})")
    for j in (chrono or {}).get("jalons", []):
        for e in j.get("entrees", []):
            if e not in ids:
                err(f"{rep_data}/chronologie.yml : jalon {j['id']}, entrée « {e} » inconnue")
        for t in j.get("termes", []) or []:
            if t not in ids_gloss:
                err(f"{rep_data}/chronologie.yml : jalon {j['id']}, terme « {t} » inconnu")
    for t in gloss or []:
        for e in t.get("entrees", []):
            if e not in ids:
                err(f"{rep_data}/glossaire.yml : terme {t['id']}, entrée « {e} » inconnue")
    for l in lignees or []:
        for etape in l["etapes"]:
            for e in etape:
                if re.fullmatch(r"[a-z0-9-]+", str(e)) and e not in ids:
                    warn(f"{rep_data}/lignees.yml : « {e} » n'est pas une entrée (texte libre ?)")

# 4 bis. voitures : identifiants cités (termes, jalons, concepteurs) et images
for lang, (coll_v, rep_data) in {"fr": ("_voitures", "_data"), "en": ("_cars", "_data/en")}.items():
    if not os.path.isdir(coll_v):
        continue
    gl = charger_yaml(f"{rep_data}/glossaire.yml") or []
    ch = charger_yaml(f"{rep_data}/chronologie.yml") or {}
    ids_g, ids_j = {t["id"] for t in gl}, {j["id"] for j in ch.get("jalons", [])}
    ids_e = ids_par_langue.get(lang, set())
    for f in sorted(os.listdir(coll_v)):
        chemin = f"{coll_v}/{f}"
        fm, _ = corps_par_page.get(chemin, (None, ""))
        if fm is None:
            continue
        for champ in ("title", "nom_tri", "accroche", "annee", "equipe", "moteur", "image"):
            if not fm.get(champ):
                err(f"{chemin} : champ « {champ} » manquant")
        for t in fm.get("termes") or []:
            if t not in ids_g: err(f"{chemin} : terme « {t} » inconnu")
        for j in fm.get("jalons") or []:
            if j not in ids_j: err(f"{chemin} : jalon « {j} » inconnu")
        for c in fm.get("concepteurs") or []:
            if re.fullmatch(r"[a-z0-9-]+", c) and c not in ids_e:
                err(f"{chemin} : concepteur « {c} » ressemble à un identifiant mais n'est pas une entrée")
        for img in [fm.get("image"), (fm.get("photo") or {}).get("fichier")]:
            if img and not os.path.exists(img.lstrip("/")):
                err(f"{chemin} : image absente ({img})")
    if lang == "en" and os.path.isdir("_voitures"):
        fr_v = {f for f in os.listdir("_voitures")}; en_v = set(os.listdir(coll_v))
        for m in sorted(fr_v - en_v): warn(f"en : pas de traduction pour la voiture {m[:-3]}")
        for o in sorted(en_v - fr_v): err(f"en : la voiture {o[:-3]} n'existe pas en français")

# 5. correspondance entre langues
if "fr" in ids_par_langue and "en" in ids_par_langue:
    for manque in sorted(ids_par_langue["fr"] - ids_par_langue["en"]):
        warn(f"en : pas de traduction pour {manque}")
    for orphelin in sorted(ids_par_langue["en"] - ids_par_langue["fr"]):
        err(f"en : {orphelin} n'existe pas en français")

# 6. synchronisation : une traduction plus ancienne que son original français est signalée
#    (date du dernier commit qui touche le fichier ; date du fichier s'il a des modifications non commitées)
import subprocess
def date_modif(chemin):
    sale = subprocess.run(["git", "status", "--porcelain", "--", chemin], capture_output=True, text=True).stdout.strip()
    if sale:
        return os.path.getmtime(chemin)
    sortie = subprocess.run(["git", "log", "-1", "--format=%ct", "--", chemin], capture_output=True, text=True).stdout.strip()
    return float(sortie) if sortie else os.path.getmtime(chemin)

PAIRES = [("_ingenieurs", "_engineers"), ("_dossiers", "_features"), ("_voitures", "_cars")]
couples = []
for fr_dir, en_dir in PAIRES:
    if os.path.isdir(fr_dir) and os.path.isdir(en_dir):
        couples += [(f"{fr_dir}/{f}", f"{en_dir}/{f}") for f in os.listdir(fr_dir) if os.path.exists(f"{en_dir}/{f}")]
for f in os.listdir("_data"):
    if f.endswith(".yml") and os.path.exists(f"_data/en/{f}"):
        couples.append((f"_data/{f}", f"_data/en/{f}"))
for fr, en in sorted(couples):
    if date_modif(fr) > date_modif(en) + 60:
        warn(f"traduction à mettre à jour : {fr} a été modifié après {en}")

for a in avertissements:
    print("attention :", a)
for e in erreurs:
    print("ERREUR :", e)
print(f"{len(pages)} pages contrôlées, {len(erreurs)} erreur(s), {len(avertissements)} avertissement(s).")
sys.exit(1 if erreurs else 0)
