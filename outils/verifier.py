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
        if not j.get("entrees") and not j.get("sources"):
            err(f"{rep_data}/chronologie.yml : jalon {j['id']} sans entrée ni source")
        for e in j.get("entrees", []) or []:
            if e not in ids:
                err(f"{rep_data}/chronologie.yml : jalon {j['id']}, entrée « {e} » inconnue")
        for t in j.get("termes", []) or []:
            if t not in ids_gloss:
                err(f"{rep_data}/chronologie.yml : jalon {j['id']}, terme « {t} » inconnu")
    # contexte de la frise : catégorie connue, liens complets vers des jalons existants, au moins une source
    ids_cat = {c["id"] for c in (chrono or {}).get("categories", [])}
    ids_jal = {j["id"] for j in (chrono or {}).get("jalons", [])}
    ids_meca = {m["id"] for m in (chrono or {}).get("mecanismes", [])}
    ids_preuve = {p["id"] for p in (chrono or {}).get("preuves", [])}
    ids_ctx = {c["id"] for c in (chrono or {}).get("contexte", []) or []}
    for c in (chrono or {}).get("contexte", []) or []:
        if c.get("categorie") not in ids_cat:
            err(f"{rep_data}/chronologie.yml : contexte {c['id']}, catégorie « {c.get('categorie')} » inconnue")
        if "jalons" in c:
            err(f"{rep_data}/chronologie.yml : contexte {c['id']}, ancien champ « jalons » (remplacé par « liens »)")
        for l in c.get("liens", []) or []:
            # un lien vise soit un jalon, soit un autre événement de contexte (mécanisme « declenche »)
            if ("jalon" in l) == ("evenement" in l):
                err(f"{rep_data}/chronologie.yml : contexte {c['id']}, lien sans cible unique (jalon ou evenement)")
            elif "jalon" in l and l["jalon"] not in ids_jal:
                err(f"{rep_data}/chronologie.yml : contexte {c['id']}, jalon « {l.get('jalon')} » inconnu")
            elif "evenement" in l and (l["evenement"] not in ids_ctx or l["evenement"] == c["id"]):
                err(f"{rep_data}/chronologie.yml : contexte {c['id']}, événement « {l.get('evenement')} » inconnu ou lui-même")
            if (l.get("mecanisme") == "declenche") != ("evenement" in l):
                err(f"{rep_data}/chronologie.yml : contexte {c['id']}, « declenche » est réservé aux liens entre événements")
            if l.get("mecanisme") not in ids_meca:
                err(f"{rep_data}/chronologie.yml : contexte {c['id']}, mécanisme « {l.get('mecanisme')} » inconnu")
            if l.get("preuve") not in ids_preuve:
                err(f"{rep_data}/chronologie.yml : contexte {c['id']}, preuve « {l.get('preuve')} » inconnue")
            if not l.get("pourquoi"):
                err(f"{rep_data}/chronologie.yml : contexte {c['id']}, lien vers {l.get('jalon')} sans « pourquoi »")
        if not c.get("sources"):
            err(f"{rep_data}/chronologie.yml : contexte {c['id']} sans source")
    for t in gloss or []:
        for e in t.get("entrees", []):
            if e not in ids:
                err(f"{rep_data}/glossaire.yml : terme {t['id']}, entrée « {e} » inconnue")
    preuves_ok = {p["id"] for p in (chrono or {}).get("preuves", [])}
    for l in lignees or []:
        for i, etape in enumerate(l["etapes"]):
            if not isinstance(etape, dict) or bool(etape.get("entrees")) == bool(etape.get("texte")):
                err(f"{rep_data}/lignees.yml : {l['id']}, étape {i + 1} : « entrees » ou « texte », l'un des deux")
                continue
            for e in etape.get("entrees") or []:
                if e not in ids:
                    err(f"{rep_data}/lignees.yml : {l['id']}, entrée « {e} » inconnue")
            if i == 0:
                continue
            lien = etape.get("lien") or {}
            if lien.get("preuve") not in preuves_ok:
                err(f"{rep_data}/lignees.yml : {l['id']}, étape {i + 1} : preuve « {lien.get('preuve')} » invalide")
            if not lien.get("pourquoi") or not lien.get("sources"):
                err(f"{rep_data}/lignees.yml : {l['id']}, étape {i + 1} : lien sans pourquoi ou sans sources (non publié)")
            for s in lien.get("sources") or []:
                if not s.get("titre") or not str(s.get("url", "")).startswith("http"):
                    err(f"{rep_data}/lignees.yml : {l['id']}, étape {i + 1} : source incomplète")
    # chaque valeur de domaine appartient a une famille du filtre de l'index
    familles = charger_yaml(f"{rep_data}/domaines.yml") if os.path.exists(f"{rep_data}/domaines.yml") else []
    valeurs = {v for fam in familles or [] for v in fam.get("valeurs", [])}
    for f in sorted(os.listdir(coll)):
        fm = corps_par_page.get(f"{coll}/{f}", (None, ""))[0]
        if fm and fm.get("domaine") and fm["domaine"] not in valeurs:
            err(f"{coll}/{f} : domaine « {fm['domaine']} » absent de {rep_data}/domaines.yml (filtre de l'index)")
    # le champ lignees des entrees et les etapes des lignees disent la meme chose
    membres = {l["id"]: {e for et in l["etapes"] if isinstance(et, dict) for e in (et.get("entrees") or [])} for l in lignees or []}
    for f in sorted(os.listdir(coll)):
        fm = corps_par_page.get(f"{coll}/{f}", (None, ""))[0]
        if fm is None:
            continue
        declarees = set(fm.get("lignees") or [])
        reelles = {lid for lid, m in membres.items() if f[:-3] in m}
        if declarees != reelles:
            err(f"{coll}/{f} : lignees {sorted(declarees)} ≠ lignées où l'entrée figure {sorted(reelles)}")

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

