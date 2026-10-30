# f1-eng -- Ingenieurs de la F1

Encyclopedie en ligne des vingt ingenieurs qui ont le plus transforme la
conception des Formule 1, classes selon leur influence technique durable et non
selon leur palmares : https://s-geffroy.github.io/f1-eng/

Site **Jekyll** publie par **GitHub Pages**. **Rien n'est heberge ici.**

## Ce que ce depot est

Un espace de travail versionne, isole des autres applications du VPS, avec son
propre Claude Code authentifie. Le site, lui, est construit par GitHub a chaque
`git push` et servi depuis les serveurs de GitHub.

`sudo appctl validate` repondra « 0 service », et c'est normal : `app.yaml` et
`compose.yaml` declarent explicitement qu'il n'y a rien a demarrer.

Si quelqu'un demande de « deployer le site ici », c'est qu'il s'est trompe de
template : `static` est celui d'un site servi par ce VPS.

## Prerequis, a trancher AVANT de creer le depot distant

GitHub Pages est disponible :

- sur un depot **public**, avec un compte **GitHub Free** ;
- sur un depot **prive**, seulement a partir de **GitHub Pro** (payant).

Et dans les deux cas, **le site publie est public**. Un depot prive protege les
sources, pas le site. Restreindre l'acces au site lui-meme demande une
organisation sur GitHub Enterprise Cloud.

C'est a decider avant l'etape « Rattacher un depot GitHub prive ? » de
`workon new` : apres, le depot existe.

## Activer Pages

1. Creer le depot sur GitHub, y pousser ce projet.
2. Depot > **Settings** > **Pages**.
3. **Source** : *Deploy from a branch*.
4. **Branch** : `main`, dossier `/ (root)`.

Aucun workflow GitHub Actions n'est necessaire : le constructeur Jekyll natif
fait le travail. Le modele inverse -- Jekyll 4 et greffons libres, batis par un
workflow de ce depot -- est le template `github-pages-ci` ; les deux s'excluent,
puisqu'ils demandent des reglages differents dans Settings > Pages.

## Publier

Chaque push publie immediatement : verifier le front matter des fichiers
touches avant de pousser.

```bash
git add -A
git commit -m "..."
git push
```

C'est tout. La construction prend une a deux minutes ; son deroulement et ses
echecs sont visibles dans l'onglet **Actions** du depot, meme sans workflow --
le constructeur natif s'y affiche.

## Organisation

```
_config.yml          reglages : url, baseurl, collections, greffons, exclusions
index.html           accueil : portail (ingenieurs, ecuries, voitures), frise des ecuries,
                     frise des dominations, dossiers
ingenieurs.html      index alphabetique des ingenieurs, recherche et filtres
ecuries.html         genealogie des ecuries (donnees : _data/ecuries.yml)
cartes.html          cartes des usines, souffleries et circuits
voitures.html        planche des voitures qui ont fait date
tiers.html           les quatre tiers et leurs membres
lignees.html         filiations techniques (donnees : _data/lignees.yml)
chronologie.html     frise cliquable : innovations et contexte (donnees : _data/chronologie.yml)
glossaire.html       glossaire technique (donnees : _data/glossaire.yml)
recherche.html       recherche (index : recherche.json)
dossiers/index.html  liste des dossiers
404.html             page servie sur une adresse inconnue (bilingue)
en/                  pages anglaises (memes gabarits)
_ingenieurs/         une entree par ingenieur  -> /ingenieurs/<id>/   (en : _engineers/)
_dossiers/           textes de synthese        -> /dossiers/<id>/     (en : _features/)
_voitures/           une entree par voiture    -> /voitures/<id>/     (en : _cars/)
_ecuries/            une fiche par ecurie      -> /ecuries/<id>/      (en : _teams/ ; outils/fiches-ecuries.py)
_data/               donnees : ecuries, chronologie, resultats, domination, i18n... (en : _data/en/)
_layouts/            default, entree, dossier, voiture, ecurie
_includes/           pages/ (corps des pages), frises, genealogie, carte, domination, liens
assets/css/          encyclopedie.css (seule feuille de style, pas de theme)
assets/portraits/    portraits libres de droits (credits dans les entrees)
assets/voitures/     photos libres des voitures, 960 px de large au plus
assets/partage/      cartes de partage 1200x630 (generees par deck/cartes.js)
assets/docs/         presentation PDF telechargeable, fr et en (generee par deck/)
outils/              scripts Python : verifier.py (avant chaque push), releve-resultats.py,
                     domination.py, fiches-ecuries.py, carte-usines.py
deck/                outils Node : presentation .pptx/PDF, cartes de partage
specs/               specifications de travail : jamais versionnees (.gitignore)
```

