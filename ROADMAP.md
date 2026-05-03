# Roadmap — Phase 1-9 Baseline

This roadmap follows the canonical baseline in `PHASE1_6_REQUIREMENTS_BASELINE.md` (Phases 1-6) and `PHASE9_CORE_STACK.md` (Phases 7-9).

## Source Of Truth

- Phases 1-6 requirements: `PHASE1_6_REQUIREMENTS_BASELINE.md`
- Phases 7-9 (Core Stack): `PHASE9_CORE_STACK.md`
- If older docs conflict with the phase naming or sequencing, the baseline files win.

## Phase Sequence

1. Phase 1 — Core Intelligence (Foundation)
2. Phase 2 — Tooling + Action Layer
3. Phase 3 — Memory + RAG
4. Phase 4 — Planning + Orchestration
5. Phase 5 — Voice Interface
6. Phase 6 — API + UI Layer + Security + Science
7. Phase 7 — Desktop Application (PyQt6)
8. Phase 8 — Science Lab Dashboard
9. Phase 9 — Core Stack Baseline (Ollama model management)

## Tracking Checklist

### Phase 1 — Core Intelligence
- [x] Local LLM via Ollama
- [x] Prompt templates (system + user)
- [x] Short-term memory buffer
- [x] CLI interaction loop
- [x] Pass criteria validated

### Phase 2 — Tooling + Action
- [x] Tool registry and execution manager
- [x] File read/write wrappers
- [x] Script execution wrapper
- [x] Structured tool-call plans
- [x] Action logging + graceful failure handling

### Phase 3 — Memory + RAG
- [x] Vector database integration (`ChromaDB`)
- [x] Embeddings + ingestion pipeline
- [x] Memory service (`store`, `retrieve`)
- [x] Context retrieval and prompt injection
- [x] Hallucination reduction when data exists

### Phase 4 — Planning + Orchestration
- [x] Goal decomposition into steps
- [x] Sequential execution loop
- [x] Retry/failure handling
- [x] State tracking
- [x] Multi-step task reliability validation

### Phase 5 — Voice Interface
- [x] Whisper STT integration
- [x] Coqui TTS integration
- [x] Real-time audio loop
- [x] Interrupt / cancel handling
- [x] End-to-end latency validation (<5s target)

### Phase 6 — API + UI Layer + Security + Science
- [x] FastAPI backend endpoints (`/chat`, `/tools`, `/memory`)
- [x] Web dashboard (chat, logs, settings)
- [x] Real-time updates (WebSocket)
- [x] Live settings controls
- [x] CLI-independence validation
- [x] Approval queue for sensitive tool operations
- [x] Tool sandboxing with resource limits
- [x] Full audit logging
- [x] `SimulationEnvironment` — iterative hypothesis testing
- [x] `ScientificLiteratureSystem` — persistent vector search
- [x] `PhysicsConstrainedRegressor` — hybrid physics/neural model
- [x] `ExperimentTracker` — reproducible run logging

### Phase 7 — Desktop Application
- [x] Standalone `PyQt6` desktop app (`desktop_entry.py`)
- [x] Reskinned UI (gradients, neon status chips)
- [x] `DesktopVoiceController` synchronized STT/TTS state machine
- [x] Stop Voice button + `Esc` shortcut
- [x] `DiagnosticsPanel` tab
- [x] Desktop + Start Menu shortcut installer

### Phase 8 — Science Lab Dashboard
- [x] Science Lab nav view in web dashboard
- [x] `/api/science/*` REST endpoints (simulate, literature, hybrid, experiments)
- [x] Experiment config YAMLs under `config/experiments/`
- [x] `matplotlib` plotting with graceful degradation

### Phase 9 — Core Stack Baseline
- [x] Ollama model stack reset (8 models installed, 4 removed)
- [x] `ModelSelector` with `math` task category
- [x] Per-task routing in `config/phase4_config.yaml`
- [x] `scripts/reset_ollama_models2.ps1` for repeatable resets

## Notes

- This file intentionally focuses on requirement capture and acceptance tracking.
- Implementation detail docs can evolve per phase, but phase goals and pass criteria must remain aligned to the baseline.
- All phases 1-9 are complete as of April 2026 (Phase 9 — Core Stack Baseline).
