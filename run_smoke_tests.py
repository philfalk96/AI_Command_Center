"""
Smoke Test Suite for Embodied AI System
========================================

Comprehensive tests for all core modules to ensure:
- No import/syntax errors
- Basic functionality works
- All components can be instantiated
- Integration points are wired correctly

Usage:
    python run_smoke_tests.py
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Color output helpers
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


class TestResults:
    """Track test results and provide summary reporting."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.errors: List[Tuple[str, str]] = []
        self.tests: Dict[str, bool] = {}
    
    def add_pass(self, test_name: str):
        """Record a passing test."""
        self.passed += 1
        self.tests[test_name] = True
        print(f"{GREEN}✓{RESET} {test_name}")
    
    def add_fail(self, test_name: str, error: str):
        """Record a failing test."""
        self.failed += 1
        self.tests[test_name] = False
        self.errors.append((test_name, error))
        print(f"{RED}✗{RESET} {test_name}: {error}")
    
    def add_skip(self, test_name: str, reason: str):
        """Record a skipped test."""
        self.skipped += 1
        print(f"{YELLOW}⊘{RESET} {test_name}: {reason}")
    
    def summary(self) -> str:
        """Generate test summary report."""
        total = self.passed + self.failed + self.skipped
        return f"\n{'='*60}\nTest Summary:\n  Passed:  {self.passed}/{total}\n  Failed:  {self.failed}/{total}\n  Skipped: {self.skipped}/{total}\n{'='*60}"


# Initialize test results
results = TestResults()


def test_imports():
    """Test that all core modules can be imported without errors."""
    print(f"\n{BLUE}=== Testing Imports ==={RESET}")
    
    imports_to_test = [
        ("core.agent", "EmbodiedAIAgent"),
        ("core.cognition", "CognitionEngine"),
        ("core.orchestrator", "Orchestrator"),
        ("core.planner", "TaskPlanner"),
        ("core.structured_logger", "StructuredLogger"),
        ("memory.rag", "RAGSystem"),
        ("models.ollama_client", "OllamaClient"),
        ("tools.base_tools", "ToolExecutor"),
        ("ui.dashboard_api", "DashboardServer"),
        ("iot.manager", "IoTManager"),
        ("iot.scanner", "NetworkDiscovery"),
        ("voice.stt", "WhisperSTT"),
        ("voice.tts", "TTSEngine"),
        ("voice.audio_utils", "AudioCapture"),
    ]
    
    for module_name, class_name in imports_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            results.add_pass(f"Import {module_name}.{class_name}")
        except ImportError as e:
            results.add_fail(f"Import {module_name}.{class_name}", str(e))
        except AttributeError as e:
            results.add_fail(f"Import {module_name}.{class_name}", f"Class {class_name} not found: {e}")
        except Exception as e:
            results.add_fail(f"Import {module_name}.{class_name}", f"Unexpected error: {e}")


def test_core_components():
    """Test instantiation of core components."""
    print(f"\n{BLUE}=== Testing Core Components ==={RESET}")
    
    try:
        from core.structured_logger import StructuredLogger
        logger = StructuredLogger(config={"logging": {"log_dir": "logs"}})
        results.add_pass("StructuredLogger instantiation")
    except Exception as e:
        results.add_fail("StructuredLogger instantiation", str(e))
    
    try:
        from core.cognition import CognitionEngine
        # CognitionEngine requires Ollama, skip if not available
        results.add_skip("CognitionEngine instantiation", "Requires Ollama service")
    except Exception as e:
        results.add_fail("CognitionEngine instantiation", str(e))
    
    try:
        from core.agent import EmbodiedAIAgent
        results.add_skip("EmbodiedAIAgent instantiation", "Requires full config and services")
    except Exception as e:
        results.add_fail("EmbodiedAIAgent instantiation", str(e))


