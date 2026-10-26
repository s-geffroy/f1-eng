// Deck « Les ingénieurs qui ont révolutionné la Formule 1 » — storyboard §13 de la spec.
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
// node build.js [pptx|pdf] [fr|en]
//   pptx -> .pptx (pptxgenjs) ; pdf -> .pdf (mêmes appels, rejoués par pdf-recorder.js avec pdfkit)
//   fr (défaut) ou en : une seule description du deck, les textes en deux langues via t(fr, en)
const MODE = process.argv[2] || "pptx";
const LANG = process.argv[3] || "fr";
const EN = LANG === "en";
const t = (fr, en) => (EN ? en : fr);
const pres = MODE === "pdf" ? require("./pdf-recorder").create() : new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.title = t("Les ingénieurs qui ont révolutionné la Formule 1", "The engineers who revolutionised Formula 1");

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
// Ponctuation : espace avant les deux-points en français, pas en anglais.
const DP = t(" : ", ": ");

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
  msActive: ["Motor Sport — Active suspension (2001)", "https://www.motorsportmagazine.com/archive/article/december-2001/69/active-suspension"],
  ms67: ["Motor Sport — The Lotus 49 (1967)", "https://www.motorsportmagazine.com/archive/article/july-1967/26/the-lotus-49/"],
  wp88: [t("Wikipédia", "Wikipedia") + " — Lotus 88", "https://en.wikipedia.org/wiki/Lotus_88"],
  wpNewey: [t("Wikipédia", "Wikipedia") + " — Adrian Newey", "https://en.wikipedia.org/wiki/Adrian_Newey"],
};
const CONSULT = t("Date de consultation des sources : 9 août 2026.", "Sources consulted on 9 August 2026.");
const RETOUCHE = t("recadrée et passée en noir et blanc", "cropped and converted to black and white");

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
  const cells = [[t("Rang", "Rank"), String(rang), 0.65], ["Tier", tier, 0.65], ["Score", score, 0.95], [t("Confiance", "Confidence"), conf, 1.25]];
  const total = cells.reduce((a, c) => a + c[2], 0), y = 6.05, h = 0.8;
  let x = W - M - total;
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: total, h, fill: { color: C.white }, line: { color: C.ink, width: 2 } });
  cells.forEach(([lab, val, w], i) => {
    const isTier = i === 1, fg = isTier && tier !== "D" ? C.white : C.ink;
    if (isTier) s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: TIER[tier] }, line: { color: C.ink, width: 0 } });
    if (i > 0) s.addShape(pres.shapes.LINE, { x, y, w: 0, h, line: { color: C.rule, width: 0.75 } });
    s.addText(lab, { x, y: y + 0.03, w, h: 0.26, fontFace: F, fontSize: 10, color: isTier ? fg : C.sub });
    s.addText(val, { x, y: y + 0.27, w, h: 0.48, fontFace: F, fontSize: i === 3 ? 15 : 22, bold: true, color: fg, valign: "middle" });
    x += w;
  });
  s.addShape(pres.shapes.RECTANGLE, { x: W - M - total, y, w: total, h, fill: { type: "none" }, line: { color: C.ink, width: 2 } });
}
// Portraits : préparés par portraits.js (niveaux de gris, recadrés), crédits lus dans le site.
const PORTRAITS = path.join(__dirname, "portraits");
const CREDITS = JSON.parse(fs.readFileSync(path.join(PORTRAITS, EN ? "credits.en.json" : "credits.json"), "utf8"));
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
  const parts = keys.length ? ["Sources" + DP + keys.map(k => SRC[k][0]).join(" · ")] : [];
  for (const c of s.photos || []) parts.push(`Photo${DP}${c.auteur} (${c.licence}, Wikimedia Commons), ${RETOUCHE}`);
  if (s.groupePhotos) parts.push(t("Photos : crédits diapositive 22", "Photos: credits on slide 22"));
  const txt = parts.join(" · ");
  s.addText(txt, { x: M, y: 7.0, w: W - 2 * M - 0.8, h: 0.3, fontFace: FS, fontSize: 9, color: C.sub, italic: true });
}
function notes(s, { idee, faits, nuance, sources, photos }) {
  if (photos) s.photos = Object.entries(CREDITS).filter(([id]) => RANK.some(r => idOf(r[0]) === id)).map(([, c]) => c);
  const src = (sources || []).map(k => `- ${SRC[k][0]}${DP}${SRC[k][1]}`)
    .concat((s.photos || []).map(c => `- Photo${DP}${c.auteur}, ${c.licence}${DP}${c.source} (${RETOUCHE})`)).join("\n");
  const [hIdee, hFaits, hNuance] = EN ? ["IDEA TO DEFEND", "FACTS", "HISTORIOGRAPHICAL NUANCE"] : ["IDÉE À DÉFENDRE", "FAITS", "NUANCE HISTORIOGRAPHIQUE"];
  s.addNotes(
    `${hIdee}\n${idee}\n\n${hFaits}\n${faits.map(f => "- " + f).join("\n")}\n\n${hNuance}\n${nuance}` +
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
// 96,0 en français, 96.0 en anglais
const num = v => (EN ? v.toFixed(1) : v.toFixed(1).replace(".", ","));
const MARQUE = t("Ingénieurs de la F1", "F1 Engineers");

// ===== 1 — Titre =====
{
  const s = newSlide(1);
  s.addText(MARQUE, { x: M, y: 0.35, w: 6, h: 0.45, fontFace: F, fontSize: 20, bold: true, color: C.ink });
  s.addShape(pres.shapes.LINE, { x: M, y: 0.85, w: W - 2 * M, h: 0, line: { color: C.ink, width: 2 } });
  s.addText(pres.title, { x: M, y: 1.7, w: 11.5, h: 1.9, fontFace: F, fontSize: 60, bold: true, color: C.ink, valign: "top" });
  s.addText(t("De Cooper à Newey : qui a réellement changé la grammaire technique de la discipline ?", "From Cooper to Newey: who really changed the technical grammar of the sport?"),
    { x: M, y: 3.95, w: 11, h: 0.9, fontFace: FS, fontSize: 22, italic: true, color: C.sub, valign: "top" });
  // Frise des générations, sans noms
  const y = 5.6, x0 = M, x1 = W - M;
  s.addShape(pres.shapes.LINE, { x: x0, y, w: x1 - x0, h: 0, line: { color: C.ink, width: 1.5 } });
  ["1950", "1960", "1970", "1980", "1990", "2000", "2010", "2020"].forEach((d, i, a) => {
    const x = x0 + (i * (x1 - x0)) / (a.length - 1);
    s.addShape(pres.shapes.LINE, { x, y: y - 0.12, w: 0, h: 0.24, line: { color: C.ink, width: 1.5 } });
    s.addText(d, { x: x - 0.4, y: y + 0.15, w: 0.8, h: 0.3, fontFace: F, fontSize: 11, color: C.sub, align: "center" });
  });
  notes(s, {
    idee: t("Le sujet n'est pas « qui a gagné le plus », mais qui a obligé le plateau à changer sa manière de construire une F1.",
      "The question is not “who won the most”, but who forced the grid to change the way it built an F1 car."),
    faits: EN
      ? ["Twenty engineers, four tiers.", "Five of them (Tier A) changed the grammar of F1; fifteen others transformed subsystems, methods or technical trajectories."]
      : ["Vingt ingénieurs, quatre tiers.", "Cinq d'entre eux (Tier A) ont changé la grammaire de la F1 ; quinze autres ont transformé des sous-systèmes, des méthodes ou des trajectoires."],
    nuance: t("Le classement est un instrument comparatif construit par une méthode explicite, pas un verdict historique.",
      "The ranking is a comparative instrument built with an explicit method, not a historical verdict."),
    sources: [],
  });
}

// ===== 2 — La mauvaise question =====
{
  const s = newSlide(2);
  title(s, t("« Qui a gagné le plus ? » n'est pas la bonne question", "“Who won the most?” is not the right question"), t("Point de départ", "Starting point"));
  const pairs = EN
    ? [["Titles", "Innovation"], ["Innovation", "Invention"], ["Invention", "Diffusion"], ["Technical direction", "Personal authorship"]]
    : [["Titres", "Innovation"], ["Innovation", "Invention"], ["Invention", "Diffusion"], ["Direction technique", "Paternité personnelle"]];
  pairs.forEach(([a, b], i) => {
    const y = 2.0 + i * 0.85;
    box(s, 2.2, y, 3.6, 0.65, a, { size: 18, bold: true });
    s.addText("≠", { x: 5.9, y, w: 1.5, h: 0.65, fontFace: F, fontSize: 30, bold: true, color: C.ink, align: "center", valign: "middle" });
    box(s, 7.5, y, 3.6, 0.65, b, { size: 18, bold: true });
  });
  s.addText(t("Le classement mesure la capacité à déplacer durablement la frontière technique.", "The ranking measures the capacity to shift the technical frontier for good."),
    { x: M, y: 5.7, w: W - 2 * M, h: 0.6, fontFace: FS, fontSize: 18, italic: true, color: C.ink, align: "center" });
  notes(s, {
    idee: t("Le palmarès brut ne suffit pas à mesurer une révolution technique.", "A raw record of results is not enough to measure a technical revolution."),
    faits: EN
      ? ["Sporting results count for only 10% of the score.", "Lasting influence on F1 car design counts for 35%: it is the dominant criterion.", "The same innovation passes through several roles: inventor, first applier, developer, diffuser."]
      : ["Les résultats sportifs ne pèsent que 10 % de la note.", "L'influence durable sur la conception des F1 pèse 35 %, c'est le critère dominant.", "Une même innovation passe par plusieurs rôles : inventeur, applicateur, développeur, diffuseur."],
    nuance: t("Une voiture championne peut n'avoir rien inventé ; une rupture majeure peut n'avoir rien gagné tout de suite.",
      "A championship-winning car may have invented nothing; a major breakthrough may have won nothing straight away."),
    sources: ["innov"],
  });
}

// ===== 3 — La méthode =====
{
  const s = newSlide(3);
  title(s, t("Cinq critères, dominés par l'influence durable", "Five criteria, led by lasting influence"), t("La méthode", "The method"));
  const crit = EN
    ? [["Lasting influence", 35], ["Identifiable breakthrough", 30], ["Breadth of the field transformed", 15], ["Linked sporting results", 10], ["Authorship / traceability", 10]]
    : [["Influence durable", 35], ["Rupture identifiable", 30], ["Amplitude du champ transformé", 15], ["Résultats sportifs liés", 10], ["Paternité / traçabilité", 10]];
  const x0 = 4.6, maxW = 7.4;
  crit.forEach(([lab, p], i) => {
    const y = 2.05 + i * 0.8;
    s.addText(lab, { x: M, y, w: 3.9, h: 0.55, fontFace: F, fontSize: 16, color: C.ink, align: "right", valign: "middle" });
    s.addShape(pres.shapes.RECTANGLE, { x: x0, y: y + 0.08, w: (maxW * p) / 35, h: 0.4, fill: { color: i === 0 ? C.ink : C.D }, line: { color: i === 0 ? C.ink : C.D } });
    s.addText(p + t(" %", "%"), { x: x0 + (maxW * p) / 35 + 0.1, y, w: 1, h: 0.55, fontFace: F, fontSize: 16, bold: true, color: C.ink, valign: "middle" });
  });
  s.addText(t("Les scores sont un instrument comparatif, pas des faits historiques.", "The scores are a comparative instrument, not historical facts."),
    { x: M, y: 6.2, w: W - 2 * M, h: 0.4, fontFace: FS, fontSize: 14, italic: true, color: C.sub, align: "center" });
  notes(s, {
    idee: t("La note privilégie l'influence durable et la rupture identifiable (65 % à elles deux).", "The score favours lasting influence and an identifiable breakthrough (65% between them)."),
    faits: EN
      ? ["Weighting: breakthrough 30%, lasting influence 35%, breadth 15%, results 10%, authorship 10%.", "Secondary diagnostics (nature of the breakthrough, diffusion, longevity, banned innovation, repetition, counterfactual, object/process) correct and interpret the score without being added to it."]
      : ["Pondération : rupture 30 %, influence durable 35 %, amplitude 15 %, résultats 10 %, paternité 10 %.", "Des diagnostics secondaires (nature de la rupture, diffusion, longévité, innovation interdite, répétition, contrefactuel, objet/processus) corrigent et interprètent la note, sans s'y additionner."],
    nuance: t("Un écart de 1 ou 2 points ne doit pas être interprété comme une différence scientifique de valeur.",
      "A gap of 1 or 2 points must not be read as a scientific difference in merit."),
    sources: [],
  });
}

// ===== 4 — Le test de causalité =====
{
  const s = newSlide(4);
  title(s, t("Une innovation a plusieurs auteurs, à des étapes différentes", "An innovation has several authors, at different stages"), t("Le test de causalité", "The causation test"));
  const steps = EN
    ? ["Invention", "F1 application", "Maturation", "Domination", "Diffusion", "Standard"]
    : ["Invention", "Application F1", "Maturation", "Domination", "Diffusion", "Standard"];
  const bw = 1.7, gap = 0.32, x0 = (W - (steps.length * bw + (steps.length - 1) * gap)) / 2, y = 2.6;
  steps.forEach((st, i) => {
    const x = x0 + i * (bw + gap);
    box(s, x, y, bw, 0.9, st, { size: 15, bold: true });
    if (i < steps.length - 1) arrow(s, x + bw + 0.03, y + 0.45, x + bw + gap - 0.03, y + 0.45);
  });
  const ex = EN
    ? ["Ground effect", "Cooper rear engine", "Cosworth DFV", "Williams active suspension"]
    : ["Effet de sol", "Cooper moteur arrière", "Cosworth DFV", "Suspension active Williams"];
  s.addText(t("Exemples", "Examples"), { x: M, y: 4.6, w: 3, h: 0.35, fontFace: F, fontSize: 12, bold: true, color: C.sub });
  ex.forEach((e, i) => box(s, M + i * 3.07, 5.0, 2.9, 0.7, e, { size: 14, fill: C.bg }));
  notes(s, {
    idee: t("Il faut distribuer le mérite selon le rôle réel : on ne crédite jamais intégralement plusieurs personnes de la même contribution.",
      "Credit must be shared out according to each person's actual role: several people are never given full credit for the same contribution."),
    faits: EN ? [
      "Ground effect: Wright and Rudd (BRM, then Lotus), Chapman who sets the mission; Bellamy draws the Lotus 78, Ogilvie its suspension, Southgate takes part in development.",
      "Cooper: John Cooper as architect of the switch, Owen Maddock as central designer of the T51/T53.",
      "DFV: a Cosworth achievement, Duckworth the central technical figure, Costin co-founder and a major contributor.",
      "Williams active suspension: Head, Dernie, Lowe and others.",
    ] : [
      "Effet de sol : Wright et Rudd (BRM puis Lotus), Chapman qui fixe la mission ; Bellamy dessine la Lotus 78, Ogilvie ses suspensions, Southgate participe au développement.",
      "Cooper : John Cooper architecte du basculement, Owen Maddock concepteur central des T51/T53.",
      "DFV : réalisation Cosworth, Duckworth figure technique centrale, Costin cofondateur et acteur majeur.",
      "Williams active : Head, Dernie, Lowe et d'autres.",
    ],
    nuance: t("Sept rôles distincts : inventeur, premier applicateur, architecte, développeur, industrialiseur, leader technique, diffuseur.",
      "Seven distinct roles: inventor, first applier, architect, developer, industrialiser, technical leader, diffuser."),
    sources: ["lotus79", "msT51", "innov", "fw15c"],
  });
}

// ===== 5 — Les quatre tiers =====
{
  const s = newSlide(5);
  title(s, t("Vingt ingénieurs, quatre tiers", "Twenty engineers, four tiers"), t("Vue d'ensemble", "Overview"));
  const tiers = EN
    ? [["A", "Paradigm revolutionaries"], ["B", "Major systemic transformers"], ["C", "Structuring innovators"], ["D", "More localised or more shared impact"]]
    : [["A", "Révolutionnaires de paradigme"], ["B", "Transformateurs systémiques majeurs"], ["C", "Innovateurs structurants"], ["D", "Impact plus localisé ou plus partagé"]];
  const hs = [1.15, 0.8, 0.8, 0.8];
  let y = 1.85;
  tiers.forEach(([tr, lab], r) => {
    const h = hs[r], col = TIER[tr];
    s.addText([{ text: "Tier " + tr, options: { bold: true, fontSize: r === 0 ? 20 : 15, color: col === C.D ? C.Cc : col, breakLine: true } }, { text: lab, options: { fontSize: 10, color: C.sub } }],
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
    idee: t("Cinq ingénieurs ont changé la grammaire de la F1 ; quinze autres ont transformé des sous-systèmes, des méthodes ou des trajectoires majeures.",
      "Five engineers changed the grammar of F1; fifteen others transformed subsystems, methods or major technical trajectories."),
    faits: EN
      ? ["Tier A: a lasting change to the technical grammar, a clear “before / after”, diffusion across the whole grid, well-documented personal causation.", "Tier B: at least one limit (a more collective attribution, a more specialised reach, a shorter duration, a dependence on the regulations).", "Tiers C and D: a major contribution, but less paradigmatic or less exclusive."]
      : ["Tier A : changement durable de la grammaire technique, « avant / après », diffusion à tout le plateau, causalité personnelle documentée.", "Tier B : au moins une limite (attribution plus collective, portée plus spécialisée, durée plus courte, dépendance réglementaire).", "Tiers C et D : contribution majeure, mais moins paradigmatique ou moins exclusive."],
    nuance: t("Les scores détaillés ne sont pas encore montrés : on lit d'abord la structure, pas les décimales.",
      "The detailed scores are not shown yet: read the structure first, not the decimals."),
    sources: [],
  });
}

// ===== 6 — Tier A : la thèse =====
{
  const s = newSlide(6);
  title(s, t("Cinq questions qui ont changé la F1", "Five questions that changed F1"), t("Tier A — la thèse", "Tier A — the thesis"));
  const q = EN
    ? [["Cooper", "john-cooper", "Where should the engine go?"], ["Chapman", "colin-chapman", "How should the car be built?"], ["Duckworth", "keith-duckworth", "How should the engine be integrated?"], ["Barnard", "john-barnard", "With which materials and interfaces?"], ["Newey", "adrian-newey", "How can the whole aerodynamic system be optimised?"]]
    : [["Cooper", "john-cooper", "Où placer le moteur ?"], ["Chapman", "colin-chapman", "Comment construire la voiture ?"], ["Duckworth", "keith-duckworth", "Comment intégrer le moteur ?"], ["Barnard", "john-barnard", "Avec quels matériaux et interfaces ?"], ["Newey", "adrian-newey", "Comment optimiser le système aérodynamique complet ?"]];
  q.forEach(([n, id, txt], i) => {
    const y = 1.95 + i * 0.95;
    s.addText(String(i + 1), { x: M, y, w: 0.6, h: 0.75, fontFace: F, fontSize: 28, bold: true, color: C.A, valign: "middle" });
    vignette(s, id, M + 0.55, y + 0.02, 0.52, 0.71);
    s.addText(n, { x: M + 1.25, y, w: 2.05, h: 0.75, fontFace: F, fontSize: 20, bold: true, color: C.ink, valign: "middle" });
    s.addText(txt, { x: M + 3.4, y, w: 8.4, h: 0.75, fontFace: F, fontSize: 20, color: C.ink, valign: "middle" });
    if (i < 4) s.addShape(pres.shapes.LINE, { x: M, y: y + 0.85, w: W - 2 * M, h: 0, line: { color: C.rule, width: 0.75 } });
  });
  footer(s, []);
  notes(s, {
    idee: t("Chaque membre du Tier A a transformé une question fondamentale de la conception d'une F1. C'est la clé intellectuelle du deck.",
      "Each member of Tier A transformed a fundamental question of F1 car design. This is the intellectual key to the deck."),
    faits: EN
      ? ["Cooper: the position of the fundamental components (mid-rear engine).", "Chapman: the architecture of the car (monocoque, stressed engine, aerodynamics, ground effect).", "Duckworth: integrating and supplying the power unit (DFV).", "Barnard: materials and interfaces (carbon, semi-automatic gearbox).", "Newey: optimising the whole as an aerodynamic system."]
      : ["Cooper : position des organes fondamentaux (moteur central-arrière).", "Chapman : architecture de la monoplace (monocoque, moteur structurel, aéro, effet de sol).", "Duckworth : intégration et fourniture du groupe propulseur (DFV).", "Barnard : matériaux et interfaces (carbone, boîte semi-automatique).", "Newey : optimisation de l'ensemble comme système aérodynamique."],
    nuance: t("L'ordre de la slide suit la logique des questions, pas le rang (Chapman est n° 1).",
      "The order on the slide follows the logic of the questions, not the rank (Chapman is no. 1)."),
    sources: ["innov"],
  });
}

// ===== 7 — Chapman =====
{
  const s = newSlide(7);
  title(s, t("Trois ruptures, une philosophie : architecture + légèreté + aéro", "Three breakthroughs, one philosophy: architecture + lightness + aero"), "Colin Chapman");
  cartouche(s, 1, "A", num(96), t("Élevée", "High"));
  portrait(s, "colin-chapman", 10.93, 1.95, 1.8, 2.45);
  const cols = EN
    ? [["Lotus 25", "Aluminium monocoque"], ["Lotus 49", "Engine as a stressed member"], ["Lotus 78 / 79", "Ground effect programme"]]
    : [["Lotus 25", "Monocoque aluminium"], ["Lotus 49", "Moteur élément structurel"], ["Lotus 78 / 79", "Programme effet de sol"]];
  cols.forEach(([car, txt], i) => {
    const x = M + i * 3.42, w = 3.2;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.95, w, h: 2.45, fill: { color: C.white }, line: { color: C.ink, width: 1.5 } });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.95, w, h: 0.08, fill: { color: C.A }, line: { color: C.A } });
    s.addText(car, { x, y: 2.3, w, h: 0.8, fontFace: F, fontSize: 26, bold: true, color: C.ink, align: "center" });
    s.addText(txt, { x, y: 3.2, w, h: 0.8, fontFace: F, fontSize: 17, color: C.sub, align: "center" });
  });
  s.addShape(pres.shapes.RECTANGLE, { x: M, y: 4.9, w: W - 2 * M, h: 1.0, fill: { color: C.bg }, line: { color: C.A, width: 1.5, dashType: "dash" } });
  s.addText([{ text: t("Attribution partagée : ", "Shared attribution: "), options: { bold: true } }, { text: t("Wright / Rudd pour l'effet de sol.", "Wright / Rudd for ground effect.") }],
    { x: M + 0.2, y: 4.9, w: W - 2 * M - 0.4, h: 1.0, fontFace: F, fontSize: 16, color: C.ink, valign: "middle" });
  footer(s, ["type25", "lotusStory", "lotus79"]);
  notes(s, {
    idee: t("Chapman est n° 1 par l'accumulation de ruptures architecturales, pas par une invention unique.",
      "Chapman is no. 1 through an accumulation of architectural breakthroughs, not through a single invention."),
    faits: EN
      ? ["Lotus Type 25: the aluminium monocoque generalised as the F1 chassis architecture.", "Lotus family of the second half of the 1960s: the engine used as a stressed member (Lotus 49, with the DFV) — a principle already seen on the Lancia D50, here established as the standard.", "Launched and led the programme that led to ground effect (Lotus 78/79).", "Lotus 72 (1970), co-signed by Maurice Philippe: side-mounted radiators; with its developments, 22 Grands Prix and five titles (Classic Team Lotus)."]
      : ["Lotus Type 25 : généralisation du monocoque aluminium comme architecture de châssis F1.", "Famille Lotus de la seconde moitié des années 1960 : moteur utilisé comme élément structurel (Lotus 49, avec le DFV) — principe déjà vu sur la Lancia D50, ici imposé comme standard.", "Lancement et direction du programme qui débouche sur l'effet de sol (Lotus 78/79).", "Lotus 72 (1970), cosignée par Maurice Philippe : radiateurs latéraux ; avec ses évolutions, 22 Grands Prix et cinq titres (Classic Team Lotus)."],
    nuance: t("Ne pas dire « Chapman a inventé l'effet de sol ». Dire : Chapman a dirigé et catalysé le programme Lotus qui a rendu l'effet de sol opératoire et dominant en F1. Wright et Rudd avaient travaillé le concept chez BRM ; Bellamy dessine la Lotus 78, avec Ogilvie (suspensions) et Southgate (développement).",
      "Do not say “Chapman invented ground effect”. Say: Chapman led and catalysed the Lotus programme that made ground effect work and dominate in F1. Wright and Rudd had worked on the concept at BRM; Bellamy drew the Lotus 78, with Ogilvie (suspension) and Southgate (development)."),
    sources: ["type25", "lotusStory", "lotus79"],
  });
}

