#!/usr/bin/env bash
# Raportoi mitkä suomennokset ovat puutteellisia tai vanhentuneita.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EN_DIR="$ROOT/Chapters"
FI_DIR="$ROOT/fi/Chapters"

missing=0
outdated=0
draft=0
ok=0

printf "%-40s %-12s %s\n" "LUKU" "TILA" "HUOM"
printf "%-40s %-12s %s\n" "----" "----" "----"

check_file() {
  local rel="$1"
  local en="$ROOT/$rel"
  local fi_file="$ROOT/fi/$rel"
  local base
  base="$(basename "$rel")"

  if [[ ! -f "$en" ]]; then
    return
  fi

  if [[ ! -f "$fi_file" ]]; then
    printf "%-40s %-12s %s\n" "$rel" "PUUTTUU" "Ei suomennosta"
    missing=$((missing + 1))
    return
  fi

  local en_hash
  en_hash="$(sha256sum "$en" | awk '{print $1}')"
  local recorded_hash
  recorded_hash="$(grep -E '^  source_sha256:' "$fi_file" 2>/dev/null | head -1 | sed 's/.*: *"\?\([^"]*\)"\?.*/\1/' || true)"
  local status
  status="$(grep -E '^  status:' "$fi_file" 2>/dev/null | head -1 | sed 's/.*: *//' || echo "unknown")"

  if [[ -z "$recorded_hash" || "$recorded_hash" == '""' || "$recorded_hash" == "''" ]]; then
    printf "%-40s %-12s %s\n" "fi/$rel" "LUONNOS" "source_sha256 puuttuu"
    draft=$((draft + 1))
  elif [[ "$en_hash" != "$recorded_hash" ]]; then
    printf "%-40s %-12s %s\n" "fi/$rel" "VANHENTUNUT" "EN muuttunut"
    outdated=$((outdated + 1))
  elif [[ "$status" != "complete" ]]; then
    printf "%-40s %-12s %s\n" "fi/$rel" "$status" "Sisältö synkassa, status != complete"
    draft=$((draft + 1))
  else
    printf "%-40s %-12s %s\n" "fi/$rel" "VALMIS" ""
    ok=$((ok + 1))
  fi
}

check_file "index.qmd"

for en in "$EN_DIR"/*.qmd; do
  [[ -f "$en" ]] || continue
  rel="Chapters/$(basename "$en")"
  check_file "$rel"
done

echo ""
echo "Yhteenveto: valmis=$ok luonnos=$draft vanhentunut=$outdated puuttuu=$missing"

if [[ $missing -gt 0 || $outdated -gt 0 ]]; then
  exit 1
fi
