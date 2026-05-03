# Phase 9 — Core Stack Baseline

**Date:** April 29, 2026  
**Status:** Complete ✅  
**Supersedes:** `PHASE1_6_REQUIREMENTS_BASELINE.md` (extends it for Phases 7-9)

---

## Overview

Phase 9 establishes the canonical Ollama model stack and wires automatic task-routing into
the model selector. It also documents the completed Desktop App (Phase 7) and Science Lab
Dashboard (Phase 8) that preceded it.

---

## Phase 7 — Desktop Application

### Goal
Run the AI system as a standalone desktop window without a browser or terminal.

### Key Adds
- `PyQt6` desktop application (`ui/desktop_app.py`, entry via `desktop_entry.py`)
- Reskinned UI: gradients, neon status chips, card-based layout
- `DesktopVoiceController` (`ui/desktop/voice_controller.py`) — full STT/TTS state machine
- Stop Voice button + `Esc` keyboard shortcut (`QShortcut`)
- `DiagnosticsPanel` tab (`ui/desktop/widgets/diagnostics_panel.py`) — service health at launch
- Desktop + Start Menu shortcut installer (`scripts/install-shortcut.ps1`)

### Phase Pass Criteria
- App launches without terminal
- Voice turns can be cancelled mid-stream
- Diagnostics panel shows service health on open
- Shortcut installers work on Windows

---

## Phase 8 — Science Lab Dashboard

### Goal
Provide a research environment for hypothesis simulation, literature search, and hybrid
physics/neural model training, fully accessible from the web dashboard.

### Key Adds
- `science/simulation.py` — `SimulationEnvironment` with iterative hypothesis testing
- `science/literature.py` — `ScientificLiteratureSystem` with persistent `ChromaDB` storage
- `science/hybrid_model.py` — `PhysicsConstrainedRegressor` + `HybridModelTrainer`
- `science/experiment_tracker.py` — reproducible run logging (JSONL index + per-run JSON)
- Science Lab nav view in `ui/dashboard.html`
- `/api/science/*` REST endpoints in `ui/dashboard_api.py`:
  - `POST /api/science/simulate/run`
  - `POST /api/science/simulate/rerun-ai`
  - `POST /api/science/literature/ingest-text`
  - `POST /api/science/literature/query`
  - `POST /api/science/literature/summarize`
  - `POST /api/science/literature/gaps`
  - `POST /api/science/hybrid/train`
  - `GET  /api/science/status`
  - `GET  /api/science/experiments`
- Experiment config YAMLs under `config/experiments/`:
  - `simulation.yaml`
  - `literature.yaml`
  - `hybrid_model.yaml`

### Phase Pass Criteria
- All 5 core science endpoint checks pass (status, simulate/run, lit/ingest, lit/summarize, lit/gaps)
- Chroma vectors persist across restarts
- Experiment runs logged with reproducible metadata

---

## Phase 9 — Core Stack Baseline

### Goal
Lock the Ollama model stack to a minimum practical set of production models and route each
task type automatically to the best available model.

### Minimum Practical Stack

| Model | Tag | Role | Size |
|-------|-----|------|------|
| `qwen2.5` | `latest` | Primary brain (general chat, tools) | ~4.7 GB |
| `deepseek-coder` | `latest` | Code execution | ~776 MB |
| `mistral` | `latest` | Speed / general / creative | ~4.4 GB |
| `deepseek-r1` | `latest` | Math + deep reasoning | ~5.2 GB |
| `llava` | `latest` | Vision (multimodal) | ~4.7 GB |

**Total Ollama stack:** ~19.8 GB

**Note:** Runtime embeddings use local Sentence Transformers (`all-MiniLM-L6-v2`), and voice STT uses Whisper `base`; neither is an Ollama model.

### Model Routing (Auto Mode)

When `ollama.model: "auto"` in config, `models/selector.py` routes by task type:

| Task Type | Routed To | Trigger Keywords (sample) |
|-----------|-----------|--------------------------|
| `code` | `deepseek-coder:latest` | `code`, `script`, `function`, `debug`, `sql` |
| `math` | `deepseek-r1:latest` | `calculate`, `integral`, `equation`, `proof`, `matrix` |
| `reasoning` | `deepseek-r1:latest` | `analyze`, `compare`, `evaluate`, `logic`, `deduce` |
| `creative` | `mistral:latest` | `story`, `poem`, `essay`, `brainstorm` |
| `tools` | `qwen2.5:latest` | `search`, `find file`, `iot`, `device`, `control` |
| `chat` | `qwen2.5:latest` | (default fallback) |
| `vision` | `llava:latest` | (explicit config override) |

Config override in `config/phase4_config.yaml`:

```yaml
model_routing:
  code: "deepseek-coder:latest"
  reasoning: "deepseek-r1:latest"
  math: "deepseek-r1:latest"
  chat: "qwen2.5:latest"
  creative: "mistral:latest"
  vision: "llava:latest"
```

### Repeatable Stack Reset

```powershell
# Pull all target models and remove any that are not in the stack:
powershell -ExecutionPolicy Bypass -File scripts/reset_ollama_models2.ps1
```

### Key Files Changed

| File | Change |
|------|--------|
| `models/selector.py` | Added `math` task category; rewrote `_MODEL_PROFILES` for new stack; embedding/vision profiles added |
| `config/phase4_config.yaml` | Updated `model_routing`; fallback changed from `mistral` to `qwen2.5:latest` |
| `scripts/reset_ollama_models2.ps1` | New — pulls target models, removes off-stack models |

### Phase Pass Criteria
- `ollama list` includes the 5 routed generation models used by the app
- `models/selector.py` routes `code` task to `deepseek-coder`, `math` to `deepseek-r1`
- `config/phase4_config.yaml` `model_routing` matches table above
- `scripts/reset_ollama_models2.ps1` runs cleanly and produces correct final stack

---

## Alignment Note

- Phases 1-6 canonical baseline: `PHASE1_6_REQUIREMENTS_BASELINE.md`
- Phases 7-9 canonical baseline: this file (`PHASE9_CORE_STACK.md`)
- If docs conflict, these baseline files take precedence.
