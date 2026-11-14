#!/bin/sh
# Rebuild the site from _build/ and refresh the published files at the repo root.
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$(mktemp -d)/site"
python3 "$REPO/_build/build.py" "$OUT"
cd "$REPO"
find . -mindepth 1 -maxdepth 1 ! -name .git ! -name _build ! -name README.md -exec rm -rf {} +
cp -r "$OUT"/. "$REPO"/
echo "Site rebuilt into $REPO"
