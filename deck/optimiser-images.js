// Allège les portraits du site et produit les vignettes des voitures (fin du fichier). Portraits : 640 px de large au plus (deux fois la largeur d'affichage, pour les
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

  // Vignettes des voitures (planches /voitures/ et accueil, cartes de la généalogie) : 480 px de large,
  // JPEG qualité 78, dans assets/voitures/vignettes/ ; les gabarits les proposent par srcset à côté de
  // l'original. Régénérées si l'original est plus récent que la vignette.
  const SRC = path.join(__dirname, "..", "assets", "voitures"), VIG = path.join(SRC, "vignettes");
  const LARGEUR_VIG = 480, QUALITE_VIG = 78;
  fs.mkdirSync(VIG, { recursive: true });
  let n = 0, poids = 0, orig = 0;
  for (const f of fs.readdirSync(SRC).filter(f => f.endsWith(".jpg"))) {
    const p = path.join(SRC, f), v = path.join(VIG, f);
    orig += fs.statSync(p).size;
    if (!fs.existsSync(v) || fs.statSync(v).mtimeMs < fs.statSync(p).mtimeMs) {
      const img = await Jimp.read(p);
      if (img.bitmap.width > LARGEUR_VIG) img.resize(LARGEUR_VIG, Jimp.AUTO);
      await img.quality(QUALITE_VIG).writeAsync(v);
      n++;
    }
    poids += fs.statSync(v).size;
  }
  for (const f of fs.readdirSync(VIG).filter(f => !fs.existsSync(path.join(SRC, f)))) fs.unlinkSync(path.join(VIG, f));
  console.log(`vignettes : ${n} générées ; ${Math.round(orig / 1024)} Ko d'originaux -> ${Math.round(poids / 1024)} Ko de vignettes`);
})().catch(e => { console.error(e); process.exit(1); });