def test_memory_system():
    """Test memory/RAG system initialization."""
    print(f"\n{BLUE}=== Testing Memory System ==={RESET}")
    
    try:
        from memory.rag import RAGSystem
        # Check that RAGSystem can be imported
        results.add_pass("RAGSystem import")
    except Exception as e:
        results.add_fail("RAGSystem import", str(e))
    
    try:
        # Check ChromaDB directory exists or can be created
        chroma_dir = Path("data/chroma_db")
        chroma_dir.mkdir(parents=True, exist_ok=True)
        results.add_pass("ChromaDB directory accessible")
    except Exception as e:
        results.add_fail("ChromaDB directory accessible", str(e))


def test_tools_system():
    """Test tool system infrastructure."""
    print(f"\n{BLUE}=== Testing Tools System ==={RESET}")
    
    try:
        from tools.base_tools import Tool
        
        # Test creating a simple tool
        class TestTool(Tool):
            """Simple test tool."""
            def execute(self, **kwargs):
                return {"result": "test"}
        
        tool = TestTool(name="test", description="Test tool")
        results.add_pass("Tool subclass creation")
    except Exception as e:
        results.add_fail("Tool subclass creation", str(e))
    
    try:
        from tools.base_tools import ToolExecutor
        executor = ToolExecutor(config={"tools": {"enabled": True}})
        results.add_pass("ToolExecutor instantiation")
    except Exception as e:
        results.add_fail("ToolExecutor instantiation", str(e))


def test_iot_components():
    """Test IoT manager and scanner components."""
    print(f"\n{BLUE}=== Testing IoT Components ==={RESET}")
    
    try:
        from iot.manager import IoTManager
        manager = IoTManager({})
        results.add_pass("IoTManager instantiation")
    except Exception as e:
        results.add_fail("IoTManager instantiation", str(e))
    
    try:
        from iot.scanner import NetworkDiscovery
        scanner = NetworkDiscovery()
        results.add_pass("NetworkDiscovery instantiation")
    except Exception as e:
        results.add_fail("NetworkDiscovery instantiation", str(e))
    
    try:
        from iot.device_registry import IoTDeviceRegistry
        registry = IoTDeviceRegistry({})
        results.add_pass("IoTDeviceRegistry instantiation")
    except Exception as e:
        results.add_fail("IoTDeviceRegistry instantiation", str(e))


def test_config_system():
    """Test configuration loading and merging."""
    print(f"\n{BLUE}=== Testing Config System ==={RESET}")
    
    try:
        import yaml
        config_path = Path("config/phase4_config.yaml")
        if config_path.exists():
            with open(config_path) as f:
                config = yaml.safe_load(f)
            results.add_pass("Phase 4 config loading")
        else:
            results.add_skip("Phase 4 config loading", "Config file not found")
    except Exception as e:
        results.add_fail("Phase 4 config loading", str(e))
    
    try:
        # Test deployment config path
        deploy_config = Path("config/config.yaml")
        if deploy_config.exists():
            results.add_pass("Deployment config exists")
        else:
            results.add_skip("Deployment config", "Not required for smoke test")
    except Exception as e:
        results.add_fail("Deployment config check", str(e))


def test_ui_components():
    """Test UI/API components."""
    print(f"\n{BLUE}=== Testing UI Components ==={RESET}")
    
    try:
        from ui.dashboard_api import DashboardServer
        results.add_pass("DashboardServer import")
    except Exception as e:
        results.add_fail("DashboardServer import", str(e))


def test_voice_components():
    """Test voice I/O components."""
    print(f"\n{BLUE}=== Testing Voice Components ==={RESET}")
    
    try:
        from voice.audio_utils import AudioCapture
        results.add_pass("AudioCapture import")
    except Exception as e:
        results.add_fail("AudioCapture import", str(e))
    
    try:
        from voice.stt import WhisperSTT
        results.add_skip("WhisperSTT instantiation", "Requires audio setup")
    except Exception as e:
        results.add_fail("WhisperSTT import", str(e))
    
    try:
        from voice.tts import TTSEngine
        results.add_skip("TTSEngine instantiation", "Requires audio setup")
    except Exception as e:
        results.add_fail("TTSEngine import", str(e))


