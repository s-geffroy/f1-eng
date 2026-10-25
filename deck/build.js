// Deck « Les ingénieurs qui ont révolutionné la Formule 1 » — storyboard §13 de la spec.
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
// node build.js        -> .pptx (pptxgenjs)
// node build.js pdf    -> .pdf  (mêmes appels, rejoués par pdf-recorder.js avec pdfkit)
const MODE = process.argv[2] || "pptx";
const pres = MODE === "pdf" ? require("./pdf-recorder").create() : new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.title = "Les ingénieurs qui ont révolutionné la Formule 1";

// Palette du site (assets/css/encyclopedie.css) : papier calque froid, encre graphite,
// un code par tier ; le rouge est réservé au Tier A.
const C = {
  bg: "D9DEDF", ink: "2E3338", sub: "4F575E", rule: "8E979D", light: "C2C9CC",
  A: "C0182C", B: "3D5B74", Cc: "6E767C", D: "AEB5BA", white: "FFFFFF",
};
const TIER = { A: C.A, B: C.B, C: C.Cc, D: C.D };
// Polices du site : Barlow Condensed (lettrage technique) et Spectral (texte de lecture).
const F = "Barlow Condensed", FS = "Spectral";
const W = 13.333, M = 0.6;

// ---------- Sources ----------
const SRC = {
  innov: ["F1 — Most influential technical innovator", "https://www.formula1.com/en/latest/article/vote-now-who-is-the-most-influential-technical-innovator-in-f1-history.dUby3oyTgDmCPqkvkYttX"],
  f175: ["F1 — The 75 best… in F1 history", "https://www.formula1.com/en/latest/article/the-75-best-drivers-cars-innovations-teams-and-key-figures-in-f1-history.6VcYXd7l9aI6fysNWtxFja"],
  lotus79: ["F1 — Tech Tuesday: The Lotus 79", "https://www.formula1.com/en/latest/article/tech-tuesday-the-lotus-79-f1s-ground-effect-marvel.sAD9PXt7mC8iMSwwe6CCw"],
  barnard: ["F1 — John Barnard podcast", "https://www.formula1.com/en/latest/article/listen-to-john-barnard-f1-podcast.BMSWfX9hs5BvvOWoM9xvF"],
  f1990: ["F1 — How F1 looked in 1990", "https://www.formula1.com/en/latest/article/tech-tuesday-france-flashback-how-f1-looked-in-1990.1ysdfhQzeImE2IeqokCeQG"],
  fw15c: ["F1 — Williams FW15C", "https://www.formula1.com/en/latest/article/tech-tuesday-wizardry-behind-williams-fw15c.6IzOXYuuPYOWyaaGGS4AgS"],
  lowe: ["F1 — Paddy Lowe interview", "https://www.formula1.com/en/latest/article/paddy-lowe-on-why-his-2017-return-to-williams-didnt-work-out-and-why-the.6rUD5xWXMyxMa8RA2krMWN"],
  brawn: ["F1 — Ross Brawn favourite car designs", "https://www.formula1.com/en/latest/article/exclusive-from-trendsetters-to-title-winners-ross-brawn-reveals-his.6FIAnV6e71kvi8PVInIuPo"],
  murray: ["F1 — Most Influential Person: final 4", "https://www.formula1.com/en/latest/article/most-influential-person-in-f1-history-who-is-going-through-to-the-final-4.5Uk4yx3U0zEckWhWU02HM1"],
  f312t: ["F1 — Ferrari 312T", "https://www.formula1.com/en/latest/article/tech-tuesday-under-the-bodywork-of-mauro-forghieris-masterpiece-the-ferrari.kftnvmyfKpzrrB5NdO1xz"],
  f312b3: ["F1 — Ferrari 312B3", "https://www.formula1.com/en/latest/article/under-the-bodywork-of-the-ferrari-312b3-on-the-anniversary-of-niki-laudas.zcaL509YxSDEQWI2721oN"],
  forgObit: ["F1 — Obituary Mauro Forghieri", "https://www.formula1.com/en/latest/article/obituary-mauro-forghieri-technical-genius-behind-some-of-formula-1s-greatest.67IR5vwYq73vG9mhaKYd3N"],
  newey: ["F1 — Newey's Red Bull exit", "https://www.formula1.com/en/latest/article/analysis-adrian-neweys-red-bull-exit-is-confirmed-what-next-for-the-star.461uBy91tP22ooEFMTQuBd"],
  byrne: ["F1 — Ferrari technical reshuffle", "https://www.formula1.com/en/latest/article/analysis-why-ferraris-technical-reshuffle-and-nod-to-the-past-is-so.2oJQc1Vo8nRxOOR5PeAt1R"],
  type25: ["Lotus — Type 25", "https://www.lotuscars.com/en/lotus-story/race-cars/type-25"],
  lotusStory: ["Lotus — Lotus Story", "https://www.lotuscars.com/en/lotus-story"],
  mp41: ["McLaren — MP4/1", "https://www.mclaren.com/racing/heritage/formula-1/cars/1981-formula-1-mclaren-mp4-1/"],
  renault: ["Renault — 30 ans de Formule 1", "https://cdn.group.renault.com/ren/master/renault-classic/tools-and-services/30AnsDeFormule1.pdf"],
  d50: ["Stellantis Heritage — Lancia D50", "https://www.stellantisheritage.com/en-uk/heritage/stories/lancia-d50"],
  msRenault: ["Motor Sport — Renault Returns", "https://www.motorsportmagazine.com/archive/article/july-1988/7/renault-returns/"],
  msDernie: ["Motor Sport — Lunch with Frank Dernie", "https://www.motorsportmagazine.com/archive/article/august-2016/100/lunch-frank-dernie/"],
  msT51: ["Motor Sport — Cooper T51", "https://www.motorsportmagazine.com/archive/article/june-2019/122/cooper-t51/"],
  nye: ["Goodwood / Doug Nye — Cooper", "https://www.goodwood.com/grr/columnists/doug-nye/the-rise-and-fall-of-the-single-seater-cooper/"],
};
const CONSULT = "Date de consultation des sources : 9 août 2026.";