// ===== 8 — Barnard =====
{
  const s = newSlide(8);
  title(s, t("Deux innovations indépendantes devenues universelles", "Two independent innovations that became universal"), "John Barnard");
  cartouche(s, 2, "A", num(95), t("Très élevée", "Very high"));
  portrait(s, "john-barnard", 10.93, 1.95, 1.8, 2.45);
  (EN
    ? [["1981", "McLaren MP4/1", "Full carbon-fibre monocoque"], ["1989", "Ferrari 640", "Semi-automatic gearbox, paddles on the wheel"]]
    : [["1981", "McLaren MP4/1", "Monocoque intégral en carbone"], ["1989", "Ferrari 640", "Boîte semi-automatique au volant"]]
  ).forEach(([yr, car, txt], i) => {
    const x = M + i * 5.1, w = 4.9;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.95, w, h: 3.4, fill: { color: C.white }, line: { color: C.ink, width: 1.5 } });
    s.addText(yr, { x, y: 2.1, w, h: 1.1, fontFace: F, fontSize: 54, bold: true, color: C.A, align: "center" });
    s.addText(car, { x, y: 3.3, w, h: 0.7, fontFace: F, fontSize: 24, bold: true, color: C.ink, align: "center" });
    s.addText(txt, { x, y: 4.05, w, h: 0.7, fontFace: F, fontSize: 18, color: C.sub, align: "center" });
  });
  s.addText(t("La paternité personnelle la plus nette : le principal challenger de Chapman.", "The clearest personal authorship: Chapman's main challenger."),
    { x: M, y: 5.5, w: 10.0, h: 0.4, fontFace: FS, fontSize: 17, italic: true, color: C.ink, align: "center" });
  footer(s, ["mp41", "barnard", "f1990"]);
  notes(s, {
    idee: t("Barnard porte deux ruptures indépendantes, directement attribuables, toutes deux devenues des standards.",
      "Barnard carries two independent breakthroughs, directly attributable to him, both of which became standards."),
    faits: EN
      ? ["MP4/1 (1981): the first F1 car with a full carbon-composite monocoque to race in a Grand Prix (the Lotus 88, presented before it, was never allowed to race) — stiffness, weight, safety, industrialisation of composites. The principle became universal.", "Ferrari 640 (1989): semi-automatic gearbox operated from the steering wheel — the gradual end of the H-pattern lever, fewer errors, hands on the wheel, a more compact cockpit."]
      : ["MP4/1 (1981) : première F1 à monocoque intégral en composite carbone à courir en Grand Prix (la Lotus 88, présentée avant elle, n'a jamais été autorisée à courir) — rigidité, masse, sécurité, industrialisation du composite. Le principe devient universel.", "Ferrari 640 (1989) : boîte semi-automatique commandée au volant — fin progressive du levier en H, moins d'erreurs, mains sur le volant, cockpit plus compact."],
    nuance: t("Si la pondération « paternité directe » augmentait sensiblement, Barnard pourrait passer devant Chapman. Barnard conçoit la MP4/1 entouré notamment de Steve Nichols et d'Alan Jenkins. L'idée des palettes vient de son bureau d'études selon lui, de Piero Lardi Ferrari selon Motorsport.com : Barnard les a conçues et introduites en course.",
      "If the weight given to direct authorship rose significantly, Barnard could move ahead of Chapman. Barnard designed the MP4/1 with, among others, Steve Nichols and Alan Jenkins. The idea of the paddles came from his own design office according to him, from Piero Lardi Ferrari according to Motorsport.com: Barnard designed them and brought them into racing."),
    sources: ["mp41", "barnard", "f1990", "wp88"],
  });
}

