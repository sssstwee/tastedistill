#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PATTERN='[Ww][Aa][Zz][Aa]|[Jj][Aa][Ss][Oo][Nn]|/Users/|[Ss]{5}[Tt]|[Ee]ver[Mm]odel|api[_-]?key|private key|BEGIN RSA|BEGIN OPENSSH|gho_[A-Za-z0-9_]+|sk-[A-Za-z0-9_-]+'

if rg -n -i "$PATTERN" "$ROOT" \
  --glob '!scripts/scan-public-safety.sh' \
  --glob '!.git/**'
then
  echo "Public safety scan failed: restricted marker found." >&2
  exit 1
fi

echo "Public safety scan passed."
