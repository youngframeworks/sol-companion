#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SHARED_SYNC_SCRIPT="$ROOT_DIR/../aistudio/sol-os-cloud/scripts/sync_os_to_project.sh"

if [[ ! -f "$SHARED_SYNC_SCRIPT" ]]; then
  echo "[sync] ERROR: shared sync script not found: $SHARED_SYNC_SCRIPT" >&2
  exit 1
fi

bash "$SHARED_SYNC_SCRIPT" --target sol-companion