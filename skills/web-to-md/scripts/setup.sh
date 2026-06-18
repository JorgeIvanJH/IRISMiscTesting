#!/usr/bin/env bash
# Create a local venv for the web-to-md skill and install trafilatura.
# Idempotent: safe to re-run.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$SKILL_DIR/.venv"

if [ ! -d "$VENV" ]; then
    echo "Creating venv at $VENV..."
    python3 -m venv "$VENV"
fi

# shellcheck disable=SC1091
source "$VENV/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet trafilatura

echo "OK: trafilatura $(python -c 'import trafilatura; print(trafilatura.__version__)') installed in $VENV"
