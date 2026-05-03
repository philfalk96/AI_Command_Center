# Getting Started with Embodied AI System (Phase 9 — Core Stack)

> **NEW in Phase 9:** Locked Ollama model stack, `ModelSelector` with math routing, Science Lab, PyQt6 Desktop App.

## Before You Start

**What you need:**
- [ ] Ollama installed and running (`ollama serve`)
- [ ] Python 3.10 or newer
- [ ] 4 GB+ RAM available (8 GB+ recommended for full features)
- [ ] 32 GB+ free disk space (full model stack ~26 GB)
- [ ] Internet connection (for first-time setup only; runs offline after)

---

## Quick Start (5 Minutes)

### Option A: Fastest Setup
```powershell
# Windows
.\quickstart.bat
```
```bash
# macOS/Linux
./quickstart.sh
```

Then start using:
```bash
python main.py --mode repl
```

### Option B: Manual Setup (Recommended for Developers)

**1. Install Ollama** (https://ollama.ai)

**Create virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Install dependencies:**
```bash
cd ai-ui-system
pip install -r requirements.txt
```

**Verify installation:**
```bash
python -c "import ollama, chromadb, sentence_transformers; print('✅ All dependencies installed')"
```

---

## Step 3: Run the System

**Start in REPL mode (interactive):**
```bash
python main.py --mode repl
```

**Or single-query mode:**
```bash
python main.py --mode cli
```

---

## Step 4: First Interaction

```
You: Hello, what can you do?
Assistant: I'm an Embodied AI assistant built with Ollama and RAG...

You: List my abilities
Assistant: [Lists available tools and capabilities]

You: Can you read a file?
Assistant: Yes, I can read files in your working directory...

You: help
[Shows available commands]
```

---

---

## 📚 Documentation Quick Links

For more information, see:

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Complete feature overview |
| [INSTALLATION.md](INSTALLATION.md) | Full setup & configuration guide |
| [ARCHITECTURE_AND_FLOW.md](ARCHITECTURE_AND_FLOW.md) | Technical architecture & flow diagrams |
| [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md) | Complete module reference |
| [PHASE9_CORE_STACK.md](PHASE9_CORE_STACK.md) | Phase 7-9 details (desktop, science, model stack) |
| [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) | For developers extending the system |

---

## Operating Modes

---

## Customization

**Change the model:**
1. Edit `config/phase1_config.yaml`
2. Change `ollama: model: "auto"` to a pinned model if you want to disable routing, or update `model_routing`
3. Download the model: `ollama pull [model_name]`

**Popular models:**
- `qwen2.5:latest` - Default fallback for chat and tool-use
- `deepseek-coder:latest` - Best for code tasks
- `deepseek-r1:latest` - Best for reasoning and math
- `mistral:latest` - Fast creative/general fallback

**Change temperature (creativity):**
1. Edit `config/phase1_config.yaml`
2. `temperature: 0.5` = Focused
3. `temperature: 1.0` = Creative

---

## Troubleshooting

### Issue: "Cannot connect to Ollama"

**Solution:**
1. Make sure Ollama is running: `ollama serve`
2. Check base_url in config: `http://localhost:11434`
3. Try: `curl http://localhost:11434/api/tags`

### Issue: "Model not found"

**Solution:**
```bash
ollama pull qwen2.5
# Wait for download to complete (~5-10 minutes)
```

### Issue: System runs very slowly

**Solutions:**
1. Reduce `temperature` in config
2. Pin a lighter installed model instead of `auto`
3. Close other apps (reduce RAM pressure)
4. Reduce `chunk_size` in memory config

### Issue: Memory error ("out of VRAM")

**Solutions:**
1. Reduce `context_length` in config
2. Use smaller model
3. Reduce `num_predict` in config

---

## Next Steps

1. **Explore tools:**
   - Try `read_file` to read text files
   - Try `list_directory` to see files
   - Try `execute_python` to run code

2. **Add context to memory:**
   - Use `add` command to store important information
   - Ask questions that reference added context
   - Watch how RAG improves answers

3. **Review logs:**
   - Check `logs/phase1.log` for detailed operation info
   - Useful for debugging issues

4. **Customize configuration:**
   - Edit `config/phase1_config.yaml`
   - Adjust model, temperature, timeouts
   - Enable/disable tools

---

## Tips for Best Results

✅ **DO:**
- Use specific, clear questions
- Reference previous context
- Add relevant information to memory
- Monitor logs for errors
- Test tools individually first

❌ **DON'T:**
- Ask questions outside of English
- Give extremely long prompts (yet)
- Run too many tools in one query
- Expect real-time streaming (Phase 2)
- Run without Ollama server

---

## System Architecture (Simplified)

```
Your Question
     ↓
Search Memory
     ↓
Ask Ollama (local LLM)
     ↓
Parse Response for Tools
     ↓
Run Tools (if any)
     ↓
Your Answer
```

No data leaves your computer! Everything runs locally.

---

## Example Session

```bash
$ python main.py --mode repl

You: Add this to memory: I work in Python development
Assistant: ✅ Added to memory

You: What do I do?
Assistant: Based on your memory, you work in Python development. 
          How can I help with your Python work?

You: Can you help me write a script?
Assistant: Absolutely! I can help you write Python scripts.
          [More details...]

You: history
Recent conversation:
USER: Add this to memory...
ASSISTANT: ✅ Added to memory...
USER: What do I do?...
ASSISTANT: Based on your memory...

You: exit
Goodbye!
```

---

## Getting Help

1. **Check logs:** `tail -f logs/phase1.log`
2. **Enable debug:** Edit config, set `logging.level: DEBUG`
3. **Check Ollama:** `ollama list`, `ollama show [model]`
4. **Review code:** Comments in source files explain each component

---

## Performance Expectations

| Operation | Time |
|-----------|------|
| Connection to Ollama | < 1 second |
| Memory retrieval | 1-2 seconds |
| LLM response | 3-10 seconds (depends on model and prompt) |
| Tool execution | 1-5 seconds (depends on tool) |

Total response time: 5-20 seconds (typical)

---

## Data Privacy

✅ **Private:**
- All data stays on your machine
- No cloud calls
- No data collection
- No telemetry

---

## Next Phase

After mastering Phase 1:
- Phase 2: Add web UI and more tools
- Phase 3: Voice interface
- Phase 4: Home automation
- Phase 5: Advanced planning

---

**Ready? Run:** `python main.py --mode repl`