// ===== 9 — Cooper =====
{
  const s = newSlide(9);
  title(s, t("Une révolution topologique de la monoplace", "A topological revolution of the single-seater"), "John Cooper");
  cartouche(s, 3, "A", num(93.5), t("Élevée", "High"));
  // Schémas vue de dessus : avant / après
  function car(x, engineFront, label) {
    const y = 2.6, w = 4.6, h = 1.3;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.4, fill: { color: C.white }, line: { color: C.ink, width: 1.5 } });
    const ex = engineFront ? x + 0.35 : x + w - 1.85;
    s.addShape(pres.shapes.RECTANGLE, { x: ex, y: y + 0.3, w: 1.5, h: h - 0.6, fill: { color: engineFront ? C.Cc : C.A }, line: { color: C.ink, width: 0 } });
    s.addText(t("moteur", "engine"), { x: ex, y: y + 0.3, w: 1.5, h: h - 0.6, fontFace: F, fontSize: 12, bold: true, color: C.white, align: "center", valign: "middle" });
    const px = engineFront ? x + w - 1.6 : x + 1.4;
    s.addShape(pres.shapes.OVAL, { x: px, y: y + 0.35, w: 0.6, h: 0.6, fill: { color: C.bg }, line: { color: C.ink, width: 1.5 } });
    s.addText(t("pilote", "driver"), { x: px - 0.3, y: y + h + 0.05, w: 1.2, h: 0.3, fontFace: F, fontSize: 10, color: C.sub, align: "center" });
    s.addText(label, { x, y: y - 0.6, w, h: 0.45, fontFace: F, fontSize: 18, bold: true, color: C.ink, align: "center" });
    s.addText(t("avant", "front"), { x, y: y + h + 0.05, w: 1.2, h: 0.3, fontFace: F, fontSize: 10, color: C.sub });
  }
  car(M + 0.2, true, t("Moteur avant", "Front engine"));
  arrow(s, 5.75, 3.25, 7.35, 3.25, C.A);
  car(7.6, false, t("Moteur central-arrière", "Mid-rear engine"));
  s.addText([{ text: t("Cooper T51, titres 1959 et 1960", "Cooper T51, 1959 and 1960 titles"), options: { bold: true, breakLine: true } }, { text: t("Chef designer : Owen Maddock", "Chief designer: Owen Maddock") }],
    { x: M, y: 4.9, w: W - 2 * M, h: 0.9, fontFace: F, fontSize: 17, color: C.ink, align: "center" });
  footer(s, ["msT51", "nye", "innov"]);
  notes(s, {
    idee: t("Le passage au moteur central-arrière change la topologie même de la monoplace.", "The move to a mid-rear engine changes the very topology of the single-seater."),
    faits: EN
      ? ["Simultaneous effects: weight distribution, polar moment, traction, packaging, chassis architecture, future aerodynamics.", "After Cooper's titles in 1959 and 1960, the front engine quickly became obsolete.", "Since 1959, every F1 world champion has driven with the engine behind them (Motor Sport)."]
      : ["Effets simultanés : répartition des masses, moment polaire, motricité, encombrement, architecture du châssis, aérodynamique future.", "Après les titres Cooper de 1959 et 1960, le moteur avant devient rapidement obsolète.", "Depuis 1959, tous les champions du monde de F1 ont roulé avec le moteur derrière eux (Motor Sport)."],
    nuance: t("Cooper n'a pas inventé la disposition (déjà employée, et choisie sur la première 500 « pour des raisons largement pratiques ») : il l'a popularisée et rendue victorieuse. Ne pas effacer Owen Maddock, chef designer. Formulation : Cooper a imposé l'architecture moteur arrière avec une équipe de conception dans laquelle Owen Maddock joue un rôle central (T51/T53).",
      "Cooper did not invent the layout (already used, and chosen on the first 500 “for largely practical reasons”): he popularised it and made it win. Do not erase Owen Maddock, the chief designer. Wording: Cooper established the rear-engine architecture with a design team in which Owen Maddock played a central role (T51/T53)."),
    sources: ["msT51", "nye", "innov"],
  });
}

