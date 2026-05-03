# Embodied AI System - Legacy README (Archived)

> This file is preserved for historical Phase 1 context only.
>
> For current system documentation (Phase 9+), use:
> - README.md
> - GENERAL_SUMMARY_README.md
> - DOCUMENTATION_INDEX.md

# Embodied AI System - Phase 1
# Main README

```
╔══════════════════════════════════════════════════════════════╗
║          EMBODIED AI OPERATING SYSTEM - PHASE 1              ║
║              Core Intelligence (No UI, No Voice)             ║
╚══════════════════════════════════════════════════════════════╝
```

## 🎯 Phase 1 Goal

Build the **brain** of an embodied AI system:
- ✅ Local LLM (Ollama)
- ✅ Basic agent loop
- ✅ Tool system
- ✅ Memory/RAG
- ✅ CLI interface

**Output:** A CLI AI assistant that can:
- 🧠 Answer questions
- 🔧 Use tools  
- 💾 Remember context

## Phase Baseline (1-6)

For the canonical Phase 1 through Phase 6 requirements and pass criteria, use:

- `PHASE1_6_REQUIREMENTS_BASELINE.md`

If older docs conflict with phase naming/sequencing, the baseline file is the source of truth.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              EMBODIED AI AGENT (CLI)                │
└─────────────────────────────────────────────────────┘
          ▲                                    ▼
     User Input                          Response Output
          ▲                                    ▼
┌──────────────────┬───────────────┬──────────────────┐
│  User Interface  │   Core Agent  │  Tool Executor   │
│     (CLI)        │    Loop       │    (Actions)     │
└──────────────────┴───────────────┴──────────────────┘
         ▲            ▲                  ▲
         │            │                  │
    ┌────┴────┬───────┴────────┬────────┴─────┐
    ▼         ▼                ▼               ▼
┌────────┐ ┌────────┐  ┌──────────┐  ┌──────────────┐
│ RAG    │ │ Ollama │  │ Security │  │ Tools        │
│Memory  │ │ LLM    │  │ Manager  │  │ - File I/O   │
│        │ │        │  │          │  │ - Execute    │
└────────┘ └────────┘  └──────────┘  └──────────────┘
    ▼         ▼                ▼               ▼
┌────────┬────────┬───────────────────────────────────┐
│ Context │ Local  │    Permissions & Sandboxing     │
│Retrieval│ Model  │                                 │
└────────┴────────┴───────────────────────────────────┘
```

---

## ⚡ Quick Start

### 1. Prerequisites

**System Requirements:**
- Python 3.10+
- Ollama (https://ollama.ai)
- 4GB+ RAM
- 10GB+ disk space

**Install Ollama:**
```bash
# Download from https://ollama.ai
# Run Ollama server
ollama serve
```

**Download a model:**
```bash
ollama pull mistral
# or: ollama pull llama2, neural-chat, etc.
```

### 2. Install Dependencies

```bash
cd ai-ui-system

# Create virtual environment (recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 3. Run the System

**Interactive Mode (Recommended):**
```bash
python main.py --mode repl
```

**Single Query Mode:**
```bash
python main.py --mode cli
```

### 4. First Run

```
You: Hello! Can you introduce yourself?
Assistant: I'm an embodied AI assistant...

You: What tools do you have available?
Assistant: I can read files, list directories...

You: Add this information to memory: [text]
Assistant: ✅ Added to memory

You: history
[Shows last 5 messages]

You: exit
```

---

## 📁 Project Structure

```
ai-ui-system/
├── core/                          # 🧠 Agent Logic
│   ├── agent.py                   #   - Main intelligence loop
│   ├── orchestrator.py            #   - Workflow management
│   └── __init__.py
│
├── models/                        # 🤖 LLM Integration
│   ├── ollama_client.py           #   - Ollama interface
│   └── embeddings.py              #   - Coming in Phase 2
│
├── memory/                        # 💾 RAG System
│   ├── rag.py                     #   - Vector database
│   ├── embeddings.py              #   - Embedding manager
│   └── data/                      #   - ChromaDB storage
│
├── tools/                         # 🔧 Action System
│   ├── base_tools.py              #   - File I/O, execution
│   ├── coding_tools.py            #   - Coming in Phase 2
│   └── system_tools.py            #   - Coming in Phase 2
│
├── security/                      # 🔒 Sandboxing
│   ├── sandbox.py                 #   - Permissions & limits
│   └── audit.py                   #   - Logging
│
├── voice/                         # 🎤 STT/TTS (Phase 2+)
├── avatar/                        # 👤 Avatar Engine (Phase 3+)
├── iot/                           # 🏠 IoT Integration (Phase 4+)
├── ui/                            # 🎨 Web Dashboard (Phase 2+)
│
├── config/
│   └── phase1_config.yaml         # 📋 Configuration
│
├── main.py                        # ▶️ Entry Point
├── requirements.txt               # 📦 Dependencies
└── README.md                      # 📖 This file
```

---

## 🔧 Configuration

Edit `config/phase1_config.yaml` to customize:

