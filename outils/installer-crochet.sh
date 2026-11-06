#!/bin/sh
# Active les crochets Git versionnés de outils/crochets/ (pre-push : outils/verifier.py, un push est
# refusé si le contrôle échoue). A lancer une fois par clone : core.hooksPath est un réglage local,
# que Git ne transmet pas. Le crochet lui-même est versionné : une modification s'applique aussitôt.
set -eu
cd "$(dirname "$0")/.."
git config core.hooksPath outils/crochets
# Ancienne installation (copie dans .git/hooks/) : sans objet désormais, retirée pour éviter la confusion.
if [ -f .git/hooks/pre-push ] && grep -q "outils/verifier.py" .git/hooks/pre-push; then
    rm .git/hooks/pre-push
fi
echo "Crochets actifs : $(git config core.hooksPath)"
