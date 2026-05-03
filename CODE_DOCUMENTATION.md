# Embodied AI System - Code Documentation

## Complete Module Reference

## Recent Updates (April 30, 2026)

### `core/profiler.py` - Profiler

**Purpose:** Lightweight runtime performance tracing for request spans, token usage, and GPU memory snapshots.

**Key APIs:**
```python
class Profiler:
        def span(name: str, **tags)          # Timed context manager
        def record_tokens(model, prompt_tokens, completion_tokens)
        def gpu_snapshot() -> Dict[str, Any]
        def to_dict() -> Dict[str, Any]
        def summary() -> str
```

### `models/selector.py` - Timeout Fallback Routing

**New API:**
```python
def select_with_fallback(prompt, generate_fn, timeout=None)
```

Fallback chain:
1. Primary routed model
2. Smaller model on timeout
3. Configured hard fallback model

### `tools/base_tools.py` - ToolResult Envelope

Tool execution now normalizes responses into:
```json
{
    "status": "ok|error",
    "output": "...",
    "metadata": {"tool": "...", "duration_ms": 1.2}
}
```

### `rag/embeddings.py` - Batch Embedding

**New API:**
```python
def embed_batch(texts: List[str], batch_size: int = 32) -> List[List[float]]
```

Uses cache-aware batching to reduce repeated embedding cost during ingestion.

