#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -f "$ROOT_DIR/../aistudio/.venv/bin/activate" ]]; then
  # Reuse the AI Studio virtual environment for consistent dependencies.
  source "$ROOT_DIR/../aistudio/.venv/bin/activate"
fi

export PYTHONPATH="$ROOT_DIR/../aistudio:$ROOT_DIR:${PYTHONPATH:-}"
exec uvicorn app.sol_server:app --host 127.0.0.1 --port 8777 --reload --app-dir "$ROOT_DIR"
