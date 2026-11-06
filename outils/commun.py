"""Constantes et lecture du front matter, partagées par les scripts de outils/.

Une nouvelle saison relevée ne se reporte qu'ici : DERNIERE_SAISON et GP_RELEVES (verifier.py contrôle
le total de _data/resultats.yml), SAISON_EN_COURS pour les écuries engagées (lignées, généalogie).

Les scripts tournent en python3 -I, qui n'ajoute pas leur dossier au chemin d'import : chacun l'ajoute
lui-même, explicitement, avant « import commun »."""
import yaml

PREMIERE_SAISON = 1950   # premier championnat du monde
DERNIERE_SAISON = 2025   # dernière saison complète relevée dans _data/resultats.yml
SAISON_EN_COURS = 2026   # saison des écuries « actuelles » (dernier segment des lignées actuelles)
GP_RELEVES = 1149        # Grands Prix de PREMIERE_SAISON à DERNIERE_SAISON (Indianapolis 1950-1960 compris)


def front_matter(chemin):
    """(front matter, corps) d'une page Markdown ou HTML. Front matter None si la page n'en a pas ;
    ValueError s'il n'est pas refermé ou n'est pas du YAML valide (le message dit pourquoi)."""
    texte = open(chemin, encoding="utf-8").read()
    if not texte.startswith("---\n"):
        return None, texte
    try:
        _, fm, corps = texte.split("---\n", 2)
    except ValueError:
        raise ValueError("front matter non refermé")
    try:
        return (yaml.safe_load(fm) or {}), corps
    except yaml.YAMLError as e:
        raise ValueError(f"front matter invalide ({str(e).splitlines()[0]})")
