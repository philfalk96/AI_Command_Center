# Embodied AI System — Complete Installation & Setup Guide

> **Phase 9 — Core Stack Baseline** | April 2026

## Table of Contents
1. [System Overview](#system-overview)
2. [Features](#features)
3. [Architecture & Flow](#architecture--flow)
4. [Requirements](#requirements)
5. [Installation](#installation)
6. [Quick Start](#quick-start)
7. [Configuration](#configuration)
8. [Operating Modes](#operating-modes)
9. [Network Architecture](#network-architecture)
10. [Maintenance & Troubleshooting](#maintenance--troubleshooting)
11. [API Reference](#api-reference)

---

## System Overview

The **Embodied AI System** is a modular, local-first artificial intelligence platform that integrates:
- **Local LLM** (Ollama-based) for offline inference
- **RAG Memory** (ChromaDB) for context persistence
- **Voice I/O** (Whisper STT + multi-backend TTS)
- **IoT Control** (Home Assistant integration + local network discovery)
- **Web Dashboard** (FastAPI + real-time API)
- **Security Sandbox** (tool execution with approval workflows)

**Deployment Model:** Private network, fully offline-capable, single-machine or distributed deployment

---

## Features

### Phase 1-2: Core Intelligence
- ✅ CLI REPL interface with multi-turn conversation
- ✅ Local RAG retrieval from embeddings
- ✅ Tool execution with sandboxing
- ✅ Structured activity logging
- ✅ File I/O and code execution tools
- ✅ Multi-step task planning

### Phase 3: Voice Capabilities
- ✅ Real-time speech-to-text (Whisper)
- ✅ Multiple TTS backends (edge-tts, coqui, pyttsx3)
- ✅ Push-to-talk mode
- ✅ VAD (Voice Activity Detection) ready

### Phase 4: Web Dashboard & API
- ✅ FastAPI web server with CORS support
- ✅ Real-time dashboard UI
- ✅ Model switching and prompt tuning
- ✅ Memory inspection interface
- ✅ Tool permission management

### Phase 5: IoT & Home Automation
- ✅ Home Assistant integration
- ✅ ARP-based network device discovery
- ✅ Safe port scanning (top 20 ports)
- ✅ Device fingerprinting and classification
- ✅ SQLite persistence of scan results
- ✅ Merged discovery results (LocalNetworkScanner + NetworkDiscovery)

### Phase 6: Security + Science
- ✅ Approval queue for sensitive tool operations
- ✅ Tool sandboxing with resource limits
- ✅ Audit logging with full operation trails
- ✅ `SimulationEnvironment` — iterative hypothesis testing
- ✅ `ScientificLiteratureSystem` — Chroma-backed vector search
- ✅ `PhysicsConstrainedRegressor` — hybrid physics/neural model
- ✅ `ExperimentTracker` — reproducible JSONL run logging

### Phase 7: Desktop Application
- ✅ Standalone `PyQt6` desktop app (`desktop_entry.py`)
- ✅ Reskinned UI with gradients, neon status chips, and card layout
- ✅ `DesktopVoiceController` with synchronized STT/TTS state machine
- ✅ Stop Voice button (`Esc` shortcut)
- ✅ `DiagnosticsPanel` tab showing service health
- ✅ Desktop + Start Menu shortcut installer

### Phase 8: Science Lab Dashboard
- ✅ Science Lab nav view in web dashboard
- ✅ `/api/science/*` REST endpoints
- ✅ Experiment config YAMLs under `config/experiments/`

### Phase 9: Core Stack Baseline
- ✅ Ollama model stack locked to 8 production models
- ✅ `ModelSelector` with `math` task category
- ✅ Per-task routing: code→`deepseek-coder`, math→`deepseek-r1`, chat→`qwen2.5`, vision→`llava`
- ✅ `scripts/reset_ollama_models2.ps1` for repeatable stack resets

---

## Architecture & Flow

### High-Level System Architecture

```
┌──────────────────────────────────────────────────────┐
│            EMBODIED AI SYSTEM (Phase 4-5)            │
└──────────────────────────────────────────────────────┘
          │
          ├─ Input Layer (CLI / Voice / Dashboard)
          │
          ├─ Orchestration Layer
          │   ├─ Task Planner (multi-step execution)
          │   ├─ Structured Logger (audit trail)
          │   └─ Cognition Engine (LLM inference)
          │
          ├─ Memory Layer
          │   ├─ RAG System (ChromaDB embeddings)
          │   └─ Session State
          │
          ├─ Execution Layer
          │   ├─ Tool Executor (sandbox + permissions)
          │   ├─ File System Tools
          │   └─ Code Execution
          │
          ├─ Integration Layer
          │   ├─ IoT Manager (HA + Network Discovery)
          │   ├─ Home Assistant Client
          │   └─ Device Registry
          │
          └─ Output Layer
              ├─ CLI Output
              ├─ Voice Output (TTS)
              └─ Dashboard API
```

### Request Flow Diagram

```
┌─ User Query (CLI/Voice/API)
│
├─ StructuredLogger: Audit & session tracking
│
├─ TaskPlanner: Break into sub-tasks
│
├─ RAGSystem: Retrieve relevant context
│  (Semantic search in ChromaDB)
│
├─ CognitionEngine: LLM inference
│  (Call Ollama with context + system prompt)
│
├─ ToolExecutor: Execute tools needed for response
│  ├─ FileSystemTools (read/write/list)
│  ├─ PythonExecuteTool (safe code exec)
│  └─ IoT/Network tools
│
├─ Refinement: LLM processes tool results
│
└─ Output: Return response + audit log
```

### Component Interaction

```
Dashboard UI ──────┐
         ▲         │
         │         ▼
CLI REPL ──── Main.py
         │         │
Voice I/O┘         ├─────► Orchestrator
                   │           │
                   │           ├─► TaskPlanner
                   │           ├─► CognitionEngine (Ollama)
                   │           └─► ToolExecutor
                   │
                   ├─────► Memory Layer
                   │       ├─ RAGSystem (ChromaDB)
                   │       └─ StructuredLogger
                   │
                   ├─────► IoT Layer
                   │       ├─ IoTManager
                   │       ├─ NetworkDiscovery (ARP scan)
                   │       └─ HomeAssistantClient
                   │
                   └─────► Security Layer
                           ├─ SecurityManager
                           └─ Sandbox
```

### Data Flow for Network Discovery

```
User calls: manager.discover_devices()
│
├─ LocalNetworkScanner.scan()
│  ├─ Get adapter profiles (ipconfig/ifconfig)
│  ├─ Perform ARP sweep
│  └─ Port scanning on detected IPs
│
├─ NetworkDiscovery.scan_network()
│  ├─ ARP table parsing
│  ├─ Safe port scanning (top 20 ports)
│  ├─ Device classification
│  └─ Store in SQLite (data/network_discovery.db)
│
├─ _merge_discovery_results()
│  ├─ Deduplicate by IP
│  ├─ Merge ports (union)
│  ├─ Keep highest confidence
│  └─ Mark discovery source
│
└─ Return merged device list to device_registry
```

---

## Requirements

### System Requirements
- **OS:** Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python:** 3.10+ (3.11+ recommended)
- **RAM:** 4GB minimum (8GB+ for full features)
- **Disk:** 10GB+ free (for models and ChromaDB)
- **Network:** Local network access for IoT discovery

### Software Dependencies

#### Core Runtime
- **Ollama 0.1.15+** (https://ollama.ai)
  - Download and run: `ollama serve`
  - Provides local LLM inference engine
  - Can run offline once model is cached

#### Python Packages (see requirements.txt)
```
# LLM & ML
ollama>=0.1.15
chromadb>=0.4.0
sentence-transformers>=2.2.0
torch>=2.0.0 (installed with transformers)

# Web Framework
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0

# Speech & Audio
edge-tts>=6.1.0
openai-whisper>=20230314
pyttsx3>=2.90
coqui-tts>=0.6.1
sounddevice>=0.4.6
numpy>=1.24.0

# Utilities
pyyaml>=6.0
click>=8.1.0
colorama>=0.4.6
requests>=2.31.0

# Security & Performance
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
```

### Device Network Requirements
- **For IoT Discovery:** Local network connectivity (192.168.x.x, 10.x.x.x, or 172.16-31.x.x)
- **For Home Assistant:** HA instance running on same local network (http://homeassistant.local or configured IP)
- **Ports:** 8000 (dashboard), 11434 (Ollama), 5000-5100 (dynamic tool ports)

---

## Installation

### Option 1: Quick Installation (Recommended)

#### Windows:
```powershell
# 1. Clone or extract the ai-ui-system repository
cd ai-ui-system

# 2. Run the quickstart script
.\quickstart.bat

# 3. Start Ollama in another terminal
ollama serve
```

#### macOS/Linux:
```bash
# 1. Clone or extract the ai-ui-system repository
cd ai-ui-system

# 2. Run the quickstart script
chmod +x quickstart.sh
./quickstart.sh

# 3. Start Ollama in another terminal
ollama serve
```

### Option 2: Manual Installation

#### Step 1: Install Ollama
```bash
# Download from https://ollama.ai
# Run in background/separate terminal
ollama serve
```

#### Step 2: Install Python Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Install torch with CUDA support (optional, for GPU acceleration)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### Step 3: Download LLM Model
```bash
# Download the active Ollama routing stack
ollama pull qwen2.5
ollama pull deepseek-coder
ollama pull deepseek-r1
ollama pull mistral
ollama pull llava

# Embeddings and speech models are configured locally via Python packages:
# - sentence-transformers: all-MiniLM-L6-v2
# - Whisper STT: base
```

#### Step 4: Verify Installation
```bash
python run_smoke_tests.py
```

### Option 3: Docker Deployment (Future)
```bash
docker build -t embodied-ai .
docker run -p 8000:8000 -p 11434:11434 embodied-ai
```

---

## Quick Start

### Mode 1: CLI REPL (Default)
```bash
python main.py
# or
python main.py --mode repl

# In REPL, type commands:
> What is the weather?
> Save a file with my notes
> List files in the data directory
> Tell me about my network devices
```

### Mode 2: Single-Query CLI
```bash
python main.py --mode cli
# Prompts for a single query, outputs response, exits

python main.py --mode cli --config config/phase4_config.yaml
```

### Mode 3: Voice Interaction
```bash
python main.py --mode voice
# Listens for voice input, processes, and speaks response

python main.py --mode voice --input ptt
# Push-to-talk mode (press Enter to start listening)
```

### Mode 4: Dashboard (FastAPI)
```bash
python main.py --mode dashboard

# Open browser to http://localhost:8000
# Dashboard shows:
# - Real-time conversation
# - Model/prompt controls
# - Memory inspection
# - Tool permissions
# - Network/IoT status
```

---

## Configuration

### Configuration Files Location
```
ai-ui-system/
├── config/
│   ├── phase1_config.yaml      # Core settings
│   ├── phase2_config.yaml      # Logging & planning
│   ├── phase3_config.yaml      # Voice settings
│   ├── phase4_config.yaml      # Dashboard & API
│   ├── phase4_integration_map.yaml  # Integration points
│   └── config.yaml             # Deployment overlay
```

### Key Configuration Options

#### Ollama/LLM (phase1_config.yaml)
```yaml
ollama:
  base_url: "http://localhost:11434"
  model: "auto"
  fallback_model: "qwen2.5:latest"
  temperature: 0.7

model_routing:
  code: "deepseek-coder:latest"
  reasoning: "deepseek-r1:latest"
  math: "deepseek-r1:latest"
  chat: "qwen2.5:latest"
  creative: "mistral:latest"
  vision: "llava:latest"
```

#### Memory/RAG (phase1_config.yaml)
```yaml
memory:
  type: "chromadb"
  db_path: "./data/chroma_db"
  embedding_model: "all-MiniLM-L6-v2"
  chunk_size: 512
  overlap: 50
```

#### Voice (phase3_config.yaml)
```yaml
voice:
  stt:
    engine: "whisper"
    model_size: "base"           # tiny, small, base, medium, large
    language: "en"
  tts:
    engine: "edge-tts"           # or coqui-tts, pyttsx3
    voice: "en-US-AriaNeural"
    rate: 1.0
```

#### Dashboard/API (phase4_config.yaml)
```yaml
ui:
  dashboard:
    enabled: true
    host: "127.0.0.1"
    port: 8000
    cors_origins: ["localhost", "127.0.0.1"]
```

#### IoT/Network (phase4_integration_map.yaml)
```yaml
iot:
  enabled: true
  local_network:
    enabled: true
    timeout_ms: 220
    ports: [22, 80, 443, 1883, 5353, 8080]
    max_workers: 32
    discovery_db_path: "data/network_discovery.db"
  home_assistant:
    enabled: true
    base_url: "http://homeassistant.local:8123"
    token: "YOUR_HA_TOKEN"
```

### Deployment Configuration (config.yaml)
Override settings at deployment time without modifying base configs:
```yaml
model:
  name: "auto"
backend:
  host: "0.0.0.0"               # Bind to all interfaces
  port: 8000
offline_mode: false
logging:
  directory: "logs"
  level: "INFO"
```

Use with:
```bash
python main.py --deploy-config config/config.yaml
```

---

## Operating Modes

### 1. REPL Mode (Interactive)
- Multi-turn conversation
- Tool execution feedback
- Memory inspection
- Best for: Development, testing, interactive use

### 2. CLI Mode (Single Query)
- One query → one response → exit
- Useful for: Scripting, one-off tasks

### 3. Voice Mode (Voice I/O)
- Speak → speech-to-text → process → speak response
- Supports push-to-talk (--input ptt)
- Best for: Hands-free operation

### 4. Dashboard Mode (Web UI)
- Web-based interface
- Real-time API
- Model/prompt controls
- Memory inspection
- Best for: Operations, monitoring

### 5. Deployment Mode (Production)
- Headless server
- Full API surface
- Configuration overlays
- Best for: Production deployment

---

## Network Architecture

### Local Network Discovery (IoT)

#### Supported Device Types
```
router       - Detected by: DNS port 53
phone        - Detected by: UPnP port 1900
iot          - Detected by: MQTT port 1883 or mDNS 5353
pc           - Detected by: SSH (22), RDP (3389), HTTP (80, 443)
printer      - Detected by: Printer service ports
nas          - Detected by: NAS service ports (445, 139, 8000+)
```

#### Default Top 20 Scanned Ports
```
22   - SSH (Linux/Mac)
23   - Telnet (legacy)
25   - SMTP (mail)
53   - DNS
80   - HTTP
110  - POP3 (mail)
135  - RPC (Windows)
139  - NetBIOS (Windows)
143  - IMAP (mail)
443  - HTTPS
445  - SMB (Windows/NAS)
587  - SMTP (mail)
993  - IMAPS (mail)
995  - POP3S (mail)
1433 - SQL Server
3306 - MySQL
3389 - RDP (Windows)
5432 - PostgreSQL
5900 - VNC
8080 - HTTP alternate
```

#### Discovery Flow
1. **ARP Scan** → Find all active IPs on subnet
2. **Port Scan** → Check which ports are open (timeout: 220ms/host)
3. **Device Classification** → Fingerprint device type by ports
4. **SQLite Persistence** → Store results with scan_id and timestamp
5. **Merge Results** → Combine LocalNetworkScanner + NetworkDiscovery
6. **Device Registry** → Store in manager for queries

#### Database Schema (network_discovery.db)
```sql
-- Scans table
CREATE TABLE scans (
    scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    subnet TEXT,
    device_count INTEGER
);

-- Devices table
CREATE TABLE devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id INTEGER REFERENCES scans(scan_id),
    ip TEXT,
    mac TEXT,
    vendor TEXT,
    ports TEXT,                    -- JSON array of port numbers
    device_type TEXT,              -- router, phone, iot, pc, etc.
    hostname TEXT,
    confidence REAL,               -- 0.0 to 1.0
    UNIQUE(scan_id, ip)
);
```

### Home Assistant Integration
- Automatic discovery of HA entities
- Service call support
- Domain-based filtering
- Entity-level permissions

---

## Maintenance & Troubleshooting

### Common Issues

#### Issue: "Ollama connection refused"
```bash
# Check if Ollama is running
ollama list

# If not running, start it
ollama serve

# Verify connectivity
curl http://localhost:11434/api/health
```

#### Issue: "ChromaDB initialization fails"
```bash
# Check disk space
df -h

# Clear ChromaDB cache
rm -rf data/chroma_db

# Reinitialize
python main.py --mode repl
```

#### Issue: "No devices found in network discovery"
```bash
# Check network connectivity
ping 8.8.8.8

# Check subnet detection
ipconfig (Windows) or ifconfig (Unix)

# Try with specific subnet
python -c "from iot.scanner import scan_network; scan_network(subnet='192.168.1.0/24')"
```

#### Issue: "Dashboard port already in use"
```bash
# Change port in config.yaml
backend:
  port: 8001  # or another free port

# Or kill existing process
lsof -i :8000     # Find process
kill -9 <PID>     # Kill it
```

### Maintenance Tasks

#### Daily
- Check logs for errors: `logs/phase1.log`
- Monitor Ollama health: `curl http://localhost:11434/api/health`
- Verify network discovery works: `python run_smoke_tests.py`

#### Weekly
- Archive old logs: `logs/sessions/` (auto-rolling)
- Review permission approvals (Phase 6): Dashboard → Approvals

#### Monthly
- Refresh routed models: `ollama pull qwen2.5 ; ollama pull deepseek-coder ; ollama pull deepseek-r1 ; ollama pull mistral ; ollama pull llava`
- Backup ChromaDB: `cp -r data/chroma_db data/chroma_db.backup`
- Clean temporary files: `rm -rf __pycache__ logs/temp*`

#### Quarterly
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Review security logs: `logs/security/` (Phase 6)
- Performance tuning: Check memory/CPU usage

### Logging

Logs are stored in:
```
logs/
├── phase1.log              # Main application log
├── sessions/
│   ├── {session_id}.jsonl  # Per-session structured logs
│   └── ...
├── cognition/              # LLM inference logs
├── tts/                    # Text-to-speech logs
└── tasks/                  # Task execution logs
```

View logs:
```bash
# Current session
tail -f logs/phase1.log

# Recent structured logs
cat logs/sessions/*.jsonl | tail -20

# Search for errors
grep ERROR logs/phase1.log
```

---

## API Reference

### Main Entry Point: `main.py`

```bash
python main.py [OPTIONS]

Options:
  --mode {repl,cli,voice,dashboard}     Operating mode (default: repl)
  --config PATH                         Config file to load
  --deploy-config PATH                  Deployment config overlay
  --model MODEL_NAME                    Override LLM model
  --port PORT                          Override dashboard port
  --offline                            Run in offline mode
  --help                               Show help
```

### IoT Manager API

```python
from iot.manager import IoTManager

manager = IoTManager(config)

# Discover devices (both LocalNetworkScanner + NetworkDiscovery)
result = manager.discover_devices(
    subnet="192.168.1.0/24",           # Optional: specific subnet
    ports=[22, 80, 443],               # Optional: specific ports
    domain="light"                      # Optional: HA domain filter
)
# Returns: {ok, message, scanner_hosts_seen, discovery_hosts_seen, 
#           merged_hosts_registered, arp_discovery, inventory}

# Get status
status = manager.status()

# List devices
devices = manager.list_devices(domain="light")

# Control device (via Home Assistant)
result = manager.control_intent(
    intent="turn_on",
    target="bedroom_light",
    args={"brightness": 100}
)
```

### Network Discovery API

```python
from iot.scanner import scan_network

# Run ARP-based discovery
result = scan_network(
    subnet=None,                   # Auto-detect if None
    timeout_ms=220,                # Per-host timeout
    max_ports=20                   # Limit to top 20 ports
)
# Returns: {ok, subnet, device_count, scan_id, devices, database}

# Access results
print(result['device_count'])      # Total devices found
print(result['scan_id'])           # Scan ID for querying database
for device in result['devices']:
    print(f"{device['ip']} - {device['ports']}")
```

### Tool Execution API

```python
from tools.base_tools import ToolExecutor

executor = ToolExecutor(config)

# Register a new tool
from tools.base_tools import Tool

class MyTool(Tool):
    def execute(self, input_file: str, **kwargs):
        with open(input_file) as f:
            return f.read()

executor.tools['my_tool'] = MyTool(name='my_tool', description='...')

# Execute tool
result = executor.execute(tool_name='my_tool', input_file='data.txt')
```

---

## Support & Resources

- **Documentation:** See README.md, ARCHITECTURE.md, DEVELOPMENT_GUIDE.md
- **Issues:** Run `python run_smoke_tests.py` to diagnose problems
- **Logs:** Check `logs/` directory for detailed diagnostics
- **Configuration:** Modify `config/` YAML files for customization
- **Models:** Visit https://ollama.ai for available models

---

**Last Updated:** 2026-04-28  
**Version:** Phase 4-5 (IoT + Web Dashboard)  
**Status:** Production Ready