// ---------- Helpers ----------
function newSlide(n) {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  s.addText(String(n).padStart(2, "0"), { x: W - M - 0.6, y: 7.0, w: 0.6, h: 0.3, fontFace: F, fontSize: 9, color: C.sub, align: "right" });
  return s;
}
function title(s, text, kicker) {
  if (kicker) s.addText(kicker, { x: M, y: 0.32, w: 9, h: 0.34, fontFace: F, fontSize: 15, color: C.sub });
  s.addText(text, { x: M, y: 0.62, w: W - 2 * M, h: 0.9, fontFace: F, fontSize: 34, bold: true, color: C.ink, valign: "top" });
  // trait fort sous le titre, comme l'en-tête du site
  s.addShape(pres.shapes.LINE, { x: M, y: 1.55, w: W - 2 * M, h: 0, line: { color: C.ink, width: 2 } });
}
// Cartouche (bloc-titre de plan) : trait fort autour, traits fins dedans, nom du champ en petit.
function cartouche(s, rang, tier, score, conf) {
  const cells = [["Rang", String(rang), 0.65], ["Tier", tier, 0.65], ["Score", score, 0.95], ["Confiance", conf, 1.25]];
  const total = cells.reduce((a, c) => a + c[2], 0), y = 6.05, h = 0.8;
  let x = W - M - total;
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: total, h, fill: { color: C.white }, line: { color: C.ink, width: 2 } });
  cells.forEach(([lab, val, w], i) => {
    const isTier = lab === "Tier", fg = isTier && tier !== "D" ? C.white : C.ink;
    if (isTier) s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: TIER[tier] }, line: { color: C.ink, width: 0 } });
    if (i > 0) s.addShape(pres.shapes.LINE, { x, y, w: 0, h, line: { color: C.rule, width: 0.75 } });
    s.addText(lab, { x, y: y + 0.03, w, h: 0.26, fontFace: F, fontSize: 10, color: isTier ? fg : C.sub });
    s.addText(val, { x, y: y + 0.27, w, h: 0.48, fontFace: F, fontSize: lab === "Confiance" ? 15 : 22, bold: true, color: fg, valign: "middle" });
    x += w;
  });
  s.addShape(pres.shapes.RECTANGLE, { x: W - M - total, y, w: total, h, fill: { type: "none" }, line: { color: C.ink, width: 2 } });
}
// Portraits : préparés par portraits.js (niveaux de gris, recadrés), crédits lus dans le site.
const PORTRAITS = path.join(__dirname, "portraits");
const CREDITS = JSON.parse(fs.readFileSync(path.join(PORTRAITS, "credits.json"), "utf8"));
function portrait(s, id, x, y, w, h) {
  const c = CREDITS[id];
  if (!c) return;
  s.addImage({ path: path.join(PORTRAITS, id + ".jpg"), x, y, w, h });
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { type: "none" }, line: { color: C.ink, width: 2 } });
  (s.photos = s.photos || []).push(c);
}
// Vignette de diapositive de groupe : le portrait s'il existe, sinon une case neutre
// avec les initiales (aucun portrait libre de droits connu).
const idOf = nom => nom.toLowerCase().replace(/ /g, "-");
function vignette(s, id, x, y, w, h) {
  if (CREDITS[id]) {
    s.addImage({ path: path.join(PORTRAITS, id + ".jpg"), x, y, w, h });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { type: "none" }, line: { color: C.ink, width: 1.25 } });
    s.groupePhotos = true;
  } else {
    const parts = id.split("-"), ini = (parts[0][0] + parts[parts.length - 1][0]).toUpperCase(); // prénom + nom
    s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: C.light }, line: { color: C.rule, width: 1 } });
    // zone de texte plus large que la case : les marges internes ne coupent pas les initiales
    s.addText(ini, { x: x - 0.3, y, w: w + 0.6, h, fontFace: F, fontSize: Math.max(8, Math.round(Math.min(h * 22, w * 36))), bold: true, color: C.sub, align: "center", valign: "middle" });
  }
}
function footer(s, keys) {
  const parts = keys.length ? ["Sources : " + keys.map(k => SRC[k][0]).join(" · ")] : [];
  for (const c of s.photos || []) parts.push(`Photo : ${c.auteur} (${c.licence}, Wikimedia Commons), recadrée et passée en noir et blanc`);
  if (s.groupePhotos) parts.push("Photos : crédits diapositive 21");
  const t = parts.join(" · ");
  s.addText(t, { x: M, y: 7.0, w: W - 2 * M - 0.8, h: 0.3, fontFace: FS, fontSize: 9, color: C.sub, italic: true });
}
function notes(s, { idee, faits, nuance, sources, photos }) {
  if (photos) s.photos = Object.values(CREDITS);
  const src = (sources || []).map(k => `- ${SRC[k][0]} : ${SRC[k][1]}`)
    .concat((s.photos || []).map(c => `- Photo : ${c.auteur}, ${c.licence} : ${c.source} (recadrée et passée en noir et blanc)`)).join("\n");
  s.addNotes(
    `IDÉE À DÉFENDRE\n${idee}\n\nFAITS\n${faits.map(f => "- " + f).join("\n")}\n\nNUANCE HISTORIOGRAPHIQUE\n${nuance}` +
    (src ? `\n\nSOURCES\n${src}\n${CONSULT}` : "")
  );
}
function box(s, x, y, w, h, text, o = {}) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: o.fill || C.white }, line: { color: o.line || C.ink, width: o.lw || 1.5 } });
  s.addText(text, { x: x + 0.1, y, w: w - 0.2, h, fontFace: F, fontSize: o.size || 14, bold: !!o.bold, color: o.color || C.ink, align: o.align || "center", valign: "middle" });
}
function arrow(s, x1, y1, x2, y2, color) {
  s.addShape(pres.shapes.LINE, { x: x1, y: y1, w: x2 - x1, h: y2 - y1, line: { color: color || C.sub, width: 1.5, endArrowType: "triangle" } });
}

// ---------- Données ----------
const RANK = [
  ["Colin Chapman", "A", 96.0], ["John Barnard", "A", 95.0], ["John Cooper", "A", 93.5], ["Keith Duckworth", "A", 92.5], ["Adrian Newey", "A", 91.5],
  ["Bernard Dudot", "B", 90.0], ["Gordon Murray", "B", 88.5], ["Mauro Forghieri", "B", 87.5], ["Peter Wright", "B", 86.5], ["Frank Dernie", "B", 85.0],
  ["Patrick Head", "C", 83.5], ["Ross Brawn", "C", 82.0], ["Andy Cowell", "C", 81.0], ["Jean-Claude Migeot", "C", 80.0], ["Tony Rudd", "C", 79.0],
  ["Mike Costin", "D", 77.5], ["Vittorio Jano", "D", 76.5], ["Owen Maddock", "D", 75.5], ["Paddy Lowe", "D", 74.5], ["Rory Byrne", "D", 73.5],
];
const fr = v => v.toFixed(1).replace(".", ",");

// ===== 1 — Titre =====
{
  const s = newSlide(1);
  s.addText("Ingénieurs de la F1", { x: M, y: 0.35, w: 6, h: 0.45, fontFace: F, fontSize: 20, bold: true, color: C.ink });
  s.addShape(pres.shapes.LINE, { x: M, y: 0.85, w: W - 2 * M, h: 0, line: { color: C.ink, width: 2 } });
  s.addText("Les ingénieurs qui ont révolutionné la Formule 1", { x: M, y: 1.7, w: 11.5, h: 1.9, fontFace: F, fontSize: 60, bold: true, color: C.ink, valign: "top" });
  s.addText("De Cooper à Newey : qui a réellement changé la grammaire technique de la discipline ?", { x: M, y: 3.95, w: 11, h: 0.9, fontFace: FS, fontSize: 22, italic: true, color: C.sub, valign: "top" });
  // Frise des générations, sans noms
  const y = 5.6, x0 = M, x1 = W - M;
  s.addShape(pres.shapes.LINE, { x: x0, y, w: x1 - x0, h: 0, line: { color: C.ink, width: 1.5 } });
  ["1950", "1960", "1970", "1980", "1990", "2000", "2010", "2020"].forEach((d, i, a) => {
    const x = x0 + (i * (x1 - x0)) / (a.length - 1);
    s.addShape(pres.shapes.LINE, { x, y: y - 0.12, w: 0, h: 0.24, line: { color: C.ink, width: 1.5 } });
    s.addText(d, { x: x - 0.4, y: y + 0.15, w: 0.8, h: 0.3, fontFace: F, fontSize: 11, color: C.sub, align: "center" });
  });
  notes(s, {
    idee: "Le sujet n'est pas « qui a gagné le plus », mais qui a obligé le plateau à changer sa manière de construire une F1.",
    faits: ["Vingt ingénieurs, quatre tiers.", "Cinq d'entre eux (Tier A) ont changé la grammaire de la F1 ; quinze autres ont transformé des sous-systèmes, des méthodes ou des trajectoires."],
    nuance: "Le classement est un instrument comparatif construit par une méthode explicite, pas un verdict historique.",
    sources: [],
  });
}

