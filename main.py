"""
Embodied AI System — Phase 4 Entry Point
==========================================

CLI interface for the Embodied AI system.

Phase 3 adds:
- Whisper speech-to-text
- Multi-backend TTS (edge-tts / coqui / pyttsx3)
- Real-time voice interaction loop (VAD, push-to-talk, or text)

Phase 4 adds:
- FastAPI backend
- Dashboard UI for control + visibility
- Model switching, prompt tuning, memory inspection, tool permissions

Usage:
    python main.py                          # REPL mode (default)
    python main.py --mode voice             # Voice loop (Phase 3)
    python main.py --mode voice --input ptt # Push-to-talk variant
    python main.py --mode cli               # Single-query CLI
    python main.py --mode dashboard         # FastAPI + local dashboard (Phase 4)
    python main.py --config config/phase4_config.yaml
"""

import os
import sys
import logging
import json
from pathlib import Path
from typing import Dict, Any

import yaml
from colorama import init, Fore, Style
import click

# Initialize colorama for colored terminal output
init(autoreset=True)

# Force UTF-8 console streams on Windows when console streams exist.
if sys.platform == 'win32':
    import io

    if getattr(sys, 'stdout', None) is not None and hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if getattr(sys, 'stderr', None) is not None and hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Ensure log directory exists before creating file handlers.
Path('logs').mkdir(parents=True, exist_ok=True)

# Configure logging; in pythonw contexts stderr/stdout may be None.
_handlers = [logging.FileHandler('logs/phase1.log', encoding='utf-8')]
if getattr(sys, 'stderr', None) is not None:
    _handlers.append(logging.StreamHandler(sys.stderr))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=_handlers,
)
logger = logging.getLogger(__name__)


def load_config(config_path: str = 'config/phase4_config.yaml') -> Dict[str, Any]:
    """
    Load system configuration from YAML file.
    Falls back to phase1_config.yaml if phase2 is missing.

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary
    """
    # Auto-fallback chain: phase4 → phase3 → phase2 → phase1
    if not Path(config_path).exists():
        fallbacks = [config_path]
        for phase in ('phase4', 'phase3', 'phase2'):
            prev = fallbacks[-1]
            if phase in prev:
                next_phase = f"phase{int(phase[-1]) - 1}"
                fallbacks.append(prev.replace(phase, next_phase))

        for fallback in fallbacks[1:]:
            if Path(fallback).exists():
                logger.warning(f"Config not found; falling back to {fallback}")
                config_path = fallback
                break
    try:
        if not Path(config_path).exists():
            logger.error(f"❌ Config file not found: {config_path}")
            sys.exit(1)
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"✅ Configuration loaded from {config_path}")
        return config
    
    except Exception as e:
        logger.error(f"❌ Failed to load configuration: {e}")
        sys.exit(1)


