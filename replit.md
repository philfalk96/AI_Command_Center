# Nagatha AI Control Center

## Overview

A full-stack local AI control center that pairs with Ollama for locally-run AI models. Built with React + Vite frontend and Express API backend.

## Stack

- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5
- **Database**: PostgreSQL + Drizzle ORM
- **Validation**: Zod (`zod/v4`), `drizzle-zod`
- **API codegen**: Orval (from OpenAPI spec)
- **Frontend**: React + Vite (artifacts/nagatha-ai)
- **Build**: esbuild (CJS bundle)

## Architecture

### Frontend (artifacts/nagatha-ai)
- **Dashboard** `/` — System overview: Ollama status, sessions, training data, IoT devices
- **AI Chat** `/chat` — Full chat interface with session history sidebar, model selection, powered by Ollama
- **Nagatha Agent** `/nagatha` — Dedicated AI persona page with animated orb presence, voice input (Web Speech API), text-to-speech, HITL review panel
- **IoT Control** `/iot` — Home automation hub: register devices by room, send commands via HTTP/webhooks
- **Training Data** `/training` — Submit and manage training examples by category (instruction/example/context/correction/persona)
- **Connected Devices** `/devices` — Register and manage WiFi/mobile/IoT extension devices
- **Settings** `/settings` — Ollama URL, default model, Nagatha system prompt, voice settings (stored in localStorage)

### Backend (artifacts/api-server)
- `/api/ollama/*` — Proxy to local Ollama instance (status, models, chat)
- `/api/chat/*` — Chat session and message management
- `/api/training/*` — Training data CRUD with stats
- `/api/iot/*` — IoT device management and command forwarding
- `/api/devices/*` — Connected device registry

### Database Schema (lib/db/src/schema/)
- `chat_sessions` — Chat sessions with model and agent mode
- `chat_messages` — Individual messages per session
- `training_entries` — Training data (prompt/response pairs with category/status)
- `iot_devices` — Smart home/IoT devices with endpoint URLs
- `connected_devices` — WiFi/mobile extension devices

## Key Commands

- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- `pnpm --filter @workspace/api-server run dev` — run API server locally

## Ollama Integration

The backend proxies to a local Ollama instance. Default URL: `http://localhost:11434`. Configure via `OLLAMA_URL` environment variable or the Settings page (stored in localStorage on the client).

## Voice Features (Nagatha Page)

- **Voice input**: Uses `window.SpeechRecognition` / `window.webkitSpeechRecognition` browser API
- **Text-to-speech**: Uses `window.speechSynthesis` API
- Settings page allows configuring voice, speech rate, and pitch

## IoT / Home Control

Devices are registered with an HTTP endpoint URL. Commands are forwarded as POST requests with `{ command, payload }`. Device status (online/offline) is updated based on response.

## Extension / Future Integration

The Connected Devices section is designed for future extensions:
- Mobile apps can register themselves with their IP address and capabilities
- WiFi-capable devices (ESP32, Arduino, Raspberry Pi) can be registered and tracked
- The device endpoint pattern enables webhook-based command dispatch

See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details.
