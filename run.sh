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
        # Install dependencies if needed
        if ! python3 -c "import numpy" &> /dev/null; then
            echo "📥 Installing dependencies..."
            pip3 install numpy
        fi
        
        # Run the application
        python3 main.py
    else
        echo "❌ Python 3 not found. Please install Python 3.11 or higher."
        exit 1
    fi
fi