// ===== 10 — Duckworth =====
{
  const s = newSlide(10);
  title(s, t("Une révolution technique et économique simultanée", "A technical and economic revolution at once"), "Keith Duckworth");
  cartouche(s, 4, "A", num(92.5), t("Élevée", "High"));
  const steps = EN
    ? ["DFV", "High-performance engine", "Stressed engine", "Available to all teams", "A new economy for the grid"]
    : ["DFV", "Moteur performant", "Moteur structurel", "Accessible aux équipes", "Nouvelle économie du plateau"];
  const bw = 2.15, gap = 0.3, x0 = M;
  steps.forEach((st, i) => {
    const x = x0 + i * (bw + gap);
    box(s, x, 2.0, bw, 1.0, st, { size: 15, bold: true, fill: i === 0 ? C.A : C.white, color: i === 0 ? C.white : C.ink, line: i === 0 ? C.A : C.ink });
    if (i < steps.length - 1) arrow(s, x + bw + 0.02, 2.5, x + bw + gap - 0.02, 2.5);
  });
  s.addText("155", { x: M, y: 3.4, w: 4, h: 1.6, fontFace: F, fontSize: 96, bold: true, color: C.A });
  s.addText(t("victoires en Grand Prix de championnat du monde, 1967-1983", "world championship Grand Prix wins, 1967-1983"), { x: M + 2.4, y: 3.75, w: 7, h: 0.9, fontFace: F, fontSize: 22, color: C.ink, valign: "middle" });
  s.addText(t("Cosworth = Duckworth + Costin + organisation", "Cosworth = Duckworth + Costin + an organisation"), { x: M, y: 5.4, w: W - 2 * M, h: 0.6, fontFace: F, fontSize: 18, bold: true, color: C.ink });
  footer(s, ["innov", "ms67"]);
  notes(s, {
    idee: t("Le DFV transforme le moteur et l'écosystème industriel de la F1.", "The DFV transforms both the engine and the industrial ecosystem of F1."),
    faits: EN
      ? ["A compact, powerful engine, a structural component of the Lotus 49 (a principle already used by the Lancia D50 in 1954, generalised with the DFV).", "Available to many teams: no more need for an in-house engine, resources focused on chassis and aerodynamics.", "155 world championship Grand Prix wins according to Formula 1, from 1967 to 1983, the last ones in DFY form (GrandPrix.com counts 154).", "First race: Zandvoort, 4 June 1967, pole for Hill, win for Clark."]
      : ["Moteur compact et performant, composant structurel de la Lotus 49 (principe déjà employé par la Lancia D50 en 1954, généralisé avec le DFV).", "Disponible pour de nombreuses équipes : plus besoin de moteur propriétaire, ressources concentrées sur châssis et aéro.", "155 victoires en Grand Prix de championnat du monde selon Formula 1, de 1967 à 1983, les dernières en version DFY (GrandPrix.com en compte 154).", "Première course : Zandvoort, 4 juin 1967, pole de Hill, victoire de Clark."],
    nuance: t("Ne pas présenter le DFV comme une création individuelle : réalisation Cosworth, Duckworth figure technique centrale, Mike Costin cofondateur et acteur majeur.",
      "Do not present the DFV as an individual creation: a Cosworth achievement, with Duckworth as the central technical figure and Mike Costin as co-founder and a major contributor."),
    sources: ["innov", "ms67"],
  });
}

// ===== 11 — Newey =====
{
  const s = newSlide(11);
  title(s, t("Le génie de Newey est la répétition, pas le coup unique", "Newey's genius is repetition, not a single stroke"), "Adrian Newey");
  cartouche(s, 5, "A", num(91.5), t("Très élevée", "Very high"));
  portrait(s, "adrian-newey", 10.93, 1.95, 1.8, 2.45);
  const teams = ["March / Leyton House", "Williams", "McLaren", "Red Bull", "Aston Martin"];
  const y = 3.0, x0 = M + 1.0, x1 = 9.5;
  s.addShape(pres.shapes.LINE, { x: x0, y, w: x1 - x0, h: 0, line: { color: C.ink, width: 2 } });
  teams.forEach((tm, i) => {
    const x = x0 + (i * (x1 - x0)) / (teams.length - 1);
    s.addShape(pres.shapes.OVAL, { x: x - 0.15, y: y - 0.15, w: 0.3, h: 0.3, fill: { color: C.A }, line: { color: C.A } });
    s.addText(tm, { x: x - 1.1, y: y - 0.95, w: 2.2, h: 0.6, fontFace: F, fontSize: 18, bold: true, color: C.ink, align: "center", valign: "bottom" });
    s.addText(["1988-1990", "1991-1996", "1997-2005", "2006-2024", t("depuis 2025", "since 2025")][i], { x: x - 1.1, y: y + 0.25, w: 2.2, h: 0.4, fontFace: F, fontSize: 12, color: C.sub, align: "center" });
  });
  s.addText(t("Règlements différents, même compétence : contrôle du système aérodynamique.", "Different regulations, the same skill: mastery of the aerodynamic system."),
    { x: M, y: 4.3, w: 10.0, h: 0.7, fontFace: F, fontSize: 20, color: C.ink, align: "center" });
  footer(s, ["innov", "newey", "f1990"]);
  notes(s, {
    idee: t("Ne pas chercher « l'invention Newey » : son apport est une méthode systémique, démontrée sous plusieurs règlements et dans plusieurs équipes.",
      "Do not look for “the Newey invention”: his contribution is a systemic method, demonstrated under several sets of regulations and in several teams."),
    faits: EN
      ? ["Designing the car as an integrated aerodynamic system: suspension, geometry, cooling, structure and packaging serving the airflow.", "Results at the very top with Williams, McLaren and Red Bull; career: March (which became Leyton House), Williams, McLaren, Red Bull, Aston Martin since 2025."]
      : ["Concevoir la monoplace comme un système aérodynamique intégré : suspension, géométrie, refroidissement, structure et packaging au service du flux.", "Résultats au sommet chez Williams, McLaren et Red Bull ; parcours : March devenue Leyton House, Williams, McLaren, Red Bull, Aston Martin depuis 2025."],
    nuance: t("Pourquoi pas n° 1 : le palmarès ne pèse que 10 %, et sa paternité est plus distribuée dans les grandes organisations modernes. Formulation : rôle de premier plan dans l'architecture aérodynamique de plusieurs générations de voitures championnes, au sein d'équipes techniques collectives. Selon Patrick Head, Newey n'a pris aucune part à la suspension active Williams, qui servait de plateforme stable à son aérodynamique.",
      "Why not no. 1: results count for only 10%, and his authorship is more distributed within large modern organisations. Wording: a leading role in the aerodynamic architecture of several generations of championship-winning cars, within collective technical teams. According to Patrick Head, Newey took no part in the Williams active suspension, which served as a stable platform for his aerodynamics."),
    sources: ["innov", "newey", "f1990", "wpNewey"],
  });
}

