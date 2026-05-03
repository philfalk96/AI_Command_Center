#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

CONFIG="${1:-config/phase4_config.yaml}"
DEPLOY_CONFIG="${2:-config/config.yaml}"
MODE="${3:-dashboard}"

if [[ ! -x "./venv/bin/python" ]]; then
  python3 -m venv venv
fi

./venv/bin/python -m pip install -r requirements.txt
./venv/bin/python ./startup.py --config "$CONFIG" --deploy-config "$DEPLOY_CONFIG" --mode "$MODE"
