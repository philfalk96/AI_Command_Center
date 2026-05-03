#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

NAME="${1:-ai-ui-system}"

if [[ ! -x "./venv/bin/python" ]]; then
  python3 -m venv venv
fi

./venv/bin/python -m pip install --upgrade pip
./venv/bin/python -m pip install -r requirements.txt pyinstaller

rm -rf ./build ./dist

./venv/bin/pyinstaller \
  --noconfirm \
  --clean \
  --onedir \
  --name "$NAME" \
  --collect-all chromadb \
  --collect-all sentence_transformers \
  --collect-all transformers \
  --collect-all tokenizers \
  --collect-all torch \
  --hidden-import uvicorn \
  --hidden-import fastapi \
  --hidden-import edge_tts \
  --hidden-import whisper \
  --hidden-import pyttsx3 \
  --add-data "config:config" \
  --add-data "avatar:avatar" \
  --add-data "backgrounds:backgrounds" \
  --add-data "ui/dashboard.html:ui" \
  --add-data "config/config.yaml:config" \
  main.py

mkdir -p "./dist/$NAME/logs" "./dist/$NAME/data/chroma_db"
cp ./startup.sh "./dist/$NAME/startup.sh"
cp ./startup.py "./dist/$NAME/startup.py"
cp ./config/config.yaml "./dist/$NAME/config.yaml"
chmod +x "./dist/$NAME/startup.sh"

echo "Build completed: ./dist/$NAME"