// ===== 12 — Chapman vs Barnard =====
{
  const s = newSlide(12);
  title(s, t("Pourquoi Chapman devant Barnard ?", "Why Chapman ahead of Barnard?"), t("Le vrai débat pour la première place", "The real debate for first place"));
  portrait(s, "colin-chapman", M, 1.9, 1.4, 1.9);
  portrait(s, "john-barnard", W - M - 1.4, 1.9, 1.4, 1.9);
  footer(s, []);
  const hdr = { bold: true, color: C.white, fill: { color: C.ink }, align: "center" };
  const crit = EN
    ? [["Number of breakthroughs", "++", "+"], ["Direct authorship", "+", "++"], ["Architectural reach", "++", "++"], ["Diffusion", "++", "++"], ["Repetition", "++", "+"]]
    : [["Nombre de ruptures", "++", "+"], ["Paternité directe", "+", "++"], ["Portée architecturale", "++", "++"], ["Diffusion", "++", "++"], ["Répétition", "++", "+"]];
  const rows = [
    [{ text: t("Critère", "Criterion"), options: { ...hdr, align: "left" } }, { text: "Chapman", options: hdr }, { text: "Barnard", options: hdr }],
    ...crit.map(([c, a, b]) => [
      { text: c }, { text: a, options: { align: "center", bold: a === "++", color: a === "++" ? C.A : C.ink } }, { text: b, options: { align: "center", bold: b === "++", color: b === "++" ? C.A : C.ink } },
    ]),
  ];
  s.addTable(rows, { x: 2.2, y: 1.9, w: 8.9, colW: [4.3, 2.3, 2.3], fontFace: F, fontSize: 18, color: C.ink, fill: { color: C.white }, border: { type: "solid", color: C.rule, pt: 0.75 }, rowH: 0.55 });
  s.addText(t("Chapman gagne par largeur historique ; Barnard gagne en traçabilité personnelle.", "Chapman wins on historical breadth; Barnard wins on personal traceability."),
    { x: M, y: 5.6, w: W - 2 * M, h: 0.6, fontFace: FS, fontSize: 19, italic: true, color: C.ink, align: "center" });
  notes(s, {
    idee: t("Avec cette méthode, le débat sérieux n'est pas Chapman contre Newey, mais Chapman contre Barnard.",
      "With this method, the serious debate is not Chapman versus Newey, but Chapman versus Barnard."),
    faits: EN
      ? ["Chapman leads through an accumulation of architectural breakthroughs.", "Barnard leads on direct authorship of two innovations that became universal.", "One point apart (96 against 95): the difference is not scientific."]
      : ["Chapman domine par l'accumulation de ruptures architecturales.", "Barnard domine en paternité directe de deux innovations devenues universelles.", "Un point d'écart (96 contre 95) : la différence n'est pas scientifique."],
    nuance: t("Le résultat dépend de la pondération : avec une paternité directe plus lourde, Barnard passerait devant.",
      "The result depends on the weighting: with more weight on direct authorship, Barnard would move ahead."),
    sources: ["type25", "mp41"],
  });
}

// ===== 13 — Tier B =====
{
  const s = newSlide(13);
  title(s, t("Tier B : cinq transformateurs systémiques", "Tier B: five systemic transformers"), t("Rangs 6 à 10", "Ranks 6 to 10"));
  const cards = EN
    ? [["Dudot", "bernard-dudot", "Power"], ["Murray", "gordon-murray", "Radical architecture"], ["Forghieri", "mauro-forghieri", "Total engineering"], ["Wright", "peter-wright", "Ground effect"], ["Dernie", "frank-dernie", "A silent digital revolution"]]
    : [["Dudot", "bernard-dudot", "Propulsion"], ["Murray", "gordon-murray", "Architecture radicale"], ["Forghieri", "mauro-forghieri", "Ingénierie totale"], ["Wright", "peter-wright", "Effet de sol"], ["Dernie", "frank-dernie", "Révolution numérique silencieuse"]];
  cards.forEach(([n, id, txt], i) => {
    const x = M + i * 2.45;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.85, w: 2.25, h: 3.75, fill: { color: C.white }, line: { color: C.ink, width: 1.5 } });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.85, w: 2.25, h: 0.08, fill: { color: C.B }, line: { color: C.B } });
    vignette(s, id, x + (2.25 - 1.0) / 2, 2.05, 1.0, 1.36);
    s.addText(String(i + 6), { x, y: 3.45, w: 2.25, h: 0.45, fontFace: F, fontSize: 22, bold: true, color: C.B, align: "center" });
    s.addText(n, { x, y: 3.85, w: 2.25, h: 0.5, fontFace: F, fontSize: 20, bold: true, color: C.ink, align: "center" });
    s.addText(txt, { x: x + 0.1, y: 4.35, w: 2.05, h: 1.1, fontFace: F, fontSize: 15, color: C.sub, align: "center", valign: "top" });
  });
  s.addText(t("Face au Tier A : attribution plus collective, portée plus spécialisée ou diffusion inégale.", "Compared with Tier A: a more collective attribution, a more specialised reach or uneven diffusion."),
    { x: M, y: 5.8, w: W - 2 * M, h: 0.7, fontFace: FS, fontSize: 15, italic: true, color: C.ink, align: "center" });
  footer(s, ["renault", "murray", "f312t", "lotus79", "msDernie"]);
  notes(s, {
    idee: t("Le Tier B transforme durablement un domaine central de la F1, avec une limite par rapport au Tier A.",
      "Tier B lastingly transforms a central field of F1, with one limit compared with Tier A."),
    faits: EN
      ? ["Dudot (90): turbo, pneumatic valve return, V10 at Renault.", "Murray (88.5): BT46B, Brabham architectures, the tactical pit stop, a contribution to the MP4/4 (whose authorship is disputed with Steve Nichols).", "Forghieri (87.5): 312T and transverse gearbox, centralisation of masses.", "Wright (86.5): causal development of Lotus ground effect.", "Dernie (85): CAD/CAE, data acquisition, wind tunnel, active suspension."]
      : ["Dudot (90) : turbo, distribution pneumatique, V10 chez Renault.", "Murray (88,5) : BT46B, architectures Brabham, pit-stop tactique, contribution à la MP4/4 (paternité discutée avec Steve Nichols).", "Forghieri (87,5) : 312T et boîte transversale, centralisation des masses.", "Wright (86,5) : développement causal de l'effet de sol Lotus.", "Dernie (85) : CAO/CAE, acquisition de données, soufflerie, suspension active."],
    nuance: t("Murray : diffusion inégale de certaines ruptures. Dudot : réalisations d'une organisation, Renault Sport.",
      "Murray: uneven diffusion of some breakthroughs. Dudot: the achievements of an organisation, Renault Sport."),
    sources: ["renault", "msRenault", "murray", "f312t", "f312b3", "forgObit", "lotus79", "msDernie"],
  });
}

// ===== 14 — Dudot =====
{
  const s = newSlide(14);
  title(s, t("La révolution moteur : turbo, rappel pneumatique, V10", "The engine revolution: turbo, pneumatic valves, V10"), "Bernard Dudot");
  cartouche(s, 6, "B", num(90), t("Élevée", "High"));
  const st = EN
    ? [["Turbo", "Adopted by the whole grid"], ["Pneumatic valve return", "The general solution in the 1990s"], ["V10", "67° V10 under Dudot's direction"]]
    : [["Turbo", "Adopté par tout le plateau"], ["Rappel pneumatique des soupapes", "Solution générale dans les années 1990"], ["V10", "V10 67° sous la direction de Dudot"]];
  st.forEach(([a, d], i) => {
    const x = M + 0.3 + i * 4.15;
    box(s, x, 2.2, 3.4, 1.1, a, { size: 18, bold: true, line: C.B, lw: 1.5 });
    s.addText(d, { x, y: 3.45, w: 3.4, h: 0.8, fontFace: F, fontSize: 14, color: C.sub, align: "center", valign: "top" });
    if (i < 2) arrow(s, x + 3.45, 2.75, x + 4.1, 2.75, C.B);
  });
  s.addShape(pres.shapes.RECTANGLE, { x: M, y: 4.8, w: W - 2 * M, h: 1.0, fill: { color: C.bg }, line: { color: C.B, width: 1.5, dashType: "dash" } });
  s.addText(t("Renault Sport est une organisation : Dudot n'est pas un inventeur solitaire.", "Renault Sport is an organisation: Dudot is not a lone inventor."),
    { x: M + 0.2, y: 4.8, w: W - 2 * M - 0.4, h: 1.0, fontFace: F, fontSize: 16, color: C.ink, valign: "middle" });
  footer(s, ["renault", "msRenault"]);
  notes(s, {
    idee: t("Dudot est au cœur de trois mutations moteur successives, toutes diffusées au plateau.",
      "Dudot is at the heart of three successive engine changes, all of which spread to the grid."),
    faits: EN
      ? ["Renault's documentation: the turbo was eventually adopted by the whole grid.", "Pneumatic valve return became the general solution in the 1990s.", "Motor Sport documents the 67° V10 designed under Bernard Dudot's direction."]
      : ["Documentation Renault : le turbo finit par être adopté par tout le plateau.", "Le rappel pneumatique des soupapes devient une solution générale dans les années 1990.", "Motor Sport documente le V10 67° conçu sous la direction de Bernard Dudot."],
    nuance: t("Ces réalisations sont celles d'une organisation, Renault Sport ; Dudot ne doit pas être présenté comme inventeur solitaire.",
      "These are the achievements of an organisation, Renault Sport; Dudot must not be presented as a lone inventor."),
    sources: ["renault", "msRenault"],
  });
}

