#!/usr/bin/env python3
"""
Test script for live data functionality
"""

import sys
import os
from datetime import datetime, timedelta

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from data_fetcher import YahooFinanceDataFetcher
    from options_models import IronCondor, Straddle
    from strategy_analyzer import StrategyAnalyzer
    
    print("✓ All modules imported successfully!")
    
    # Test data fetcher
    fetcher = YahooFinanceDataFetcher()
    
    # Test stock price
    print("\n--- Testing Stock Price Fetch ---")
    aapl_price = fetcher.get_stock_price("AAPL")
    print(f"AAPL current price: ${aapl_price:.2f}")
    
    # Test market status
    print("\n--- Testing Market Status ---")
    status = fetcher.get_market_status()
    print(f"Market state: {status['market_state']}")
    print(f"Market open: {status['is_open']}")
    
    # Test available expirations
    print("\n--- Testing Options Expirations ---")
    expirations = fetcher.get_available_expirations("AAPL")
    print(f"AAPL expirations: {[exp.strftime('%Y-%m-%d') for exp in expirations[:3]]}")
    
    # Test iron condor data
    print("\n--- Testing Iron Condor Data ---")
    if expirations:
        iron_condor_data = fetcher.get_iron_condor_data("AAPL", aapl_price, expirations[0])
        if iron_condor_data:
            print(f"Iron Condor data: {iron_condor_data}")
        else:
            print("No iron condor data available")
    
    # Test straddle data
    print("\n--- Testing Straddle Data ---")
    if expirations:
        straddle_data = fetcher.get_straddle_data("AAPL", aapl_price, expirations[0])
        if straddle_data:
            print(f"Straddle data: {straddle_data}")
        else:
            print("No straddle data available")
    
    # Test volatility
    print("\n--- Testing Volatility Calculation ---")
    volatility = fetcher.get_volatility("AAPL")
    print(f"AAPL volatility: {volatility:.2%}")
    
    print("\n�� Live data tests completed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required dependencies: pip install yfinance numpy pandas")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
