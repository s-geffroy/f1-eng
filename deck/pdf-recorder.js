// Enregistre les appels pptxgenjs utilisés par build.js (addSlide, addText, addShape,
// addTable, addNotes) et les rejoue dans un PDF avec pdfkit. Une seule description du
// deck produit donc le .pptx et le .pdf, avec la même géométrie.
const fs = require("fs");
const PDFDocument = require("pdfkit");

const PT = 72; // points par pouce
const SHAPES = { RECTANGLE: "rect", ROUNDED_RECTANGLE: "roundRect", OVAL: "ellipse", LINE: "line" };

function create() {
  const slides = [];
  const pres = {
    layout: "LAYOUT_WIDE",
    title: "",
    shapes: SHAPES,
    addSlide() {
      const ops = [];
      const slide = {
        background: null,
        addText: (text, o) => ops.push({ k: "text", text, o }),
        addShape: (type, o) => ops.push({ k: "shape", type, o }),
        addTable: (rows, o) => ops.push({ k: "table", rows, o }),
        addNotes: () => {},
      };
      slides.push({ slide, ops });
      return slide;
    },
    renderPdf(file, fontDir) {
      const doc = new PDFDocument({ size: [13.333 * PT, 7.5 * PT], margin: 0, autoFirstPage: false,
        // date fixe : sans elle, chaque génération produit un PDF différent (date et identifiant),
        // et Git voit un fichier modifié alors que rien n'a changé
        info: { Title: pres.title, CreationDate: new Date("2026-10-25T00:00:00Z") } });
      const reg = (name, f) => doc.registerFont(name, `${fontDir}/${f}.ttf`);
      reg("Barlow Condensed", "BarlowCondensed-Regular");
      reg("Barlow Condensed|b", "BarlowCondensed-Bold");
      reg("Barlow Condensed|i", "BarlowCondensed-Regular");
      reg("Barlow Condensed|bi", "BarlowCondensed-Bold");
      reg("Spectral", "Spectral-Regular");
      reg("Spectral|b", "Spectral-Bold");
      reg("Spectral|i", "Spectral-Italic");
      reg("Spectral|bi", "Spectral-BoldItalic");
      const out = fs.createWriteStream(file);
      doc.pipe(out);
      for (const { slide, ops } of slides) {
        doc.addPage();
        if (slide.background && slide.background.color) doc.rect(0, 0, doc.page.width, doc.page.height).fill("#" + slide.background.color);
        for (const op of ops) {
          if (op.k === "shape") drawShape(doc, op.type, op.o);
          else if (op.k === "text") drawText(doc, op.text, op.o);
          else if (op.k === "table") drawTable(doc, op.rows, op.o);
        }
      }
      doc.end();
      return new Promise((res, rej) => { out.on("finish", () => res(file)); out.on("error", rej); });
    },
  };
  return pres;
}

function fontName(o) {
  const face = o.fontFace || "Barlow Condensed";
  const st = (o.bold ? "b" : "") + (o.italic ? "i" : "");
  return st ? `${face}|${st}` : face;
}

function strokeFill(doc, o) {
  const fill = o.fill && o.fill.type !== "none" && o.fill.color ? "#" + o.fill.color : null;
  const ln = o.line || {};
  const stroke = ln.color && ln.width !== 0 ? "#" + ln.color : null;
  if (stroke) {
    doc.lineWidth(ln.width || 0.75);
    if (ln.dashType === "dash") doc.dash(4 * (ln.width || 1), { space: 3 * (ln.width || 1) }); else doc.undash();
  }
  if (fill && stroke) doc.fillAndStroke(fill, stroke);
  else if (fill) doc.fill(fill);
  else if (stroke) doc.stroke(stroke);
  doc.undash();
}

function drawShape(doc, type, o) {
  const x = o.x * PT, y = o.y * PT, w = (o.w || 0) * PT, h = (o.h || 0) * PT;
  doc.save();
  if (type === "line") {
    const ln = o.line || {};
    const x2 = x + w, y2 = y + h;
    doc.moveTo(x, y).lineTo(x2, y2);
    strokeFill(doc, { line: ln });
    if (ln.endArrowType) {
      const a = Math.atan2(y2 - y, x2 - x), s = 3.2 * (ln.width || 1) + 3;
      doc.moveTo(x2, y2)
        .lineTo(x2 - s * Math.cos(a - 0.45), y2 - s * Math.sin(a - 0.45))
        .lineTo(x2 - s * Math.cos(a + 0.45), y2 - s * Math.sin(a + 0.45))
        .closePath().fill("#" + (ln.color || "000000"));
    }
  } else {
    if (type === "roundRect") doc.roundedRect(x, y, w, h, Math.min((o.rectRadius || 0.1) * PT, h / 2, w / 2));
    else if (type === "ellipse") doc.ellipse(x + w / 2, y + h / 2, w / 2, h / 2);
    else doc.rect(x, y, w, h);
    strokeFill(doc, o);
  }
  doc.restore();
}

