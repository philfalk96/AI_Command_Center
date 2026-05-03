# Phase 4 Implementation Guide

## Goal

Deliver API + UI layer for control and visibility.

## Completed Scope

- FastAPI backend with runtime control endpoints
- Browser dashboard UI with chat + observability
- Model switching without restart
- Prompt tuning without restart
- Memory inspection from ChromaDB chunks
- Tool permission inspection/toggling
- Whisper STT microphone capture and backend transcription endpoint

## Orchestration Flow

1. User submits message in dashboard.
2. Backend sends message to EmbodiedAIAgent.process.
3. Agent retrieves RAG context (with metadata).
4. Agent runs LLM, executes tool calls, records traces.
5. API returns response + tool traces + RAG source chips.
6. UI renders markdown reply and observability badges.

## Integration Points

- Agent runtime controls:
  - set_model
  - set_prompt
  - get_memory_inspection
  - get_tool_permissions
  - set_tool_permission
- Memory layer extensions:
  - retrieve_with_metadata
  - inspect_documents
- Security layer extensions:
  - get_tool_permissions
  - set_tool_permission

## API Contract Summary

### Chat
POST /api/chat
{
  "message": "..."
}

Response includes:
- assistant
- metadata
- tool_traces
- rag_sources

### Model
GET /api/models
POST /api/models/switch

### Prompt
GET /api/prompt
PUT /api/prompt

### Memory
GET /api/memory?limit=25

### Tool Permissions
GET /api/tools/permissions
POST /api/tools/permissions

### STT
POST /api/stt/transcribe (multipart audio)

## Mapping File

See config/phase4_integration_map.yaml for module responsibilities and endpoint mapping.