// ===== 2 — La mauvaise question =====
{
  const s = newSlide(2);
  title(s, "« Qui a gagné le plus ? » n'est pas la bonne question", "Point de départ");
  const pairs = [["Titres", "Innovation"], ["Innovation", "Invention"], ["Invention", "Diffusion"], ["Direction technique", "Paternité personnelle"]];
  pairs.forEach(([a, b], i) => {
    const y = 2.0 + i * 0.85;
    box(s, 2.2, y, 3.6, 0.65, a, { size: 18, bold: true });
    s.addText("≠", { x: 5.9, y, w: 1.5, h: 0.65, fontFace: F, fontSize: 30, bold: true, color: C.ink, align: "center", valign: "middle" });
    box(s, 7.5, y, 3.6, 0.65, b, { size: 18, bold: true });
  });
  s.addText("Le classement mesure la capacité à déplacer durablement la frontière technique.", { x: M, y: 5.7, w: W - 2 * M, h: 0.6, fontFace: FS, fontSize: 18, italic: true, color: C.ink, align: "center" });
  notes(s, {
    idee: "Le palmarès brut ne suffit pas à mesurer une révolution technique.",
    faits: ["Les résultats sportifs ne pèsent que 10 % de la note.", "L'influence durable sur la conception des F1 pèse 35 %, c'est le critère dominant.", "Une même innovation passe par plusieurs rôles : inventeur, applicateur, développeur, diffuseur."],
    nuance: "Une voiture championne peut n'avoir rien inventé ; une rupture majeure peut n'avoir rien gagné tout de suite.",
    sources: ["innov"],
  });
}

// ===== 3 — La méthode =====
{
  const s = newSlide(3);
  title(s, "Cinq critères, dominés par l'influence durable", "La méthode");
  const crit = [["Influence durable", 35], ["Rupture identifiable", 30], ["Amplitude du champ transformé", 15], ["Résultats sportifs liés", 10], ["Paternité / traçabilité", 10]];
  const x0 = 4.6, maxW = 7.4;
  crit.forEach(([lab, p], i) => {
    const y = 2.05 + i * 0.8;
    s.addText(lab, { x: M, y, w: 3.9, h: 0.55, fontFace: F, fontSize: 16, color: C.ink, align: "right", valign: "middle" });
    s.addShape(pres.shapes.RECTANGLE, { x: x0, y: y + 0.08, w: (maxW * p) / 35, h: 0.4, fill: { color: i === 0 ? C.ink : C.D }, line: { color: i === 0 ? C.ink : C.D } });
    s.addText(p + " %", { x: x0 + (maxW * p) / 35 + 0.1, y, w: 1, h: 0.55, fontFace: F, fontSize: 16, bold: true, color: C.ink, valign: "middle" });
  });
  s.addText("Les scores sont un instrument comparatif, pas des faits historiques.", { x: M, y: 6.2, w: W - 2 * M, h: 0.4, fontFace: FS, fontSize: 14, italic: true, color: C.sub, align: "center" });
  notes(s, {
    idee: "La note privilégie l'influence durable et la rupture identifiable (65 % à elles deux).",
    faits: ["Pondération : rupture 30 %, influence durable 35 %, amplitude 15 %, résultats 10 %, paternité 10 %.", "Des diagnostics secondaires (nature de la rupture, diffusion, longévité, innovation interdite, répétition, contrefactuel, objet/processus) corrigent et interprètent la note, sans s'y additionner."],
    nuance: "Un écart de 1 ou 2 points ne doit pas être interprété comme une différence scientifique de valeur.",
    sources: [],
  });
}

// ===== 4 — Le test de causalité =====
{
  const s = newSlide(4);
  title(s, "Une innovation a plusieurs auteurs, à des étapes différentes", "Le test de causalité");
  const steps = ["Invention", "Application F1", "Maturation", "Domination", "Diffusion", "Standard"];
  const bw = 1.7, gap = 0.32, x0 = (W - (steps.length * bw + (steps.length - 1) * gap)) / 2, y = 2.6;
  steps.forEach((t, i) => {
    const x = x0 + i * (bw + gap);
    box(s, x, y, bw, 0.9, t, { size: 15, bold: true });
    if (i < steps.length - 1) arrow(s, x + bw + 0.03, y + 0.45, x + bw + gap - 0.03, y + 0.45);
  });
  const ex = ["Effet de sol", "Cooper moteur arrière", "Cosworth DFV", "Suspension active Williams"];
  s.addText("Exemples", { x: M, y: 4.6, w: 3, h: 0.35, fontFace: F, fontSize: 12, bold: true, color: C.sub });
  ex.forEach((t, i) => box(s, M + i * 3.07, 5.0, 2.9, 0.7, t, { size: 14, fill: C.bg }));
  notes(s, {
    idee: "Il faut distribuer le mérite selon le rôle réel : on ne crédite jamais intégralement plusieurs personnes de la même contribution.",
    faits: [
      "Effet de sol : Wright et Rudd (BRM puis Lotus), Chapman qui fixe la mission ; Bellamy et Southgate interviennent aussi sur la Lotus 78.",
      "Cooper : John Cooper architecte du basculement, Owen Maddock concepteur central des T51/T53.",
      "DFV : réalisation Cosworth, Duckworth figure technique centrale, Costin cofondateur et acteur majeur.",
      "Williams active : Head, Dernie, Lowe, Newey et d'autres.",
    ],
    nuance: "Sept rôles distincts : inventeur, premier applicateur, architecte, développeur, industrialiseur, leader technique, diffuseur.",
    sources: ["lotus79", "msT51", "innov", "fw15c"],
  });
}

// ===== 5 — Les quatre tiers =====
{
  const s = newSlide(5);
  title(s, "Vingt ingénieurs, quatre tiers", "Vue d'ensemble");
  const tiers = [["A", "Révolutionnaires de paradigme"], ["B", "Transformateurs systémiques majeurs"], ["C", "Innovateurs structurants"], ["D", "Impact plus localisé ou plus partagé"]];
  const hs = [1.15, 0.8, 0.8, 0.8];
  let y = 1.85;
  tiers.forEach(([t, lab], r) => {
    const h = hs[r], col = TIER[t];
    s.addText([{ text: "Tier " + t, options: { bold: true, fontSize: r === 0 ? 20 : 15, color: col === C.D ? C.Cc : col, breakLine: true } }, { text: lab, options: { fontSize: 10, color: C.sub } }],
      { x: M, y, w: 2.5, h, fontFace: F, valign: "middle" });
    for (let i = 0; i < 5; i++) {
      const [name] = RANK[r * 5 + i];
      const x = 3.2 + i * 1.93;
      s.addShape(pres.shapes.RECTANGLE, { x, y, w: 1.83, h: h - 0.1, fill: { color: r === 0 ? C.A : C.white }, line: { color: col, width: r === 0 ? 0 : 1.5 } });
      const vh = h - 0.22, vw = vh * 0.735;
      vignette(s, idOf(name), x + 0.06, y + 0.06, vw, vh);
      s.addText(name, { x: x + vw + 0.08, y, w: 1.83 - vw - 0.1, h: h - 0.1, fontFace: F, fontSize: r === 0 ? 15 : 12, bold: r <= 1, color: r === 0 ? C.white : C.ink, align: "center", valign: "middle" });
    }
    y += h + 0.15;
  });
  footer(s, []);
  notes(s, {
    idee: "Cinq ingénieurs ont changé la grammaire de la F1 ; quinze autres ont transformé des sous-systèmes, des méthodes ou des trajectoires majeures.",
    faits: ["Tier A : changement durable de la grammaire technique, « avant / après », diffusion à tout le plateau, causalité personnelle documentée.", "Tier B : au moins une limite (attribution plus collective, portée plus spécialisée, durée plus courte, dépendance réglementaire).", "Tiers C et D : contribution majeure, mais moins paradigmatique ou moins exclusive."],
    nuance: "Les scores détaillés ne sont pas encore montrés : on lit d'abord la structure, pas les décimales.",
    sources: [],
  });
}

