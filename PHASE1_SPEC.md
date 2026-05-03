# Phase 1 Technical Specification

## Overview

Phase 1 establishes the **foundational intelligence layer** for the Embodied AI system. This is a CLI-based assistant with:

- Local LLM inference via Ollama
- Retrieval-Augmented Generation (RAG) for context
- Tool calling system
- Basic security sandboxing
- Conversation memory

## Components

### 1. Core Agent (`core/agent.py`)

**Responsibility:** Main intelligence loop

**Flow:**
```
User Input
    ↓
Retrieve Context (RAG)
    ↓
Call LLM
    ↓
Parse Tool Calls
    ↓
Execute Tools
    ↓
Return Response
```

**Key Methods:**
- `process(user_input)` - Main entry point
- `retrieve_context(query)` - RAG retrieval
- `call_llm(prompt, context)` - LLM inference
- `parse_tool_calls(response)` - Extract [TOOL: ...] patterns
- `execute_tools(tool_calls)` - Run tools safely

**Message Format:**
```python
@dataclass
class Message:
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: datetime
    metadata: Dict[str, Any]
```

### 2. LLM Integration (`models/ollama_client.py`)

**Responsibility:** Interface with Ollama local server

**Features:**
- Connection management
- Model loading
- Text generation
- Error handling

**Configuration:**
```yaml
ollama:
  base_url: "http://localhost:11434"
    model: "auto"
    fallback_model: "qwen2.5:latest"
  temperature: 0.7
  timeout: 60
  context_length: 4096
```

**Usage:**
```python
client = OllamaClient(config)
response = client.generate(prompt)
```

### 3. Memory System (`memory/rag.py`)

**Responsibility:** Context retrieval for LLM

**Technology Stack:**
- **Vector DB:** ChromaDB (local, embedded)
- **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)

**Process:**
1. Split documents into chunks (512 tokens)
2. Generate embeddings for each chunk
3. Store in ChromaDB
4. Retrieve similar chunks for queries

**Usage:**
```python
rag = RAGSystem(config)

# Add to memory
rag.add_document("Important information", metadata={...})

# Retrieve context
docs = rag.retrieve("query", top_k=3)
```

### 4. Tool System (`tools/base_tools.py`)

**Responsibility:** AI-driven actions

**Tool Pattern:** LLM outputs `[TOOL: tool_name] args`

**Current Tools:**
- `read_file` - Read file contents
- `write_file` - Write to file (restricted)
- `list_directory` - List directory contents
- `execute_python` - Execute Python code

**Adding Tools:**
```python
class CustomTool(Tool):
    def execute(self, args: Dict) -> str:
        # Implementation
        return result

executor.register_tool(CustomTool())
```

### 5. Security (`security/sandbox.py`)

**Responsibility:** Permissions and resource limits

**Features:**
- Tool whitelisting/blacklisting
- File access restrictions
- Extension filtering
- Resource monitoring (stub for Phase 1)

**Security Model:**
```
User Request
    ↓
Security Check:
  - Tool allowed?
  - File operation safe?
  - Extension allowed?
    ↓
Execute or Deny
```

## Configuration

**Main Config:** `config/phase1_config.yaml`

Key sections:
- `ollama:` - LLM settings
- `memory:` - RAG settings
- `agent:` - Agent loop settings
- `security:` - Permission settings
- `logging:` - Log levels

## Data Flow Diagram

```
┌─────────────────┐
│   User Input    │ "What is AI?"
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│   Parse & Validate Input    │
└────────┬────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│   Retrieve Context (RAG)         │
│   ChromaDB + Embeddings          │
└────────┬─────────────────────────┘
         │
         ▼ (context retrieved or empty)
┌──────────────────────────────────┐
│   Call Ollama LLM                │
│   Input: prompt + context        │
└────────┬─────────────────────────┘
         │
         ▼ (response from LLM)
┌──────────────────────────────────┐
│   Parse Tool Calls               │
│   Look for [TOOL: ...] patterns  │
└────────┬─────────────────────────┘
         │
    ┌────┴────┐
    │          │
    ▼          ▼
Tools?       No
   │          │
   Yes        │
   │    ┌─────┘
   ▼    ▼
┌──────────────────────────────────┐
│ Check Security & Execute         │
│ • Tool allowed?                  │
│ • Safe to execute?               │
│ • Apply limits                   │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│ Return Final Response            │
│ (LLM output + tool results)      │
└────────┬─────────────────────────┘
         │
         ▼
┌─────────────────┐
│   Add to History │
│   Store Message  │
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│ User Receives Response   │
└──────────────────────────┘
```

## Conversation State Management

**History Storage:**
```python
[
    Message(role="user", content="...", timestamp=..., metadata={...}),
    Message(role="assistant", content="...", timestamp=..., metadata={...}),
    ...
]
```

**Metadata Example:**
```python
{
    "timestamp": "2024-01-15T10:30:00",
    "iterations": 1,
    "context_retrieved": True,
    "tools_called": False
}
```

## Error Handling

**Graceful Degradation:**
- LLM timeout → Return error message
- Tool execution fails → Return error, continue
- Memory unavailable → Continue without context
- Invalid tool → Log and skip

**Logging:**
- All major operations logged to `logs/phase1.log`
- Color-coded console output
- Debug metadata available

## Performance Targets (Phase 1)

- Response time: < 10 seconds (depends on Ollama)
- Memory retrieval: < 2 seconds
- Tool execution: < 5 seconds (per tool)
- Conversation history: Unlimited (in-memory)

## API Example

```python
from core.agent import EmbodiedAIAgent
import yaml

# Load config
with open('config/phase1_config.yaml') as f:
    config = yaml.safe_load(f)

# Create agent
agent = EmbodiedAIAgent(config)

# Process query
response, metadata = agent.process("Hello!")
print(response)

# Add to memory
agent.add_to_memory("Important context")

# Get history
history = agent.get_history(last_n=10)

# Get status
status = agent.get_status()
```

## Limitations (Phase 1)

- ❌ No streaming responses
- ❌ No voice I/O
- ❌ No persistence across restarts (except memory)
- ❌ Limited tool sandboxing
- ❌ Single conversation (no multi-user)
- ❌ No multi-step planning
- ❌ No long-term learning

## Planned Improvements (Phase 2+)

- ✅ Better tool calling syntax
- ✅ Tool result feedback to LLM
- ✅ Persistent conversation storage
- ✅ Web-based UI
- ✅ Voice interface
- ✅ Multi-user support
- ✅ Advanced planning

## Testing

Run basic tests:
```bash
python -c "from core.agent import EmbodiedAIAgent; print('✅ Imports work')"
```

## Deployment

**Single machine (local):**
```bash
ollama serve &
python main.py --mode repl
```

**With logging:**
```bash
python main.py --mode repl 2>&1 | tee output.log
```

---

**Technical Lead Notes:**
- All components are independently testable
- Clean separation of concerns (agent, models, memory, tools, security)
- Extensible architecture for future phases
- Comprehensive error handling and logging