```yaml
# Ollama settings
ollama:
  base_url: "http://localhost:11434"
  model: "mistral"           # Change model here
  temperature: 0.7           # 0=deterministic, 1=creative

# Memory settings
memory:
  chunk_size: 512            # Document chunk size
  retrieval_top_k: 3         # Context documents to retrieve

# Agent settings
agent:
  max_iterations: 10         # Max reasoning steps
  enable_tools: true
```

---

## 💡 Usage Examples

### Example 1: Simple Q&A

```
You: What is machine learning?
Assistant: [Retrieves from memory if available, 
            then answers via Ollama]
```

### Example 2: Using Tools

```
You: Read the file data.txt and summarize it
Assistant: [Uses read_file tool, then summarizes]
```

### Example 3: Adding Context

```
You: add
Text to add: My company is TechCorp, we build AI systems.
Assistant: ✅ Added to memory

You: Who are we?
Assistant: [References added context]
```

---

## 🧠 How It Works

### Agent Loop (Simplified)

```python
1. User Input
   ↓
2. Retrieve Context (RAG)
   ↓
3. Call LLM with Context (Ollama)
   ↓
4. Parse Tool Calls
   ↓
5. Execute Tools (if any)
   ↓
6. Return Response
   ↓
7. Add to History
```

### Example Interaction

```
User: "How many files are in the data folder?"

STEP 1: Agent receives query
STEP 2: RAG searches memory (no previous context)
STEP 3: Agent asks Ollama LLM
        LLM: "I should use the list_directory tool"
STEP 4: Agent parses [TOOL: list_directory] {"path": "data"}
STEP 5: Tool lists files in data/
STEP 6: Returns file list to user
STEP 7: Stores interaction in history
```

---

## 🔒 Security Features (Phase 1)

- ✅ Tool whitelisting (only allowed tools run)
- ✅ File sandboxing (no access outside working directory)
- ✅ Execution limits (timeouts)
- ⏳ Full sandboxing (Phase 2+)

**Current Allowed Tools:**
- `read_file` - Read text files
- `list_directory` - List files
- `execute_python` - Run Python code

**Blocked Tools:**
- `write_file` (can be enabled)
- `delete_file`
- `execute_system_command`

---

## 📊 Monitoring

### View Logs

```bash
tail -f logs/phase1.log
```

### Check Memory Stats

```
You: status
Assistant: [Shows system statistics]
```

### View History

```
You: history
Assistant: [Shows last 5 messages]
```

---

## 🚀 Next Steps (Phase 2+)

- [ ] **Phase 2 - Agents + Tools**
  - Tool calling improvements
  - File system assistant
  - Basic automation
  
- [ ] **Phase 3 - Avatar**
  - Unreal Engine integration
  - Visual representation
  - Animation sync
  
- [ ] **Phase 4 - IoT**
  - Home Assistant integration
  - Device control
  - Local network
  
- [ ] **Phase 5 - Advanced Intelligence**
  - Long-term memory
  - Planning agents
  - Fine-tuning dashboard

---

## 🐛 Troubleshooting

### "Cannot connect to Ollama"
```
✗ Make sure Ollama is running:
  ollama serve

✗ Check the base_url in config/phase1_config.yaml
  Should be: http://localhost:11434
```

### "Model not found"
```
✗ Install the model:
  ollama pull mistral

✗ Check available models:
  ollama list
```

### "Out of memory"
```
✗ Reduce context_length in config
✗ Use a smaller model (e.g., neural-chat instead of mistral)
✗ Reduce chunk_size for RAG
```

### "Tool execution failed"
```
✗ Check logs/phase1.log for details
✗ Ensure file path is within working directory
✗ Verify tool is in allowed_tools list
```

---

## 📚 Development

### Adding a New Tool

```python
# In tools/base_tools.py

class MyNewTool(Tool):
    def __init__(self):
        super().__init__("my_tool", "Does something useful")
    
    def execute(self, args):
        # Implementation here
        return result

# Register in ToolExecutor
self.tools['my_tool'] = MyNewTool()
```

### Adding Memory

```python
agent.add_to_memory("Important information for context")
```

### Extending Agent

```python
# In core/agent.py
# Customize process() method for specific workflows
```

---

## 📖 Documentation

- **Core Agent**: See [core/agent.py](core/agent.py) for detailed flow
- **Models**: See [models/ollama_client.py](models/ollama_client.py)
- **Memory**: See [memory/rag.py](memory/rag.py)
- **Tools**: See [tools/base_tools.py](tools/base_tools.py)
- **Security**: See [security/sandbox.py](security/sandbox.py)

---

## 🤝 Contributing

Phase 1 is complete for core foundation. Improvements welcome:

1. Fork the repository
2. Create feature branch
3. Add inline comments
4. Create README for your feature
5. Submit PR

---

## 📝 License

MIT License - See LICENSE file

---

## 🔗 Resources

- **Ollama**: https://ollama.ai
- **ChromaDB**: https://www.trychroma.com
- **Sentence Transformers**: https://huggingface.co/sentence-transformers

---

## 📧 Support

- Check [Troubleshooting](#troubleshooting) section
- Review logs in `logs/phase1.log`
- Check system status with `status` command

---

**Built with ❤️ for embodied AI**

*Phase 1 Complete: Foundation Layer Ready* ✅
