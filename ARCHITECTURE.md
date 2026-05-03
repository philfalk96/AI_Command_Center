# System Integration & Orchestration Map

> **Phase 9+ Runtime Architecture** | Updated April 30, 2026
>
> Canonical architecture references:
> - `ARCHITECTURE_AND_FLOW.md` (detailed deep-dive + workflow diagrams)
> - `GENERAL_SUMMARY_README.md` (full-picture executive summary)

## Architecture Layers

```
┌─────────────────────────────────────────┐
│         User Interface Layer             │
│  (CLI in Phase 1, Web/Voice in Phase 2+) │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      Orchestration Layer                │
│  (core/orchestrator.py)                 │
│  - Workflow coordination                │
│  - Cross-layer communication            │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────┬──────────────┐
    ▼            ▼            ▼              ▼
┌────────┐ ┌───────┐ ┌──────────┐ ┌──────────┐
│  Core  │ │Memory │ │  Tools   │ │Security  │
│ Agent  │ │ (RAG) │ │(Executor)│ │ Manager  │
└────┬───┘ └───┬───┘ └────┬─────┘ └────┬─────┘
     │         │          │            │
     └─────────┼──────────┼────────────┘
               │          │
    ┌──────────▼──────────▼─────────┐
    │   Models Layer               │
    │  (LLM Interface - Ollama)    │
    └──────────┬────────────────────┘
               │
    ┌──────────▼────────────────────┐
    │   Infrastructure             │
    │  (Local Ollama Server)       │
    └─────────────────────────────┘
```

## 📊 Component Interactions

### 1. Core Agent ↔ Memory (RAG)

```python
# Flow
agent.process(user_input)
  ├─ context = rag_system.retrieve(user_input)
  │   └─ Returns: [chunk1, chunk2, chunk3]
  └─ Returns: response with context

# Data Flow
User Query → Embedding → Similarity Search → Retrieved Chunks
```

### 2. Core Agent ↔ LLM (Ollama)

```python
# Flow
response = llm_client.generate(prompt_with_context)
  └─ Ollama responds with text

# Data Flow
Prompt (text) → Ollama Process → Response (text)
```

### 3. Core Agent ↔ Tools (ToolExecutor)

```python
# Flow
tool_calls = agent.parse_tool_calls(llm_response)
tool_results = executor.execute(tool_calls)
final_response = combine(llm_response, tool_results)

# Example Tool Flow
[TOOL: read_file] {"path": "data.txt"}
  ↓
Tool Executor receives call
  ↓
Security check: allowed?
  ↓
Execute ReadFileTool
  ↓
Return file content
```

### 4. Agent ↔ Security Manager

```python
# Flow
for tool in tool_calls:
    if security_manager.is_tool_allowed(tool.name):
        execute_tool(tool)
    else:
        deny_tool(tool)

# Security Checks
- Tool in whitelist?
- File operation safe?
- Resource within limits?
```

### 5. Memory (RAG) ↔ Embeddings

```python
# Flow
rag_system.add_document(text)
  ├─ embedding_model.encode(chunk)
  │   └─ Returns: vector
  ├─ chromadb.add(id, vector, text)
  └─ Stored

rag_system.retrieve(query)
  ├─ embedding_model.encode(query)
  ├─ chromadb.query(query_vector)
  └─ Returns: similar documents
```

## 🔄 Message Flow Example

