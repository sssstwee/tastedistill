#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PRIVATE_PATTERN='[Jj][Aa][Ss][Oo][Nn]|/Users/|[Ss]{5}[Tt]|[Ee]ver[Mm]odel|api[_-]?key|private key|BEGIN RSA|BEGIN OPENSSH|gho_[A-Za-z0-9_]+|sk-[A-Za-z0-9_-]+'
SKILL_SOURCE_PATTERN='[Ww][Aa][Zz][Aa]'

if rg -n -i "$PRIVATE_PATTERN" "$ROOT" \
  --glob '!scripts/scan-public-safety.sh' \
  --glob '!.git/**'
then
  echo "Public safety scan failed: private marker found." >&2
  exit 1
fi

if rg -n -i "$SKILL_SOURCE_PATTERN" "$ROOT/skills" \
  --glob '!.git/**'
then
  echo "Public safety scan failed: source-brand marker found inside skills/." >&2
  exit 1
fi

echo "Public safety scan passed."