// ===== 6 — Tier A : la thèse =====
{
  const s = newSlide(6);
  title(s, "Cinq questions qui ont changé la F1", "Tier A — la thèse");
  const q = [["Cooper", "john-cooper", "Où placer le moteur ?"], ["Chapman", "colin-chapman", "Comment construire la voiture ?"], ["Duckworth", "keith-duckworth", "Comment intégrer le moteur ?"], ["Barnard", "john-barnard", "Avec quels matériaux et interfaces ?"], ["Newey", "adrian-newey", "Comment optimiser le système aérodynamique complet ?"]];
  q.forEach(([n, id, t], i) => {
    const y = 1.95 + i * 0.95;
    s.addText(String(i + 1), { x: M, y, w: 0.6, h: 0.75, fontFace: F, fontSize: 28, bold: true, color: C.A, valign: "middle" });
    vignette(s, id, M + 0.55, y + 0.02, 0.52, 0.71);
    s.addText(n, { x: M + 1.25, y, w: 2.05, h: 0.75, fontFace: F, fontSize: 20, bold: true, color: C.ink, valign: "middle" });
    s.addText(t, { x: M + 3.4, y, w: 8.4, h: 0.75, fontFace: F, fontSize: 20, color: C.ink, valign: "middle" });
    if (i < 4) s.addShape(pres.shapes.LINE, { x: M, y: y + 0.85, w: W - 2 * M, h: 0, line: { color: C.rule, width: 0.75 } });
  });
  footer(s, []);
  notes(s, {
    idee: "Chaque membre du Tier A a transformé une question fondamentale de la conception d'une F1. C'est la clé intellectuelle du deck.",
    faits: ["Cooper : position des organes fondamentaux (moteur central-arrière).", "Chapman : architecture de la monoplace (monocoque, moteur structurel, aéro, effet de sol).", "Duckworth : intégration et fourniture du groupe propulseur (DFV).", "Barnard : matériaux et interfaces (carbone, boîte semi-automatique).", "Newey : optimisation de l'ensemble comme système aérodynamique."],
    nuance: "L'ordre de la slide suit la logique des questions, pas le rang (Chapman est n° 1).",
    sources: ["innov"],
  });
}

// ===== 7 — Chapman =====
{
  const s = newSlide(7);
  title(s, "Trois ruptures, une philosophie : architecture + légèreté + aéro", "Colin Chapman");
  cartouche(s, 1, "A", "96,0", "Élevée");
  portrait(s, "colin-chapman", 10.93, 1.95, 1.8, 2.45);
  const cols = [["Lotus 25", "Monocoque aluminium"], ["Lotus 49", "Moteur élément structurel"], ["Lotus 78 / 79", "Programme effet de sol"]];
  cols.forEach(([car, t], i) => {
    const x = M + i * 3.42, w = 3.2;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.95, w, h: 2.45, fill: { color: C.white }, line: { color: C.ink, width: 1.5 } });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.95, w, h: 0.08, fill: { color: C.A }, line: { color: C.A } });
    s.addText(car, { x, y: 2.3, w, h: 0.8, fontFace: F, fontSize: 26, bold: true, color: C.ink, align: "center" });
    s.addText(t, { x, y: 3.2, w, h: 0.8, fontFace: F, fontSize: 17, color: C.sub, align: "center" });
  });
  s.addShape(pres.shapes.RECTANGLE, { x: M, y: 4.9, w: W - 2 * M, h: 1.0, fill: { color: C.bg }, line: { color: C.A, width: 1.5, dashType: "dash" } });
  s.addText([{ text: "Attribution partagée : ", options: { bold: true } }, { text: "Wright / Rudd pour l'effet de sol." }],
    { x: M + 0.2, y: 4.9, w: W - 2 * M - 0.4, h: 1.0, fontFace: F, fontSize: 16, color: C.ink, valign: "middle" });
  footer(s, ["type25", "lotusStory", "lotus79"]);
  notes(s, {
    idee: "Chapman est n° 1 par l'accumulation de ruptures architecturales, pas par une invention unique.",
    faits: ["Lotus Type 25 : généralisation du monocoque aluminium comme architecture de châssis F1.", "Famille Lotus de la seconde moitié des années 1960 : moteur utilisé comme élément structurel (Lotus 49, avec le DFV).", "Lancement et direction du programme qui débouche sur l'effet de sol (Lotus 78/79)."],
    nuance: "Ne pas dire « Chapman a inventé l'effet de sol ». Dire : Chapman a dirigé et catalysé le programme Lotus qui a rendu l'effet de sol opératoire et dominant en F1. Wright et Rudd avaient travaillé le concept chez BRM ; Bellamy et Southgate interviennent aussi.",
    sources: ["type25", "lotusStory", "lotus79"],
  });
}

// ===== 8 — Barnard =====
{
  const s = newSlide(8);
  title(s, "Deux innovations indépendantes devenues universelles", "John Barnard");
  cartouche(s, 2, "A", "95,0", "Très élevée");
  portrait(s, "john-barnard", 10.93, 1.95, 1.8, 2.45);
  [["1981", "McLaren MP4/1", "Monocoque intégral en carbone"], ["1989", "Ferrari 640", "Boîte semi-automatique au volant"]].forEach(([yr, car, t], i) => {
    const x = M + i * 5.1, w = 4.9;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.95, w, h: 3.4, fill: { color: C.white }, line: { color: C.ink, width: 1.5 } });
    s.addText(yr, { x, y: 2.1, w, h: 1.1, fontFace: F, fontSize: 54, bold: true, color: C.A, align: "center" });
    s.addText(car, { x, y: 3.3, w, h: 0.7, fontFace: F, fontSize: 24, bold: true, color: C.ink, align: "center" });
    s.addText(t, { x, y: 4.05, w, h: 0.7, fontFace: F, fontSize: 18, color: C.sub, align: "center" });
  });
  s.addText("La paternité personnelle la plus nette : le principal challenger de Chapman.", { x: M, y: 5.5, w: 10.0, h: 0.4, fontFace: FS, fontSize: 17, italic: true, color: C.ink, align: "center" });
  footer(s, ["mp41", "barnard", "f1990"]);
  notes(s, {
    idee: "Barnard porte deux ruptures indépendantes, directement attribuables, toutes deux devenues des standards.",
    faits: ["MP4/1 (1981) : première F1 construite autour d'un monocoque intégral en composite carbone — rigidité, masse, sécurité, industrialisation du composite. Le principe devient universel.", "Ferrari 640 (1989) : boîte semi-automatique commandée au volant — fin progressive du levier en H, moins d'erreurs, mains sur le volant, cockpit plus compact."],
    nuance: "Si la pondération « paternité directe » augmentait sensiblement, Barnard pourrait passer devant Chapman.",
    sources: ["mp41", "barnard", "f1990"],
  });
}

