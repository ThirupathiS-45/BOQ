#!/bin/bash
# Startup script for BOQ Backend API

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 BOQ Prediction API - Startup Script${NC}\n"

# Check Python
echo "✓ Checking Python installation..."
python3 --version

# Check if in correct directory
if [ ! -f "main.py" ]; then
    echo -e "${RED}❌ Error: main.py not found. Please run this script from the backend directory.${NC}"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "⚠️  Please edit .env and add your OPENROUTER_API_KEY"
        echo "   You can still run without it (fallback parser will be used)"
    fi
fi

# Install requirements if needed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -q -r requirements.txt
    echo "✓ Dependencies installed"
fi

# Check if model exists
if [ ! -f "../model/boq_model_v3.pkl" ]; then
    echo -e "${RED}❌ Error: Model file not found at ../model/boq_model_v3.pkl${NC}"
    echo "   Please ensure the model file is in the correct location"
    exit 1
fi
echo "✓ Model file found"

# Get configuration from .env
if [ -f ".env" ]; then
    source .env
fi

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}

echo -e "\n${GREEN}─────────────────────────────────────${NC}"
echo -e "${GREEN}Configuration:${NC}"
echo "  Host: $HOST"
echo "  Port: $PORT"
echo "  Model: ../model/boq_model_v3.pkl"
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo -e "  ${YELLOW}NLP Parser: DISABLED (using fallback)${NC}"
else
    echo "  NLP Parser: ENABLED (OpenRouter)"
fi
echo -e "${GREEN}─────────────────────────────────────${NC}\n"

echo -e "${GREEN}Starting API server...${NC}"
echo "📡 Server will be available at http://$HOST:$PORT"
echo "📚 API Docs at http://localhost:$PORT/docs"
echo "🏥 Health check at http://localhost:$PORT/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 main.py
