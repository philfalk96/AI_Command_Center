# Development & Deployment Guide

## 📝 Inline Comment Standards

All code should follow these comment patterns:

### Module-Level Comments
```python
"""
Module Name - Brief Description
=================================

Longer description explaining purpose, functionality,
and relationships to other components.
"""
```

### Function Comments
```python
def process(self, user_input: str) -> Tuple[str, Dict]:
    """
    Process user input through the agent loop.
    
    This function:
    1. Retrieves context from memory
    2. Calls the LLM
    3. Parses tool calls
    4. Returns response
    
    Args:
        user_input: User's query or command
        
    Returns:
        Tuple of (response_text, metadata_dict)
        
    Raises:
        RuntimeError: If LLM connection fails
    """
```

### Inline Comments
```python
# These are action comments (not "what" but "why")
# BAD: increment counter
# GOOD: increment counter to track iterations

# TODO: Add async support for tool execution
# FIXME: Handle edge case where context is empty
# NOTE: This matches Ollama API v2.0 spec
# HACK: Temporary workaround for ChromaDB bug #123
```

## 📚 Documentation Workflow Standards

When changing runtime behavior, update docs in the same pull request:

1. Update `README.md` for user-visible behavior.
2. Update `GENERAL_SUMMARY_README.md` for full-picture architecture status.
3. Update `ARCHITECTURE_AND_FLOW.md` when execution flow changes.
4. Update `CODE_DOCUMENTATION.md` when module APIs or contracts change.
5. Update `DOCUMENTATION_INDEX.md` and `DOCUMENTATION_SUMMARY.md` dates/status.

### Diagram Rules

- Keep at least one Mermaid flowchart for orchestration path.
- Keep one Mermaid sequence diagram for model/tool fallback behavior.
- Keep ASCII diagrams only as supplemental references.
- Diagram updates must reflect actual class/module names in source.

## 🧪 Testing Strategy

### Phase 1 Manual Testing

```bash
# Test 1: Ollama Connection
python -c "from models.ollama_client import OllamaClient; \
           c = OllamaClient({'base_url': 'http://localhost:11434', 'model': 'auto', 'fallback_model': 'qwen2.5:latest'}); \
           print('✅ Connected')"

# Test 2: RAG System
python -c "from memory.rag import RAGSystem; \
           r = RAGSystem({'db_type': 'chroma', 'db_path': './data/test_db'}); \
           r.add_document('test'); \
           docs = r.retrieve('test'); \
           print(f'✅ Retrieved {len(docs)} docs')"

# Test 3: Tool Execution
python -c "from tools.base_tools import ToolExecutor; \
           t = ToolExecutor({}); \
           result = t.execute('list_directory', {'path': '.'}); \
           print('✅ Tools working')"

# Test 4: Full Agent Loop
python -c "from core.agent import EmbodiedAIAgent; \
           import yaml; \
           with open('config/phase1_config.yaml') as f: \
               config = yaml.safe_load(f); \
           agent = EmbodiedAIAgent(config); \
           response, _ = agent.process('Hello'); \
           print('✅ Agent working')"
```

### Future: Automated Tests (Phase 2)

```bash
pytest tests/
pytest tests/ --cov=core,models,memory,tools,security
```

## 🚀 Deployment Scenarios

### Scenario 1: Local Development

```bash
# In development directory
ollama serve &
python main.py --mode repl
```

### Scenario 2: Headless Server (SSH)

```bash
# On remote server
nohup ollama serve > ollama.log 2>&1 &
nohup python main.py --mode repl > agent.log 2>&1 &

# Check status
tail -f agent.log
```

### Scenario 3: Docker (Future)

```dockerfile
FROM python:3.10

# Install dependencies
RUN apt-get update && apt-get install -y ollama

# Copy code
COPY ai-ui-system /app

# Setup Python
WORKDIR /app
RUN pip install -r requirements.txt

# Run
CMD ["python", "main.py", "--mode", "repl"]
```

### Scenario 4: Multiple Users (Phase 2)

```
Web Server (FastAPI)
├─ API Endpoint /api/chat
├─ User 1 Session
├─ User 2 Session
└─ Shared Resources (Ollama, ChromaDB)
```

## 📚 Documentation Structure

