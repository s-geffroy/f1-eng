// Cartes de partage (Open Graph, 1200 x 630) : une par entrée, plus une carte générique.
// Même vocabulaire que le site : papier calque, encre graphite, cartouche, rouge réservé au Tier A.
// Portraits : ceux préparés par portraits.js (niveaux de gris). Sortie : ../assets/partage/
// (versionnée : c'est ce que GitHub Pages sert aux réseaux sociaux).
const fs = require("fs");
const path = require("path");
const PImage = require("pureimage");

const RACINE = path.join(__dirname, "..");
// Une carte par entrée et par langue : français dans assets/partage/, anglais dans assets/partage/en/.
const LANGUES = {
  fr: { entrees: "_ingenieurs", sortie: path.join(RACINE, "assets", "partage"), marque: "Ingénieurs de la F1",
        rang: "Rang", classement: "Classement", hc: "Hors classement", domaine: "Domaine",
        titre: ["Les ingénieurs qui ont", "changé la Formule 1"],
        sous: "Vingt ingénieurs classés selon ce qu'ils ont changé dans la manière de construire une F1, et non selon leur palmarès." },
  en: { entrees: "_engineers", sortie: path.join(RACINE, "assets", "partage", "en"), marque: "F1 Engineers",
        rang: "Rank", classement: "Ranking", hc: "Unranked", domaine: "Field",
        titre: ["The engineers who", "changed Formula 1"],
        sous: "Twenty engineers ranked by what they changed in the way an F1 car is built, not by their trophy count." },
};
let L = LANGUES.fr;
const PORTRAITS = path.join(__dirname, "portraits");
const W = 1200, H = 630, M = 64;
const C = { calque: "#D9DEDF", feuille: "#FFFFFF", graphite: "#2E3338", mine: "#4F575E", trait: "#8E979D", clair: "#C2C9CC",
  A: "#C0182C", B: "#3D5B74", C: "#6E767C", D: "#AEB5BA" };

const police = (f, fam, w, st) => PImage.registerFont(path.join(__dirname, "fonts", f + ".ttf"), fam, w, st, "normal").loadSync();
police("BarlowCondensed-Regular", "Barlow", 400, "normal");
police("BarlowCondensed-Bold", "BarlowB", 700, "normal");
police("Spectral-Italic", "SpectralI", 400, "italic");

// Lit le front matter simple des entrées (clé: valeur sur une ligne, valeurs JSON ou nues).
function frontMatter(file) {
  const fm = fs.readFileSync(file, "utf8").split("---\n")[1];
  const o = {};
  for (const l of fm.split("\n")) {
    const m = l.match(/^(\w+): (.*)$/);
    if (!m) continue;
    try { o[m[1]] = JSON.parse(m[2]); } catch { o[m[1]] = m[2]; }
  }
  return o;
}

function lignes(ctx, texte, largeur) {
  const mots = texte.split(" "), out = [];
  let l = "";
  for (const m of mots) {
    const essai = l ? l + " " + m : m;
    if (ctx.measureText(essai).width > largeur && l) { out.push(l); l = m; } else l = essai;
  }
  if (l) out.push(l);
  return out;
}

function trait(ctx, x1, y1, x2, y2, ep, couleur) {
  ctx.fillStyle = couleur;
  if (y1 === y2) ctx.fillRect(x1, y1 - ep / 2, x2 - x1, ep); else ctx.fillRect(x1 - ep / 2, y1, ep, y2 - y1);
}

function cadre(ctx, x, y, w, h, ep, couleur) {
  ctx.fillStyle = couleur;
  ctx.fillRect(x, y, w, ep); ctx.fillRect(x, y + h - ep, w, ep);
  ctx.fillRect(x, y, ep, h); ctx.fillRect(x + w - ep, y, ep, h);
}

function texte(ctx, t, x, y, fam, taille, couleur) {
  ctx.font = `${taille}pt ${fam}`;
  ctx.fillStyle = couleur;
  ctx.fillText(t, x, y);
}

function enTete(ctx) {
  ctx.fillStyle = C.calque; ctx.fillRect(0, 0, W, H);
  texte(ctx, L.marque, M, 70, "BarlowB", 26, C.graphite);
  trait(ctx, M, 92, W - M, 92, 4, C.graphite);
}

async function ecrire(img, nom) {
  await PImage.encodePNGToStream(img, fs.createWriteStream(path.join(L.sortie, nom)));
}

