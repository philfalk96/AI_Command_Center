from __future__ import annotations

import sys
from pathlib import Path

# NOTE: project imports are intentionally deferred into main() so that
# PyInstaller analysis subprocesses can import this module without executing
# the blocking module-level code in main.py (stdout replacement, file handlers).


def _runtime_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def _resolve_config_paths(root: Path) -> tuple[Path, Path]:
    candidates = [root, root / "_internal"]

    config_path = None
    for base in candidates:
        candidate = base / "config" / "phase4_config.yaml"
        if candidate.exists():
            config_path = candidate
            break
    if config_path is None:
        config_path = root / "config" / "phase4_config.yaml"

    deploy_config_path = None
    deploy_candidates = [
        root / "config.yaml",
        root / "config" / "config.yaml",
        (root / "_internal") / "config" / "config.yaml",
    ]
    for candidate in deploy_candidates:
        if candidate.exists():
            deploy_config_path = candidate
            break
    if deploy_config_path is None:
        deploy_config_path = root / "config" / "config.yaml"

    return config_path, deploy_config_path


def main() -> int:
    from main import apply_deployment_config, load_config  # deferred
    from ui.dashboard_api import run_dashboard_server  # deferred

    root = _runtime_root()
    config_path, deploy_config_path = _resolve_config_paths(root)
    config = load_config(str(config_path))
    config = apply_deployment_config(config, str(deploy_config_path))
    run_dashboard_server(config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())