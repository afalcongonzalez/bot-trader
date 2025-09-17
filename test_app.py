#!/usr/bin/env python3
"""
Simple test script for the options trading simulator
"""

import sys
import os
from datetime import datetime, timedelta

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from options_models import IronCondor, Straddle
    from strategy_analyzer import StrategyAnalyzer
    from trading_engine import TradingEngine
    
    print("✓ All modules imported successfully!")
    
    # Test creating strategies
    iron_condor = IronCondor(
        symbol="AAPL",
        current_price=150.0,
        expiration=(datetime.now() + timedelta(days=30)).date(),
        short_call_strike=155.0,
        long_call_strike=160.0,
        short_put_strike=145.0,
        long_put_strike=140.0,
        net_credit=2.50
    )
    
    straddle = Straddle(
        symbol="TSLA",
        strike=200.0,
        current_price=200.0,
        expiration=(datetime.now() + timedelta(days=21)).date(),
        call_premium=15.0,
        put_premium=12.0
    )
    
    print("✓ Strategies created successfully!")
    
    # Test analyzer
    analyzer = StrategyAnalyzer()
    analysis = analyzer.analyze_strategy(iron_condor)
    print("✓ Strategy analysis completed!")
    print(f"  Max Profit: ${analysis['max_profit']:.2f}")
    print(f"  Max Loss: ${analysis['max_loss']:.2f}")
    print(f"  Risk/Reward: {analysis['risk_reward_ratio']:.2f}")
    
    # Test trading engine
    engine = TradingEngine()
    engine.add_strategy(iron_condor)
    engine.add_strategy(straddle)
    print("✓ Trading engine initialized!")
    
    print("\n🎉 All tests passed! The application is ready to use.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required dependencies: pip install numpy")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