```
ai-ui-system/
├── README.md                      # Main overview
├── GETTING_STARTED.md            # Setup guide
├── PHASE1_SPEC.md                # Technical specification
├── ARCHITECTURE.md               # This file
├── DEVELOPMENT_GUIDE.md          # Dev guidelines
└── [Phase files]
    ├── PHASE2_PLAN.md
    ├── PHASE3_PLAN.md
    ...
```

## 🔄 CI/CD Pipeline (Future)

```yaml
# .github/workflows/test.yml (when we move to Git)
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest
      - run: python -m pylint core/ models/ memory/ tools/ security/
      - run: python -m mypy core/ models/ memory/ tools/ security/
```

## 🔧 Configuration Management

### Environment Variables (Future)

```bash
# .env file
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=auto
OLLAMA_FALLBACK_MODEL=qwen2.5:latest
CHROMA_DB_PATH=/var/lib/ai-system/chroma
LOG_LEVEL=INFO
MAX_CONTEXT_LENGTH=4096
```

### Configuration Hierarchy

```
1. Default (in code)
2. config/phase1_config.yaml
3. Environment variables
4. Command-line args

# Example precedence
python main.py --config custom.yaml  # Uses custom.yaml
```

## 🐛 Debugging

### Enable Debug Logging

```bash
# Edit config/phase1_config.yaml
logging:
  level: "DEBUG"

python main.py --mode repl
# More verbose output in logs/phase1.log
```

### Use Interactive Debugger

```python
# In any file, add:
import pdb; pdb.set_trace()

# Then run and interact:
python main.py --mode cli
(Pdb) n  # next
(Pdb) s  # step
(Pdb) c  # continue
(Pdb) p variable  # print variable
```

### Monitor Ollama

```bash
# In separate terminal
watch -n 1 'curl http://localhost:11434/api/tags'

# Monitor ChromaDB
python -c "from memory.rag import RAGSystem; \
           r = RAGSystem({}); \
           print(r.get_memory_stats())"
```

## 📊 Monitoring & Logging

### Log Levels

```
DEBUG   - Detailed diagnostic info (development only)
INFO    - Informational messages (normal operation)
WARNING - Warning messages (potential issues)
ERROR   - Error messages (something failed)
CRITICAL- Critical errors (system failing)
```

### Log Format

```
2024-01-15 10:30:45,123 - core.agent - INFO - ✅ Ollama client initialized
                          ^^^^^^^^^^   ^^^^   ^^^^^^ Message
                          Module name  Level  Content
```

## 🎯 Code Quality Standards

### Formatting
- Use Black: `pip install black`
- Format: `black core/ models/ memory/ tools/ security/`

### Linting
- Use Pylint: `pip install pylint`
- Check: `pylint core/`

### Type Hints
```python
def process(self, user_input: str) -> Tuple[str, Dict[str, Any]]:
    # All functions should have type hints
    pass
```

### Naming Conventions
```python
# Classes: PascalCase
class EmbodiedAIAgent:
    pass

# Functions/Methods: snake_case
def process_input(self):
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Private: _leading_underscore
def _internal_helper(self):
    pass
```

## 🔐 Security Checklist

- [ ] All file operations checked for path traversal
- [ ] Tool execution limited to whitelist
- [ ] Resource limits enforced
- [ ] User input sanitized
- [ ] No credentials in code
- [ ] Audit logging enabled
- [ ] Security updates applied regularly

## 📦 Version Management

### Semantic Versioning

```
0.1.0 = Phase 1 (foundation)
0.2.0 = Phase 2 (agents + tools)
0.3.0 = Phase 3 (avatar)
0.4.0 = Phase 4 (IoT)
0.5.0 = Phase 5 (advanced intelligence)
1.0.0 = Production ready
```

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version number bumped
- [ ] Logs clear
- [ ] No debug code left

## 🤝 Contributing

### Branch Naming
```
feature/description          - New feature
bugfix/description          - Bug fix
docs/description            - Documentation
experiment/description      - Experimental
```

### Commit Messages
```
[TYPE] Brief description

Longer explanation if needed.

- Bullet points for changes
- One per line
```

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation

## Testing
How was this tested?

## Screenshots (if applicable)
```

---

**Remember:** Comment your "why", not your "what". Code should be self-explanatory; comments explain the reasoning.
