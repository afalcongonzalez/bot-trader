#!/usr/bin/env python3
"""
Automated Options Trading System
Self-executing trading system with AI strategy generation
"""

import sys
import os
import argparse
import time
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    from automated_trader import AutomatedTrader
    AUTOMATED_TRADER_AVAILABLE = True
except ImportError as e:
    logger.error(f"Error importing automated trader: {e}")
    AUTOMATED_TRADER_AVAILABLE = False


def main():
    """Main entry point for automated trading system"""
    parser = argparse.ArgumentParser(description="Automated Options Trading System")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--capital", type=float, default=10000.0, help="Initial capital")
    parser.add_argument("--interval", type=int, default=300, help="Monitoring interval in seconds")
    parser.add_argument("--trading-interval", type=int, default=1800, help="Trading interval in seconds")
    parser.add_argument("--max-positions", type=int, default=5, help="Maximum concurrent positions")
    parser.add_argument("--risk", type=float, default=0.02, help="Risk per trade (0.01 = 1%)")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode (no real trades)")
    parser.add_argument("--config", help="Load configuration from JSON file")
    
    args = parser.parse_args()
    
    if not AUTOMATED_TRADER_AVAILABLE:
        logger.error("❌ Automated trader not available. Check dependencies.")
        return 1
    
    # Get API key
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.warning("⚠️  No OpenAI API key provided. AI features will use fallback strategies.")
        logger.info("   Set OPENAI_API_KEY environment variable or use --api-key")
    
    try:
        # Create automated trader
        trader = AutomatedTrader(api_key=api_key, initial_capital=args.capital)
        
        # Configure settings
        trader.monitoring_interval = args.interval
        trader.trading_interval = args.trading_interval
        trader.max_positions = args.max_positions
        trader.risk_per_trade = args.risk
        
        if args.demo:
            logger.info("🎮 Running in DEMO mode - No real trades will be executed")
        
        # Load configuration if provided
        if args.config:
            load_configuration(trader, args.config)
        
        # Display startup information
        display_startup_info(trader, args)
        
        # Start trading
        logger.info("🚀 Starting automated trading system...")
        logger.info("   Press Ctrl+C to stop")
        
        trader.start_trading()
        
    except KeyboardInterrupt:
        logger.info("🛑 Stopping automated trading system...")
        if 'trader' in locals():
            trader.stop_trading()
            display_final_report(trader)
        return 0
        
    except Exception as e:
        logger.error(f"❌ Error in automated trading system: {e}")
        return 1


def display_startup_info(trader, args):
    """Display startup information"""
    print("\n" + "="*60)
    print("🤖 AUTOMATED OPTIONS TRADING SYSTEM")
    print("="*60)
    print(f"💰 Initial Capital: ${args.capital:,.2f}")
    print(f"⏱️  Monitoring Interval: {args.interval} seconds")
    print(f"🔄 Trading Interval: {args.trading_interval} seconds")
    print(f"📊 Max Positions: {args.max_positions}")
    print(f"⚠️  Risk per Trade: {args.risk*100:.1f}%")
    print(f"🎯 Symbols: {', '.join(trader.symbols_to_monitor)}")
    print(f"🤖 AI Features: {'Enabled' if trader.ai_generator.client else 'Fallback Mode'}")
    print("="*60)
    print("📋 The system will:")
    print("   • Monitor market conditions every 5 minutes")
    print("   • Generate AI trading strategies every 30 minutes")
    print("   • Execute trades automatically")
    print("   • Display real-time dashboard")
    print("   • Log all activities to trading.log")
    print("="*60)
    print("🚀 Starting in 5 seconds...")
    time.sleep(5)


def display_final_report(trader):
    """Display final performance report"""
    try:
        report = trader.get_performance_report()
        
        print("\n" + "="*60)
        print("📊 FINAL PERFORMANCE REPORT")
        print("="*60)
        
        # Portfolio Summary
        portfolio = report['portfolio']
        print(f"💰 Final Portfolio Value: ${portfolio['total_value']:,.2f}")
        print(f"💵 Cash Remaining: ${portfolio['cash']:,.2f}")
        
        # Performance Metrics
        metrics = report['performance_metrics']
        print(f"📈 Total Trades: {metrics['total_trades']}")
        print(f"✅ Winning Trades: {metrics['winning_trades']}")
        print(f"❌ Losing Trades: {metrics['losing_trades']}")
        print(f"💸 Total P&L: ${metrics['total_pnl']:,.2f}")
        
        if metrics['total_trades'] > 0:
            win_rate = (metrics['winning_trades'] / metrics['total_trades']) * 100
            print(f"🎯 Win Rate: {win_rate:.1f}%")
        
        # Recent AI Strategies
        if report['trade_log']:
            print(f"\n🤖 AI Strategies Generated: {len(report['trade_log'])}")
            print("   Recent strategies:")
            for trade in report['trade_log'][-3:]:
                print(f"   • {trade['symbol']} - {trade['strategy_type']} ({trade['risk_level']} risk)")
        
        print("="*60)
        print("📄 Detailed log saved to: trading.log")
        
    except Exception as e:
        logger.error(f"Error generating final report: {e}")


def load_configuration(trader, config_file):
    """Load configuration from JSON file"""
    try:
        import json
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        if 'symbols' in config:
            trader.symbols_to_monitor = config['symbols']
        if 'intervals' in config:
            trader.monitoring_interval = config['intervals'].get('monitoring', 300)
            trader.trading_interval = config['intervals'].get('trading', 1800)
        if 'risk' in config:
            trader.risk_per_trade = config['risk']
        if 'max_positions' in config:
            trader.max_positions = config['max_positions']
        
        logger.info(f"✅ Configuration loaded from {config_file}")
        
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")


if __name__ == "__main__":
    sys.exit(main())
