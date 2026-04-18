#!/usr/bin/env bash
# .devcontainer/setup.sh
# Post-create setup for Sol Companion Codespaces environment.
set -euo pipefail

echo "[setup] Installing Python dependencies..."
pip install --quiet -r requirements.txt 2>/dev/null || true

echo "[setup] Installing GitHub Copilot CLI..."
npm install -g @githubnext/github-copilot-cli 2>/dev/null || true

echo "[setup] Done. Use @SolManagerAgent or sol commands in the terminal."