# 4 ter. écuries (_data/ecuries.yml) : identifiants cités, saisons, chevauchements dans une lignée,
#        passages justifiés (type, preuve, pourquoi, sources), chaque voiture rattachée à une seule écurie,
#        et même structure dans les deux langues (seuls les textes changent)
_i18n = charger_yaml("_data/i18n.yml") or {}
ids_voitures = {f[:-3] for f in os.listdir("_voitures") if f.endswith(".md")} if os.path.isdir("_voitures") else set()
structures = {}
for lang, rep_data in (("fr", "_data"), ("en", "_data/en")):
    chemin = f"{rep_data}/ecuries.yml"
    if not os.path.exists(chemin):
        err(f"{chemin} absent")
        continue
    E = charger_yaml(chemin) or {}
    ch = charger_yaml(f"{rep_data}/chronologie.yml") or {}
    ids_j = {j["id"] for j in ch.get("jalons", [])}
    ids_p = {p["id"] for p in ch.get("preuves", [])}
    types = set(((_i18n.get(lang) or {}).get("ecuries") or {}).get("types") or {})
    ids_e = ids_par_langue.get(lang, set())
    ecuries = E.get("ecuries") or []
    ids_ec = [e.get("id") for e in ecuries]
    for d in sorted({i for i in ids_ec if ids_ec.count(i) > 1}):
        err(f"{chemin} : écurie « {d} » déclarée deux fois")
    rattachees = {}
    for e in ecuries:
        if not e.get("nom"):
            err(f"{chemin} : écurie {e.get('id')} sans nom")
        if not e.get("sources"):
            err(f"{chemin} : écurie {e.get('id')} sans source pour ses saisons")
        for v in e.get("voitures") or []:
            if v not in ids_voitures:
                err(f"{chemin} : écurie {e['id']}, voiture « {v} » inconnue")
            rattachees.setdefault(v, []).append(e["id"])
        for i in e.get("ingenieurs") or []:
            if i.get("id") not in ids_e:
                err(f"{chemin} : écurie {e['id']}, ingénieur « {i.get('id')} » inconnu")
        for j in e.get("jalons") or []:
            if j not in ids_j:
                err(f"{chemin} : écurie {e['id']}, jalon « {j} » inconnu")
        for src in e.get("sources") or []:
            if not src.get("titre") or not str(src.get("url", "")).startswith("http"):
                err(f"{chemin} : écurie {e['id']}, source incomplète")
    for v in sorted(ids_voitures):
        if len(rattachees.get(v, [])) != 1:
            err(f"{chemin} : la voiture {v} doit être rattachée à une écurie et une seule ({rattachees.get(v, [])})")
    utilisees, signature = set(), []
    ids_l = [l.get("id") for l in E.get("lignees") or []]
    for d in sorted({i for i in ids_l if ids_l.count(i) > 1}):
        err(f"{chemin} : lignée « {d} » déclarée deux fois")
    for l in E.get("lignees") or []:
        segs, prec = l.get("segments") or [], None
        if not l.get("nom") or not segs:
            err(f"{chemin} : lignée {l.get('id')} sans nom ou sans segment")
        for i, sg in enumerate(segs):
            lieu = f"{chemin} : lignée {l.get('id')}, segment {i + 1}"
            if sg.get("ecurie") not in ids_ec:
                err(f"{lieu} : écurie « {sg.get('ecurie')} » inconnue")
            utilisees.add(sg.get("ecurie"))
            de, a = sg.get("de"), sg.get("a")
            if not isinstance(de, int) or not isinstance(a, int) or not 1950 <= de <= a <= 2026:
                err(f"{lieu} : saisons invalides ({de}–{a})")
            elif prec and de <= prec:
                err(f"{lieu} : chevauche le segment précédent")
            prec = a if isinstance(a, int) else prec
            lien = sg.get("lien")
            if i == 0 and lien:
                err(f"{lieu} : le premier segment n'a pas de passage")
            if i > 0:
                lien = lien or {}
                if lien.get("type") not in types:
                    err(f"{lieu} : type de passage « {lien.get('type')} » inconnu")
                if lien.get("preuve") not in ids_p:
                    err(f"{lieu} : preuve « {lien.get('preuve')} » inconnue")
                if not lien.get("pourquoi") or not lien.get("sources"):
                    err(f"{lieu} : passage sans pourquoi ou sans sources (non publié)")
                for src in lien.get("sources") or []:
                    if not src.get("titre") or not str(src.get("url", "")).startswith("http"):
                        err(f"{lieu} : source incomplète")
        if l.get("actuelle") and segs and segs[-1].get("a") != 2026:
            err(f"{chemin} : lignée actuelle {l.get('id')} dont le dernier segment ne va pas jusqu'à 2026")
        signature.append((l.get("id"), bool(l.get("actuelle")),
                          [(sg.get("ecurie"), sg.get("de"), sg.get("a"), (sg.get("lien") or {}).get("type"),
                            (sg.get("lien") or {}).get("preuve"), [x.get("url") for x in (sg.get("lien") or {}).get("sources") or []])
                           for sg in segs]))
    for e in sorted(set(ids_ec) - utilisees):
        err(f"{chemin} : écurie {e} absente de toute lignée")
    structures[lang] = (signature, {e["id"]: (e.get("voitures"), [i.get("id") for i in e.get("ingenieurs") or []], e.get("jalons"),
                                             [x.get("url") for x in e.get("sources") or []]) for e in ecuries})
