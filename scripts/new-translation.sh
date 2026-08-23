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

# Kopioi pohja, säilytä yksi YAML-frontmatter ja lisää translation-kentät.
{
  tail -n +2 "$EN" | sed \
    -e 's|source("\./zig_engine.R")|source("../zig_engine.R")|g' \
    -e 's|source("\.\./zig_engine.R")|source("../../zig_engine.R")|g' \
    -e 's|syntax-definition: "\./Assets/|syntax-definition: "../Assets/|g' \
    -e 's|syntax-definition: "\.\./Assets/|syntax-definition: "../../Assets/|g' \
    -e 's|include \./Assets/|include ./Assets/|g' \
    -e 's|include \.\./Assets/|include ./Assets/|g'
} > "$FI.tmp"

# Lisää translation YAML-osion olemassa olevaan frontmatteriin.
python3 - "$FI.tmp" "$REL" "$EN_HASH" "$FI" <<'PY'
import sys, re, pathlib

tmp, rel, en_hash, out = sys.argv[1:5]
text = pathlib.Path(tmp).read_text(encoding='utf-8')
m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
if not m:
    raise SystemExit('Ei YAML-frontmatteria lähdetiedostossa')
header, body = m.group(1), text[m.end():]
extra = (
    f"translation:\n"
    f"  source: {rel}\n"
    f"  source_sha256: {en_hash}\n"
    f"  status: draft\n"
)
pathlib.Path(out).write_text(f"---\n{header}\n{extra}---\n{body}", encoding='utf-8', newline='\n')
pathlib.Path(tmp).unlink()
PY

echo "Luotu: $FI"
echo "Päivitä käännös ja aseta status: complete kun valmis."
