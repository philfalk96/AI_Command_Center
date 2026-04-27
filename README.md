# Nagatha AI Control Center

A local AI interface that pairs with [Ollama](https://ollama.ai) for running AI models entirely on your machine. Includes smart home / IoT control, the Nagatha AI persona with voice interaction, training data management, and a connected devices registry.

---

## Requirements

Install these before anything else:

| Tool | Version | Link |
|------|---------|------|
| Node.js | 20 or higher | https://nodejs.org |
| pnpm | 9 or higher | `npm install -g pnpm` |
| PostgreSQL or Docker Desktop | local runtime | https://postgresql.org/download / https://www.docker.com/products/docker-desktop |
| Ollama | latest | https://ollama.ai |

---

## Setup in VS Code

### Windows quick start

This import is already loaded at `P:\Code\Source_Code\Nagatha_AI_Control_Center`.

1. Start Docker Desktop if you want the script to provision PostgreSQL locally.
2. Run `powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action all`
3. Or run the VS Code task `Start Nagatha AI Control (script)`
4. Or press `F5` and choose `Nagatha AI Control (Local)`

That startup path bootstraps `.env`, provisions a local PostgreSQL container when native PostgreSQL is not installed, pushes the Drizzle schema, then launches the API server, frontend, and browser.

### 1. Open the project

Extract the archive, then open the folder in VS Code:

```
File → Open Folder → select the extracted nagatha-ai folder
```

Or from the terminal:

```powershell
code P:\Code\Source_Code\Nagatha_AI_Control_Center
```

---

### 2. Install dependencies

Open the VS Code integrated terminal (`Ctrl+`` ` or **Terminal → New Terminal**) and run:

```bash
pnpm install
```

---

### 3. Configure environment variables

Bootstrap the local `.env` file:

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action init-env
```

Open `.env` and edit it:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/nagatha_ai
PGHOST=localhost
PGPORT=5432
PGUSER=postgres
PGPASSWORD=yourpassword
PGDATABASE=nagatha_ai
SESSION_SECRET=any-random-string-here
NAGATHA_PG_CONTAINER=nagatha-postgres
NAGATHA_PG_VOLUME=nagatha-postgres-data
```

> **Tip:** If PostgreSQL is not installed locally but Docker Desktop is available, `start.ps1 -Action db-up` will start a local `postgres:16` container and persist its data in a Docker volume.

---

### 4. Push the database schema

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action db-up
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action schema
```

You should see: `[✓] Changes applied`

---

### 5. Start Ollama

In a separate terminal (or it may already be running as a system service):

```powershell
ollama serve
```

Pull a model if you haven't already:

```powershell
ollama pull llama3.2
# or any model: mistral, gemma3, phi4, etc.
```

---

### 6. Run the app

The easiest way on Windows is the included PowerShell entrypoint:

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action all
```

That bootstraps `.env`, starts PostgreSQL when available, pushes the schema, opens separate PowerShell windows for the API and frontend, and opens the browser.

If you want to run the pieces manually, use separate terminals:

**Terminal 1 — API server:**
```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action api
```

**Terminal 2 — Frontend:**
```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action frontend
```

Then open **http://localhost:3000** in your browser.

---

## VS Code Tasks and Launch (optional)

The imported project includes a `.vscode/tasks.json` file and a `.vscode/launch.json` profile for **Terminal → Run Task** or `F5` startup.

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Initialize Local Environment",
      "type": "shell",
      "command": "powershell -ExecutionPolicy Bypass -File .\\start.ps1 -Action init-env"
    },
    {
      "label": "Start Local PostgreSQL",
      "type": "shell",
      "command": "powershell -ExecutionPolicy Bypass -File .\\start.ps1 -Action db-up"
    },
    {
      "label": "Start API Server",
      "type": "shell",
      "command": "powershell -ExecutionPolicy Bypass -File .\\start.ps1 -Action api",
      "group": "build",
      "presentation": { "panel": "dedicated" }
    },
    {
      "label": "Start Frontend",
      "type": "shell",
      "command": "powershell -ExecutionPolicy Bypass -File .\\start.ps1 -Action frontend",
      "group": "build",
      "presentation": { "panel": "dedicated" }
    },
    {
      "label": "Start Nagatha AI Control (script)",
      "type": "shell",
      "command": "powershell -ExecutionPolicy Bypass -File .\\start.ps1 -Action all"
    }
  ]
}
```

The launch target `Nagatha AI Control (Local)` uses that script task as its pre-launch step and opens the app in Edge.

---

## App Pages

| Page | URL | What it does |
|------|-----|--------------|
| Dashboard | http://localhost:3000/ | System overview — Ollama status, session stats, device counts |
| AI Chat | http://localhost:3000/chat | Chat with any locally downloaded Ollama model |
| Nagatha Agent | http://localhost:3000/nagatha | AI persona with animated orb, voice input, text-to-speech, HITL review |
| IoT Control | http://localhost:3000/iot | Register and command smart home / IoT devices via HTTP |
| Training Data | http://localhost:3000/training | Submit prompt/response pairs to improve your AI |
| Connected Devices | http://localhost:3000/devices | Register WiFi/mobile devices for future integration |
| Settings | http://localhost:3000/settings | Ollama URL, model selection, Nagatha system prompt, voice config |

---

## Configuring Ollama

The Settings page (http://localhost:3000/settings) lets you set:

- **Ollama URL** — defaults to `http://localhost:11434`. Change this if Ollama runs on a different machine on your network.
- **Default model** — picked from your locally downloaded models.
- **Nagatha system prompt** — the personality/instructions for the Nagatha persona.