// ===== 9 — Cooper =====
{
  const s = newSlide(9);
  title(s, "Une révolution topologique de la monoplace", "John Cooper");
  cartouche(s, 3, "A", "93,5", "Élevée");
  // Schémas vue de dessus : avant / après
  function car(x, engineFront, label) {
    const y = 2.6, w = 4.6, h = 1.3;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.4, fill: { color: C.white }, line: { color: C.ink, width: 1.5 } });
    const ex = engineFront ? x + 0.35 : x + w - 1.85;
    s.addShape(pres.shapes.RECTANGLE, { x: ex, y: y + 0.3, w: 1.5, h: h - 0.6, fill: { color: engineFront ? C.Cc : C.A }, line: { color: C.ink, width: 0 } });
    s.addText("moteur", { x: ex, y: y + 0.3, w: 1.5, h: h - 0.6, fontFace: F, fontSize: 12, bold: true, color: C.white, align: "center", valign: "middle" });
    const px = engineFront ? x + w - 1.6 : x + 1.4;
    s.addShape(pres.shapes.OVAL, { x: px, y: y + 0.35, w: 0.6, h: 0.6, fill: { color: C.bg }, line: { color: C.ink, width: 1.5 } });
    s.addText("pilote", { x: px - 0.3, y: y + h + 0.05, w: 1.2, h: 0.3, fontFace: F, fontSize: 10, color: C.sub, align: "center" });
    s.addText(label, { x, y: y - 0.6, w, h: 0.45, fontFace: F, fontSize: 18, bold: true, color: C.ink, align: "center" });
    s.addText("avant", { x, y: y + h + 0.05, w: 1.2, h: 0.3, fontFace: F, fontSize: 10, color: C.sub });
  }
  car(M + 0.2, true, "Moteur avant");
  arrow(s, 5.75, 3.25, 7.35, 3.25, C.A);
  car(7.6, false, "Moteur central-arrière");
  s.addText([{ text: "Cooper T51, titres 1959 et 1960", options: { bold: true, breakLine: true } }, { text: "Concepteur central : Owen Maddock" }],
    { x: M, y: 4.9, w: W - 2 * M, h: 0.9, fontFace: F, fontSize: 17, color: C.ink, align: "center" });
  footer(s, ["msT51", "nye", "innov"]);
  notes(s, {
    idee: "Le passage au moteur central-arrière change la topologie même de la monoplace.",
    faits: ["Effets simultanés : répartition des masses, moment polaire, motricité, encombrement, architecture du châssis, aérodynamique future.", "Après les titres Cooper de 1959 et 1960, le moteur avant devient rapidement obsolète."],
    nuance: "Ne pas effacer Owen Maddock. Formulation : Cooper a imposé l'architecture moteur arrière avec une équipe de conception dans laquelle Owen Maddock joue un rôle central (T51/T53).",
    sources: ["msT51", "nye", "innov"],
  });
}

// ===== 10 — Duckworth =====
{
  const s = newSlide(10);
  title(s, "Une révolution technique et économique simultanée", "Keith Duckworth");
  cartouche(s, 4, "A", "92,5", "Élevée");
  const steps = ["DFV", "Moteur performant", "Moteur structurel", "Accessible aux équipes", "Nouvelle économie du plateau"];
  const bw = 2.15, gap = 0.3, x0 = M;
  steps.forEach((t, i) => {
    const x = x0 + i * (bw + gap);
    box(s, x, 2.0, bw, 1.0, t, { size: 15, bold: true, fill: i === 0 ? C.A : C.white, color: i === 0 ? C.white : C.ink, line: i === 0 ? C.A : C.ink });
    if (i < steps.length - 1) arrow(s, x + bw + 0.02, 2.5, x + bw + gap - 0.02, 2.5);
  });
  s.addText("155", { x: M, y: 3.4, w: 4, h: 1.6, fontFace: F, fontSize: 96, bold: true, color: C.A });
  s.addText("victoires en Grand Prix de championnat du monde", { x: M + 2.4, y: 3.75, w: 7, h: 0.9, fontFace: F, fontSize: 22, color: C.ink, valign: "middle" });
  s.addText("Cosworth = Duckworth + Costin + organisation", { x: M, y: 5.4, w: W - 2 * M, h: 0.6, fontFace: F, fontSize: 18, bold: true, color: C.ink });
  footer(s, ["innov", "f175"]);
  notes(s, {
    idee: "Le DFV transforme le moteur et l'écosystème industriel de la F1.",
    faits: ["Moteur compact et performant, composant structurel de la Lotus 49.", "Disponible pour de nombreuses équipes : plus besoin de moteur propriétaire, ressources concentrées sur châssis et aéro.", "155 victoires en Grand Prix de championnat du monde selon Formula 1."],
    nuance: "Ne pas présenter le DFV comme une création individuelle : réalisation Cosworth, Duckworth figure technique centrale, Mike Costin cofondateur et acteur majeur.",
    sources: ["innov", "f175"],
  });
}

// ===== 11 — Newey =====
{
  const s = newSlide(11);
  title(s, "Le génie de Newey est la répétition, pas le coup unique", "Adrian Newey");
  cartouche(s, 5, "A", "91,5", "Très élevée");
  portrait(s, "adrian-newey", 10.93, 1.95, 1.8, 2.45);
  const teams = ["Leyton House", "Williams", "McLaren", "Red Bull"];
  const y = 3.0, x0 = M + 1.0, x1 = 9.5;
  s.addShape(pres.shapes.LINE, { x: x0, y, w: x1 - x0, h: 0, line: { color: C.ink, width: 2 } });
  teams.forEach((t, i) => {
    const x = x0 + (i * (x1 - x0)) / (teams.length - 1);
    s.addShape(pres.shapes.OVAL, { x: x - 0.15, y: y - 0.15, w: 0.3, h: 0.3, fill: { color: C.A }, line: { color: C.A } });
    s.addText(t, { x: x - 1.3, y: y - 0.85, w: 2.6, h: 0.5, fontFace: F, fontSize: 20, bold: true, color: C.ink, align: "center" });
    s.addText("règlement " + (i + 1), { x: x - 1.3, y: y + 0.25, w: 2.6, h: 0.4, fontFace: F, fontSize: 12, color: C.sub, align: "center" });
  });
  s.addText("Règlements différents, même compétence : contrôle du système aérodynamique.", { x: M, y: 4.3, w: 10.0, h: 0.7, fontFace: F, fontSize: 20, color: C.ink, align: "center" });
  footer(s, ["innov", "newey", "f1990"]);
  notes(s, {
    idee: "Ne pas chercher « l'invention Newey » : son apport est une méthode systémique, démontrée sous plusieurs règlements et dans plusieurs équipes.",
    faits: ["Concevoir la monoplace comme un système aérodynamique intégré : suspension, géométrie, refroidissement, structure et packaging au service du flux.", "Résultats au sommet chez Williams, McLaren et Red Bull."],
    nuance: "Pourquoi pas n° 1 : le palmarès ne pèse que 10 %, et sa paternité est plus distribuée dans les grandes organisations modernes. Formulation : rôle de premier plan dans l'architecture aérodynamique de plusieurs générations de voitures championnes, au sein d'équipes techniques collectives.",
    sources: ["innov", "newey", "f1990"],
  });
}

// ===== 12 — Chapman vs Barnard =====
{
  const s = newSlide(12);
  title(s, "Pourquoi Chapman devant Barnard ?", "Le vrai débat pour la première place");
  portrait(s, "colin-chapman", M, 1.9, 1.4, 1.9);
  portrait(s, "john-barnard", W - M - 1.4, 1.9, 1.4, 1.9);
  footer(s, []);
  const hdr = { bold: true, color: C.white, fill: { color: C.ink }, align: "center" };
  const rows = [
    [{ text: "Critère", options: { ...hdr, align: "left" } }, { text: "Chapman", options: hdr }, { text: "Barnard", options: hdr }],
    ...[["Nombre de ruptures", "++", "+"], ["Paternité directe", "+", "++"], ["Portée architecturale", "++", "++"], ["Diffusion", "++", "++"], ["Répétition", "++", "+"]].map(([c, a, b]) => [
      { text: c }, { text: a, options: { align: "center", bold: a === "++", color: a === "++" ? C.A : C.ink } }, { text: b, options: { align: "center", bold: b === "++", color: b === "++" ? C.A : C.ink } },
    ]),
  ];
  s.addTable(rows, { x: 2.2, y: 1.9, w: 8.9, colW: [4.3, 2.3, 2.3], fontFace: F, fontSize: 18, color: C.ink, fill: { color: C.white }, border: { type: "solid", color: C.rule, pt: 0.75 }, rowH: 0.55 });
  s.addText("Chapman gagne par largeur historique ; Barnard gagne en traçabilité personnelle.", { x: M, y: 5.6, w: W - 2 * M, h: 0.6, fontFace: FS, fontSize: 19, italic: true, color: C.ink, align: "center" });
  notes(s, {
    idee: "Avec cette méthode, le débat sérieux n'est pas Chapman contre Newey, mais Chapman contre Barnard.",
    faits: ["Chapman domine par l'accumulation de ruptures architecturales.", "Barnard domine en paternité directe de deux innovations devenues universelles.", "Un point d'écart (96 contre 95) : la différence n'est pas scientifique."],
    nuance: "Le résultat dépend de la pondération : avec une paternité directe plus lourde, Barnard passerait devant.",
    sources: ["type25", "mp41"],
  });
}

