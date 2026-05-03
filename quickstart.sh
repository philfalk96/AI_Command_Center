#!/bin/bash
# Embodied AI System - Quick Start Script for macOS/Linux
# This script sets up and runs Phase 1 of the Embodied AI system

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  Embodied AI System - Phase 1 Quick Start         ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Check if Ollama is running
echo "[1/4] Checking if Ollama is running..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo ""
    echo "ERROR: Ollama is not running!"
    echo "Please start Ollama first: ollama serve"
    echo "Download from: https://ollama.ai"
    echo ""
    exit 1
fi
echo "✓ Ollama is running"

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo ""
    echo "[2/4] Creating Python virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment exists"
fi

# Activate virtual environment
echo ""
echo "[3/4] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install/update dependencies
echo ""
echo "[4/4] Installing dependencies..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

# Run the system
echo ""
echo "═══════════════════════════════════════════════════"
echo "Starting Embodied AI System - Phase 1"
echo "═══════════════════════════════════════════════════"
echo ""
echo "Commands:"
echo "  - Type your question or command"
echo "  - Type 'help' for available commands"
echo "  - Type 'exit' or 'quit' to stop"
echo ""

python main.py --mode repl
