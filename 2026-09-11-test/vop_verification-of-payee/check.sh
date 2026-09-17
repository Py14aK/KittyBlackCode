#!/usr/bin/env bash
# VoP folder check. Green, or do not commit.
set -u
cd "$(dirname "$0")"
PY=$(command -v python3 || command -v python) || { echo "python not found on PATH"; exit 1; }

have() { "$PY" -m "$1" --version >/dev/null 2>&1; }
if ! have ruff || ! have pytest; then
  echo "installing pytest and ruff..."
  "$PY" -m pip install --quiet --disable-pip-version-check pytest ruff 2>/dev/null \
    || "$PY" -m pip install --quiet --disable-pip-version-check --break-system-packages pytest ruff 2>/dev/null \
    || true
fi
have ruff   || { echo "ruff missing. Try: $PY -m pip install --user ruff";   exit 1; }
have pytest || { echo "pytest missing. Try: $PY -m pip install --user pytest"; exit 1; }

echo "--- ruff ---"
"$PY" -m ruff check . || { echo; echo "LINT FAILED. Read the message; it is usually right."; exit 1; }
echo "--- pytest ---"
"$PY" -m pytest -q || { echo; echo "TESTS FAILED. Do not commit."; exit 1; }
echo
echo "Expected: All checks passed, and 16 passed / 5 skipped."
echo "If the skip count dropped, check that a decision in docs/DECISIONS.md was actually answered."
