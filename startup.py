"""
Deployment startup orchestrator.

Responsibilities:
- Ensure required runtime directories exist
- Optionally start Ollama service
- Initialize memory DB (Chroma + embedding model)
- Launch FastAPI dashboard backend
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict

import yaml


ROOT = Path(__file__).resolve().parent


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        return {}
    return data


def wait_for_ollama(base_url: str, timeout_seconds: int = 25) -> bool:
    deadline = time.time() + max(1, timeout_seconds)
    url = f"{base_url.rstrip('/')}/api/tags"
    while time.time() < deadline:
        try:
            req = urllib.request.Request(url=url, method="GET")
            with urllib.request.urlopen(req, timeout=2) as resp:
                if int(resp.status) == 200:
                    return True
        except (urllib.error.URLError, TimeoutError, OSError):
            pass
        time.sleep(1)
    return False


def start_ollama_if_needed(base_url: str, auto_start: bool, timeout_seconds: int) -> None:
    if wait_for_ollama(base_url, timeout_seconds=2):
        print("[startup] Ollama already running")
        return

    if not auto_start:
        raise RuntimeError("Ollama is not running and auto_start is disabled")

    print("[startup] Starting Ollama service...")
    kwargs: Dict[str, Any] = {
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "stdin": subprocess.DEVNULL,
        "cwd": str(ROOT),
    }

    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        kwargs["creationflags"] = creationflags
    else:
        kwargs["start_new_session"] = True

    subprocess.Popen(["ollama", "serve"], **kwargs)

    if not wait_for_ollama(base_url, timeout_seconds=timeout_seconds):
        raise RuntimeError("Ollama did not become ready in time")

    print("[startup] Ollama is ready")


def initialize_memory_db(base_config_path: Path, deploy_config_path: Path) -> None:
    from main import apply_deployment_config, load_config
    from memory.rag import RAGSystem

    print("[startup] Initializing memory DB...")
    config = load_config(str(base_config_path))
    config = apply_deployment_config(config, str(deploy_config_path))

    # Instantiation creates embedding client and persistent Chroma collection.
    RAGSystem(config.get("memory", {}))
    print("[startup] Memory DB ready")


def run_backend(base_config_path: Path, deploy_config_path: Path, mode: str) -> int:
    cmd = [
        sys.executable,
        str(ROOT / "main.py"),
        "--mode",
        mode,
        "--config",
        str(base_config_path),
        "--deploy-config",
        str(deploy_config_path),
    ]
    print("[startup] Launching backend:", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=str(ROOT))
    return int(proc.returncode)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start ai-ui-system deployment runtime")
    parser.add_argument("--config", default="config/phase4_config.yaml", help="Base phase config path")
    parser.add_argument("--deploy-config", default="config/config.yaml", help="Deployment config path")
    parser.add_argument("--mode", default="dashboard", choices=["dashboard", "desktop", "repl", "cli", "voice"])
    parser.add_argument("--skip-ollama", action="store_true", help="Do not auto-start Ollama")
    parser.add_argument("--skip-memory-init", action="store_true", help="Skip memory DB initialization")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    base_config_path = (ROOT / args.config).resolve() if not Path(args.config).is_absolute() else Path(args.config)
    deploy_config_path = (ROOT / args.deploy_config).resolve() if not Path(args.deploy_config).is_absolute() else Path(args.deploy_config)

    (ROOT / "logs").mkdir(parents=True, exist_ok=True)
    (ROOT / "data").mkdir(parents=True, exist_ok=True)
    (ROOT / "data" / "chroma_db").mkdir(parents=True, exist_ok=True)

    deploy_cfg = load_yaml(deploy_config_path)
    base_url = str(deploy_cfg.get("ollama", {}).get("base_url", "http://localhost:11434"))
    auto_start = bool(deploy_cfg.get("ollama", {}).get("auto_start", True))
    timeout_seconds = int(deploy_cfg.get("ollama", {}).get("startup_timeout_seconds", 25))

    try:
        if not args.skip_ollama:
            start_ollama_if_needed(base_url, auto_start=auto_start, timeout_seconds=timeout_seconds)

        if not args.skip_memory_init:
            initialize_memory_db(base_config_path, deploy_config_path)

        return run_backend(base_config_path, deploy_config_path, args.mode)
    except Exception as exc:
        print(f"[startup] Fatal error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
