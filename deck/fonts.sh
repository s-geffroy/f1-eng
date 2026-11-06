#!/bin/sh
# Telecharge les polices du site (licence SIL OFL) dans deck/fonts/, ou pdfkit
# va les chercher pour les embarquer dans le PDF. Non versionnees : voir .gitignore.
# Version figee : un commit precis de google/fonts, et l'empreinte sha256 de chaque
# fichier (une police changee en amont changerait le PDF sans prevenir). Pour passer
# a une version plus recente : changer COMMIT, relancer, verifier le PDF, mettre a
# jour les empreintes ci-dessous.
set -eu
cd "$(dirname "$0")"
COMMIT=24ddc1f324cac5d9f5aedca126d298f56e3f1640   # google/fonts, 5 novembre 2026
mkdir -p fonts
for f in barlowcondensed/BarlowCondensed-Regular barlowcondensed/BarlowCondensed-Bold \
         spectral/Spectral-Regular spectral/Spectral-Italic spectral/Spectral-Bold spectral/Spectral-BoldItalic; do
  curl -sfL -o "fonts/$(basename "$f").ttf" "https://raw.githubusercontent.com/google/fonts/$COMMIT/ofl/$f.ttf"
done
cd fonts
sha256sum -c <<'SHA'
e476562ec9c1e16cf16475895b511f08c804f438cc9a9f80a44ea50a0eeb5b65  BarlowCondensed-Bold.ttf
583cec5da3b84bc4dc7c9c72e2a565c94d34e431518b19d7e250b7830ad5f996  BarlowCondensed-Regular.ttf
70ddb1ec6ae3b0b8d0c79231f670de786978f19baeba2130757526e407aebf9b  Spectral-Bold.ttf
709fa4f2da9be216fd52125db2d6caa4f90150f48de1a453c9ecf91117ab49b6  Spectral-BoldItalic.ttf
7ec97244259db4008c4b1224c7914e5371c797c0044af9d85c2d761ba0e5f787  Spectral-Italic.ttf
c89021dc20720c8d0dcf40b0b2f6e00c13665fa8041717f581396f51b8c78f5d  Spectral-Regular.ttf
SHA
