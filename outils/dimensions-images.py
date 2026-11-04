#!/usr/bin/env python3
"""Releve la largeur et la hauteur des portraits et des photos de voitures -> _data/images.yml.

Les gabarits (entree.html, voiture.html) en tirent les attributs width/height de l'image
principale : le navigateur reserve sa place avant le chargement (pas de decalage de mise en page).
A relancer apres tout ajout ou remplacement d'image ; outils/verifier.py signale un oubli.
Sans dependance : lit l'en-tete JPEG (marqueur SOF) ou PNG (IHDR).

    python3 -I outils/dimensions-images.py
"""
import os
import struct
import sys

DOSSIERS = ("assets/portraits", "assets/voitures")
SORTIE = "_data/images.yml"


def dimensions(chemin):
    with open(chemin, "rb") as f:
        tete = f.read(24)
        if tete[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", tete[16:24])
        if tete[:2] != b"\xff\xd8":
            raise ValueError("ni JPEG ni PNG")
        f.seek(2)
        while True:
            octet = f.read(1)
            while octet and octet != b"\xff":
                octet = f.read(1)
            while octet == b"\xff":
                octet = f.read(1)
            if not octet:
                raise ValueError("marqueur SOF introuvable")
            marqueur = octet[0]
            if marqueur in (0xD8, 0xD9) or 0xD0 <= marqueur <= 0xD7:
                continue
            (longueur,) = struct.unpack(">H", f.read(2))
            # SOF0 a SOF15, sauf DHT (C4), JPG (C8) et DAC (CC)
            if 0xC0 <= marqueur <= 0xCF and marqueur not in (0xC4, 0xC8, 0xCC):
                h, l = struct.unpack(">xHH", f.read(5))
                return l, h
            f.seek(longueur - 2, 1)


def main():
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    lignes = ["# Genere par outils/dimensions-images.py : ne pas editer a la main.",
              "# Cle : chemin publie de l'image ; l = largeur, h = hauteur, en pixels."]
    for dossier in DOSSIERS:
        for nom in sorted(os.listdir(dossier)):
            if not nom.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            try:
                l, h = dimensions(os.path.join(dossier, nom))
            except ValueError as e:
                sys.exit(f"{dossier}/{nom} : {e}")
            lignes.append(f'"/{dossier}/{nom}": {{l: {l}, h: {h}}}')
    with open(SORTIE + ".tmp", "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    os.replace(SORTIE + ".tmp", SORTIE)
    print(f"{SORTIE} : {len(lignes) - 2} images")


if __name__ == "__main__":
    main()