// ===== 13 — Tier B =====
{
  const s = newSlide(13);
  title(s, "Tier B : cinq transformateurs systémiques", "Rangs 6 à 10");
  const cards = [["Dudot", "bernard-dudot", "Propulsion"], ["Murray", "gordon-murray", "Architecture radicale"], ["Forghieri", "mauro-forghieri", "Ingénierie totale"], ["Wright", "peter-wright", "Effet de sol"], ["Dernie", "frank-dernie", "Révolution numérique silencieuse"]];
  cards.forEach(([n, id, t], i) => {
    const x = M + i * 2.45;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.85, w: 2.25, h: 3.75, fill: { color: C.white }, line: { color: C.ink, width: 1.5 } });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.85, w: 2.25, h: 0.08, fill: { color: C.B }, line: { color: C.B } });
    vignette(s, id, x + (2.25 - 1.0) / 2, 2.05, 1.0, 1.36);
    s.addText(String(i + 6), { x, y: 3.45, w: 2.25, h: 0.45, fontFace: F, fontSize: 22, bold: true, color: C.B, align: "center" });
    s.addText(n, { x, y: 3.85, w: 2.25, h: 0.5, fontFace: F, fontSize: 20, bold: true, color: C.ink, align: "center" });
    s.addText(t, { x: x + 0.1, y: 4.35, w: 2.05, h: 1.1, fontFace: F, fontSize: 15, color: C.sub, align: "center", valign: "top" });
  });
  s.addText("Face au Tier A : attribution plus collective, portée plus spécialisée ou diffusion inégale.", { x: M, y: 5.8, w: W - 2 * M, h: 0.7, fontFace: FS, fontSize: 15, italic: true, color: C.ink, align: "center" });
  footer(s, ["renault", "murray", "f312t", "lotus79", "msDernie"]);
  notes(s, {
    idee: "Le Tier B transforme durablement un domaine central de la F1, avec une limite par rapport au Tier A.",
    faits: ["Dudot (90) : turbo, distribution pneumatique, V10 chez Renault.", "Murray (88,5) : BT46B, architectures Brabham, pit-stop tactique, contribution à la MP4/4.", "Forghieri (87,5) : 312T et boîte transversale, centralisation des masses.", "Wright (86,5) : développement causal de l'effet de sol Lotus.", "Dernie (85) : CAO/CAE, acquisition de données, soufflerie, suspension active."],
    nuance: "Murray : diffusion inégale de certaines ruptures. Dudot : réalisations d'une organisation, Renault Sport.",
    sources: ["renault", "msRenault", "murray", "f312t", "f312b3", "forgObit", "lotus79", "msDernie"],
  });
}

// ===== 14 — Dudot =====
{
  const s = newSlide(14);
  title(s, "La révolution moteur : turbo, rappel pneumatique, V10", "Bernard Dudot");
  cartouche(s, 6, "B", "90,0", "Élevée");
  const st = [["Turbo", "Adopté par tout le plateau"], ["Rappel pneumatique des soupapes", "Solution générale dans les années 1990"], ["V10", "V10 67° sous la direction de Dudot"]];
  st.forEach(([t, d], i) => {
    const x = M + 0.3 + i * 4.15;
    box(s, x, 2.2, 3.4, 1.1, t, { size: 18, bold: true, line: C.B, lw: 1.5 });
    s.addText(d, { x, y: 3.45, w: 3.4, h: 0.8, fontFace: F, fontSize: 14, color: C.sub, align: "center", valign: "top" });
    if (i < 2) arrow(s, x + 3.45, 2.75, x + 4.1, 2.75, C.B);
  });
  s.addShape(pres.shapes.RECTANGLE, { x: M, y: 4.8, w: W - 2 * M, h: 1.0, fill: { color: C.bg }, line: { color: C.B, width: 1.5, dashType: "dash" } });
  s.addText("Renault Sport est une organisation : Dudot n'est pas un inventeur solitaire.", { x: M + 0.2, y: 4.8, w: W - 2 * M - 0.4, h: 1.0, fontFace: F, fontSize: 16, color: C.ink, valign: "middle" });
  footer(s, ["renault", "msRenault"]);
  notes(s, {
    idee: "Dudot est au cœur de trois mutations moteur successives, toutes diffusées au plateau.",
    faits: ["Documentation Renault : le turbo finit par être adopté par tout le plateau.", "Le rappel pneumatique des soupapes devient une solution générale dans les années 1990.", "Motor Sport documente le V10 67° conçu sous la direction de Bernard Dudot."],
    nuance: "Ces réalisations sont celles d'une organisation, Renault Sport ; Dudot ne doit pas être présenté comme inventeur solitaire.",
    sources: ["renault", "msRenault"],
  });
}

// ===== 15 — Révolutions silencieuses =====
{
  const s = newSlide(15);
  title(s, "Les révolutions silencieuses", "Changer le processus, pas la carrosserie");
  [["Frank Dernie", "B", ["CAO / CAE", "Acquisition de données", "Soufflerie", "Suspension active"]], ["Ross Brawn", "C", ["Méthodes", "Organisation", "Programme anticipé", "Intégration"]]].forEach(([n, t, items], i) => {
    const x = M + i * 6.15;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.95, w: 5.9, h: 3.4, fill: { color: C.white }, line: { color: C.ink, width: 1.5 } });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.95, w: 0.08, h: 3.4, fill: { color: TIER[t] }, line: { color: TIER[t] } });
    s.addText(n, { x: x + 0.4, y: 2.1, w: 3.5, h: 0.7, fontFace: F, fontSize: 24, bold: true, color: C.ink });
    vignette(s, idOf(n), x + 5.9 - 0.25 - 1.6, 2.1, 1.6, 2.18);
    s.addText(items.map(it => ({ text: it, options: { bullet: true, breakLine: true } })), { x: x + 0.4, y: 2.9, w: 3.5, h: 2.2, fontFace: F, fontSize: 18, color: C.ink, valign: "top", paraSpaceAfter: 6 });
  });
  s.addText("Une révolution technique peut transformer le processus sans être visible sur la carrosserie.", { x: M, y: 5.7, w: W - 2 * M, h: 0.6, fontFace: FS, fontSize: 18, italic: true, color: C.ink, align: "center" });
  footer(s, ["msDernie", "brawn"]);
  notes(s, {
    idee: "La méthode distingue la révolution de l'objet et la révolution du processus de conception.",
    faits: ["Dernie : utilisation précoce de la CAO/CAE, acquisition de données, développement de soufflerie, suspension active chez Williams.", "Brawn : programmes démarrés très en amont, intégration organisationnelle, articulation conception/exploitation/stratégie, préparation de l'architecture Mercedes 2014 avant son départ."],
    nuance: "Ne pas écrire « Dernie a inventé seul la suspension active » ni « Brawn a conçu la Mercedes W05 ». Brawn a contribué à mettre en place la méthode et l'intégration qui ont préparé Mercedes à 2014.",
    sources: ["msDernie", "fw15c", "brawn"],
  });
}

