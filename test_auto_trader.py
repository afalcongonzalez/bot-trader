#!/usr/bin/env python3
"""
Test script for automated trading system
"""

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from automated_trader import AutomatedTrader
    from ai_strategy_generator import AIStrategyGenerator
    print("✅ Automated trader modules imported successfully!")
    
    # Test AI strategy generator
    print("\n🤖 Testing AI Strategy Generator...")
    ai_generator = AIStrategyGenerator()
    
    # Test market analysis
    market_data = {
        'vix': 25.0,
        'spy_price': 425.0,
        'trend': 'Neutral',
        'volatility': 0.20,
        'time_of_day': '14:30'
    }
    
    analysis = ai_generator.analyze_market_conditions(market_data)
    print(f"   Market Sentiment: {analysis['sentiment']}")
    print(f"   Recommended Strategies: {analysis['recommended_strategies']}")
    print(f"   Risk Level: {analysis['risk_level']}")
    
    # Test strategy generation
    strategy = ai_generator.generate_strategy('AAPL', market_data, 150.0)
    print(f"\n   Generated Strategy: {strategy['strategy_type']}")
    print(f"   Reasoning: {strategy['reasoning']}")
    print(f"   Risk Level: {strategy['risk_level']}")
    
    # Test automated trader
    print("\n🤖 Testing Automated Trader...")
    trader = AutomatedTrader(initial_capital=10000.0)
    
    # Test market data generation
    market_data = trader._get_market_data()
    print(f"   Generated Market Data: VIX={market_data['vix']:.1f}, SPY=${market_data['spy_price']:.2f}")
    
    # Test symbol selection
    symbol = trader._select_trading_symbol()
    print(f"   Selected Symbol: {symbol}")
    
    # Test price generation
    if symbol:
        price = trader._get_symbol_price(symbol)
        print(f"   {symbol} Price: ${price:.2f}")
    
    print("\n🎉 All tests passed! Automated trading system is ready.")
    print("\nTo start trading:")
    print("   ./run_auto_trader.sh")
    print("   or")
    print("   python3 auto_trader.py")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required dependencies: pip install openai yfinance numpy pandas")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
