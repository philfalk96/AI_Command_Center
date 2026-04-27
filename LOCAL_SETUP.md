# Nagatha AI Control Center — Local Setup Guide

## Prerequisites

Before running the app, install these tools:

- **Node.js** v20 or higher — https://nodejs.org
- **pnpm** v9 or higher — `npm install -g pnpm`
- **PostgreSQL** v14 or higher, or **Docker Desktop** for local containerized PostgreSQL — https://www.postgresql.org/download/ / https://www.docker.com/products/docker-desktop/
- **Ollama** — https://ollama.ai (install and run locally)

## 1. Clone / Extract the Project

Extract the archive and enter the project directory:

```powershell
cd P:\Code\Source_Code\Nagatha_AI_Control_Center
```

## 2. Install Dependencies

```powershell
pnpm install
```

## 3. Set Up the Database

If PostgreSQL is already installed locally, create a PostgreSQL database:

```powershell
createdb nagatha_ai
```

If PostgreSQL is not installed locally but Docker Desktop is available, let the startup script provision a local Postgres container instead:

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action db-up
```

Bootstrap `.env` in the project root:

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action init-env
```

Then set the `DATABASE_URL` environment variable if you need to override the generated local defaults:

```
DATABASE_URL=postgresql://YOUR_USER:YOUR_PASSWORD@localhost:5432/nagatha_ai
PGHOST=localhost
PGPORT=5432
PGUSER=YOUR_USER
PGPASSWORD=YOUR_PASSWORD
PGDATABASE=nagatha_ai
```

Push the database schema:

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action schema
```

## 4. Start Ollama

Make sure Ollama is running with at least one model downloaded:

```powershell
ollama serve            # starts Ollama (may already run as a service)
ollama pull llama3.2    # or any model you prefer
```

## 5. Run the App

Run the local prerequisite check first:

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action check
```

For the one-shot local start path:

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action all
```

That bootstraps `.env`, provisions Docker-backed PostgreSQL when needed, pushes the schema, launches the API and frontend in separate PowerShell windows, and opens the browser.

Then open **two terminal windows**:

**Terminal 1 — API Server:**

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action api
```

**Terminal 2 — Frontend:**

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action frontend
```

Then open http://localhost:3000 in your browser.

## 6. Configure the App

1. Go to **Settings** in the sidebar
2. Set **Ollama URL** to `http://localhost:11434` (the default)
3. Select your default model
4. Customize Nagatha's system prompt if desired

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `PORT` | Yes (API) | Port for the API server |
| `BASE_PATH` | Yes (frontend) | Base path for the Vite dev server |
| `OLLAMA_URL` | No | Ollama server URL (default: http://localhost:11434) |

## Running with VS Code Tasks

The imported project includes these tasks:

- `Initialize Local Environment`
- `Start Local PostgreSQL`
- `Check Local Prereqs`
- `Database Status`
- `Push DB Schema`
- `Start API Server`
- `Start Frontend`
- `Start Nagatha AI (all services)`
- `Start Nagatha AI Control (script)`

They all call `start.ps1`, which loads `.env` before running the matching service.

There is also a VS Code launch target named `Nagatha AI Control (Local)` that runs the script task and opens the app in Edge.

## Production Build

To build for production (serves static files):

```bash
# Build frontend
pnpm --filter @workspace/nagatha-ai run build
# Output goes to: artifacts/nagatha-ai/dist/public

# Build API
pnpm --filter @workspace/api-server run build
# Output goes to: artifacts/api-server/dist
```

Then serve the API with `node artifacts/api-server/dist/index.mjs` and serve the frontend's `dist/public/` folder with any static server (nginx, serve, caddy, etc.).

## IoT / Home Control

To add IoT devices:
1. Go to **IoT Control** in the sidebar
2. Click **Add Device** and fill in:
   - Name, type, room
   - **Endpoint URL**: the HTTP endpoint of your smart home device (e.g., `http://192.168.1.100/api/command`)
3. Commands are sent as `POST { "command": "...", "payload": {} }` to that URL

Compatible with any device that exposes an HTTP endpoint (Home Assistant, ESPHome, custom ESP32/Arduino firmware, etc.).

## Connected Devices / Extensions

Register any WiFi-capable device (phone, tablet, Raspberry Pi, ESP32) under **Connected Devices**. This is a registry for future integration — devices can be pinged or command-dispatched once you implement device-side listeners.

## Voice Features (Nagatha Page)

Voice input and text-to-speech use native browser APIs. For best results:
- Use **Chrome** or **Edge** (best SpeechRecognition support)
- Allow microphone permission when prompted
- Select your preferred voice in **Settings**
