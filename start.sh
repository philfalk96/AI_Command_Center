#!/bin/bash
# Nagatha AI Control Center — Local Startup Script
# Edit DATABASE_URL below before running.

set -e

# ─── Configuration ───────────────────────────────────────────────────────────
DB_URL="${DATABASE_URL:-postgresql://postgres:password@localhost:5432/nagatha_ai}"
API_PORT="${API_PORT:-8080}"
FRONT_PORT="${FRONT_PORT:-3000}"
OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"
# ─────────────────────────────────────────────────────────────────────────────

export DATABASE_URL="$DB_URL"
export OLLAMA_URL="$OLLAMA_URL"

echo ""
echo "  ███╗   ██╗ █████╗  ██████╗  █████╗ ████████╗██╗  ██╗ █████╗ "
echo "  ████╗  ██║██╔══██╗██╔════╝ ██╔══██╗╚══██╔══╝██║  ██║██╔══██╗"
echo "  ██╔██╗ ██║███████║██║  ███╗███████║   ██║   ███████║███████║"
echo "  ██║╚██╗██║██╔══██║██║   ██║██╔══██║   ██║   ██╔══██║██╔══██║"
echo "  ██║ ╚████║██║  ██║╚██████╔╝██║  ██║   ██║   ██║  ██║██║  ██║"
echo "  ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝"
echo ""
echo "  AI Control Center"
echo ""

# Check Ollama
echo "[ ] Checking Ollama..."
if curl -s "$OLLAMA_URL/api/tags" > /dev/null 2>&1; then
  echo "[+] Ollama reachable at $OLLAMA_URL"
else
  echo "[!] Ollama not reachable at $OLLAMA_URL"
  echo "    Start Ollama with: ollama serve"
  echo "    Continuing anyway — configure URL in Settings."
fi

# Push DB schema
echo "[ ] Pushing database schema..."
pnpm --filter @workspace/db run push 2>/dev/null && echo "[+] Database schema ready" || echo "[!] DB push failed — check DATABASE_URL"

# Kill any existing processes on our ports
kill_port() {
  lsof -ti tcp:"$1" | xargs kill -9 2>/dev/null || true
}
kill_port "$API_PORT"
kill_port "$FRONT_PORT"

# Start API server
echo ""
echo "[ ] Starting API server on port $API_PORT..."
PORT="$API_PORT" BASE_PATH="/" pnpm --filter @workspace/api-server run dev &
API_PID=$!

sleep 2

# Start frontend
echo "[ ] Starting frontend on port $FRONT_PORT..."
PORT="$FRONT_PORT" BASE_PATH="/" pnpm --filter @workspace/nagatha-ai run dev &
FRONT_PID=$!

echo ""
echo "  ─────────────────────────────────────────────"
echo "  App:  http://localhost:$FRONT_PORT"
echo "  API:  http://localhost:$API_PORT/api/healthz"
echo "  ─────────────────────────────────────────────"
echo "  Press Ctrl+C to stop all services"
echo ""

cleanup() {
  echo ""
  echo "Stopping services..."
  kill $API_PID $FRONT_PID 2>/dev/null || true
  exit 0
}
trap cleanup INT TERM

wait
