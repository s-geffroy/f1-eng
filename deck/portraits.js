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
    // recadrage centré horizontalement, calé vers le haut (comme object-position: 50% 20%)
    img.cover(LARGEUR, HAUTEUR, Jimp.HORIZONTAL_ALIGN_CENTER | Jimp.VERTICAL_ALIGN_TOP).greyscale().quality(85);
    await img.writeAsync(path.join(SORTIE, id + ".jpg"));
    credits[id] = { auteur: p.auteur, licence: p.licence, source: p.source };
  }
  fs.writeFileSync(path.join(SORTIE, "credits.json"), JSON.stringify(credits, null, 1));
  console.log("portraits :", Object.keys(credits).join(", "));
}

main().catch(e => { console.error(e); process.exit(1); });
