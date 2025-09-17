#!/bin/bash

# Options Trading Simulator Startup Script

echo "🚀 Starting Options Trading Simulator..."

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "📦 Using Docker..."
    docker-compose up --build
else
    echo "🐍 Using Python directly..."
    
    # Check if Python 3 is available
    if command -v python3 &> /dev/null; then
        # Check if user wants to run demo
        if [ "$1" = "--demo" ]; then
            echo "🎬 Running live data demo..."
            python3 demo_live_data.py
        elif [ "$1" = "--test" ]; then
            echo "🧪 Running tests..."
            python3 test_live_data.py
        elif [ "$1" = "--live" ]; then
            echo "🌐 Running with live data..."
            # Check if dependencies are available
            if python3 -c "import yfinance, numpy, pandas" &> /dev/null; then
                python3 main.py
            else
                echo "❌ Live data dependencies not found."
                echo "Installing dependencies..."
                pip3 install yfinance numpy pandas
                python3 main.py
            fi
        else
            # Run offline version by default
            echo "📊 Running offline version (no external dependencies required)"
            python3 main_offline.py
        fi
    else
        echo "❌ Python 3 not found. Please install Python 3.11 or higher."
        exit 1
    fi
fi
