# Phase 1-9 Requirements Baseline

This document is the canonical requirements baseline for Phases 1 through 6.
Phases 7-9 are captured in `PHASE9_CORE_STACK.md`.
It supersedes older phase naming in legacy docs when conflicts exist.

## Phase 1 - Core Intelligence (Foundation)

### Goal
Create a reliable AI brain that can:
- Understand requests
- Respond coherently
- Maintain short-term context

### Key Adds
- Local LLM via Ollama
- Prompt templates (system + user roles)
- Basic conversation memory (buffer)
- CLI interface (no UI yet)
### What You Build
- Agent loop (input -> think -> respond)
- LLM wrapper (API calls to Ollama)
- Simple memory store (last N messages)

### Output (What success looks like)
You: Explain recursion simply
AI: Recursion is when a function calls itself...

### Phase Pass Criteria
- Stable responses
- No crashes
- Maintains context across 3-5 turns

## Phase 2 - Tooling + Action Layer

### Goal
Turn AI into something that can do things, not just talk.

### Key Adds
- Tool registry (functions AI can call)
- File system access
- Code execution tool
- Structured tool calling format (JSON plans)
### What You Build
- Tool manager (register, execute)
- Safe wrappers for:
  - File read/write
  - Script execution
- Action logging system

### Output
You: Create a Python script that renames files by date

AI:
1. Creates script
2. Saves to disk
3. Explains how to run it

### Phase Pass Criteria
- AI selects correct tools automatically
- Tool outputs are accurate
- Failures are handled gracefully

## Phase 3 - Memory + RAG

### Goal
Give AI long-term memory and knowledge grounding.

### Key Adds
- Vector database (for example `ChromaDB`)
- Embedding model
- Document ingestion pipeline
- Context retrieval logic

### What You Build
Memory service:
- `store()`
- `retrieve()`

Plus:
- File/document loader
- Context injection into prompts

### Output
You: What did I say about my project last week?

AI: You mentioned building a drone navigation system...

### Phase Pass Criteria
- Retrieves relevant past data
- Improves answer accuracy
- Avoids hallucination when data exists

## Phase 4 - Planning + Orchestration

### Goal
Make AI think in steps, not single responses.

### Key Adds
- Task decomposition
- Step-by-step planning
- Execution loop with feedback
- Retry/failure handling

### What You Build
Planner module:
- Breaks goals into steps

Execution engine:
- Runs steps sequentially

Plus:
- State tracker

### Output
You: Help me build a website

AI:
Step 1: Choose framework
Step 2: Create structure
Step 3: Write code
...

### Phase Pass Criteria
- Multi-step tasks complete successfully
- Logical sequencing of actions
- Minimal manual correction needed

## Phase 5 - Voice Interface

### Goal
Enable natural spoken interaction.

### Key Adds
- Speech-to-text via Whisper
- Text-to-speech via Coqui TTS
- Real-time audio loop

### What You Build
- Audio input handler
- Transcription pipeline
- Audio output playback
- Interrupt handling (optional)

### Output
User speaks -> AI responds verbally

### Phase Pass Criteria
- Accurate transcription
- Natural-sounding speech
- Low latency (<5 seconds total)

## Phase 6 — API + UI Layer

### Goal
Provide visibility and control.

### Key Adds
- Backend API (`FastAPI`)
- Web dashboard
- WebSocket support (real-time updates)

### What You Build
Endpoints:
- `/chat`
- `/tools`
- `/memory`

UI panels:
- Chat window
- Logs
- Settings

### Output
Browser-based control center

### Phase Pass Criteria
- You can control system without CLI
- View logs and memory
- Change settings live

## Alignment Note

Some existing files describe earlier alternative phase labels (for example IoT/security grouped under Phase 5/6 in prior iterations).
Use this baseline as the source of truth for Phases 1-6.
Phases 7-9 (Desktop App, Science Lab, Core Stack) are documented in `PHASE9_CORE_STACK.md`.
