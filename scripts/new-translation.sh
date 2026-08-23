#!/usr/bin/env bash
# Luo uusi suomennosluku englanninkielisen pohjalta.
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Käyttö: $0 <Chapters/tiedosto.qmd|index.qmd>"
  exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REL="$1"
EN="$ROOT/$REL"
FI="$ROOT/fi/$REL"

if [[ ! -f "$EN" ]]; then
  echo "Lähdetiedostoa ei löydy: $EN"
  exit 1
fi

if [[ -f "$FI" ]]; then
  echo "Suomennos on jo olemassa: $FI"
  exit 1
fi

mkdir -p "$(dirname "$FI")"
EN_HASH="$(sha256sum "$EN" | awk '{print $1}')"

# Kopioi pohja ja lisää käännösmetatiedot YAML-osion alkuun.
{
  echo "---"
  echo "translation:"
  echo "  source: $REL"
  echo "  source_sha256: $EN_HASH"
  echo "  status: draft"
  echo "---"
  echo ""
  tail -n +2 "$EN" | sed \
    -e 's|source("\./zig_engine.R")|source("../zig_engine.R")|g' \
    -e 's|source("\.\./zig_engine.R")|source("../../zig_engine.R")|g' \
    -e 's|syntax-definition: "\./Assets/|syntax-definition: "../Assets/|g' \
    -e 's|syntax-definition: "\.\./Assets/|syntax-definition: "../../Assets/|g' \
    -e 's|include \./Assets/|include ../Assets/|g' \
    -e 's|include \.\./Assets/|include ../../Assets/|g'
} > "$FI"

echo "Luotu: $FI"
echo "Päivitä käännös ja aseta status: complete kun valmis."