Il n'y a plus d'articles dates : `_posts/` et `_drafts/` ne servent pas. Les
anciennes adresses du blog (`/classement/2026/10/25/...`,
`/ingenieurs/2026/10/25/...`) redirigent vers les nouvelles grace a
`redirect_from:` dans chaque entree (greffon `jekyll-redirect-from`). Ne pas
retirer ces lignes.

### Une entree (`_ingenieurs/<id>.md`)

Front matter utilise par les gabarits :

```yaml
title: "Chapman, Colin"          # vedette : Nom, Prenom
nom_complet: "Colin Chapman"
nom_tri: "chapman colin"         # tri de l'index
accroche: "..."                  # phrase sous la vedette
rang: 1                          # rang, tier et score : ceux de la spec, a l'identique
tier: A
score: "96,0"
confiance: "Elevee"              # avec ses accents dans le fichier reel
domaine: "Architecture"          # alimente le filtre de l'index
lignees: ["architecture"]        # identifiants de _data/lignees.yml
voir_aussi: ["peter-wright"]     # identifiants d'autres entrees
sources:                         # affichees en marge, sous le cartouche
  - titre: "..."
    url: "https://..."
portrait:                        # facultatif : seulement une image libre verifiee
  fichier: "/assets/portraits/<id>.jpg"
  legende: "..."
  auteur: "..."
  licence: "CC BY-SA 3.0"
  licence_url: "https://..."
  source: "https://commons.wikimedia.org/wiki/File:..."
image: "/assets/partage/<id>.jpg" # carte de partage
redirect_from: "/ingenieurs/2026/10/25/<id>.html"
```

### Deux langues

- Francais (racine) et anglais (`/en/`). Memes gabarits : la langue de la page
  (`lang:`, `en` par defaut sous `en/` et dans les collections anglaises) choisit
  les textes d'interface dans `_data/i18n.yml` et les donnees dans `_data/` ou
  `_data/en/`.
- Contenus anglais : `_engineers/` (-> `/en/engineers/<id>/`), `_features/`
  (-> `/en/features/<id>/`), `_cars/` (-> `/en/cars/<id>/`), `_data/en/*.yml`. **Meme nom de fichier que le
  francais** : c'est ce qui relie une page a sa traduction (selecteur de langue,
  balises hreflang). Pages simples : champ `traduction:` dans le front matter.
- Le contenu des pages Accueil, Ingenieurs, Ecuries, Cartes, Voitures, Tiers, Lignees,
  Chronologie, Glossaire, Dossiers et Recherche est dans `_includes/pages/` ; `index.html`, `en/index.html`, etc. ne
  font que l'inclure.
- Une modification d'entree francaise doit etre reportee dans `_engineers/`.
  `outils/verifier.py` signale les entrees sans traduction.

### Recherche

`/recherche/` et `/en/search/` interrogent un index JSON genere par Jekyll
(`recherche.json`, `en/search.json`, gabarit `_includes/index-recherche.json`) :
entrees, ecuries, voitures, termes du glossaire, jalons et contexte, dossiers de la langue.

### Entrees hors classement

Une entree **sans** `rang:`, `tier:` ni `score:` est hors classement (HC) :
cartouche « Hors classement », marque HC dans l'index (filtre dedie), absente
de la page Tiers et de la suite « rang precedent / suivant », carte de partage
adaptee. Elle documente un acteur cite par les entrees classees, avec les memes
exigences de sources ; le classement des vingt n'en est pas modifie. Champ
`consultation:` pour la date de consultation des sources si elle differe du
9 aout 2026.

