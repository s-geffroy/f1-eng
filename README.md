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
index.html           accueil : index alphabetique, recherche et filtres
tiers.html           les quatre tiers et leurs membres
lignees.html         filiations techniques (donnees : _data/lignees.yml)
dossiers/index.html  liste des dossiers
404.html             page servie sur une adresse inconnue
_ingenieurs/         une entree par ingenieur  -> /ingenieurs/<id>/
_dossiers/           textes de synthese        -> /dossiers/<id>/
_data/               tiers.yml, lignees.yml
_layouts/            default, entree (cartouche, portrait), dossier
_includes/           lien-entree.html
assets/css/          encyclopedie.css (seule feuille de style, pas de theme)
assets/portraits/    portraits libres de droits (credits dans les entrees)
assets/partage/      cartes de partage 1200x630 (generees par deck/cartes.js)
assets/docs/         presentation PDF telechargeable (generee par deck/)
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
image: "/assets/partage/<id>.png" # carte de partage
redirect_from: "/ingenieurs/2026/10/25/<id>.html"
```

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
Neuf entrees n'ont pas de portrait libre connu ; elles s'affichent sans image.

### Outils (`deck/`)

```bash
cd deck
npm ci && npm run fonts     # premiere fois : dependances et polices du site
npm run pdf                 # assets/docs/ingenieurs-revolutionnaires-F1.pdf
npm run pptx                # deck/out/... .pptx (non versionne, avec notes)
npm run cartes              # assets/partage/*.png
```

Apres une modification d'une entree (accroche, rang, portrait), relancer
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
