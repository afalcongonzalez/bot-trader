#!/usr/bin/env python3
"""
Simple test without external dependencies
"""

import sys
import os
from datetime import datetime, timedelta, date

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from options_models import IronCondor, Straddle
    print("✓ Options models imported successfully!")
    
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
    print(f"  Iron Condor max profit: ${iron_condor.get_max_profit():.2f}")
    print(f"  Iron Condor max loss: ${iron_condor.get_max_loss():.2f}")
    print(f"  Straddle max loss: ${straddle.get_max_loss():.2f}")
    
    print("\n🎉 Basic functionality test passed!")
    print("The application structure is working correctly.")
    print("To use live data features, install: pip install yfinance numpy pandas")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
