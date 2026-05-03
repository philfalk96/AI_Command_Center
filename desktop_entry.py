from __future__ import annotations

import traceback
import sys
import threading
import webbrowser
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
    root = _runtime_root()
    log_dir = root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "desktop_launch.log"

    try:
        from main import apply_deployment_config, load_config  # deferred
        from ui.dashboard_api import run_dashboard_server  # deferred

        config_path, deploy_config_path = _resolve_config_paths(root)
        config = load_config(str(config_path))
        config = apply_deployment_config(config, str(deploy_config_path))

        api_cfg = config.get("api", {})
        host = api_cfg.get("host", "127.0.0.1") or "127.0.0.1"
        port = int(api_cfg.get("port", 8000) or 8000)
        launch_url = f"http://{host}:{port}"

        # Preserve legacy shortcuts by opening the web dashboard instead of the PyQt shell.
        threading.Timer(1.5, lambda: webbrowser.open(launch_url)).start()
        run_dashboard_server(config)
        return 0
    except Exception:
        details = traceback.format_exc()
        try:
            log_path.write_text(details, encoding="utf-8")
        except Exception:
            pass

        # Show visible error even when launched via pythonw/shortcut.
        try:
            import ctypes

            ctypes.windll.user32.MessageBoxW(
                0,
                f"Embodied AI Dashboard failed to launch.\n\nDetails saved to:\n{log_path}",
                "Embodied AI Dashboard",
                0x10,
            )
        except Exception:
            pass
        return 1


if __name__ == "__main__":
    raise SystemExit(main())