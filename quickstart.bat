@echo off
REM Embodied AI System - Quick Start Script for Windows
REM This script sets up and runs Phase 1 of the Embodied AI system

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║  Embodied AI System - Phase 1 Quick Start         ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Check if Ollama is running
echo [1/4] Checking if Ollama is running...
powershell -Command "(Invoke-WebRequest http://localhost:11434/api/tags -TimeoutSec 2).StatusCode" 2>nul >nul
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Ollama is not running!
    echo Please start Ollama first: ollama serve
    echo Download from: https://ollama.ai
    echo.
    pause
    exit /b 1
)
echo ✓ Ollama is running

REM Create virtual environment if needed
if not exist "venv" (
    echo.
    echo [2/4] Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment exists
)

REM Activate virtual environment
echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

REM Install/update dependencies
echo.
echo [4/4] Installing dependencies...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

REM Run the system
echo.
echo ═══════════════════════════════════════════════════
echo Starting Embodied AI System - Phase 1
echo ═══════════════════════════════════════════════════
echo.
echo Commands:
echo   - Type your question or command
echo   - Type 'help' for available commands
echo   - Type 'exit' or 'quit' to stop
echo.
python main.py --mode repl

pause
