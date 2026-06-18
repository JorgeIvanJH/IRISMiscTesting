#!/usr/bin/env bash
# Run a script inside the skill's venv. Usage: run.sh <script.py> [args...]
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$SKILL_DIR/.venv"
if [ ! -x "$VENV/bin/python" ]; then
    echo "venv missing; run: bash $SKILL_DIR/scripts/setup.sh" >&2
    exit 1
fi
SCRIPT="$1"; shift
exec "$VENV/bin/python" "$SKILL_DIR/scripts/$SCRIPT" "$@"
