// Prépare les portraits du deck à partir de ceux du site : niveaux de gris (comme le
// filtre CSS du site) et recadrage au format du cadre de diapositive.
// Les crédits sont lus dans le front matter des entrées (_ingenieurs/<id>.md) : une
// seule source pour le site et le deck. Sortie : deck/portraits/ (non versionné).
const fs = require("fs");
const path = require("path");
const Jimp = require("jimp");

const RACINE = path.join(__dirname, "..");
const SORTIE = path.join(__dirname, "portraits");
// cadre des diapositives : 1,8 x 2,45 pouces, rendu à 300 points par pouce environ
const LARGEUR = 540, HAUTEUR = 735;
// Photos de groupe ou en pied : zone du visage, en fractions de l'image (x, y, largeur).
// La hauteur suit le format du cadre. Sur le site, ces photos restent entières.
const VISAGE = {
  "gordon-murray": [0.125, 0.24, 0.40], // à gauche, Le Mans 1996
  "mike-costin": [0.27, 0.31, 0.16],    // à gauche, penché avec des notes, Silverstone 1956
  "rory-byrne": [0.66, 0.08, 0.30],     // à droite, devant la Ferrari
  "tony-rudd": [0.22, 0.04, 0.52],
  "vittorio-jano": [0.17, 0.01, 0.33],  // debout devant l'Alfa Romeo P2
};

function lirePortrait(id) {
  const md = fs.readFileSync(path.join(RACINE, "_ingenieurs", id + ".md"), "utf8");
  const bloc = md.match(/^portrait:\n((?: {2}.+\n)+)/m);
  if (!bloc) return null;
  const p = {};
  for (const l of bloc[1].trim().split("\n")) {
    const m = l.trim().match(/^(\w+): (.*)$/);
    if (m) p[m[1]] = JSON.parse(m[2]);
  }
  return p;
}

async function main() {
  fs.mkdirSync(SORTIE, { recursive: true });
  const credits = {};
  for (const f of fs.readdirSync(path.join(RACINE, "_ingenieurs"))) {
    const id = f.replace(/\.md$/, "");
    const p = lirePortrait(id);
    if (!p) continue;
    const img = await Jimp.read(path.join(RACINE, p.fichier));
    if (VISAGE[id]) {
      const [fx, fy, fw] = VISAGE[id], W = img.bitmap.width, H = img.bitmap.height;
      const w = Math.round(fw * W), h = Math.min(Math.round(w * HAUTEUR / LARGEUR), H - Math.round(fy * H));
      img.crop(Math.round(fx * W), Math.round(fy * H), w, h);
    }
    // recadrage centré horizontalement, calé vers le haut (comme object-position: 50% 20%)
    img.cover(LARGEUR, HAUTEUR, Jimp.HORIZONTAL_ALIGN_CENTER | Jimp.VERTICAL_ALIGN_TOP).greyscale().quality(85);
    await img.writeAsync(path.join(SORTIE, id + ".jpg"));
    credits[id] = { auteur: p.auteur, licence: p.licence, source: p.source };
  }
  fs.writeFileSync(path.join(SORTIE, "credits.json"), JSON.stringify(credits, null, 1));
  console.log("portraits :", Object.keys(credits).join(", "));
}

main().catch(e => { console.error(e); process.exit(1); });
