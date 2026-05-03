# Embodied AI System - Complete Documentation

```
╔════════════════════════════════════════════════════════════════════╗
║    EMBODIED AI OPERATING SYSTEM - PHASE 9 / CORE STACK           ║
║  Local LLM + Voice + Desktop App + Science Lab + Managed Models  ║
╚════════════════════════════════════════════════════════════════════╝
```

---

## 📖 Table of Contents

- [System Overview](#system-overview)
- [Current Features (Phase 4-5)](#current-features-phase-4-5)
- [Quick Start](#quick-start)
- [Operating Modes](#operating-modes)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Components](#components)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Documentation](#documentation)

---

## System Overview

**Embodied AI System** is a modular, local-first AI platform that combines:
- 🧠 **Local LLM** (Ollama - fully offline capable)
- 🎤 **Voice I/O** (Whisper STT + multi-backend TTS)
- 🎨 **Web Dashboard** (FastAPI + real-time UI)
- 🏠 **IoT Control** (Home Assistant + local network discovery)
- 💾 **Memory/RAG** (ChromaDB vector embeddings)
- 🔒 **Security** (Sandboxing + approval workflows)
- 🛠️ **Tool System** (File I/O, code execution, network ops)

**Deployment:** Private network, single-machine, fully offline after initial setup.

**Status:** Production-ready through Phase 9 (Core Stack baseline). All major layers operational.

---

## Current Features (Phase 9 — Core Stack)

### ✅ Phase 1-2: Core Intelligence & Tooling
- CLI REPL with multi-turn conversation
- RAG memory with semantic search (`ChromaDB`)
- Tool execution with permission checking
- File I/O and code execution
- Structured logging with audit trail
- Multi-step task planning

### ✅ Phase 3: Voice Interaction
- Real-time speech-to-text (Whisper)
- Multiple TTS backends (`edge-tts`, `coqui`, `pyttsx3`)
- Push-to-talk mode
- Voice activity detection (VAD) with cancellable listening

### ✅ Phase 4: Web Dashboard & API
- `FastAPI` web server
- Real-time dashboard UI
- Model switching and prompt tuning
- Memory inspection
- Tool permission management
- WebSocket support for real-time updates

### ✅ Phase 5: IoT & Network Discovery
- Home Assistant integration
- ARP-based device discovery
- Safe port scanning (top 20 ports, timeouts)
- Device classification (router, phone, IoT, PC, etc.)
- `SQLite` persistence (scan history with `scan_id` tracking)
- Merged discovery results (`LocalNetworkScanner` + `NetworkDiscovery`)
- Device registry and control

### ✅ Phase 6: Security & Science Research
- Approval queue for sensitive tool operations
- Tool sandboxing with resource limits
- Full audit logging with operation trails
- `SimulationEnvironment` — iterative hypothesis testing
- `ScientificLiteratureSystem` — persistent `Chroma`-backed vector search
- `PhysicsConstrainedRegressor` — hybrid physics/neural model
- `ExperimentTracker` — reproducible run logging (JSONL + per-run JSON)

### ✅ Phase 7: Desktop Application
- Standalone `PyQt6` desktop app (`desktop_entry.py`)
- Reskinned UI (gradients, neon status chips, card layout)
- `DesktopVoiceController` with synchronized STT/TTS state machine
- Stop Voice button + `Esc` keyboard shortcut
- `DiagnosticsPanel` tab showing service health at launch
- Desktop shortcut installer (`scripts/install-shortcut.ps1`)

### ✅ Phase 8: Science Lab Dashboard
- Science Lab nav view in web dashboard
- `/api/science/*` REST endpoints
- Experiment config YAMLs (`config/experiments/`)
- `matplotlib` plotting with graceful degradation

### ✅ Phase 9: Core Stack Baseline
- Ollama model stack reset and locked to 8 production models
- `ModelSelector` updated with `math` task category
- Per-task routing: code→`deepseek-coder`, math/reasoning→`deepseek-r1`, chat→`qwen2.5`, vision→`llava`
- Runtime embeddings use local `all-MiniLM-L6-v2`; voice STT uses Whisper `base`
- `scripts/reset_ollama_models2.ps1` for repeatable stack resets

---

## Quick Start

### Fastest Setup (One Command)

**Windows:**
```powershell
.\quickstart.bat
```

**macOS/Linux:**
```bash
chmod +x quickstart.sh
./quickstart.sh
```

### Manual Setup

**1. Install Ollama**
```bash
# Download from https://ollama.ai
# Start Ollama in background/separate terminal
ollama serve
```

**2. Install Python Dependencies**
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
```

**3. Download the Active Runtime Models**
```bash
# Active Ollama routing stack:
ollama pull qwen2.5         # Primary brain / fallback (~4.7 GB)
ollama pull deepseek-coder  # Code tasks (~776 MB)
ollama pull deepseek-r1     # Math / deep reasoning (~5.2 GB)
ollama pull mistral         # Creative / fast general (~4.4 GB)
ollama pull llava           # Vision (~4.7 GB)

# Non-Ollama runtime models come from Python packages/config:
# - sentence-transformers: all-MiniLM-L6-v2 (embeddings)
# - Whisper: base (speech-to-text)

# Or run the reset script:
powershell -ExecutionPolicy Bypass -File scripts/reset_ollama_models2.ps1
```

**4. Verify Installation**
```bash
python run_smoke_tests.py
# Should show: 42/46 passed, 0 failed, 4 skipped
```

**5. Run the System**
```bash
python main.py --mode repl
# Or: --mode cli, --mode voice, --mode dashboard
```

---

## Operating Modes

### 1. REPL Mode (CLI Interactive)
```bash
python main.py --mode repl
```
- Multi-turn conversation
- Type commands, get responses
- Memory persists across turns
- Best for: Development, exploration

### 2. CLI Mode (Single Query)
```bash
python main.py --mode cli
```
- One query, one response, exit
- Non-interactive
- Best for: Scripting, one-offs

### 3. Voice Mode (Speech I/O)
```bash
python main.py --mode voice

# Or push-to-talk
python main.py --mode voice --input ptt
```
- Speak → STT → process → TTS → speak
- Real-time audio processing
- Best for: Hands-free operation

### 4. Dashboard Mode (Web UI)
```bash
python main.py --mode dashboard
# Open http://localhost:8000
```
- Browser-based interface
- Real-time updates
- Model/prompt controls
- Memory inspection
- Network/IoT monitoring
- Best for: Operations

### 5. Deployment Mode
```bash
python main.py --deploy-config config/config.yaml
```
- Configuration overlay
- Model/port overrides
- Environment-specific settings
- Best for: Production

---

## Configuration

### Configuration Files

```
config/
├── phase1_config.yaml              # Core LLM & memory
├── phase2_config.yaml              # Logging & planning
├── phase3_config.yaml              # Voice settings
├── phase4_config.yaml              # Dashboard & API
├── phase4_integration_map.yaml     # IoT & integrations
└── config.yaml                     # Deployment overlay
```

### Quick Configuration Examples

**Change LLM Model:**
```yaml
# config/phase1_config.yaml
ollama:
  model: "auto"          # or pin qwen2.5:latest / deepseek-r1:latest
  fallback_model: "qwen2.5:latest"

model_routing:
  code: "deepseek-coder:latest"
  temperature: 0.7       # 0=deterministic, 1=creative
```

**Enable Home Assistant:**
```yaml
# config/phase4_integration_map.yaml
iot:
  home_assistant:
    enabled: true
    base_url: "http://homeassistant.local:8123"
    token: "your_token_here"
```

**Change Dashboard Port:**
```yaml
# config/phase4_config.yaml
ui:
  dashboard:
    port: 8001           # If 8000 is in use
```

**Run with Overrides:**
```bash
python main.py \
  --mode dashboard \
  --model qwen2.5:latest \
  --port 8001 \
  --offline
```

---

## Architecture

### System Layers

```
┌─ PRESENTATION LAYER ─────────────────────┐
│  CLI  │  Voice  │  Dashboard  │  API    │
└────────────────────┬──────────────────────┘
                     │
┌─ ORCHESTRATION LAYER ────────────────────┐
│  TaskPlanner  │  Orchestrator  │  Logger │
└────────────────────┬──────────────────────┘
                     │
┌─ COGNITION LAYER ────────────────────────┐
│  CognitionEngine (Ollama inference)      │
└────────────────────┬──────────────────────┘
                     │
┌─ EXECUTION LAYER ────────────────────────┐
│  ToolExecutor  │  SecurityManager │ Tools│
└────────────────────┬──────────────────────┘
                     │
┌─ MEMORY LAYER ───────────────────────────┐
│  RAGSystem  │  ChromaDB  │  Session Store │
└────────────────────┬──────────────────────┘
                     │
┌─ INTEGRATION LAYER ──────────────────────┐
│  IoTManager  │  NetworkDiscovery  │ HA  │
└──────────────────────────────────────────┘
```

### Request Flow

```
User Input → Parse → Log → Plan → Retrieve Context → LLM
                                        ↑
                                        │
                              Tool Results (loop back)
                                        │
LLM Output → Format Response → Output (CLI/Voice/API)
```

---

## Components

### Core Modules

| Module | Purpose | Status |
|--------|---------|--------|
| `core/agent.py` | Main intelligence loop | ✅ |
| `core/orchestrator.py` | Workflow management | ✅ |
| `core/cognition.py` | LLM interface | ✅ |
| `core/planner.py` | Multi-step task planning | ✅ |
| `core/structured_logger.py` | Audit logging | ✅ |
| `memory/rag.py` | Context retrieval | ✅ |
| `models/ollama_client.py` | Ollama HTTP client | ✅ |
| `models/selector.py` | Auto task-routing (code/math/reasoning/vision) | ✅ |
| `voice/stt.py` | Whisper speech-to-text | ✅ |
| `voice/tts.py` | Multi-backend TTS | ✅ |
| `ui/desktop_app.py` | PyQt6 desktop application | ✅ |
| `ui/dashboard_api.py` | FastAPI backend + science endpoints | ✅ |
| `science/simulation.py` | Iterative hypothesis simulation | ✅ |
| `science/literature.py` | Chroma-backed literature search | ✅ |
| `science/hybrid_model.py` | Physics-constrained neural model | ✅ |
| `science/experiment_tracker.py` | Reproducible run logging | ✅ |
| `iot/manager.py` | IoT device management | ✅ |
| `security/sandbox.py` | Tool sandboxing | ✅ |
| **tools/base_tools.py** | File/code execution | ✅ |
| **security/sandbox.py** | Permissions & limits | ✅ |
| **voice/stt.py** | Speech-to-text | ✅ |
| **voice/tts.py** | Text-to-speech | ✅ |
| **iot/manager.py** | IoT orchestration | ✅ |
| **iot/scanner.py** | Network discovery | ✅ **NEW** |
| **ui/dashboard_api.py** | Web API | ✅ |

### New in Phase 5

**iot/scanner.py - NetworkDiscovery**
- ARP-based device discovery
- Safe port scanning (timeouts)
- Device fingerprinting
- SQLite persistence
- Device classification (router, phone, IoT, PC)
- Integrated into IoTManager.discover_devices()

**iot/manager.py - Enhanced**
- Now calls both LocalNetworkScanner and NetworkDiscovery
- Merges results (deduplicates, unions ports)
- Returns combined discovery results

---

## Usage Examples

### Example 1: Simple Query

```bash
$ python main.py --mode repl

You: What time is it?
Assistant: I don't have access to the current time directly,
but based on my system knowledge, I can help you...

You: List all Python files in the current directory
Assistant: I'll list the Python files for you...
[Tool execution: list_directory]
Found: main.py, startup.py, run_smoke_tests.py, ...

You: exit
```

### Example 2: Multi-Turn Conversation

```bash
$ python main.py --mode repl

You: Remember that my favorite color is blue
Assistant: ✓ Added to memory: favorite color = blue

You: What's my favorite color?
Assistant: Your favorite color is blue (from your notes)

You: Change it to green
Assistant: ✓ Updated in memory: favorite color = green
```

### Example 3: Voice Interaction

```bash
$ python main.py --mode voice --input ptt

[Press Enter to start listening]
[Listening... speak now]

You: "What devices are on my network?"

[Processing speech...]
Assistant: "Scanning your network..."
[Tool execution: network discovery]
Assistant: "I found 23 devices on your network including:
           your router, phone, laptop, and 20 other devices."
[Speaking response via TTS]
```

### Example 4: Network Discovery

```python
from iot.manager import IoTManager

config = {"iot": {"enabled": True}}
manager = IoTManager(config)

# Discover all devices
result = manager.discover_devices()
print(f"Scanner found: {result['scanner_hosts_seen']} devices")
print(f"ARP discovery found: {result['discovery_hosts_seen']} devices")
print(f"Merged and registered: {result['merged_hosts_registered']} devices")

for device in result['inventory']['network_hosts']:
    print(f"  {device['ip']} - ports: {device.get('ports', [])}")
```

### Example 5: Dashboard Use

```bash
$ python main.py --mode dashboard

# Open browser to http://localhost:8000
# You'll see:
# - Real-time conversation interface
# - Model selector (switch between auto routing, qwen2.5, deepseek-r1, etc.)
# - System prompt editor
# - Memory inspection
# - Network/device status
# - Tool permissions

# WebSocket updates as you type
```

---

## Troubleshooting

### Common Issues & Solutions

**Issue: "Cannot connect to Ollama"**
```bash
# Check if Ollama is running
ollama list

# If not running:
ollama serve

# Verify with:
curl http://localhost:11434/api/health
```

**Issue: "No module named 'chromadb'"**
```bash
pip install --upgrade -r requirements.txt
```

**Issue: "Voice not working"**
```bash
# Check audio device
python -c "import sounddevice; sounddevice.default_device"

# Test microphone
python voice/audio_utils.py  # if test function exists
```

**Issue: "Dashboard port 8000 already in use"**
```bash
# Use different port
python main.py --mode dashboard --port 8001

# Or kill the process using port 8000
# Windows: netstat -ano | findstr :8000
# macOS/Linux: lsof -i :8000; kill -9 <PID>
```

**Issue: "Network discovery finds no devices"**
```bash
# Check your network connectivity
ping 8.8.8.8

# Try specific subnet
python -c "
from iot.scanner import scan_network
r = scan_network(subnet='192.168.1.0/24')
print(f'Found {r[\"device_count\"]} devices')
"
```

---

## Testing & Quality

### Run Smoke Tests

```bash
python run_smoke_tests.py
```

Expected output:
```
============================================================
Test Summary:
  Passed:  42/46
  Failed:  0/46
  Skipped: 4/46    (requires Ollama/audio setup)
============================================================
```

### Test Categories

- ✅ Directory structure validation
- ✅ Module imports
- ✅ Component instantiation
- ✅ Config loading
- ✅ Syntax validation
- ✅ Requirements check

---

## Documentation

### Internal Docs

| Document | Purpose |
|----------|---------|
| **INSTALLATION.md** | Setup guide, requirements, operating models |
| **GENERAL_SUMMARY_README.md** | Full-picture system summary (architecture, workflows, status) |
| **ARCHITECTURE_AND_FLOW.md** | Technical architecture, flow diagrams |
| **CODE_DOCUMENTATION.md** | Module-level API and implementation reference |
| **DOCUMENTATION_INDEX.md** | Documentation navigation map |
| **PHASE1_6_REQUIREMENTS_BASELINE.md** | Official phase requirements |
| **PHASE9_CORE_STACK.md** | Canonical baseline for phases 7-9 |
| **DEVELOPMENT_GUIDE.md** | Development workflow |
| **README.md** | This file |

### External Resources

- **Ollama:** https://ollama.ai/
- **ChromaDB:** https://www.trychroma.com/
- **FastAPI:** https://fastapi.tiangolo.com/
- **Home Assistant:** https://www.home-assistant.io/

---

## Project Stats

```
Total Python Files:       35
Lines of Code:            ~8,000+
Supported LLM Models:     20+ (via Ollama)
Network Ports Scanned:    20 (safe defaults)
Supported Voice Backends: 3 (edge-tts, coqui, pyttsx3)
Database:                 SQLite + ChromaDB
API Endpoints:            30+
```

---

## Version & Status

- **Current Version:** Phase 9 core stack with Phase 10 hardening work in progress
- **Python:** 3.10+
- **Status:** Production-ready local stack (offline-first), actively maintained
- **Last Updated:** 2026-04-30
- **Maintainer:** Embodied AI Project

---

## Quick Links

- 📖 **[Complete Setup Guide](INSTALLATION.md)**
- 🧭 **[General Summary (Full Picture)](GENERAL_SUMMARY_README.md)**
- 🏗️ **[Architecture & Flows](ARCHITECTURE_AND_FLOW.md)**
- 🧠 **[Code Documentation](CODE_DOCUMENTATION.md)**
- 🔧 **[Development Guide](DEVELOPMENT_GUIDE.md)**
- 📋 **[Phase Requirements](PHASE1_6_REQUIREMENTS_BASELINE.md)**
- 📚 **[Documentation Index](DOCUMENTATION_INDEX.md)**
- 🧪 **[Run Tests](run_smoke_tests.py)**

---

## Getting Started Right Now

```bash
# 1. Clone repo (if not already done)
cd ai-ui-system

# 2. Start Ollama (in another terminal)
ollama serve

# 3. Install and run
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 4. Pick a mode and go!
python main.py --mode repl        # Interactive
# OR
python main.py --mode dashboard   # Web UI (http://localhost:8000)
# OR
python main.py --mode voice       # Voice interaction
```

That's it! You're ready to interact with your local AI assistant.

---

**Happy AI-ing! 🚀**