### Table of Contents
1. [Core Components](#core-components)
2. [Memory & RAG](#memory--rag)
3. [Tools & Execution](#tools--execution)
4. [IoT & Integration](#iot--integration)
5. [Voice I/O](#voice-io)
6. [Web UI & API](#web-ui--api)
7. [Security & Logging](#security--logging)
8. [Entry Points](#entry-points)

---

## Core Components

### `core/agent.py` - EmbodiedAIAgent

**Purpose:** Main intelligence loop combining LLM, memory, tools, and security.

**Key Classes:**
```python
class EmbodiedAIAgent:
    """Core agent loop - Phase 2+"""
    def __init__(config)        # Initialize with config
    def _run_phase1(query)       # Single-turn inference
    def _run_phase2_multi_step(query)  # Multi-step with planner
    def process(query) → str     # Main entry point
```

**Flow:**
1. Accept user query
2. Log via StructuredLogger
3. Plan via TaskPlanner (Phase 2)
4. Retrieve context via RAGSystem
5. Call LLM via CognitionEngine
6. Execute tools via ToolExecutor
7. Refine results
8. Return response

**Dependencies:**
- `models.ollama_client.OllamaClient` - LLM calls
- `memory.rag.RAGSystem` - Context retrieval
- `tools.base_tools.ToolExecutor` - Tool dispatch
- `security.sandbox.SecurityManager` - Permission checking
- `core.structured_logger.StructuredLogger` - Audit logging
- `core.planner.TaskPlanner` - Multi-step planning
- `core.cognition.CognitionEngine` - LLM orchestration

**Usage:**
```python
from core.agent import EmbodiedAIAgent
import yaml

config = yaml.safe_load(open('config/phase1_config.yaml'))
agent = EmbodiedAIAgent(config)
response = agent.process("What are my files?")
```

---

### `core/orchestrator.py` - Orchestrator

**Purpose:** High-level workflow management and mode selection.

**Key Classes:**
```python
class Orchestrator:
    """Route requests to appropriate mode handler"""
    def __init__(config, mode='repl')
    def run()                    # Main orchestration
    def _run_repl()              # Interactive loop
    def _run_cli()               # Single query
    def _run_voice()             # Voice I/O
    def _run_dashboard()         # Web dashboard
```

**Responsibilities:**
- Mode selection (repl, cli, voice, dashboard)
- Agent initialization
- Error handling
- Session management

**Usage:**
```python
from core.orchestrator import Orchestrator

config = yaml.safe_load(open('config/phase4_config.yaml'))
orchestrator = Orchestrator(config, mode='repl')
orchestrator.run()
```

---

### `core/cognition.py` - CognitionEngine

**Purpose:** LLM inference orchestration (wraps OllamaClient with context management).

**Key Classes:**
```python
class CognitionEngine:
    """LLM orchestration with context"""
    def __init__(llm_config, rag_system)
    def infer(query, context, tools) → str
    def stream_infer(query, context) → Iterator[str]
    def parse_tool_call(response) → Optional[ToolCall]
```

**Key Methods:**
- `infer()` - Single inference pass with context
- `stream_infer()` - Streaming response for dashboard
- `parse_tool_call()` - Extract tool calls from LLM output
- `refine()` - Second pass LLM with tool results

**Usage:**
```python
from core.cognition import CognitionEngine

engine = CognitionEngine(llm_config, rag_system)
response = engine.infer(
    query="List my files",
    context=["Your file system has: ..."],
    tools=[file_list_tool]
)
```

---

### `core/planner.py` - TaskPlanner

**Purpose:** Multi-step goal decomposition (Phase 2+).

**Key Classes:**
```python
class TaskPlanner:
    """Decompose complex goals into steps"""
    def __init__(llm_client)
    def plan(goal: str) → TaskPlan
    def execute_step(step: TaskStep) → TaskResult
    def synthesize_results(results: List[TaskResult]) → str
```

**Classes:**
- `TaskPlan` - Complete plan with steps
- `TaskStep` - Individual step
- `TaskResult` - Step execution result

**Usage:**
```python
planner = TaskPlanner(llm_client)
plan = planner.plan("Save my notes and upload them")
for step in plan.steps:
    result = planner.execute_step(step)
```

---

### `core/structured_logger.py` - StructuredLogger

**Purpose:** Audit logging with JSON-structured records (Phase 2+).

**Key Classes:**
```python
class StructuredLogger:
    """JSON audit log for compliance"""
    def __init__(config, session_id)
    def log(message, metadata) → None
    def log_tool_call(tool, args, result) → None
    def save_session() → str
```

**Log Format:**
```json
{
  "timestamp": "2026-04-28T15:14:32",
  "session_id": "abc123def456",
  "event_type": "tool_execution",
  "tool_name": "list_directory",
  "status": "success",
  "args": {"path": "data/"},
  "result": "[...]",
  "user": "admin"
}
```

**Usage:**
```python
logger = StructuredLogger(config, session_id="sess_001")
logger.log("query_received", {"query": "What time is it?"})
logger.log_tool_call("read_file", {"path": "notes.txt"}, "File contents...")
```

---

## Memory & RAG

### `memory/rag.py` - RAGSystem

**Purpose:** Vector-based context retrieval (Retrieval-Augmented Generation).

**Key Classes:**
```python
class RAGSystem:
    """ChromaDB integration for semantic search"""
    def __init__(config)
    def add_documents(docs: List[str], metadata) → None
    def retrieve(query: str, top_k=5) → List[str]
    def embed_query(query: str) → List[float]
    def update_collection(name: str, docs) → None
```

**Internally Uses:**
- `sentence-transformers` for embeddings (all-MiniLM-L6-v2)
- `chromadb` for persistence
- Collections per topic/domain

**Usage:**
```python
rag = RAGSystem(config)

# Add documents
rag.add_documents(["My notes...", "..."], metadata={"type": "personal"})

# Retrieve context
context = rag.retrieve("Tell me my notes", top_k=3)
# Returns top-3 most similar chunks
```

---

### `models/ollama_client.py` - OllamaClient

**Purpose:** HTTP interface to Ollama local LLM server.

**Key Classes:**
```python
class OllamaClient:
    """Ollama HTTP client"""
    def __init__(base_url, model, config)
    def infer(prompt: str) → str
    def stream_infer(prompt: str) → Iterator[str]
    def list_models() → List[str]
    def pull_model(model_name) → None
    def health() → bool
```

**Usage:**
```python
client = OllamaClient(
    base_url="http://localhost:11434",
    model="auto"
)

response = client.infer(
    prompt="Q: What is 2+2?\nA: ",
    temperature=0.7,
    context_window=2048
)
print(response)  # "4"
```

---

## Tools & Execution

### `tools/base_tools.py` - Tool System

**Purpose:** Tool definition, registration, and execution.

**Key Classes:**
```python
class Tool:
    """Base class for all tools"""
    def __init__(name, description, args_schema)
    def execute(**kwargs) → Dict[str, Any]
    def to_dict() → Dict  # For LLM context

class ToolExecutor:
    """Execute registered tools with permission checking"""
    def __init__(config)
    def register_tool(tool: Tool) → None
    def execute(tool_name, args) → Dict[str, Any]
    def get_tool_definitions() → List[Dict]
```

**Built-in Tools:**
- `ReadFileTool` - Read file contents
- `WriteFileTool` - Write/append to file
- `ListDirectoryTool` - List directory contents
- `PythonExecuteTool` - Execute Python code (sandboxed)

**Usage:**
```python
from tools.base_tools import ToolExecutor, Tool

executor = ToolExecutor(config)

# Tools auto-registered in __init__

# Execute tool
result = executor.execute(
    tool_name="list_directory",
    args={"path": "."}
)
print(result['files'])  # [...file names...]
```

**Creating Custom Tool:**
```python
class MyCustomTool(Tool):
    def execute(self, input_file: str, **kwargs):
        with open(input_file) as f:
            return {"output": f.read()}

executor.register_tool(
    MyCustomTool(
        name="read_custom",
        description="Read custom file format"
    )
)
```

---

### `tools/file_system_tools.py`

**Purpose:** File I/O operations for the agent.

**Functions:**
- `read_file(path)` - Read file contents
- `write_file(path, content)` - Write to file
- `list_directory(path)` - List files
- `delete_file(path)` - Delete file
- `search_files(pattern)` - Find files matching pattern

**Usage:**
```python
from tools.file_system_tools import read_file
content = read_file("data.txt")
```

---

### `tools/code_execution_tools.py`

**Purpose:** Safe Python code execution.

**Functions:**
- `execute_python(code)` - Execute Python with timeout
- `execute_bash(command)` - Execute shell command (Unix)

**Sandboxing:**
- Timeout: 10 seconds (configurable)
- Memory limit: 512MB
- No network access
- Restricted imports

**Usage:**
```python
from tools.code_execution_tools import execute_python
result = execute_python("print(2**32)")
# Returns: {"output": "4294967296\n", "status": "success"}
```

---

## IoT & Integration

### `iot/manager.py` - IoTManager

**Purpose:** Unified IoT orchestration (Home Assistant + Network Discovery).

**Key Classes:**
```python
class IoTManager:
    """Facade for IoT operations"""
    def __init__(config)
    def status() → Dict                    # System status
    def discover_devices(subnet) → Dict    # Find devices (MERGED)
    def list_devices(domain) → Dict        # HA entities
    def control_device(domain, service) → Dict
    def control_intent(intent, target) → Dict
```

**NEW in Phase 5:**
```python
def discover_devices(subnet, ports, max_hosts):
    """
    Run BOTH discovery paths and merge results:
    1. LocalNetworkScanner.scan() - Adapter profiles + ARP
    2. NetworkDiscovery.scan_network() - ARP + safe ports
    3. _merge_discovery_results() - Deduplicate + merge
    """
    # Returns combined results with:
    # - scanner_hosts_seen
    # - discovery_hosts_seen
    # - merged_hosts_registered
    # - arp_discovery (full NetworkDiscovery result)
```

**Usage:**
```python
from iot.manager import IoTManager

manager = IoTManager(config)

# Discover devices
result = manager.discover_devices()
print(f"Found: {result['merged_hosts_registered']} devices")

# Control device
manager.control_intent(
    intent="turn_on",
    target="bedroom_light"
)
```

---

### `iot/scanner.py` - NetworkDiscovery (NEW Phase 5)

**Purpose:** ARP-based network discovery with device classification.

**Key Classes:**
```python
class NetworkDiscovery:
    """ARP + port scanning for device discovery"""
    def __init__(db_path, timeout_ms, ports, max_workers)
    def scan_network(subnet, timeout_ms) → Dict
    def classify_device(ip, ports) → str  # router, phone, iot, pc
    def persist_scan(devices, subnet) → int  # scan_id
```

**Key Functions:**
```python
def scan_network(
    subnet=None,        # Auto-detect if None
    timeout_ms=220,     # Per-host timeout
    max_ports=20        # Top 20 safe ports
) → Dict:
    """
    Perform ARP discovery + port scanning
    
    Returns:
    {
        'ok': bool,
        'subnet': '192.168.1.0/24',
        'device_count': 31,
        'scan_id': 1,
        'devices': [
            {
                'ip': '192.168.1.1',
                'mac': 'aa:bb:cc:...',
                'vendor': 'TP-Link',
                'ports': [53, 80, 443],
                'device_type': 'router',
                'confidence': 0.95
            },
            ...
        ],
        'database': 'data/network_discovery.db'
    }
    """
```

**Device Classification:**
```
router     → Port 53 (DNS)
phone      → Port 1900 (UPnP)
iot        → Port 1883 (MQTT) or 5353 (mDNS)
pc         → SSH (22), RDP (3389), various services
printer    → Port 515 (LPR), 9100 (raw)
nas        → Port 445 (SMB), 139 (NetBIOS)
```

**Database Schema:**
```sql
-- Stored in data/network_discovery.db
CREATE TABLE scans (
    scan_id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    subnet TEXT,
    device_count INTEGER
);

CREATE TABLE devices (
    id INTEGER PRIMARY KEY,
    scan_id INTEGER,
    ip TEXT,
    mac TEXT,
    vendor TEXT,
    ports TEXT,         -- JSON
    device_type TEXT,
    hostname TEXT,
    confidence REAL,
    UNIQUE(scan_id, ip)
);
```

**Usage:**
```python
from iot.scanner import scan_network

result = scan_network(timeout_ms=120)
if result['ok']:
    print(f"Found {result['device_count']} devices")
    for device in result['devices']:
        print(f"  {device['ip']} - {device['device_type']}")
```

---

### `iot/device_registry.py` - IoTDeviceRegistry

**Purpose:** Store and query known devices.

**Key Classes:**
```python
class IoTDeviceRegistry:
    """Centralized device database"""
    def __init__(config)
    def register_network_hosts(hosts) → int  # Count registered
    def register_entities(entities) → int    # HA entities
    def get_device(ip_or_id) → Dict
    def inventory() → Dict                   # All devices
```

---

### `iot/home_assistant.py` - HomeAssistantClient

**Purpose:** REST interface to Home Assistant.

**Key Methods:**
- `health()` - Check HA is reachable
- `list_entities(domain)` - Get all HA entities
- `call_service(domain, service, data)` - Execute HA service
- `get_entity(entity_id)` - Get entity state

---

### `iot/command_translation.py` - IoTCommandTranslator

**Purpose:** Translate natural intents to HA service calls.

**Key Methods:**
- `translate(intent, target, args)` - Intent → HA call
- `reverse_lookup(domain, service)` - HA → intent

**Example:**
```
"Turn on the bedroom light"
→ Intent: "turn_on", Target: "bedroom_light"
→ HA: domain="light", service="turn_on", entity_id="light.bedroom_light"
```

---

## Voice I/O

### `voice/stt.py` - WhisperSTT

**Purpose:** Speech-to-text using OpenAI Whisper.

**Key Classes:**
```python
class WhisperSTT:
    """Whisper speech-to-text"""
    def __init__(model_size="base", language="en")
    def transcribe(audio_file: str) → str
    def transcribe_stream(audio_stream) → Iterator[str]
```

---

### `voice/tts.py` - TTSEngine

**Purpose:** Text-to-speech with multiple backends.

**Key Classes:**
```python
class TTSEngine:
    """Multi-backend TTS"""
    def __init__(engine="edge-tts", voice="en-US-AriaNeural")
    def speak(text: str) → None      # Play audio
    def synthesize(text: str) → bytes  # Return audio bytes
```

**Backends:**
- `edge-tts` - Microsoft cloud (requires internet)
- `coqui-tts` - Local model (offline)
- `pyttsx3` - System text-to-speech (basic)

---

### `voice/voice_loop.py` - VoiceLoop

**Purpose:** Real-time voice interaction loop.

**Key Classes:**
```python
class VoiceLoop:
    """Voice I/O orchestration"""
    def __init__(agent, stt, tts, config)
    def run()                    # Main voice loop
    def _listen() → str          # Get user speech
    def _process(speech) → str   # Agent inference
    def _speak(response) → None  # Output audio
```

---

### `voice/audio_utils.py` - AudioCapture

**Purpose:** Audio input/output utilities.

**Key Classes:**
```python
class AudioCapture:
    """Audio device management"""
    def __init__(device_index)
    def record(duration_sec) → bytes
    def play(audio_bytes) → None
    def list_devices() → List[str]
```

---

## Web UI & API

### `ui/dashboard_api.py` - DashboardServer

**Purpose:** FastAPI web server with real-time dashboard.

**Key Classes:**
```python
class DashboardServer:
    """FastAPI server for web UI"""
    def __init__(agent, config)
    def get_health() → Dict       # Health check
    def post_chat(request) → Dict # Chat endpoint
    def ws_connect() → WebSocket  # WebSocket for streaming
```

**API Endpoints:**
- `GET /health` - Server status
- `GET /` - Dashboard HTML
- `POST /api/chat` - Send message
- `WS /ws/stream` - Real-time updates
- `GET /api/models` - Available models
- `POST /api/models/switch` - Change model
- `GET /api/memory` - Memory inspection
- `GET /api/iot/devices` - Device list
- `POST /api/iot/control` - Control device

**Request/Response:**
```python
# POST /api/chat
request = ChatRequest(
    message="What is my network?",
    model="auto",
    temperature=0.7
)

response = {
    "ok": True,
    "response": "Found 23 devices...",
    "tools_used": ["network_discover"],
    "metadata": {...}
}
```

---

## Security & Logging

### `security/sandbox.py` - SecurityManager

**Purpose:** Permission checking and tool sandboxing.

**Key Classes:**
```python
class SecurityManager:
    """Permission enforcement"""
    def __init__(config)
    def allow_tool(tool_name, domain) → bool
    def allow_service(service_name) → bool
    def sandbox_execution(func, timeout_sec) → Any
```

**Permission Model:**
```yaml
allowed_domains:
  - light
  - climate
  - switch
allowed_services:
  light: ["turn_on", "turn_off", "set_brightness"]
```

---

### Logging Structure

```
logs/
├── phase1.log              # Main application log (rolling)
├── sessions/
│   ├── {session_id}.jsonl  # Per-session structured logs
│   └── ...
├── cognition/              # LLM inference logs
├── tts/                    # Text-to-speech logs
├── tasks/                  # Task execution logs
└── temp/                   # Temporary files
```

**Log Format:**
```
2026-04-28 15:14:32,123 - core.agent - INFO - 🚀 Processing query...
2026-04-28 15:14:33,456 - tools.base_tools - DEBUG - Executing: list_directory
2026-04-28 15:14:34,789 - core.agent - INFO - ✅ Response: Found 5 files
```

---

## Entry Points

### `main.py` - Main Entry Point

**Purpose:** CLI entry point with mode selection.

**Usage:**
```bash
python main.py [--mode {repl,cli,voice,dashboard}] [options]

Options:
  --mode {repl,cli,voice,dashboard}  Operating mode (default: repl)
  --config PATH                      Config file path
  --model MODEL_NAME                 Override LLM model
  --port PORT                       Override dashboard port
  --offline                         Offline mode
```

**Modes:**
1. `repl` - Interactive multi-turn conversation
2. `cli` - Single query command-line
3. `voice` - Voice interaction loop
4. `dashboard` - Web UI with API

---

### `startup.py` - Deployment Orchestrator

**Purpose:** Production startup sequence.

**Functions:**
- `start_ollama_if_needed()` - Start Ollama service
- `initialize_memory_db()` - Initialize ChromaDB
- `run_backend()` - Start FastAPI server
- `main()` - Full startup sequence

**Usage:**
```bash
python startup.py
```

---

### `run_smoke_tests.py` - Test Suite

**Purpose:** Validate all components work.

**Usage:**
```bash
python run_smoke_tests.py
```

**Coverage:**
- Directory structure
- Module imports
- Component instantiation
- Configuration loading
- Syntax validation

---

## Configuration Files Reference

### `config/phase1_config.yaml` - Core Settings
```yaml
ollama:
  base_url: http://localhost:11434
    model: auto
    fallback_model: qwen2.5:latest
  temperature: 0.7

memory:
  chunk_size: 512
  top_k: 3

agent:
  max_iterations: 10
  enable_tools: true
```

### `config/phase4_config.yaml` - Dashboard
```yaml
ui:
  dashboard:
    enabled: true
    host: 127.0.0.1
    port: 8000

logging:
  level: INFO
```

### `config/phase4_integration_map.yaml` - IoT
```yaml
iot:
  enabled: true
  home_assistant:
    base_url: http://homeassistant.local:8123
    token: ...
  local_network:
    timeout_ms: 220
    max_workers: 32
```

---

**Document Version:** 2.0  
**Last Updated:** 2026-04-28  
**Coverage:** All 35 Python modules across Phases 1-5
