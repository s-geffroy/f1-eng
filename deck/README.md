# Presentation du classement

Une seule description du deck (`build.js`) produit deux fichiers :

- `npm run pptx` : `out/ingenieurs-revolutionnaires-F1.pptx` (pptxgenjs, avec les
  notes du presentateur). Hors du site, non versionne.
- `npm run pdf` : `../assets/docs/ingenieurs-revolutionnaires-F1.pdf`, le fichier
  que le site propose au telechargement. `pdf-recorder.js` rejoue les memes
  appels avec pdfkit ; le PDF embarque les polices, mais pas les notes.

Premiere fois :

    npm ci
    npm run fonts

Apres une modification : `npm run pdf`, verifier le PDF, puis commit + push --
c'est le push qui publie le nouveau PDF.

Le style suit le site (`assets/css/encyclopedie.css`) : memes couleurs, memes
polices (Barlow Condensed, Spectral). Barlow Condensed n'a pas de fleches : ne
pas en mettre dans un texte de diapositive compose dans cette police.

Ce dossier est exclu du site publie (`exclude:` dans `_config.yml`).