// ===== 16 — Effet de sol =====
{
  const s = newSlide(16);
  title(s, "L'effet de sol : rétablir la chaîne causale", "Historiographie");
  const ch = [["BRM", "Wright + Rudd"], ["Lotus", "Chapman fixe la mission"], ["Soufflerie", "venturi / jupes"], ["Lotus 78 / 79", "la percée"], ["Diffusion", "à tout le plateau"]];
  const bw = 2.1, gap = 0.35;
  ch.forEach(([a, b], i) => {
    const x = M + i * (bw + gap), y = 2.4;
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: bw, h: 1.5, fill: { color: i === 3 ? C.ink : C.white }, line: { color: C.ink, width: 1.5 } });
    s.addText([{ text: a, options: { bold: true, fontSize: 18, breakLine: true } }, { text: b, options: { fontSize: 13 } }], { x: x + 0.05, y, w: bw - 0.1, h: 1.5, fontFace: F, color: i === 3 ? C.white : C.ink, align: "center", valign: "middle" });
    if (i < ch.length - 1) arrow(s, x + bw + 0.02, y + 0.75, x + bw + gap - 0.02, y + 0.75);
  });
  s.addText("Aussi dans la conception de la Lotus 78 : Ralph Bellamy, Tony Southgate.", { x: M, y: 4.4, w: W - 2 * M, h: 0.5, fontFace: F, fontSize: 15, color: C.sub, align: "center" });
  footer(s, ["lotus79"]);
  notes(s, {
    idee: "L'effet de sol est une filiation collective ; il faut la raconter dans l'ordre.",
    faits: ["Peter Wright et Tony Rudd avaient travaillé sur le concept chez BRM.", "Chez Lotus, Chapman leur demande de repenser la configuration fondamentale de la F1.", "La soufflerie débouche sur la Lotus 78, puis la 79 ; Bellamy et Southgate interviennent aussi."],
    nuance: "À éviter : « Chapman a inventé l'effet de sol ». À préférer : Chapman a dirigé et catalysé le programme Lotus qui a rendu l'effet de sol opératoire et dominant. Wright (Tier B) est placé devant Rudd (Tier C) car la contribution directe de Rudd à la solution finale est plus difficile à isoler.",
    sources: ["lotus79"],
  });
}

// ===== 17 — Tiers C et D =====
{
  const s = newSlide(17);
  title(s, "Tiers C et D : dix contributions majeures", "Rangs 11 à 20");
  const data = [
    [11, "Patrick Head", "Ingénierie système", "Organisation technique Williams", "Organisation plus que rupture unique"],
    [12, "Ross Brawn", "Méthode", "Développement anticipé, intégration", "Révolution de processus"],
    [13, "Andy Cowell", "Power unit", "Hybride Mercedes 2014", "Hybridation imposée par le règlement"],
    [14, "Jean-Claude Migeot", "Aérodynamique", "Nez relevé, Tyrrell 019", "Vite absorbé par l'évolution générale"],
    [15, "Tony Rudd", "Aérodynamique", "Genèse de l'effet de sol", "Contribution difficile à isoler"],
    [16, "Mike Costin", "Moteur", "Cofondateur de Cosworth", "Paternité du DFV moins individualisable"],
    [17, "Vittorio Jano", "Architecture", "Lancia D50", "Œuvre surtout antérieure à la F1"],
    [18, "Owen Maddock", "Châssis", "Cooper T51/T53 championnes", "Crédit partagé avec John Cooper"],
    [19, "Paddy Lowe", "Électronique", "Logiciel suspension active", "Rôle dans une chaîne collective"],
    [20, "Rory Byrne", "Intégration", "Benetton, Ferrari", "Pas de rupture unique paradigmatique"],
  ];
  const hdr = { bold: true, color: C.white, fill: { color: C.ink } };
  const rows = [["Rang", "", "Ingénieur", "Domaine", "Raison du classement", "Limite"].map(t => ({ text: t, options: hdr }))];
  data.forEach(r => {
    const col = r[0] <= 15 ? C.Cc : C.D;
    rows.push([{ text: String(r[0]), options: { bold: true, color: C.white, fill: { color: col }, align: "center" } }, { text: "" }, { text: r[1], options: { bold: true } }, { text: r[2] }, { text: r[3] }, { text: r[4] }]);
  });
  const rowH = 0.43, colW = [0.7, 0.42, 2.3, 1.9, 3.4, 3.413];
  s.addTable(rows, { x: M, y: 1.8, w: W - 2 * M, colW, fontFace: F, fontSize: 12, color: C.ink, fill: { color: C.white }, border: { type: "solid", color: C.rule, pt: 0.75 }, rowH });
  data.forEach((r, i) => vignette(s, idOf(r[1]), M + colW[0] + 0.05, 1.8 + rowH * (i + 1) + 0.04, 0.32, rowH - 0.08));
  footer(s, ["fw15c", "brawn", "f1990", "d50", "msT51"]);
  notes(s, {
    idee: "Les tiers C et D réunissent des contributions majeures, mais moins paradigmatiques ou moins exclusives. Pas de slide individuelle : le tableau suffit.",
    faits: ["Tier C (11-15, gris soutenu) : innovateurs structurants.", "Tier D (16-20, gris clair) : causalité moins exclusive, diffusion moins générale ou impact plus incrémental.", "Lowe : Formula 1 le crédite d'une grande partie du logiciel de la suspension active Williams."],
    nuance: "Distinguer clairement dans l'écosystème Williams : Head (architecture et direction), Dernie (numérique et programme actif), Lowe (logiciel et électronique), Newey (aérodynamique).",
    sources: ["fw15c", "lowe", "brawn", "innov", "f1990", "lotus79", "d50", "msT51", "nye", "byrne"],
  });
}

// ===== 18 — Lignées =====
{
  const s = newSlide(18);
  title(s, "Les grandes lignées techniques", "Filiations intellectuelles");
  const L = [
    ["Architecture", ["Cooper", "Chapman", "Barnard"]],
    ["Aérodynamique", ["Chapman / Wright", "Murray / Migeot", "Newey"]],
    ["Moteur", ["Duckworth", "Dudot", "Cowell"]],
    ["Numérique / contrôle", ["Dernie", "Lowe", "Ingénierie moderne"]],
    ["Organisation système", ["Head", "Brawn", "Équipes F1 modernes"]],
  ];
  L.forEach(([b, chain], i) => {
    const y = 1.85 + i * 0.88;
    s.addText(b, { x: M, y, w: 2.9, h: 0.65, fontFace: F, fontSize: 16, bold: true, color: C.ink, valign: "middle" });
    chain.forEach((n, j) => {
      const x = 3.6 + j * 3.1;
      box(s, x, y, 2.6, 0.65, n, { size: 15 });
      if (j < 2) arrow(s, x + 2.62, y + 0.325, x + 3.08, y + 0.325);
    });
  });
  s.addText("Ce schéma montre des filiations intellectuelles, pas des relations maître-élève.", { x: M, y: 6.35, w: W - 2 * M, h: 0.45, fontFace: FS, fontSize: 14, italic: true, color: C.sub, align: "center" });
  notes(s, {
    idee: "Les vingt noms s'organisent en cinq branches de l'ingénierie F1.",
    faits: ["Architecture : Cooper → Chapman → Barnard.", "Aérodynamique : Chapman/Wright → Murray/Migeot → Newey.", "Moteur : Duckworth → Dudot → Cowell.", "Numérique/contrôle : Dernie → Lowe → ingénierie moderne.", "Organisation système : Head → Brawn → équipes F1 modernes."],
    nuance: "Ce sont des filiations intellectuelles, pas des relations maître-élève systématiques.",
    sources: [],
  });
}