### Voitures (`_voitures/<id>.md`)

```yaml
title: "Lotus 78"
nom_tri: "lotus 78"
accroche: "..."
description: "..."
annee: 1977                      # ordre de la planche et suite precedente / suivante
equipe: "Team Lotus"
moteur: "..."
statut: "..."                    # facultatif : a couru, n'a jamais couru...
concepteurs: ["colin-chapman", "Maurice Philippe"]  # identifiant d'entree = lien, sinon texte
termes: ["effet-de-sol"]         # identifiants du glossaire
jalons: ["lotus-78"]             # identifiants de la chronologie
sources: [...]
photo: {fichier, legende, auteur, licence, licence_url, source}  # comme portrait
image: "/assets/partage/voitures/<id>.jpg"
```

Les renvois sont calcules : une entree liste les voitures dont `concepteurs`
contient son identifiant ; la chronologie et le glossaire listent les voitures
qui citent le jalon ou le terme. Rien a recopier ailleurs.

### Chronologie et glossaire

- `_data/chronologie.yml` : un jalon = annee, voie (architecture, aero,
  moteur, transmission, methode), titre, texte, entrees, termes. Il ne reprend
  que des faits deja sources dans les entrees citees. Repere rouge si une entree
  du Tier A est citee. La frise est un axe unique (1940-2026) : les jalons
  au-dessus, empiles en rangees (deux reperes a moins de 2 ans changent de rangee).