if len(structures) == 2 and structures["fr"] != structures["en"]:
    err("_data/ecuries.yml et _data/en/ecuries.yml : lignées, saisons, passages, sources ou rattachements différents")

# 5. correspondance entre langues
if "fr" in ids_par_langue and "en" in ids_par_langue:
    for manque in sorted(ids_par_langue["fr"] - ids_par_langue["en"]):
        warn(f"en : pas de traduction pour {manque}")
    for orphelin in sorted(ids_par_langue["en"] - ids_par_langue["fr"]):
        err(f"en : {orphelin} n'existe pas en français")

# 5 bis. contexte de la frise : mêmes événements, et mêmes liens (jalon, mécanisme, preuve), dans les deux langues
_cf = {c["id"]: c for c in (charger_yaml("_data/chronologie.yml") or {}).get("contexte", []) or []}
_ce = {c["id"]: c for c in (charger_yaml("_data/en/chronologie.yml") or {}).get("contexte", []) or []}
for m in sorted(set(_cf) ^ set(_ce)):
    err(f"contexte « {m} » présent dans une seule langue")
def _liens(c):
    return [(l.get("jalon"), l.get("evenement"), l.get("mecanisme"), l.get("preuve")) for l in c.get("liens") or []]
for m in sorted(set(_cf) & set(_ce)):
    if (_cf[m]["annee"], _cf[m]["categorie"], _liens(_cf[m])) != (_ce[m]["annee"], _ce[m]["categorie"], _liens(_ce[m])):
        err(f"contexte « {m} » : année, catégorie ou liens différents entre fr et en")

# 5 ter. appels de source ({% include src.html n="3" %}) : numéro présent dans la liste des sources,
#        sources jamais appelées, et même suite d'appels dans les deux langues
def _appels(corps):
    return [int(x) for n in re.findall(r'\{%-?\s*include\s+src\.html\s+n="([0-9, ]+)"', corps) for x in n.split(",")]
for fr_c, en_c in (("_ingenieurs", "_engineers"), ("_voitures", "_cars")):
    for f in sorted(os.listdir(fr_c)):
        suites = {}
        for chemin in (f"{fr_c}/{f}", f"{en_c}/{f}"):
            fm, corps = corps_par_page.get(chemin, (None, ""))
            if fm is None:
                continue
            nb, appels = len(fm.get("sources") or []), _appels(corps)
            for n in sorted(set(appels)):
                if not 1 <= n <= nb:
                    err(f"{chemin} : appel de source [{n}] hors de la liste ({nb} sources)")
            if appels:
                for n in sorted(set(range(1, nb + 1)) - set(appels)):
                    warn(f"{chemin} : source [{n}] jamais appelée dans le texte")
            suites[chemin] = appels
        if len(suites) == 2 and len(set(map(tuple, suites.values()))) == 2:
            err(f"{fr_c}/{f} : appels de source différents entre fr et en")

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
