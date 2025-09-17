#!/bin/bash

# Automated Options Trading System Startup Script

echo "🤖 Starting Automated Options Trading System..."

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set. AI features will use fallback strategies."
    echo "   Set your API key: export OPENAI_API_KEY='your-api-key-here'"
    echo "   Or use: python3 auto_trader.py --api-key your-api-key-here"
    echo ""
fi

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    # Check if dependencies are available
    if python3 -c "import openai, yfinance, numpy, pandas" &> /dev/null; then
        echo "✅ All dependencies available"
        
        # Run the automated trader
        if [ "$1" = "--demo" ]; then
            echo "🎮 Running in DEMO mode"
            python3 auto_trader.py --demo
        elif [ "$1" = "--config" ] && [ -n "$2" ]; then
            echo "�� Using configuration file: $2"
            python3 auto_trader.py --config "$2"
        else
            echo "🚀 Starting automated trading..."
            python3 auto_trader.py
        fi
    else
        echo "❌ Missing dependencies. Installing..."
        pip3 install openai yfinance numpy pandas
        
        echo "🚀 Starting automated trading..."
        python3 auto_trader.py
    fi
else
    echo "❌ Python 3 not found. Please install Python 3.11 or higher."
    exit 1
fi