- Meme fichier, `contexte` : evenements sous l'axe (reglement, securite,
  economie, technologie), masques au chargement et affiches par categorie.
  Un evenement = id (ancre #c-<id>), annee, categorie, titre, texte, liens,
  sources { titre, url }. Chaque evenement a ses propres sources, verifiees par
  citation. Un lien = jalon (ou evenement, pour relier deux evenements de contexte
  avec le mecanisme declenche), mecanisme (ouvre, ferme, contourne, transfert,
  provoque, declenche), preuve (atteste, etabli, discute, chronologique) et pourquoi (une
  phrase justifiee par les sources) ; methode dans `_dossiers/causalite.md`.
  Memes identifiants, annees, categories et liens en fr et en (controle par
  outils/verifier.py).
- `_data/glossaire.yml` : un terme = id (ancre), terme, definition, premiere
  (facultatif), entrees, sources, motifs. Les motifs servent a lier la premiere
  mention du terme dans chaque entree (`[mot]({{ site.baseurl }}/glossaire/#id)`).
- **Toujours mettre les textes YAML entre guillemets** : un « : » non protege
  casse la construction (c'est arrive). Verifier avant de pousser :
  `python3 -c "import yaml,sys;[yaml.safe_load(open(f)) for f in sys.argv[1:]]" _data/*.yml`.

### Domination (`/dossiers/domination/`, ancienne adresse `/dossiers/hegemonies/` redirigee)

- `_data/resultats.yml` : vainqueur, podium et pole de chaque GP, classements finaux 1950-2025,
  releves sur formula1.com par `python3 -I outils/releve-resultats.py <cache hors depot>`
  (environ 2 300 pages de course au premier passage, une heure). Un nom d'equipe inconnu arrete
  le script : completer sa table, ne pas deviner.
- `_data/croisement.yml` : comparaison course par course avec la base Jolpica (ex-Ergast), par
  `python3 -I outils/releve-jolpica.py <cache hors depot>`. Un desaccord est signale, jamais
  corrige : on va voir les deux sources.
- `_data/domination.yml` : calcule par `python3 outils/domination.py` (seuils en tete du script).
  Trois degres : saison dominante (1 saison), domination (2 saisons dominantes ou plus),
  hegemonie (3 ou plus, robuste). Les confrontations portent sur les dominations longues (3 ou plus).
  Les deux fichiers ne s'editent jamais a la main ; relancer les scripts apres une modification
  des ecuries, des ingenieurs ou de la chronologie.
- Tableaux du dossier : `_includes/domination.html`, libelles dans `_data/i18n.yml` (domination).
  Graphiques : `_includes/domination/*.svg`, generes par le meme script (ne pas editer).
- Compteur de domination des fiches ecuries : `_includes/compteur/<lignee>-<langue>.svg` et
  `_data/compteur.yml` (seuil calibre), generes par `outils/domination.py`. Indice composite =
  moyenne des parts de victoires, de poles et de places sur le podium ; ne pas editer.
- `_data/technologies.yml` : saisi a la main, chaque cas source ; technologie de la voiture
  gagnante pendant les fenetres de transition (domination technique). Une victoire non classee
  arrete domination.py.
- Ordre : releve-resultats.py, releve-jolpica.py, domination.py, verifier.py.

### Regles de contenu

- Le contenu publie s'ecrit en francais normal, avec ses accents.
- Rangs, tiers et scores viennent de la specification et ne se modifient pas
  sans demande explicite ; les scores sont un instrument comparatif.
- Chaque fait s'appuie sur une source ouverte et verifiee, citee dans l'entree.
  Pas de fait de memoire.
- Paternite : ne jamais crediter un ingenieur seul d'une realisation
  collective (effet de sol Lotus, DFV, Cooper moteur arriere, Williams active).

### Portraits

Seulement des images reellement libres (domaine public, CC0, CC BY, CC BY-SA,
Art Libre), verifiees une a une sur Wikimedia Commons : bonne personne, licence
et auteur. Le credit (auteur, licence et lien, source) est obligatoire, ainsi
que la mention des modifications (affichage en noir et blanc sur le site,
recadrage dans le deck). Une image « fair use » ou sous droits reserves
demande une autorisation ecrite : citer l'auteur ne suffit pas.
Vingt et une entrees n'ont pas de portrait libre connu ; elles s'affichent sans image.
Memes regles pour les photos de voitures, avec en plus la verification du
modele photographie (categorie Commons, description, image regardee).

### Outils (`deck/`)

```bash
cd deck
npm ci && npm run fonts     # premiere fois : dependances et polices du site
npm run pdf                 # assets/docs/ingenieurs-revolutionnaires-F1.pdf et revolutionary-engineers-F1.pdf
npm run pptx                # deck/out/... .pptx fr et en (non versionnes, avec notes)
npm run cartes              # assets/partage/*.jpg (fr), en/*.jpg, voitures/ et en/voitures/
```

Apres une modification d'une entree ou d'une voiture (accroche, rang, photo), relancer
`npm run cartes` ; apres une modification du deck, `npm run pdf`. Puis commit
+ push. Detail dans `deck/README.md`.

## Domaine personnalise

Saisir le domaine dans **Settings > Pages** : GitHub cree lui-meme le commit du
fichier `CNAME`. Cote DNS, chez le registrar :

- apex (`exemple.fr`) : quatre enregistrements **A** vers `185.199.108.153`,
  `185.199.109.153`, `185.199.110.153`, `185.199.111.153` ;
- sous-domaine (`www`) : un **CNAME** vers `<utilisateur>.github.io`.

Puis cocher **Enforce HTTPS** -- disponible jusqu'a 24 h apres la
configuration, le temps que le certificat soit emis.

**Rien de tout cela ne passe par ce VPS** : ni Traefik, ni `app.yaml`, ni
`app-exposure.py`, ni la zone publique de `/opt/infra/.env`.

Ne pas oublier de vider `baseurl` dans `_config.yml` en meme temps.

## Ce que le constructeur natif ne sait pas faire

- Il tourne en **safe mode** : les greffons deposes dans `_plugins/` sont
  **ignores**, sans erreur ni avertissement.
- Seule la liste blanche de <https://pages.github.com/versions.json> est
  chargeable -- `jekyll-feed`, `jekyll-seo-tag`, `jekyll-sitemap`,
  `jekyll-redirect-from`, `jekyll-remote-theme` et quelques autres.
- La version de Jekyll est **3.10**, pas Jekyll 4. Les recettes du web qui
  supposent Jekyll 4 ne marchent pas ici.
- Pour changer de theme sans sortir du constructeur natif : `remote_theme:`,
  qui est dans la liste blanche.

## Commandes

`sudo appctl validate` repond « 0 service » ; `build`, `up`, `down`, `rebuild`
et `restart` sortent en 0 sans rien faire.