// Découpe le texte pptxgenjs (chaîne ou suite de « runs ») en paragraphes.
function paragraphs(text, base) {
  const runs = typeof text === "string" ? [{ text, options: {} }] : text;
  const paras = [[]];
  for (const r of runs) {
    const o = { ...base, ...(r.options || {}) };
    const parts = String(r.text).split("\n");
    parts.forEach((p, i) => {
      if (i > 0) paras.push([]);
      paras[paras.length - 1].push({ text: p, o });
    });
    if (r.options && r.options.breakLine) paras.push([]);
  }
  return paras.filter(p => p.length && p.some(r => r.text !== ""));
}

function layoutParas(doc, paras, width, o) {
  const gap = (o.paraSpaceAfter || 0);
  return paras.map(p => {
    const first = p[0].o;
    const bullet = !!first.bullet;
    const w = width - (bullet ? 18 : 0);
    doc.font(fontName(first)).fontSize(first.fontSize || 18);
    const h = doc.heightOfString(p.map(r => r.text).join(""), { width: w, align: first.align || "left" });
    return { p, h, bullet, w, gap };
  });
}

function drawText(doc, text, o, inset = { l: 0.1, r: 0.1, t: 0.05, b: 0.05 }) {
  const x = (o.x + inset.l) * PT, w = (o.w - inset.l - inset.r) * PT;
  const top = (o.y + inset.t) * PT, boxH = (o.h - inset.t - inset.b) * PT;
  const paras = layoutParas(doc, paragraphs(text, o), w, o);
  const total = paras.reduce((a, q, i) => a + q.h + (i < paras.length - 1 ? q.gap : 0), 0);
  let y = top;
  if (o.valign === "middle") y = top + (boxH - total) / 2;
  else if (o.valign === "bottom") y = top + boxH - total;
  for (const q of paras) {
    const first = q.p[0].o;
    const tx = x + (q.bullet ? 18 : 0);
    if (q.bullet) {
      doc.font(fontName(first)).fontSize(first.fontSize || 18).fillColor("#" + (first.color || "000000"));
      doc.text("•", x + 4, y, { lineBreak: false });
    }
    q.p.forEach((r, i) => {
      const ro = r.o;
      doc.font(fontName(ro)).fontSize(ro.fontSize || 18).fillColor("#" + (ro.color || "000000"));
      const opts = { width: q.w, align: first.align || "left", continued: i < q.p.length - 1, characterSpacing: ro.charSpacing || 0 };
      if (i === 0) doc.text(r.text, tx, y, opts); else doc.text(r.text, opts);
    });
    y += q.h + q.gap;
  }
}

function drawTable(doc, rows, o) {
  const colW = o.colW || rows[0].map(() => o.w / rows[0].length);
  const cellInset = { l: 0.1, r: 0.1, t: 0.05, b: 0.05 };
  const border = o.border || { color: "000000", pt: 1 };
  let y = o.y;
  for (const row of rows) {
    // hauteur : celle demandée, ou plus si le texte l'exige (comme PowerPoint)
    let rh = o.rowH || 0.4;
    row.forEach((c, j) => {
      const cell = typeof c === "string" ? { text: c } : c;
      const co = { ...o, ...(cell.options || {}) };
      const paras = layoutParas(doc, paragraphs(cell.text, co), (colW[j] - cellInset.l - cellInset.r) * PT, co);
      const need = paras.reduce((a, q) => a + q.h, 0) / PT + cellInset.t + cellInset.b;
      rh = Math.max(rh, need);
    });
    let x = o.x;
    row.forEach((c, j) => {
      const cell = typeof c === "string" ? { text: c } : c;
      const co = { ...o, ...(cell.options || {}) };
      drawShape(doc, "rect", { x, y, w: colW[j], h: rh, fill: co.fill, line: { color: border.color, width: border.pt } });
      drawText(doc, cell.text, { ...co, x, y, w: colW[j], h: rh, valign: co.valign || "middle" }, cellInset);
      x += colW[j];
    });
    y += rh;
  }
}

module.exports = { create };
