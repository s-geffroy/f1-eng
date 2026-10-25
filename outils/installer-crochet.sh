#!/bin/sh
# Installe un crochet Git local « pre-push » qui lance outils/verifier.py :
# un push est refusé si le contrôle échoue. A lancer une fois par clone.
set -eu
cd "$(dirname "$0")/.."
cat > .git/hooks/pre-push <<'HOOK'
#!/bin/sh
python3 outils/verifier.py || { echo "Push annulé : corriger les erreurs ci-dessus."; exit 1; }
HOOK
chmod +x .git/hooks/pre-push
echo "Crochet pre-push installé."