// ===== 19 — Classement final =====
{
  const s = newSlide(19);
  title(s, "Le classement final", "Scores sur 100");
  const colX = [M, M + 6.25], bx = 2.55, bmax = 2.9;
  RANK.forEach(([n, t, v], i) => {
    const c = Math.floor(i / 10), r = i % 10, x = colX[c], y = 1.85 + r * 0.46;
    s.addText(`${i + 1}. ${n}`, { x, y, w: bx - 0.1, h: 0.4, fontFace: F, fontSize: 13, bold: t === "A", color: C.ink, valign: "middle" });
    s.addShape(pres.shapes.RECTANGLE, { x: x + bx, y: y + 0.08, w: (bmax * v) / 100, h: 0.26, fill: { color: TIER[t] }, line: { color: TIER[t] } });
    s.addText(fr(v), { x: x + bx + (bmax * v) / 100 + 0.08, y, w: 0.7, h: 0.4, fontFace: F, fontSize: 12, bold: t === "A", color: C.ink, valign: "middle" });
  });
  [["A", "Tier A"], ["B", "Tier B"], ["C", "Tier C"], ["D", "Tier D"]].forEach(([t, l], i) => {
    const x = M + i * 1.6;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 6.55, w: 0.25, h: 0.2, fill: { color: TIER[t] }, line: { color: TIER[t] } });
    s.addText(l, { x: x + 0.3, y: 6.48, w: 1.2, h: 0.34, fontFace: F, fontSize: 11, color: C.ink });
  });
  s.addText("Ne pas surinterpréter les écarts de 1 ou 2 points.", { x: 7.0, y: 6.48, w: W - M - 7.0, h: 0.34, fontFace: FS, fontSize: 12, italic: true, color: C.sub, align: "right" });
  notes(s, {
    idee: "Le classement complet, avec les scores, n'arrive qu'à la fin : la méthode et la structure d'abord.",
    faits: ["Tier A : Chapman 96 ; Barnard 95 ; Cooper 93,5 ; Duckworth 92,5 ; Newey 91,5.", "Tier B : Dudot 90 ; Murray 88,5 ; Forghieri 87,5 ; Wright 86,5 ; Dernie 85.", "Tier C : Head 83,5 ; Brawn 82 ; Cowell 81 ; Migeot 80 ; Rudd 79.", "Tier D : Costin 77,5 ; Jano 76,5 ; Maddock 75,5 ; Lowe 74,5 ; Byrne 73,5."],
    nuance: "Les barres partent de zéro : les écarts sont visuellement faibles, et c'est voulu. Les scores sont un instrument comparatif, pas une vérité scientifique.",
    sources: [],
  });
}

// ===== 20 — Conclusion =====
{
  const s = newSlide(20);
  s.addText("Ingénieurs de la F1", { x: M, y: 0.35, w: 6, h: 0.45, fontFace: F, fontSize: 20, bold: true, color: C.ink });
  s.addShape(pres.shapes.LINE, { x: M, y: 0.85, w: W - 2 * M, h: 0, line: { color: C.ink, width: 2 } });
  s.addText("Révolutionner la F1, ce n'est pas seulement construire la voiture la plus rapide : c'est obliger les autres à changer leur manière de construire une F1.",
    { x: M, y: 1.3, w: 12, h: 2.4, fontFace: F, fontSize: 36, bold: true, color: C.ink, valign: "top" });
  [["Chapman", "rupture multiple"], ["Barnard", "paternité la plus nette"], ["Newey", "adaptation la plus durable"]].forEach(([n, t], i) => {
    const y = 4.0 + i * 0.75;
    s.addText(n, { x: M, y, w: 2.6, h: 0.6, fontFace: F, fontSize: 26, bold: true, color: C.ink, valign: "middle" });
    s.addText(t, { x: M + 2.6, y, w: 7, h: 0.6, fontFace: FS, fontSize: 22, italic: true, color: C.sub, valign: "middle" });
  });
  notes(s, {
    idee: "Le classement mesure des capacités historiques à déplacer la frontière technique, pas une échelle unique de « génie ».",
    faits: ["Chapman domine par l'accumulation de ruptures architecturales.", "Barnard domine en paternité directe de deux innovations devenues universelles.", "Newey domine la capacité à rester au sommet de l'aérodynamique sous plusieurs générations de règlements."],
    nuance: "Revenir aux cinq questions du Tier A (slide 6), qui sont la synthèse conceptuelle du classement : où placer le moteur, comment construire la voiture, comment intégrer le moteur, avec quels matériaux et interfaces, comment optimiser le système aérodynamique complet.",
    sources: [],
  });
}

// ===== 21 — Sources =====
{
  const s = newSlide(21);
  title(s, "Sources principales", "Consultées le 9 août 2026");
  const keys = ["innov", "f175", "lotus79", "barnard", "fw15c", "type25", "mp41", "renault", "msT51", "msDernie"];
  s.addText(keys.map(k => ({ text: SRC[k][0], options: { bullet: true, breakLine: true } })), { x: M, y: 1.9, w: 5.6, h: 4.4, fontFace: F, fontSize: 17, color: C.ink, valign: "top", paraSpaceAfter: 4 });
  // Crédits photographiques (licences CC : auteur et licence pour chaque portrait)
  const nomDe = id => RANK.map(r => r[0]).find(n => idOf(n) === id) || id;
  s.addText("Crédits photographiques (Wikimedia Commons)", { x: 6.6, y: 1.9, w: 6.1, h: 0.4, fontFace: F, fontSize: 16, bold: true, color: C.ink });
  s.addText(Object.entries(CREDITS).sort((a, b) => RANK.findIndex(r => idOf(r[0]) === a[0]) - RANK.findIndex(r => idOf(r[0]) === b[0]))
    .map(([id, c]) => ({ text: `${nomDe(id)} : ${c.auteur}, ${c.licence}`, options: { breakLine: true } })),
    { x: 6.6, y: 2.35, w: 6.1, h: 3.3, fontFace: F, fontSize: 12, color: C.ink, valign: "top", paraSpaceAfter: 3 });
  s.addText("Modifications : images recadrées et passées en noir et blanc pour cette présentation. Les versions modifiées des images sous licence CC BY-SA ou Art Libre sont diffusées sous la même licence que l'original.",
    { x: 6.6, y: 5.55, w: 6.1, h: 0.7, fontFace: FS, fontSize: 11, italic: true, color: C.sub, valign: "top" });
  s.addText("Bibliographie complète, avec les adresses : notes du présentateur (.pptx) et s-geffroy.github.io/f1-eng", { x: M, y: 6.4, w: W - 2 * M, h: 0.4, fontFace: FS, fontSize: 13, italic: true, color: C.sub });
  notes(s, {
    idee: "Toutes les attributions sensibles reposent sur des sources officielles ou des publications historiques reconnues.",
    faits: ["Priorité aux sources officielles des constructeurs et de Formula 1.", "Aucune attribution controversée importante ne repose sur une seule source."],
    nuance: "Images : aucune photo n'est intégrée au deck ; toute image ajoutée doit faire l'objet d'une vérification des droits.",
    sources: Object.keys(SRC),
    photos: true,
  });
}

// Le PDF va directement là où le site le sert ; le .pptx reste hors du site (deck/out/).
const NOM = "ingenieurs-revolutionnaires-F1";
const sortie = MODE === "pdf" ? `${__dirname}/../assets/docs/${NOM}.pdf` : `${__dirname}/out/${NOM}.pptx`;
require("fs").mkdirSync(require("path").dirname(sortie), { recursive: true });
(MODE === "pdf" ? pres.renderPdf(sortie, __dirname + "/fonts") : pres.writeFile({ fileName: sortie }))
  .then(f => console.log("OK", f));