async function carteEntree(id, e) {
  const img = PImage.make(W, H), ctx = img.getContext("2d");
  enTete(ctx);
  // vue de gauche : portrait, ou initiales s'il n'existe pas d'image libre
  const px = M, py = 130, pw = 330, ph = 449;
  const fichier = path.join(PORTRAITS, id + ".jpg");
  if (fs.existsSync(fichier)) {
    const p = await PImage.decodeJPEGFromStream(fs.createReadStream(fichier));
    ctx.drawImage(p, 0, 0, p.width, p.height, px, py, pw, ph);
  } else {
    ctx.fillStyle = C.clair; ctx.fillRect(px, py, pw, ph);
    const [nom, prenom] = e.title.split(", ");          // vedette « Nom, Prénom »
    const ini = (prenom[0] + nom[0]).toUpperCase();      // Jean-Claude Migeot -> JM, Ettore Zaccone Mina -> EZ
    ctx.font = "96pt BarlowB"; ctx.fillStyle = C.mine;
    ctx.fillText(ini, px + (pw - ctx.measureText(ini).width) / 2, py + ph / 2 + 45);
  }
  cadre(ctx, px, py, pw, ph, 4, C.graphite);

  // vedette, accroche, cartouche
  const tx = px + pw + 48, tw = W - M - tx;
  const [nom, prenom] = e.title.split(", ");
  let taille = 92;
  ctx.font = `${taille}pt BarlowB`;
  while (ctx.measureText(nom + ",").width > tw && taille > 54) { taille -= 4; ctx.font = `${taille}pt BarlowB`; }
  texte(ctx, nom + ",", tx, 205, "BarlowB", taille, C.graphite);
  texte(ctx, prenom, tx, 205 + taille * 0.95, "Barlow", Math.round(taille * 0.7), C.graphite);
  ctx.font = "30pt SpectralI";
  lignes(ctx, e.accroche, tw).slice(0, 2).forEach((l, i) => texte(ctx, l, tx, 345 + i * 40, "SpectralI", 30, C.mine));

  const cy = 450, ch = 130;
  const cases = e.rang
    ? [[L.rang, String(e.rang), 150], ["Tier", e.tier, 150], ["Score", e.score, tw - 300]]
    : [[L.classement, L.hc, tw * 0.55], [L.domaine, e.domaine, tw * 0.45]]; // entrée HC : ni rang, ni tier, ni score
  ctx.fillStyle = C.feuille; ctx.fillRect(tx, cy, tw, ch);
  let x = tx;
  for (const [lab, val, w] of cases) {
    const estTier = lab === "Tier", fg = estTier && e.tier !== "D" ? C.feuille : C.graphite;
    if (estTier) { ctx.fillStyle = C[e.tier]; ctx.fillRect(x, cy, w, ch); }
    if (x > tx) trait(ctx, x, cy, x, cy + ch, 2, C.trait);
    texte(ctx, lab, x + 16, cy + 34, "Barlow", 20, estTier ? fg : C.mine);
    let t = val + (lab === "Score" ? " / 100" : ""), taille = 56;
    ctx.font = `${taille}pt BarlowB`;
    while (ctx.measureText(t).width > w - 32 && taille > 26) { taille -= 2; ctx.font = `${taille}pt BarlowB`; }
    texte(ctx, t, x + 16, cy + 108, "BarlowB", taille, fg);
    x += w;
  }
  cadre(ctx, tx, cy, tw, ch, 4, C.graphite);
  await ecrire(img, id + ".png");
}

async function carteGenerique() {
  const img = PImage.make(W, H), ctx = img.getContext("2d");
  enTete(ctx);
  L.titre.forEach((l, i) => texte(ctx, l, M, 250 + i * 110, "BarlowB", 100, C.graphite));
  ctx.font = "32pt SpectralI";
  lignes(ctx, L.sous, W - 2 * M)
    .forEach((l, i) => texte(ctx, l, M, 470 + i * 44, "SpectralI", 32, C.mine));
  // rappel des quatre tiers, dans leurs couleurs
  ["A", "B", "C", "D"].forEach((t, i) => {
    const x = W - M - (4 - i) * 70;
    ctx.fillStyle = C[t]; ctx.fillRect(x, 60 - 36, 56, 46);
    texte(ctx, t, x + 18, 58, "BarlowB", 28, t === "D" ? C.graphite : C.feuille);
  });
  await ecrire(img, "defaut.png");
}

(async () => {
  for (const code of Object.keys(LANGUES)) {
    L = LANGUES[code];
    const dir = path.join(RACINE, L.entrees);
    if (!fs.existsSync(dir)) continue;               // langue pas encore traduite
    fs.mkdirSync(L.sortie, { recursive: true });
    for (const f of fs.readdirSync(dir)) await carteEntree(f.replace(/\.md$/, ""), frontMatter(path.join(dir, f)));
    await carteGenerique();
    console.log(`cartes (${code}) :`, fs.readdirSync(L.sortie).filter(f => f.endsWith(".png")).length);
  }
})().catch(e => { console.error(e); process.exit(1); });