Settings are saved in your browser's local storage.

---

## IoT / Home Control

Devices are registered with an HTTP endpoint URL. When you send a command from the IoT page, the app POSTs:

```json
{ "command": "toggle", "payload": {} }
```

to that device's URL. Works with:

- **Home Assistant** webhooks
- **ESPHome** HTTP API
- **Custom ESP32 / Arduino** firmware with an HTTP server
- Any device that accepts HTTP POST requests

---

## Voice Features (Nagatha Page)

- **Voice input** uses the browser's built-in Speech Recognition API — works best in Chrome or Edge
- **Text-to-speech** uses the browser's built-in Speech Synthesis API
- Configure voice, speed, and pitch in **Settings**
- Allow microphone permission when the browser prompts

---

## Project Structure

```
nagatha-ai/
├── artifacts/
│   ├── nagatha-ai/          # React + Vite frontend
│   │   └── src/
│   │       ├── pages/       # Dashboard, Chat, Nagatha, IoT, Training, Devices, Settings
│   │       └── components/  # UI components
│   └── api-server/          # Express API server
│       └── src/
│           └── routes/      # ollama, chat, training, iot, devices
├── lib/
│   ├── db/src/schema/       # PostgreSQL schema (Drizzle ORM)
│   ├── api-spec/            # OpenAPI specification
│   └── api-client-react/    # Auto-generated React Query hooks
├── .env.example             # Copy to .env and configure
├── start.sh                 # One-command startup script
└── LOCAL_SETUP.md           # Full setup reference
```

---

## Troubleshooting

**"Ollama Disconnected" on dashboard**
→ Make sure `ollama serve` is running and the URL in Settings matches.

**Database connection error**
→ Check your `.env` values and that PostgreSQL is running: `pg_isready`

**Port already in use**
→ Change `API_PORT` and `FRONT_PORT` in `.env`, or stop the existing process on Windows:
```powershell
Get-NetTCPConnection -LocalPort 8080 | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ }
Get-NetTCPConnection -LocalPort 3000 | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ }
```

**Voice input not working**
→ Use Chrome or Edge. Safari has limited Speech Recognition support. Make sure you're on `http://localhost` (not a remote URL) or HTTPS.

**pnpm not found**
→ Install it: `npm install -g pnpm`
