// Front matter d'une page du site (entrées, voitures...) : objet YAML complet, lu avec js-yaml, comme
// le fait Jekyll (outils/commun.py en Python). null si la page n'en a pas ; une erreur qui nomme le
// fichier s'il n'est pas refermé ou n'est pas du YAML valide.
const fs = require("fs");
const yaml = require("js-yaml");

module.exports = function frontMatter(fichier) {
  const texte = fs.readFileSync(fichier, "utf8");
  if (!texte.startsWith("---\n")) return null;
  const fin = texte.indexOf("\n---\n", 3);
  if (fin < 0) throw new Error(`${fichier} : front matter non refermé`);
  try {
    return yaml.load(texte.slice(4, fin + 1)) || {};
  } catch (e) {
    throw new Error(`${fichier} : front matter invalide (${e.message.split("\n")[0]})`);
  }
};
