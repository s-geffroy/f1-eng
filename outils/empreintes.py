#!/usr/bin/env python3
"""Empreinte du contenu des ressources versionnées dans leur URL -> _data/empreintes.yml.

_layouts/default.html sert la feuille de style sous « encyclopedie.css?v=<empreinte> » : le navigateur
la garde en cache tant qu'elle ne change pas, et la recharge dès qu'elle change (la date de construction,
utilisée avant, changeait à chaque push). A relancer après toute modification de la CSS ;
outils/verifier.py signale une empreinte périmée, et le crochet pre-push refuse alors le push.

    python3 -I outils/empreintes.py
"""
import hashlib
import os

RESSOURCES = {"css": "assets/css/encyclopedie.css"}   # clé de _data/empreintes.yml -> fichier
SORTIE = "_data/empreintes.yml"


def empreinte(chemin):
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:10]


def contenu():
    return ("# Généré par outils/empreintes.py : ne pas éditer à la main.\n"
            "# Empreinte (sha256, 10 premiers caractères) de chaque ressource, ajoutée à son URL.\n"
            + "".join(f"{k}: \"{empreinte(f)}\"\n" for k, f in RESSOURCES.items()))


def main():
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    with open(SORTIE + ".tmp", "w", encoding="utf-8") as f:
        f.write(contenu())
    os.replace(SORTIE + ".tmp", SORTIE)
    print(open(SORTIE, encoding="utf-8").read().splitlines()[-1])


if __name__ == "__main__":
    main()
