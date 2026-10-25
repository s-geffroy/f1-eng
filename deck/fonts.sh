#!/bin/sh
# Telecharge les polices du site (licence SIL OFL) dans deck/fonts/, ou pdfkit
# va les chercher pour les embarquer dans le PDF. Non versionnees : voir .gitignore.
set -eu
cd "$(dirname "$0")"
mkdir -p fonts
for f in barlowcondensed/BarlowCondensed-Regular barlowcondensed/BarlowCondensed-Bold \
         spectral/Spectral-Regular spectral/Spectral-Italic spectral/Spectral-Bold spectral/Spectral-BoldItalic; do
  curl -sfL -o "fonts/$(basename "$f").ttf" "https://raw.githubusercontent.com/google/fonts/main/ofl/$f.ttf"
done
ls fonts
