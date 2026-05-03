# Phase 5 + 6 Implementation Notes

This document summarizes the Phase 5 IoT integration and Phase 6 security hardening added to the local AI dashboard stack.

## Phase 5: IoT + Network Integration

Implemented components:
- `iot/home_assistant.py`
  - Home Assistant REST client with local-first URL checks.
  - Entity listing via `/api/states`.
  - Service invocation via `/api/services/{domain}/{service}`.
  - Domain/entity policy gating.
- `iot/network_scanner.py`
  - Safe local scanner for private/loopback IPv4 subnets.
  - Timeout-limited TCP checks with host count caps.
  - Default common IoT ports: `80,443,8123,1883`.
- `iot/manager.py`
  - Unified facade for status, scan, list devices, and control operations.
- `tools/iot_tools.py`
  - Registered tools:
    - `iot_status`
    - `iot_list_entities`
    - `scan_local_network`
    - `iot_call_service`

## Phase 6: Security Hardening

Implemented components:
- `security/sandbox.py`
  - Approval queue for high-risk tools.
  - Fingerprinted action approvals with TTL.
  - Security status API payload helpers.
  - JSONL action logging to `logs/security_actions.jsonl`.
  - Sandbox metadata (`sandbox_mode`, Docker settings).
- `core/agent.py`
  - Authorization gate switched to `authorize_tool_call()`.
  - Pending approvals surfaced as actionable tool results.
  - Runtime methods for approval queue and IoT operations.
- `tools/code_execution_tools.py`
  - `run_python` supports `sandbox_mode: docker`.
  - Docker mode runs script in constrained container with no network by default.

## API Surface Added

New endpoints in `ui/dashboard_api.py`:
- `GET /api/security/status`
- `GET /api/security/approvals`
- `POST /api/security/approvals/resolve`
- `GET /api/iot/status`
- `GET /api/iot/devices`
- `GET /api/iot/scan`
- `POST /api/iot/control`

## Dashboard UI Additions

Updated `ui/dashboard.html` with:
- IoT panel:
  - Status indicators
  - Device control form
  - Local network scan controls
  - JSON result viewer
- Approval Queue panel:
  - Pending request list
  - Approve / Deny actions

## Configuration Keys

Added under `config/phase4_config.yaml`:
- `security.require_tool_approval`
- `security.approval_ttl_seconds`
- `security.approval_required_tools`
- `security.sandbox_mode`
- `security.docker_image`
- `security.docker_network`
- `security.security_log_dir`
- `iot.*` (feature, Home Assistant, scanner)

## Safety Defaults

- Home Assistant integration is present but disabled by default.
- Local network scanner is restricted to private/loopback ranges.
- IoT control operations require approval by default.
- Docker sandbox mode is enabled in config for Python tool execution.