def _deep_merge(base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge overlay into base and return base."""
    for key, value in (overlay or {}).items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def apply_deployment_config(config: Dict[str, Any], deploy_config_path: str) -> Dict[str, Any]:
    """
    Apply deployment-time overrides from a lightweight config file.

    Expected keys (all optional):
      model.name
      backend.host/backend.port
      runtime.offline_mode
      logging.directory
    """
    deploy_path = Path(deploy_config_path)
    if not deploy_path.exists():
        logger.info(f"ℹ️ Deployment config not found at {deploy_config_path}; using base config")
        return config

    try:
        with deploy_path.open('r', encoding='utf-8') as f:
            deploy_cfg = yaml.safe_load(f) or {}
    except Exception as e:
        logger.error(f"❌ Failed to load deployment config ({deploy_config_path}): {e}")
        sys.exit(1)

    # Optional pass-through merge for advanced overrides.
    if isinstance(deploy_cfg.get('overrides'), dict):
        _deep_merge(config, deploy_cfg['overrides'])

    # Model selection
    model_name = str(deploy_cfg.get('model', {}).get('name', '')).strip()
    if model_name:
        config.setdefault('ollama', {})
        config['ollama']['model'] = model_name

    # API host/port
    backend = deploy_cfg.get('backend', {}) or {}
    host = str(backend.get('host', '')).strip()
    port = backend.get('port')
    config.setdefault('api', {})
    if host:
        config['api']['host'] = host
    if port is not None:
        try:
            config['api']['port'] = int(port)
        except (TypeError, ValueError):
            logger.warning(f"Invalid backend.port value in {deploy_config_path}: {port}")

    # Offline mode toggle
    offline_mode = bool(deploy_cfg.get('runtime', {}).get('offline_mode', False))
    config.setdefault('runtime', {})
    config['runtime']['offline_mode'] = offline_mode
    if offline_mode:
        os.environ['HF_HUB_OFFLINE'] = '1'
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        os.environ['TOKENIZERS_PARALLELISM'] = 'false'

    # Logging directory (defaults to /logs under project root)
    log_dir = str(deploy_cfg.get('logging', {}).get('directory', './logs')).strip() or './logs'
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    config.setdefault('logging', {})
    config['logging']['log_dir'] = log_dir

    logger.info(f"✅ Deployment config applied from {deploy_config_path}")
    return config


def cli_mode(agent, config: Dict[str, Any]) -> None:
    """
    Single-query CLI mode
    
    Args:
        agent: EmbodiedAIAgent instance
        config: Configuration dictionary
    """
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Embodied AI System - Phase 2 (CLI Mode)")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    # Get user input from command line
    user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
    
    if not user_input:
        print(f"{Fore.YELLOW}No input provided.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}Processing...{Style.RESET_ALL}\n")
    
    # Process query
    response, metadata = agent.process(user_input)
    
    # Display response
    print(f"{Fore.BLUE}Assistant: {Style.RESET_ALL}{response}\n")
    
    # Display metadata if verbose
    if config.get('logging', {}).get('level') == 'DEBUG':
        print(f"{Fore.YELLOW}Metadata:{Style.RESET_ALL}")
        print(json.dumps(metadata, indent=2))


def voice_mode(agent, config: Dict[str, Any], input_mode: str = 'vad') -> None:
    """
    Phase 3 voice loop mode.

    Args:
        agent:      EmbodiedAIAgent instance
        config:     Configuration dictionary
        input_mode: 'vad' | 'ptt' | 'text'
    """
    from voice.voice_loop import VoiceLoop

    # Override input_mode from CLI if provided
    if input_mode:
        config.setdefault('voice', {})
        config['voice']['input_mode'] = input_mode

    loop = VoiceLoop(agent, config)
    loop.run()


def repl_mode(agent, config: Dict[str, Any]) -> None:
    """
    Interactive REPL (Read-Eval-Print-Loop) mode
    
    Args:
        agent: EmbodiedAIAgent instance
        config: Configuration dictionary
    """
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Embodied AI System - Phase 2 (REPL Mode)")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Commands:{Style.RESET_ALL}")
    print(f"  quit / exit  — Exit the system")
    print(f"  history      — Show recent conversation")
    print(f"  clear        — Clear conversation history")
    print(f"  status       — Show system status and tools")
    print(f"  tools        — List all registered tools")
    print(f"  logs [n]     — Show last n structured log entries (default 20)")
    print(f"  tasks        — List saved task plans")
    print(f"  add          — Add text to RAG memory")
    print(f"  help         — Show this help message\n")
    
    # Conversation loop
    while True:
        try:
            # Get user input
            user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit']:
                print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break
            
            elif user_input.lower() == 'history':
                history = agent.get_history(last_n=5)
                print(f"\n{Fore.YELLOW}Recent conversation:{Style.RESET_ALL}")
                for i, msg in enumerate(history, 1):
                    role = Fore.GREEN if msg['role'] == 'user' else Fore.BLUE
                    print(f"{role}{msg['role'].upper()}: {Style.RESET_ALL}{msg['content'][:100]}...")
                print()
                continue
            
            elif user_input.lower() == 'clear':
                agent.clear_history()
                print(f"{Fore.CYAN}✅ History cleared{Style.RESET_ALL}\n")
                continue
            
            elif user_input.lower() == 'status':
                status = agent.get_status()
                print(f"\n{Fore.YELLOW}System Status:{Style.RESET_ALL}")
                print(json.dumps(status, indent=2))
                print()
                continue
            
            elif user_input.lower() == 'add':
                text = input(f"{Fore.CYAN}Text to add to memory: {Style.RESET_ALL}").strip()
                if text:
                    agent.add_to_memory(text)
                print()
                continue
            
            elif user_input.lower() == 'tools':
                tools = agent.tool_executor.list_tools()
                print(f"\n{Fore.YELLOW}Registered tools ({len(tools)}):{Style.RESET_ALL}")
                for t in tools:
                    print(f"  {Fore.GREEN}{t['name']:25s}{Style.RESET_ALL} {t.get('description','')[:60]}")
                print()
                continue

            elif user_input.lower().startswith('logs'):
                parts = user_input.split()
                n = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 20
                print(f"\n{Fore.YELLOW}Session log (last {n} entries):{Style.RESET_ALL}")
                print(agent.get_log_tail(n=n))
                print()
                continue

            elif user_input.lower() == 'tasks':
                plans = agent.list_plans()
                if not plans:
                    print(f"{Fore.YELLOW}No saved task plans found.{Style.RESET_ALL}\n")
                else:
                    print(f"\n{Fore.YELLOW}Saved task plans:{Style.RESET_ALL}")
                    for p in plans:
                        status_color = Fore.GREEN if p['status'] == 'done' else Fore.RED if p['status'] == 'failed' else Fore.YELLOW
                        print(f"  {Fore.CYAN}{p['plan_id']}{Style.RESET_ALL}  [{status_color}{p['status']}{Style.RESET_ALL}]  {p['goal'][:60]}  ({p['steps']} steps)")
                    print()
                continue

            elif user_input.lower() == 'help':
                print(f"\n{Fore.YELLOW}Available commands:{Style.RESET_ALL}")
                print("  quit/exit, history, clear, status, tools, logs [n], tasks, add, help\n")
                continue
            
            # Process query
            print(f"{Fore.CYAN}Processing...{Style.RESET_ALL}")
            response, metadata = agent.process(user_input)
            
            print(f"\n{Fore.BLUE}Assistant: {Style.RESET_ALL}{response}\n")
        
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


def dashboard_mode(config: Dict[str, Any]) -> None:
    """Run Phase 4 FastAPI dashboard server."""
    from ui.dashboard_api import run_dashboard_server
    run_dashboard_server(config)


def desktop_mode(config: Dict[str, Any], config_path: str, deploy_config_path: str) -> None:
    """Legacy desktop entrypoint now redirects to the web dashboard."""
    logger.warning("Desktop mode is deprecated; starting the web dashboard instead.")
    dashboard_mode(config)


@click.command()
@click.option(
    '--mode',
    type=click.Choice(['cli', 'repl', 'voice', 'dashboard', 'desktop']),
    default='repl',
    help='Operation mode: repl, voice, dashboard (web UI), desktop (legacy alias for dashboard), or cli'
)
@click.option(
    '--config',
    type=str,
    default='config/phase4_config.yaml',
    help='Path to configuration file'
)
@click.option(
    '--deploy-config',
    type=str,
    default='config/config.yaml',
    help='Path to deployment override config (model/port/offline/logging)'
)
@click.option(
    '--input',
    'input_mode',
    type=click.Choice(['vad', 'ptt', 'text']),
    default='vad',
    help='Voice input mode: vad (auto-detect), ptt (push-to-talk), text (typed)'
)
def main(mode: str, config: str, deploy_config: str, input_mode: str) -> None:
    """
    Embodied AI System — Phase 4

    A local-first AI assistant with voice, tools, planning, and a web dashboard.
    """
    try:
        # Load configuration
        logger.info("📋 Loading configuration...")
        config_data = load_config(config)
        config_data = apply_deployment_config(config_data, deploy_config)
        
        # Create logs directory
        Path('logs').mkdir(exist_ok=True)
        Path('data').mkdir(exist_ok=True)
        
        # Dashboard mode owns its own agent lifecycle in the FastAPI process.
        if mode == 'dashboard':
            logger.info("🚀 Starting dashboard mode...")
            dashboard_mode(config_data)
            return
        if mode == 'desktop':
            logger.info("🚀 Desktop mode requested; redirecting to dashboard mode...")
            desktop_mode(config_data, config, deploy_config)
            return

        # Import and initialize agent for CLI/REPL/voice modes
        logger.info("🚀 Initializing system...")
        from core.agent import EmbodiedAIAgent

        agent = EmbodiedAIAgent(config_data)
        
        # Run in selected mode
        if mode == 'cli':
            cli_mode(agent, config_data)
        elif mode == 'voice':
            voice_mode(agent, config_data, input_mode=input_mode)
        else:  # repl
            repl_mode(agent, config_data)
    
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}System interrupted{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == '__main__':
    main()
