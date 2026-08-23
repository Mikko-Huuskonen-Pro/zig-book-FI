#!/usr/bin/env bash
# Hae ja yhdistä upstreamin (englanninkielisen) muutokset.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! git remote get-url upstream &>/dev/null; then
  echo "Lisää upstream-remote:"
  echo "  git remote add upstream https://github.com/pedropark99/zig-book.git"
  exit 1
fi

UPSTREAM_BRANCH="${UPSTREAM_BRANCH:-main}"

echo "==> Haetaan upstream ($UPSTREAM_BRANCH)..."
git fetch upstream "$UPSTREAM_BRANCH"

echo "==> Yhdistetään upstream/$UPSTREAM_BRANCH nykyiseen haaraan..."
git merge "upstream/$UPSTREAM_BRANCH" --no-edit

echo ""
echo "==> Upstream synkronoitu. Tarkista käännösten tila:"
echo "    ./scripts/translation-status.sh"
