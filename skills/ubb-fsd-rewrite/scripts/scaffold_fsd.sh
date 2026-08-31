#!/usr/bin/env bash
set -euo pipefail
FSD_ID="${1:-}"
SLUG="${2:-}"
OUT="${3:-.}"
if [[ -z "$FSD_ID" || -z "$SLUG" ]]; then
  echo "usage: scaffold_fsd.sh FSD_ID slug [outdir]" >&2
  exit 1
fi
DIR="$OUT/${FSD_ID}_${SLUG}"
TPL="$(cd "$(dirname "$0")/.." && pwd)/assets/folder-template"
mkdir -p "$DIR/raw"
if [[ -d "$TPL" ]]; then
  cp -n "$TPL"/*.txt "$DIR"/ 2>/dev/null || cp "$TPL"/*.txt "$DIR"/
fi
printf 'FSD: %s\nSLUG: %s\nSTATUS: scaffold\nPACKS: FSD_REWRITE\n' "$FSD_ID" "$SLUG" > "$DIR/00_INDEX.txt"
echo "$DIR"
