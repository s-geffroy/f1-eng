# Presentation du classement

Une seule description du deck (`build.js`) produit deux fichiers, en francais et
en anglais (`node build.js <pptx|pdf> <fr|en>` ; les textes passent par `t(fr, en)`) :

- `npm run pptx` : `out/ingenieurs-revolutionnaires-F1.pptx` et
  `out/revolutionary-engineers-F1.pptx` (pptxgenjs, avec les
  notes du presentateur). Hors du site, non versionne.
- `npm run pdf` : `../assets/docs/ingenieurs-revolutionnaires-F1.pdf` et
  `../assets/docs/revolutionary-engineers-F1.pdf`, les fichiers que le site propose
  au telechargement (chacun dans sa langue, cle `url.pdf` de `_data/i18n.yml`). `pdf-recorder.js` rejoue les memes
  appels avec pdfkit ; le PDF embarque les polices, mais pas les notes.

Deux autres scripts :

- `portraits.js` (lance par les commandes ci-dessus) : prepare les portraits
  du deck a partir de `../assets/portraits/` (niveaux de gris, recadrage ;
  visage cible pour les photos de groupe, table `VISAGE`). Les credits sont lus
  dans le front matter des entrees `../_ingenieurs/` (et `../_engineers/` pour le
  deck anglais).
- `npm run cartes` : `cartes.js` dessine les cartes de partage 1200x630 dans
  `../assets/partage/` (une par entree + `defaut.png`), avec pureimage
  (JavaScript pur). A relancer apres une modification d'accroche, de rang ou de
  portrait.
- `npm run images` : `optimiser-images.js` ramene les portraits de `../assets/portraits/`
  a 640 px de large (reencodage en place, avec perte, seulement au-dessus de 640 px ou de
  150 Ko) et produit les vignettes de 480 px des voitures dans `../assets/voitures/vignettes/`
  (regenerees quand l'original est plus recent).

Premiere fois :

    npm ci
    npm run fonts

Node 20 ou plus (`engines` de `package.json`). `fonts.sh` telecharge les polices d'un commit fige
de google/fonts et verifie leur empreinte sha256 : le PDF ne change pas si les polices changent en
amont. `front-matter.js` lit le front matter des fiches (js-yaml), pour `build.js`, `cartes.js` et
`portraits.js`.

Le classement (rang, tier, score, confiance, domaine) est lu dans le front matter des
fiches `../_ingenieurs/` et `../_engineers/` : un changement de classement sur le site passe
dans le deck en relancant `npm run pdf`, et un classement incomplet (rangs 1 a 20) arrete la
construction. Le reste du texte des diapositives (theses, raisons et limites de la
diapositive 17, notes) est ecrit dans `build.js` : a relire a la main apres un tel changement.

Apres une modification : `npm run pdf`, verifier le PDF, puis commit + push --
c'est le push qui publie le nouveau PDF.

Le style suit le site (`assets/css/encyclopedie.css`) : memes couleurs, memes
polices (Barlow Condensed, Spectral). Barlow Condensed n'a pas de fleches : ne
pas en mettre dans un texte de diapositive compose dans cette police.

Ce dossier est exclu du site publie (`exclude:` dans `_config.yml`).