// ===== 15 — Révolutions silencieuses =====
{
  const s = newSlide(15);
  title(s, t("Les révolutions silencieuses", "The silent revolutions"), t("Changer le processus, pas la carrosserie", "Changing the process, not the bodywork"));
  (EN
    ? [["Frank Dernie", "B", ["CAD / CAE", "Data acquisition", "Wind tunnel", "Active suspension"]], ["Ross Brawn", "C", ["Methods", "Organisation", "Early programmes", "Integration"]]]
    : [["Frank Dernie", "B", ["CAO / CAE", "Acquisition de données", "Soufflerie", "Suspension active"]], ["Ross Brawn", "C", ["Méthodes", "Organisation", "Programme anticipé", "Intégration"]]]
  ).forEach(([n, tr, items], i) => {
    const x = M + i * 6.15;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.95, w: 5.9, h: 3.4, fill: { color: C.white }, line: { color: C.ink, width: 1.5 } });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.95, w: 0.08, h: 3.4, fill: { color: TIER[tr] }, line: { color: TIER[tr] } });
    s.addText(n, { x: x + 0.4, y: 2.1, w: 3.5, h: 0.7, fontFace: F, fontSize: 24, bold: true, color: C.ink });
    vignette(s, idOf(n), x + 5.9 - 0.25 - 1.6, 2.1, 1.6, 2.18);
    s.addText(items.map(it => ({ text: it, options: { bullet: true, breakLine: true } })), { x: x + 0.4, y: 2.9, w: 3.5, h: 2.2, fontFace: F, fontSize: 18, color: C.ink, valign: "top", paraSpaceAfter: 6 });
  });
  s.addText(t("Une révolution technique peut transformer le processus sans être visible sur la carrosserie.", "A technical revolution can transform the process without showing on the bodywork."),
    { x: M, y: 5.7, w: W - 2 * M, h: 0.6, fontFace: FS, fontSize: 18, italic: true, color: C.ink, align: "center" });
  footer(s, ["msDernie", "brawn"]);
  notes(s, {
    idee: t("La méthode distingue la révolution de l'objet et la révolution du processus de conception.",
      "The method distinguishes a revolution in the object from a revolution in the design process."),
    faits: EN
      ? ["Dernie: by his own account, early use of CAD/CAE and data acquisition; designer of the first Williams active suspension system (Motor Sport, 2001).", "Brawn: programmes started very early, organisational integration, linking design, operations and strategy; the Mercedes 2014 programme launched early with chassis and engine integrated, before his departure at the end of 2013."]
      : ["Dernie : selon ses propres déclarations, utilisation précoce de la CAO/CAE et de l'acquisition de données ; concepteur du premier système Williams de suspension active (Motor Sport, 2001).", "Brawn : programmes démarrés très en amont, intégration organisationnelle, articulation conception/exploitation/stratégie, programme Mercedes 2014 lancé tôt et intégré châssis-moteur, avant son départ fin 2013."],
    nuance: t("Ne pas écrire « Dernie a inventé seul la suspension active » ni « Brawn a conçu la Mercedes W05 ». Brawn a contribué à mettre en place la méthode et l'intégration qui ont préparé Mercedes à 2014.",
      "Do not write “Dernie single-handedly invented active suspension” or “Brawn designed the Mercedes W05”. Brawn helped put in place the method and integration that prepared Mercedes for 2014."),
    sources: ["msDernie", "msActive", "brawn"],
  });
}

// ===== 16 — Effet de sol =====
{
  const s = newSlide(16);
  title(s, t("L'effet de sol : rétablir la chaîne causale", "Ground effect: restoring the causal chain"), t("Historiographie", "Historiography"));
  const ch = EN
    ? [["BRM", "Wright + Rudd"], ["Lotus", "Chapman sets the mission"], ["Wind tunnel", "venturis / skirts"], ["Lotus 78 / 79", "the breakthrough"], ["Diffusion", "to the whole grid"]]
    : [["BRM", "Wright + Rudd"], ["Lotus", "Chapman fixe la mission"], ["Soufflerie", "venturi / jupes"], ["Lotus 78 / 79", "la percée"], ["Diffusion", "à tout le plateau"]];
  const bw = 2.1, gap = 0.35;
  ch.forEach(([a, b], i) => {
    const x = M + i * (bw + gap), y = 2.4;
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: bw, h: 1.5, fill: { color: i === 3 ? C.ink : C.white }, line: { color: C.ink, width: 1.5 } });
    s.addText([{ text: a, options: { bold: true, fontSize: 18, breakLine: true } }, { text: b, options: { fontSize: 13 } }], { x: x + 0.05, y, w: bw - 0.1, h: 1.5, fontFace: F, color: i === 3 ? C.white : C.ink, align: "center", valign: "middle" });
    if (i < ch.length - 1) arrow(s, x + bw + 0.02, y + 0.75, x + bw + gap - 0.02, y + 0.75);
  });
  s.addText(t("Lotus 78 : dessin Ralph Bellamy, suspensions Martin Ogilvie, développement Tony Southgate.", "Lotus 78: drawn by Ralph Bellamy, suspension by Martin Ogilvie, development with Tony Southgate."),
    { x: M, y: 4.4, w: W - 2 * M, h: 0.5, fontFace: F, fontSize: 15, color: C.sub, align: "center" });
  footer(s, ["lotus79"]);
  notes(s, {
    idee: t("L'effet de sol est une filiation collective ; il faut la raconter dans l'ordre.", "Ground effect is a collective lineage; it has to be told in order."),
    faits: EN
      ? ["Peter Wright and Tony Rudd had worked on the concept at BRM.", "At Lotus, Chapman asked them to rethink the fundamental configuration of an F1 car.", "The wind tunnel work led to the Lotus 78, then the 79; Bellamy drew the 78, Ogilvie its suspension, Southgate took part in development (Formula 1 credits the design to Bellamy and Southgate)."]
      : ["Peter Wright et Tony Rudd avaient travaillé sur le concept chez BRM.", "Chez Lotus, Chapman leur demande de repenser la configuration fondamentale de la F1.", "La soufflerie débouche sur la Lotus 78, puis la 79 ; Bellamy dessine la 78, Ogilvie ses suspensions, Southgate participe au développement (Formula 1 crédite la conception à Bellamy et Southgate)."],
    nuance: t("À éviter : « Chapman a inventé l'effet de sol ». À préférer : Chapman a dirigé et catalysé le programme Lotus qui a rendu l'effet de sol opératoire et dominant. Wright (Tier B) est placé devant Rudd (Tier C) car la contribution directe de Rudd à la solution finale est plus difficile à isoler.",
      "Avoid: “Chapman invented ground effect”. Prefer: Chapman led and catalysed the Lotus programme that made ground effect work and dominate. Wright (Tier B) is placed ahead of Rudd (Tier C) because Rudd's direct contribution to the final solution is harder to isolate."),
    sources: ["lotus79"],
  });
}