```
┌──────────────────────────────────────────────────────────┐
│ User: "How many files in the data folder?"              │
└────────────────┬─────────────────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │   REPL (CLI)        │
        │  Accepts input      │
        └────────┬────────────┘
                 │
                 ▼
        ┌─────────────────────────────────────┐
        │  Orchestrator                       │
        │  process_query(user_input)          │
        └────────┬────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────────────────────┐
        │  Agent.process()                    │
        │  1. Store in history                │
        │  2. Retrieve context (RAG)          │
        └────────┬────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────────────────────┐
        │  RAG System                         │
        │  1. Encode query to vector          │
        │  2. Search ChromaDB                 │
        │  3. Return similar docs (if any)    │
        └────────┬────────────────────────────┘
                 │ (no previous context)
                 ▼
        ┌─────────────────────────────────────┐
        │  Agent continues                    │
        │  call_llm(user_input, context="")   │
        └────────┬────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────────────────────┐
        │  Ollama Client                      │
        │  POST /api/generate                 │
        │  Prompt: "How many files..."        │
        │  LLM thinks: "Use list_directory"   │
        └────────┬────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────────────────────┐
        │  Agent parses response              │
        │  Finds: [TOOL: list_directory]      │
        │         {"path": "data"}            │
        └────────┬────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────────────────────┐
        │  Security Manager check             │
        │  is_tool_allowed("list_directory")? │
        │  YES ✅                              │
        └────────┬────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────────────────────┐
        │  Tool Executor                      │
        │  execute("list_directory",          │
        │          {"path": "data"})          │
        └────────┬────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────────────────────┐
        │  ListDirectoryTool                  │
        │  Reads os.listdir("data")           │
        │  Returns: "file1.txt\nfile2.csv..." │
        └────────┬────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────────────────────┐
        │  Agent combines                     │
        │  LLM output +                       │
        │  Tool results +                     │
        │  Generates final response           │
        └────────┬────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────────────────────┐
        │  Store in history                   │
        │  Add metadata                       │
        └────────┬────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────────────────────┐
        │  Return to User                     │
        │  "There are 5 files in data:"       │
        │  [Lists files]                      │
        └─────────────────────────────────────┘
```

## 🔌 Integration Points

### Input Points
- **CLI:** `main.py` → `Orchestrator.process_query()`
- **Phase 2 Web:** API endpoint → `Orchestrator.process_query()`
- **Phase 3 Voice:** Voice input → `Orchestrator.process_query()`

### Output Points
- **CLI:** Print to console
- **Phase 2 Web:** JSON response
- **Phase 3 Avatar:** Text + animation data
- **Phase 4 IoT:** Commands to devices

### Tool Extension Points
```python
# Add new tool to core/agent.py
executor.register_tool(MyNewTool())

# Tool becomes immediately available
# LLM can call it with [TOOL: my_tool] args
```

### Memory Extension Points
```python
# Add domain-specific knowledge
agent.add_to_memory("AI system notes about domain X")

# Automatically used in context retrieval
# Improves relevant results
```

## 📈 Data Persistence

### Phase 1 (Current)
- **In-Memory:** Conversation history (lost on exit)
- **Persistent:** ChromaDB embeddings (survives restarts)

### Phase 2+
- **Database:** PostgreSQL for conversations
- **Cache:** Redis for frequently used context
- **Archive:** Compression for old conversations

## 🔒 Security Checkpoint

Every tool execution passes through:
1. **Tool Whitelist** - Is this tool allowed?
2. **File Check** - Is this file accessible?
3. **Resource Check** - Are we within limits?
4. **Audit Log** - Log for security review

## 📡 API Examples

### Direct Agent Usage
```python
from core.agent import EmbodiedAIAgent

config = load_config()
agent = EmbodiedAIAgent(config)
response, metadata = agent.process("Your query")
```

### Via Orchestrator
```python
from core.orchestrator import Orchestrator

config = load_config()
orchestrator = Orchestrator(config)
response = orchestrator.process_query("Your query")
```

### Advanced Workflow
```python
# Start complex workflow
orchestrator.start_workflow("analyze_logs", params={...})

# Get status
status = orchestrator.get_system_status()

# End workflow
result = orchestrator.end_workflow("analyze_logs", result={...})
```

## 🎯 Component Responsibilities

| Component | Input | Output | Side Effects |
|-----------|-------|--------|--------------|
| Agent | User query | Response | Stores in history |
| RAG | Query | Context docs | None |
| Ollama | Prompt | Text | Network I/O |
| Tools | Args | Result | File I/O, Execution |
| Security | Tool name | Allow/Deny | Audit log |
| Orchestrator | User input | Response | Manages workflows |

## 🚀 Initialization Order

```
1. main.py
2. Load config
3. Create Orchestrator
4. Create EmbodiedAIAgent
5. Initialize LLM client (test Ollama connection)
6. Initialize RAG system (load embedding model, connect to ChromaDB)
7. Initialize Tool executor (register tools)
8. Initialize Security manager
9. Ready for user input
```

## 📋 Extension Framework

### Adding a New Component

```
1. Create folder in ai-ui-system/
2. Add __init__.py with exports
3. Implement component class
4. Add to Orchestrator
5. Add configuration to phase1_config.yaml
6. Update this map
7. Document in README
```

---

**Last Updated:** Phase 1 Foundation
**Status:** ✅ Complete
**Next:** Phase 2 - Web UI & Advanced Tools