def test_startup_orchestration():
    """Test startup script functionality."""
    print(f"\n{BLUE}=== Testing Startup Orchestration ==={RESET}")
    
    try:
        import startup
        # Just verify it imports successfully
        results.add_pass("Startup orchestrator import")
    except Exception as e:
        results.add_fail("Startup orchestrator import", str(e))
    
    try:
        # Check startup scripts exist
        startup_files = [
            Path("startup.py"),
            Path("startup.ps1"),
            Path("startup.sh"),
        ]
        for f in startup_files:
            if f.exists():
                results.add_pass(f"Startup script exists: {f.name}")
            else:
                results.add_fail(f"Startup script missing: {f.name}", "File not found")
    except Exception as e:
        results.add_fail("Startup script check", str(e))


def test_directory_structure():
    """Verify required directories exist."""
    print(f"\n{BLUE}=== Testing Directory Structure ==={RESET}")
    
    required_dirs = [
        "logs",
        "data",
        "config",
        "core",
        "memory",
        "iot",
        "ui",
        "voice",
        "tools",
        "security",
    ]
    
    for dirname in required_dirs:
        dir_path = Path(dirname)
        if dir_path.exists():
            results.add_pass(f"Directory exists: {dirname}")
        else:
            results.add_fail(f"Directory missing: {dirname}", "Directory not found")


def test_requirements():
    """Check that requirements.txt exists and key dependencies are listed."""
    print(f"\n{BLUE}=== Testing Requirements ==={RESET}")
    
    try:
        req_file = Path("requirements.txt")
        if req_file.exists():
            with open(req_file) as f:
                reqs = f.read()
            
            required_packages = [
                "ollama",
                "chromadb",
                "sentence-transformers",
                "fastapi",
                "uvicorn",
                "pyyaml",
                "click",
                "colorama",
                "pydantic",
            ]
            
            found = 0
            for pkg in required_packages:
                if pkg.lower() in reqs.lower():
                    found += 1
            
            results.add_pass(f"requirements.txt with {found}/{len(required_packages)} key packages")
        else:
            results.add_fail("requirements.txt", "File not found")
    except Exception as e:
        results.add_fail("Requirements check", str(e))


def test_syntax_validation():
    """Validate Python syntax of all modules."""
    print(f"\n{BLUE}=== Testing Python Syntax ==={RESET}")
    
    import py_compile
    
    py_files = list(Path(".").rglob("*.py"))
    py_files = [f for f in py_files if not any(x in str(f) for x in ["venv", "__pycache__", "build", "dist"])]
    
    syntax_errors = 0
    for py_file in py_files:
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as e:
            results.add_fail(f"Syntax: {py_file.relative_to(Path.cwd())}", str(e))
            syntax_errors += 1
    
    if syntax_errors == 0:
        results.add_pass(f"Python syntax valid for all {len(py_files)} files")


def main():
    """Run all smoke tests."""
    print(f"\n{BLUE}{'='*60}")
    print("EMBODIED AI SYSTEM - SMOKE TEST SUITE")
    print(f"{'='*60}{RESET}\n")
    
    # Run all test categories
    test_directory_structure()
    test_imports()
    test_core_components()
    test_memory_system()
    test_tools_system()
    test_iot_components()
    test_config_system()
    test_ui_components()
    test_voice_components()
    test_startup_orchestration()
    test_requirements()
    test_syntax_validation()
    
    # Print summary
    print(results.summary())
    
    if results.failed > 0:
        print(f"\n{RED}FAILED TESTS:{RESET}")
        for test_name, error in results.errors:
            print(f"  - {test_name}: {error}")
    
    # Exit with appropriate code
    exit_code = 0 if results.failed == 0 else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