// ===== 17 — Tiers C et D =====
{
  const s = newSlide(17);
  title(s, t("Tiers C et D : dix contributions majeures", "Tiers C and D: ten major contributions"), t("Rangs 11 à 20", "Ranks 11 to 20"));
  const data = EN ? [
    [11, "Patrick Head", "Systems engineering", "Williams technical organisation", "Organisation rather than a single breakthrough"],
    [12, "Ross Brawn", "Method", "Early development, integration", "A revolution in process"],
    [13, "Andy Cowell", "Power unit", "Mercedes 2014 hybrid", "Hybridisation imposed by the regulations"],
    [14, "Jean-Claude Migeot", "Aerodynamics", "Raised nose, Tyrrell 019", "Quickly absorbed by general evolution"],
    [15, "Tony Rudd", "Aerodynamics", "Origins of ground effect", "Contribution hard to isolate"],
    [16, "Mike Costin", "Engine", "Co-founder of Cosworth", "DFV authorship less individual"],
    [17, "Vittorio Jano", "Architecture", "Lancia D50", "Work mostly before F1"],
    [18, "Owen Maddock", "Chassis", "Chief designer, 1959-1960 titles", "Credit shared with John Cooper"],
    [19, "Paddy Lowe", "Electronics", "Active suspension software", "A role in a collective chain"],
    [20, "Rory Byrne", "Integration", "Benetton, Ferrari", "No single paradigmatic breakthrough"],
  ] : [
    [11, "Patrick Head", "Ingénierie système", "Organisation technique Williams", "Organisation plus que rupture unique"],
    [12, "Ross Brawn", "Méthode", "Développement anticipé, intégration", "Révolution de processus"],
    [13, "Andy Cowell", "Power unit", "Hybride Mercedes 2014", "Hybridation imposée par le règlement"],
    [14, "Jean-Claude Migeot", "Aérodynamique", "Nez relevé, Tyrrell 019", "Vite absorbé par l'évolution générale"],
    [15, "Tony Rudd", "Aérodynamique", "Genèse de l'effet de sol", "Contribution difficile à isoler"],
    [16, "Mike Costin", "Moteur", "Cofondateur de Cosworth", "Paternité du DFV moins individualisable"],
    [17, "Vittorio Jano", "Architecture", "Lancia D50", "Œuvre surtout antérieure à la F1"],
    [18, "Owen Maddock", "Châssis", "Chef designer, titres 1959-1960", "Crédit partagé avec John Cooper"],
    [19, "Paddy Lowe", "Électronique", "Logiciel suspension active", "Rôle dans une chaîne collective"],
    [20, "Rory Byrne", "Intégration", "Benetton, Ferrari", "Pas de rupture unique paradigmatique"],
  ];
  const hdr = { bold: true, color: C.white, fill: { color: C.ink } };
  const heads = EN ? ["Rank", "", "Engineer", "Field", "Reason for the ranking", "Limit"] : ["Rang", "", "Ingénieur", "Domaine", "Raison du classement", "Limite"];
  const rows = [heads.map(h => ({ text: h, options: hdr }))];
  data.forEach(r => {
    const col = r[0] <= 15 ? C.Cc : C.D;
    rows.push([{ text: String(r[0]), options: { bold: true, color: C.white, fill: { color: col }, align: "center" } }, { text: "" }, { text: r[1], options: { bold: true } }, { text: r[2] }, { text: r[3] }, { text: r[4] }]);
  });
  const rowH = 0.43, colW = [0.7, 0.42, 2.3, 1.9, 3.4, 3.413];
  s.addTable(rows, { x: M, y: 1.8, w: W - 2 * M, colW, fontFace: F, fontSize: 12, color: C.ink, fill: { color: C.white }, border: { type: "solid", color: C.rule, pt: 0.75 }, rowH });
  data.forEach((r, i) => vignette(s, idOf(r[1]), M + colW[0] + 0.05, 1.8 + rowH * (i + 1) + 0.04, 0.32, rowH - 0.08));
  footer(s, ["fw15c", "brawn", "f1990", "d50", "msT51"]);
  notes(s, {
    idee: t("Les tiers C et D réunissent des contributions majeures, mais moins paradigmatiques ou moins exclusives. Pas de slide individuelle : le tableau suffit.",
      "Tiers C and D bring together major contributions that are less paradigmatic or less exclusive. No individual slides: the table is enough."),
    faits: EN
      ? ["Tier C (11-15, dark grey): structuring innovators.", "Tier D (16-20, light grey): less exclusive causation, less general diffusion or a more incremental impact.", "Lowe: Formula 1 credits him with much of the software for the Williams active suspension."]
      : ["Tier C (11-15, gris soutenu) : innovateurs structurants.", "Tier D (16-20, gris clair) : causalité moins exclusive, diffusion moins générale ou impact plus incrémental.", "Lowe : Formula 1 le crédite d'une grande partie du logiciel de la suspension active Williams."],
    nuance: t("Distinguer clairement dans l'écosystème Williams : Head (architecture et direction), Dernie (numérique et programme actif), Lowe (logiciel et électronique), Newey (aérodynamique).",
      "Clearly distinguish roles within the Williams ecosystem: Head (architecture and direction), Dernie (digital tools and the active programme), Lowe (software and electronics), Newey (aerodynamics)."),
    sources: ["fw15c", "lowe", "brawn", "innov", "f1990", "lotus79", "d50", "msT51", "nye", "byrne"],
  });
}

// ===== 18 — Lignées =====
{
  const s = newSlide(18);
  title(s, t("Les grandes lignées techniques", "The great technical lineages"), t("Filiations intellectuelles", "Intellectual lineages"));
  const L = EN ? [
    ["Architecture", ["Cooper", "Chapman", "Barnard"]],
    ["Aerodynamics", ["Chapman / Wright", "Murray / Migeot", "Newey"]],
    ["Engine", ["Duckworth", "Dudot", "Cowell"]],
    ["Digital and control", ["Dernie", "Lowe", "Modern engineering"]],
    ["Systems organisation", ["Head", "Brawn", "Modern F1 teams"]],
  ] : [
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
  s.addText(t("Ce schéma montre des filiations intellectuelles, pas des relations maître-élève.", "This diagram shows intellectual lineages, not master-pupil relationships."),
    { x: M, y: 6.35, w: W - 2 * M, h: 0.45, fontFace: FS, fontSize: 14, italic: true, color: C.sub, align: "center" });
  notes(s, {
    idee: t("Les vingt noms s'organisent en cinq branches de l'ingénierie F1.", "The twenty names fall into five branches of F1 engineering."),
    faits: L.map(([b, chain]) => b + DP + chain.join(" → ") + "."),
    nuance: t("Ce sont des filiations intellectuelles, pas des relations maître-élève systématiques.", "These are intellectual lineages, not systematic master-pupil relationships."),
    sources: [],
  });
}

// ===== 19 — Chronologie (données du site : _data/chronologie.yml, _data/en/chronologie.yml) =====
{
  const s = newSlide(19);
  title(s, t("Soixante-dix ans de ruptures", "Seventy years of breakthroughs"), t("Chronologie", "Timeline"));
  const chrono = require("js-yaml").load(fs.readFileSync(path.join(__dirname, "..", "_data", ...(EN ? ["en"] : []), "chronologie.yml"), "utf8"));
  const tierA = new Set(RANK.filter(r => r[1] === "A").map(r => idOf(r[0])));
  const DEBUT = 1945, FIN = 2025, x0 = M + 2.3, x1 = W - M - 0.2, y0 = 2.05, hv = 0.86;
  const X = a => x0 + ((a - DEBUT) / (FIN - DEBUT)) * (x1 - x0);
  // étiquettes affichées pour une sélection de jalons ; les autres restent des repères
  const ETIQ = EN
    ? { "lancia-d50": "D50", "cooper-titres": "Cooper", "lotus-25": "Lotus 25", "dfv": "DFV", "ferrari-312t": "312T",
      "lotus-78": "Lotus 78", "turbo-victoire": "Turbo", "mp4-1": "Carbon", "ferrari-640": "Paddles", "tyrrell-019": "Raised nose",
      "double-diffuseur": "Double diffuser", "hybride": "Hybrid" }
    : { "lancia-d50": "D50", "cooper-titres": "Cooper", "lotus-25": "Lotus 25", "dfv": "DFV", "ferrari-312t": "312T",
      "lotus-78": "Lotus 78", "turbo-victoire": "Turbo", "mp4-1": "Carbone", "ferrari-640": "Palettes", "tyrrell-019": "Nez relevé",
      "double-diffuseur": "Double diffuseur", "hybride": "Hybride" };
  for (let a = 1950; a <= 2020; a += 10) {
    s.addShape(pres.shapes.LINE, { x: X(a), y: y0 - 0.15, w: 0, h: hv * 5 + 0.15, line: { color: C.light, width: 0.75, dashType: "dash" } });
    s.addText(String(a), { x: X(a) - 0.4, y: y0 - 0.42, w: 0.8, h: 0.26, fontFace: F, fontSize: 10, bold: true, color: C.sub, align: "center" });
  }
  chrono.voies.forEach((v, i) => {
    const y = y0 + i * hv;
    s.addShape(pres.shapes.LINE, { x: M, y, w: W - 2 * M, h: 0, line: { color: C.rule, width: 0.75 } });
    s.addText(v.nom, { x: M, y, w: 2.2, h: hv, fontFace: F, fontSize: 12, bold: true, color: C.ink, valign: "middle" });
    let precedent = -100, haut = true;
    chrono.jalons.filter(j => j.voie === v.id).sort((a, b) => a.annee - b.annee).forEach(j => {
      haut = j.annee - precedent < 3 ? !haut : true; precedent = j.annee;
      const cx = X(j.annee), cy = y + hv * (haut ? 0.38 : 0.7), d = 0.17;
      const rouge = (j.entrees || []).some(e => tierA.has(e));
      s.addShape(pres.shapes.DIAMOND, { x: cx - d / 2, y: cy - d / 2, w: d, h: d, fill: { color: rouge ? C.A : C.ink }, line: { color: C.white, width: 1 } });
      if (ETIQ[j.id]) s.addText(`${j.annee} ${ETIQ[j.id]}`, { x: cx - 0.8, y: haut ? cy - 0.36 : cy + 0.08, w: 1.6, h: 0.26, fontFace: F, fontSize: 9, color: C.ink, align: "center" });
    });
  });
  s.addShape(pres.shapes.LINE, { x: M, y: y0 + 5 * hv, w: W - 2 * M, h: 0, line: { color: C.rule, width: 0.75 } });
  s.addShape(pres.shapes.DIAMOND, { x: M, y: 6.55, w: 0.15, h: 0.15, fill: { color: C.A }, line: { color: C.A, width: 0 } });
  s.addText(t("porté par un ingénieur du Tier A", "carried by a Tier A engineer"), { x: M + 0.2, y: 6.47, w: 3.2, h: 0.3, fontFace: F, fontSize: 10, color: C.sub });
  s.addText(t("Frise interactive : s-geffroy.github.io/f1-eng/chronologie", "Interactive timeline: s-geffroy.github.io/f1-eng/en/timeline"),
    { x: 6.5, y: 6.47, w: W - M - 6.5, h: 0.3, fontFace: FS, fontSize: 11, italic: true, color: C.sub, align: "right" });
  notes(s, {
    idee: t("Les ruptures se répartissent sur cinq domaines et soixante-dix ans ; le Tier A est présent dans chacun des grands tournants.",
      "The breakthroughs are spread over five fields and seventy years; Tier A is present at each of the major turning points."),
    faits: chrono.jalons.slice().sort((a, b) => a.annee - b.annee).map(j => `${j.annee} — ${j.titre}`),
    nuance: t("Chaque jalon reprend des faits sourcés dans les entrées du site ; la frise interactive donne le détail et les ingénieurs concernés.",
      "Each milestone uses facts sourced in the site's entries; the interactive timeline gives the detail and the engineers involved."),
    sources: [],
  });
}

// ===== 20 — Classement final =====
{
  const s = newSlide(20);
  title(s, t("Le classement final", "The final ranking"), t("Scores sur 100", "Scores out of 100"));
  const colX = [M, M + 6.25], bx = 2.55, bmax = 2.9;
  RANK.forEach(([n, tr, v], i) => {
    const c = Math.floor(i / 10), r = i % 10, x = colX[c], y = 1.85 + r * 0.46;
    s.addText(`${i + 1}. ${n}`, { x, y, w: bx - 0.1, h: 0.4, fontFace: F, fontSize: 13, bold: tr === "A", color: C.ink, valign: "middle" });
    s.addShape(pres.shapes.RECTANGLE, { x: x + bx, y: y + 0.08, w: (bmax * v) / 100, h: 0.26, fill: { color: TIER[tr] }, line: { color: TIER[tr] } });
    s.addText(num(v), { x: x + bx + (bmax * v) / 100 + 0.08, y, w: 0.7, h: 0.4, fontFace: F, fontSize: 12, bold: tr === "A", color: C.ink, valign: "middle" });
  });
  ["A", "B", "C", "D"].forEach((tr, i) => {
    const x = M + i * 1.6;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 6.55, w: 0.25, h: 0.2, fill: { color: TIER[tr] }, line: { color: TIER[tr] } });
    s.addText("Tier " + tr, { x: x + 0.3, y: 6.48, w: 1.2, h: 0.34, fontFace: F, fontSize: 11, color: C.ink });
  });
  s.addText(t("Ne pas surinterpréter les écarts de 1 ou 2 points.", "Do not over-interpret gaps of 1 or 2 points."),
    { x: 7.0, y: 6.48, w: W - M - 7.0, h: 0.34, fontFace: FS, fontSize: 12, italic: true, color: C.sub, align: "right" });
  // scores des notes : « Chapman 96 ; Barnard 95 ; Cooper 93,5 »
  const ligne = tr => `Tier ${tr}${DP}` + RANK.filter(r => r[1] === tr).map(([n, , v]) => `${n.split(" ").pop()} ${Number.isInteger(v) ? v : num(v)}`).join(t(" ; ", "; ")) + ".";
  notes(s, {
    idee: t("Le classement complet, avec les scores, n'arrive qu'à la fin : la méthode et la structure d'abord.",
      "The full ranking, with scores, comes only at the end: method and structure first."),
    faits: ["A", "B", "C", "D"].map(ligne),
    nuance: t("Les barres partent de zéro : les écarts sont visuellement faibles, et c'est voulu. Les scores sont un instrument comparatif, pas une vérité scientifique.",
      "The bars start from zero: the gaps look small, and that is deliberate. The scores are a comparative instrument, not a scientific truth."),
    sources: [],
  });
}

