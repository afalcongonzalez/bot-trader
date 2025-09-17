#!/usr/bin/env python3
"""
Demo script showing live data functionality
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
    
    print("🚀 Options Trading Simulator - Live Data Demo")
    print("=" * 50)
    
    # Initialize components
    fetcher = YahooFinanceDataFetcher()
    analyzer = StrategyAnalyzer()
    
    # Demo 1: Market Status
    print("\n📊 Market Status:")
    status = fetcher.get_market_status()
    print(f"  Market State: {status['market_state']}")
    print(f"  Market Open: {'Yes' if status['is_open'] else 'No'}")
    
    # Demo 2: Stock Prices
    print("\n💰 Current Stock Prices:")
    symbols = ['AAPL', 'TSLA', 'SPY', 'QQQ']
    for symbol in symbols:
        price = fetcher.get_stock_price(symbol)
        if price > 0:
            print(f"  {symbol}: ${price:.2f}")
        else:
            print(f"  {symbol}: Data unavailable")
    
    # Demo 3: Options Data for AAPL
    print("\n📈 AAPL Options Data:")
    aapl_price = fetcher.get_stock_price("AAPL")
    if aapl_price > 0:
        print(f"  Current Price: ${aapl_price:.2f}")
        
        # Get expirations
        expirations = fetcher.get_available_expirations("AAPL")
        if expirations:
            print(f"  Available Expirations: {len(expirations)}")
            print(f"  Next 3: {[exp.strftime('%Y-%m-%d') for exp in expirations[:3]]}")
            
            # Demo Iron Condor
            print("\n  🦅 Iron Condor Data:")
            iron_condor_data = fetcher.get_iron_condor_data("AAPL", aapl_price, expirations[0])
            if iron_condor_data:
                print(f"    Short Call: ${iron_condor_data['short_call_strike']:.2f} @ ${iron_condor_data['short_call_premium']:.2f}")
                print(f"    Long Call: ${iron_condor_data['long_call_strike']:.2f} @ ${iron_condor_data['long_call_premium']:.2f}")
                print(f"    Short Put: ${iron_condor_data['short_put_strike']:.2f} @ ${iron_condor_data['short_put_premium']:.2f}")
                print(f"    Long Put: ${iron_condor_data['long_put_strike']:.2f} @ ${iron_condor_data['long_put_premium']:.2f}")
                print(f"    Net Credit: ${iron_condor_data['net_credit']:.2f}")
                
                # Create and analyze strategy
                iron_condor = IronCondor(
                    symbol="AAPL",
                    current_price=aapl_price,
                    expiration=expirations[0],
                    short_call_strike=iron_condor_data['short_call_strike'],
                    long_call_strike=iron_condor_data['long_call_strike'],
                    short_put_strike=iron_condor_data['short_put_strike'],
                    long_put_strike=iron_condor_data['long_put_strike'],
                    net_credit=iron_condor_data['net_credit']
                )
                
                analysis = analyzer.analyze_strategy(iron_condor)
                print(f"\n    📊 Analysis:")
                print(f"      Max Profit: ${analysis['max_profit']:.2f}")
                print(f"      Max Loss: ${analysis['max_loss']:.2f}")
                print(f"      Risk/Reward: {analysis['risk_reward_ratio']:.2f}")
                print(f"      Recommendation: {analysis['recommendation']}")
            
            # Demo Straddle
            print("\n  🎯 Straddle Data:")
            straddle_data = fetcher.get_straddle_data("AAPL", aapl_price, expirations[0])
            if straddle_data:
                print(f"    Strike: ${straddle_data['strike']:.2f}")
                print(f"    Call Premium: ${straddle_data['call_premium']:.2f}")
                print(f"    Put Premium: ${straddle_data['put_premium']:.2f}")
                print(f"    Total Cost: ${straddle_data['total_cost']:.2f}")
                
                # Create and analyze strategy
                straddle = Straddle(
                    symbol="AAPL",
                    strike=straddle_data['strike'],
                    current_price=aapl_price,
                    expiration=expirations[0],
                    call_premium=straddle_data['call_premium'],
                    put_premium=straddle_data['put_premium']
                )
                
                analysis = analyzer.analyze_strategy(straddle)
                print(f"\n    📊 Analysis:")
                print(f"      Max Profit: Unlimited")
                print(f"      Max Loss: ${analysis['max_loss']:.2f}")
                print(f"      Break-even Points: {analysis['break_even_points']}")
                print(f"      Recommendation: {analysis['recommendation']}")
    
    # Demo 4: Volatility
    print("\n📊 Volatility Analysis:")
    for symbol in ['AAPL', 'TSLA']:
        volatility = fetcher.get_volatility(symbol)
        if volatility > 0:
            print(f"  {symbol}: {volatility:.1%}")
    
    print("\n🎉 Demo completed! Run 'python main.py' to start the full application.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required dependencies: pip install yfinance numpy pandas")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    print("This might be due to network issues or market hours.")
    sys.exit(1)
