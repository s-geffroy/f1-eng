// Allège les portraits du site : 640 px de large au plus (deux fois la largeur d'affichage, pour les
// écrans haute densité), JPEG qualité 80, sans métadonnées EXIF. Idempotent : une image déjà à la bonne
// taille est seulement réencodée si elle pèse plus de 150 Ko.
const fs = require("fs");
const path = require("path");
const Jimp = require("jimp");

const DOSSIER = path.join(__dirname, "..", "assets", "portraits");
const LARGEUR_MAX = 640, QUALITE = 80, POIDS_MAX = 150 * 1024;

(async () => {
  let avant = 0, apres = 0;
  for (const f of fs.readdirSync(DOSSIER).filter(f => f.endsWith(".jpg"))) {
    const p = path.join(DOSSIER, f), t0 = fs.statSync(p).size;
    const img = await Jimp.read(p);
    if (img.bitmap.width <= LARGEUR_MAX && t0 <= POIDS_MAX) { avant += t0; apres += t0; continue; }
    if (img.bitmap.width > LARGEUR_MAX) img.resize(LARGEUR_MAX, Jimp.AUTO);
    await img.quality(QUALITE).writeAsync(p);
    const t1 = fs.statSync(p).size;
    avant += t0; apres += t1;
    console.log(`${f} : ${Math.round(t0 / 1024)} Ko -> ${Math.round(t1 / 1024)} Ko`);
  }
  console.log(`portraits : ${Math.round(avant / 1024)} Ko -> ${Math.round(apres / 1024)} Ko`);
})().catch(e => { console.error(e); process.exit(1); });