// ===== 21 — Conclusion =====
{
  const s = newSlide(21);
  s.addText(MARQUE, { x: M, y: 0.35, w: 6, h: 0.45, fontFace: F, fontSize: 20, bold: true, color: C.ink });
  s.addShape(pres.shapes.LINE, { x: M, y: 0.85, w: W - 2 * M, h: 0, line: { color: C.ink, width: 2 } });
  s.addText(t("Révolutionner la F1, ce n'est pas seulement construire la voiture la plus rapide : c'est obliger les autres à changer leur manière de construire une F1.",
    "Revolutionising F1 is not just about building the fastest car: it is about forcing others to change the way they build an F1 car."),
    { x: M, y: 1.3, w: 12, h: 2.4, fontFace: F, fontSize: 36, bold: true, color: C.ink, valign: "top" });
  (EN
    ? [["Chapman", "multiple breakthroughs"], ["Barnard", "the clearest authorship"], ["Newey", "the most durable adaptation"]]
    : [["Chapman", "rupture multiple"], ["Barnard", "paternité la plus nette"], ["Newey", "adaptation la plus durable"]]
  ).forEach(([n, txt], i) => {
    const y = 4.0 + i * 0.75;
    s.addText(n, { x: M, y, w: 2.6, h: 0.6, fontFace: F, fontSize: 26, bold: true, color: C.ink, valign: "middle" });
    s.addText(txt, { x: M + 2.6, y, w: 7, h: 0.6, fontFace: FS, fontSize: 22, italic: true, color: C.sub, valign: "middle" });
  });
  notes(s, {
    idee: t("Le classement mesure des capacités historiques à déplacer la frontière technique, pas une échelle unique de « génie ».",
      "The ranking measures historical capacities to shift the technical frontier, not a one-dimensional scale of “genius”."),
    faits: EN
      ? ["Chapman leads through an accumulation of architectural breakthroughs.", "Barnard leads on direct authorship of two innovations that became universal.", "Newey leads in the capacity to stay at the top of aerodynamics across several generations of regulations."]
      : ["Chapman domine par l'accumulation de ruptures architecturales.", "Barnard domine en paternité directe de deux innovations devenues universelles.", "Newey domine la capacité à rester au sommet de l'aérodynamique sous plusieurs générations de règlements."],
    nuance: t("Revenir aux cinq questions du Tier A (slide 6), qui sont la synthèse conceptuelle du classement : où placer le moteur, comment construire la voiture, comment intégrer le moteur, avec quels matériaux et interfaces, comment optimiser le système aérodynamique complet.",
      "Return to the five Tier A questions (slide 6), the conceptual synthesis of the ranking: where to put the engine, how to build the car, how to integrate the engine, with which materials and interfaces, how to optimise the whole aerodynamic system."),
    sources: [],
  });
}

// ===== 22 — Sources =====
{
  const s = newSlide(22);
  title(s, t("Sources principales", "Main sources"), t("Consultées le 9 août 2026", "Consulted on 9 August 2026"));
  const keys = ["innov", "f175", "lotus79", "barnard", "fw15c", "type25", "mp41", "renault", "msT51", "msDernie"];
  s.addText(keys.map(k => ({ text: SRC[k][0], options: { bullet: true, breakLine: true } })), { x: M, y: 1.9, w: 5.6, h: 4.4, fontFace: F, fontSize: 17, color: C.ink, valign: "top", paraSpaceAfter: 4 });
  // Crédits photographiques (licences CC : auteur et licence pour chaque portrait)
  const nomDe = id => RANK.map(r => r[0]).find(n => idOf(n) === id) || id;
  s.addText(t("Crédits photographiques (Wikimedia Commons)", "Photo credits (Wikimedia Commons)"), { x: 6.6, y: 1.9, w: 6.1, h: 0.4, fontFace: F, fontSize: 16, bold: true, color: C.ink });
  // seulement les portraits utilisés dans le deck : ceux des vingt entrées classées
  s.addText(Object.entries(CREDITS).filter(([id]) => RANK.some(r => idOf(r[0]) === id)).sort((a, b) => RANK.findIndex(r => idOf(r[0]) === a[0]) - RANK.findIndex(r => idOf(r[0]) === b[0]))
    .map(([id, c]) => ({ text: `${nomDe(id)}${DP}${c.auteur}, ${c.licence}`, options: { breakLine: true } })),
    { x: 6.6, y: 2.35, w: 6.1, h: 3.3, fontFace: F, fontSize: 12, color: C.ink, valign: "top", paraSpaceAfter: 3 });
  s.addText(t("Modifications : images recadrées et passées en noir et blanc pour cette présentation. Les versions modifiées des images sous licence CC BY-SA ou Art Libre sont diffusées sous la même licence que l'original.",
    "Changes: images cropped and converted to black and white for this presentation. Modified versions of images under a CC BY-SA or Free Art licence are distributed under the same licence as the original."),
    { x: 6.6, y: 5.55, w: 6.1, h: 0.7, fontFace: FS, fontSize: 11, italic: true, color: C.sub, valign: "top" });
  s.addText(t("Bibliographie complète, avec les adresses : notes du présentateur (.pptx) et s-geffroy.github.io/f1-eng", "Full bibliography, with addresses: speaker notes (.pptx) and s-geffroy.github.io/f1-eng/en"),
    { x: M, y: 6.4, w: W - 2 * M, h: 0.4, fontFace: FS, fontSize: 13, italic: true, color: C.sub });
  notes(s, {
    idee: t("Toutes les attributions sensibles reposent sur des sources officielles ou des publications historiques reconnues.",
      "Every sensitive attribution rests on official sources or recognised historical publications."),
    faits: EN
      ? ["Official sources from the manufacturers and Formula 1 take priority.", "No major disputed attribution rests on a single source."]
      : ["Priorité aux sources officielles des constructeurs et de Formula 1.", "Aucune attribution controversée importante ne repose sur une seule source."],
    nuance: t("Images : les portraits du deck sont sous licence libre (Wikimedia Commons), crédités ci-dessous ; toute image ajoutée doit faire l'objet d'une vérification des droits.",
      "Images: the portraits in the deck are freely licensed (Wikimedia Commons) and credited below; any image added must have its rights checked."),
    sources: Object.keys(SRC),
    photos: true,
  });
}

// Le PDF va directement là où le site le sert ; le .pptx reste hors du site (deck/out/).
const NOM = EN ? "revolutionary-engineers-F1" : "ingenieurs-revolutionnaires-F1";
const sortie = MODE === "pdf" ? `${__dirname}/../assets/docs/${NOM}.pdf` : `${__dirname}/out/${NOM}.pptx`;
fs.mkdirSync(path.dirname(sortie), { recursive: true });
(MODE === "pdf" ? pres.renderPdf(sortie, __dirname + "/fonts") : pres.writeFile({ fileName: sortie }))
  .then(f => console.log("OK", f));
