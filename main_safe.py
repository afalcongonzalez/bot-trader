#!/usr/bin/env python3
"""
Options Trading Simulator with Live Data (Safe Version)
A console application for simulating options trading strategies with optional live data
"""

import sys
import json
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import argparse

from options_models import Option, OptionsStrategy, IronCondor, Straddle, Strangle
from trading_engine import TradingEngine
from strategy_analyzer import StrategyAnalyzer

# Try to import live data components, but don't fail if they're not available
try:
    from data_fetcher import YahooFinanceDataFetcher
    LIVE_DATA_AVAILABLE = True
except ImportError:
    print("⚠️  Live data features not available. Install yfinance, numpy, pandas for full functionality.")
    LIVE_DATA_AVAILABLE = False
    
    # Create a dummy data fetcher
    class YahooFinanceDataFetcher:
        def get_stock_price(self, symbol):
            print(f"❌ Live data not available. Please install: pip install yfinance numpy pandas")
            return 0.0
        def get_market_status(self):
            return {'market_state': 'UNKNOWN', 'is_open': False, 'last_update': None}
        def get_available_expirations(self, symbol):
            return []
        def get_iron_condor_data(self, symbol, current_price, expiration):
            return {}
        def get_straddle_data(self, symbol, current_price, expiration):
            return {}
        def get_strangle_data(self, symbol, current_price, expiration):
            return {}


@dataclass
class SimulationConfig:
    """Configuration for trading simulation"""
    initial_capital: float = 10000.0
    risk_per_trade: float = 0.02  # 2% of capital per trade
    max_concurrent_trades: int = 5
    simulation_days: int = 30
    use_live_data: bool = LIVE_DATA_AVAILABLE


class OptionsSimulator:
    """Main application class for options trading simulation with optional live data"""
    
    def __init__(self):
        self.data_fetcher = YahooFinanceDataFetcher()
        self.trading_engine = TradingEngine()
        self.trading_engine.set_data_fetcher(self.data_fetcher)
        self.analyzer = StrategyAnalyzer()
        self.config = SimulationConfig()
        self.running = True
        
    def display_menu(self):
        """Display main menu options"""
        print("\n" + "="*60)
        if LIVE_DATA_AVAILABLE:
            print("    OPTIONS TRADING SIMULATOR (LIVE DATA)")
        else:
            print("    OPTIONS TRADING SIMULATOR (OFFLINE MODE)")
        print("="*60)
        print("1. Configure Simulation")
        print("2. Add Options Data")
        if LIVE_DATA_AVAILABLE:
            print("3. Fetch Live Data")
        else:
            print("3. Fetch Live Data (Not Available)")
        print("4. Analyze Strategy")
        print("5. Run Simulation")
        print("6. View Portfolio")
        print("7. View Trade History")
        print("8. Load Sample Data")
        if LIVE_DATA_AVAILABLE:
            print("9. Market Status")
        else:
            print("9. Market Status (Not Available)")
        print("10. Export Results")
        print("11. Exit")
        print("="*60)
        
    def configure_simulation(self):
        """Configure simulation parameters"""
        print("\n--- Simulation Configuration ---")
        
        try:
            capital = float(input(f"Initial Capital (current: ${self.config.initial_capital:,.2f}): ") or self.config.initial_capital)
            risk = float(input(f"Risk per Trade % (current: {self.config.risk_per_trade*100:.1f}%): ") or self.config.risk_per_trade*100) / 100
            max_trades = int(input(f"Max Concurrent Trades (current: {self.config.max_concurrent_trades}): ") or self.config.max_concurrent_trades)
            days = int(input(f"Simulation Days (current: {self.config.simulation_days}): ") or self.config.simulation_days)
            
            if LIVE_DATA_AVAILABLE:
                use_live = input(f"Use Live Data (current: {self.config.use_live_data}) [y/n]: ").lower().startswith('y') if input() else self.config.use_live_data
            else:
                use_live = False
                print("Live data not available - using simulated data only")
            
            self.config = SimulationConfig(capital, risk, max_trades, days, use_live)
            self.trading_engine.set_config(self.config)
            
            print(f"\n✓ Configuration updated:")
            print(f"  Initial Capital: ${self.config.initial_capital:,.2f}")
            print(f"  Risk per Trade: {self.config.risk_per_trade*100:.1f}%")
            print(f"  Max Concurrent Trades: {self.config.max_concurrent_trades}")
            print(f"  Simulation Days: {self.config.simulation_days}")
            print(f"  Use Live Data: {self.config.use_live_data}")
            
        except ValueError:
            print("❌ Invalid input. Please enter valid numbers.")
            
    def add_options_data(self):
        """Add options data manually"""
        print("\n--- Add Options Data ---")
        print("1. Add Single Option")
        print("2. Add Iron Condor")
        print("3. Add Straddle")
        print("4. Add Strangle")
        print("5. Back to Main Menu")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            self._add_single_option()
        elif choice == "2":
            self._add_iron_condor()
        elif choice == "3":
            self._add_straddle()
        elif choice == "4":
            self._add_strangle()
        elif choice == "5":
            return
        else:
            print("❌ Invalid choice")
            
    def fetch_live_data(self):
        """Fetch live options data"""
        if not LIVE_DATA_AVAILABLE:
            print("❌ Live data features not available.")
            print("To enable live data, install: pip install yfinance numpy pandas")
            return
            
        print("\n--- Fetch Live Options Data ---")
        
        symbol = input("Enter symbol (e.g., AAPL): ").strip().upper()
        if not symbol:
            print("❌ Symbol is required")
            return
            
        print(f"Fetching data for {symbol}...")
        
        # Get current stock price
        current_price = self.data_fetcher.get_stock_price(symbol)
        if current_price == 0:
            print(f"❌ Could not fetch price for {symbol}")
            return
            
        print(f"Current {symbol} price: ${current_price:.2f}")
        
        # Get available expirations
        expirations = self.data_fetcher.get_available_expirations(symbol)
        if not expirations:
            print(f"❌ No options data available for {symbol}")
            return
            
        print(f"Available expirations: {[exp.strftime('%Y-%m-%d') for exp in expirations[:5]]}")
        
        # Let user choose expiration
        try:
            exp_input = input("Enter expiration date (YYYY-MM-DD) or press Enter for closest: ").strip()
            if exp_input:
                expiration = datetime.strptime(exp_input, "%Y-%m-%d").date()
            else:
                expiration = expirations[0]
                
            if expiration not in expirations:
                print(f"❌ Expiration {expiration} not available")
                return
                
        except ValueError:
            print("❌ Invalid date format")
            return
            
        # Show strategy options
        print("\nAvailable strategies:")
        print("1. Iron Condor")
        print("2. Straddle")
        print("3. Strangle")
        
        strategy_choice = input("Select strategy (1-3): ").strip()
        
        if strategy_choice == "1":
            self._fetch_iron_condor(symbol, current_price, expiration)
        elif strategy_choice == "2":
            self._fetch_straddle(symbol, current_price, expiration)
        elif strategy_choice == "3":
            self._fetch_strangle(symbol, current_price, expiration)
        else:
            print("❌ Invalid choice")
            
    def _fetch_iron_condor(self, symbol: str, current_price: float, expiration: date):
        """Fetch iron condor data"""
        print("Fetching Iron Condor data...")
        
        data = self.data_fetcher.get_iron_condor_data(symbol, current_price, expiration)
        if not data:
            print("❌ Could not fetch iron condor data")
            return
            
        print(f"\nIron Condor Data for {symbol}:")
        print(f"  Short Call: ${data['short_call_strike']:.2f} @ ${data['short_call_premium']:.2f}")
        print(f"  Long Call: ${data['long_call_strike']:.2f} @ ${data['long_call_premium']:.2f}")
        print(f"  Short Put: ${data['short_put_strike']:.2f} @ ${data['short_put_premium']:.2f}")
        print(f"  Long Put: ${data['long_put_strike']:.2f} @ ${data['long_put_premium']:.2f}")
        print(f"  Net Credit: ${data['net_credit']:.2f}")
        
        if input("Add this Iron Condor? (y/n): ").lower().startswith('y'):
            iron_condor = IronCondor(
                symbol=symbol,
                current_price=current_price,
                expiration=expiration,
                short_call_strike=data['short_call_strike'],
                long_call_strike=data['long_call_strike'],
                short_put_strike=data['short_put_strike'],
                long_put_strike=data['long_put_strike'],
                net_credit=data['net_credit']
            )
            
            self.trading_engine.add_strategy(iron_condor)
            print("✓ Iron Condor added!")
            
    def _fetch_straddle(self, symbol: str, current_price: float, expiration: date):
        """Fetch straddle data"""
        print("Fetching Straddle data...")
        
        data = self.data_fetcher.get_straddle_data(symbol, current_price, expiration)
        if not data:
            print("❌ Could not fetch straddle data")
            return
            
        print(f"\nStraddle Data for {symbol}:")
        print(f"  Strike: ${data['strike']:.2f}")
        print(f"  Call Premium: ${data['call_premium']:.2f}")
        print(f"  Put Premium: ${data['put_premium']:.2f}")
        print(f"  Total Cost: ${data['total_cost']:.2f}")
        
        if input("Add this Straddle? (y/n): ").lower().startswith('y'):
            straddle = Straddle(
                symbol=symbol,
                strike=data['strike'],
                current_price=current_price,
                expiration=expiration,
                call_premium=data['call_premium'],
                put_premium=data['put_premium']
            )
            
            self.trading_engine.add_strategy(straddle)
            print("✓ Straddle added!")
            
    def _fetch_strangle(self, symbol: str, current_price: float, expiration: date):
        """Fetch strangle data"""
        print("Fetching Strangle data...")
        
        data = self.data_fetcher.get_strangle_data(symbol, current_price, expiration)
        if not data:
            print("❌ Could not fetch strangle data")
            return
            
        print(f"\nStrangle Data for {symbol}:")
        print(f"  Call Strike: ${data['call_strike']:.2f} @ ${data['call_premium']:.2f}")
        print(f"  Put Strike: ${data['put_strike']:.2f} @ ${data['put_premium']:.2f}")
        print(f"  Total Cost: ${data['total_cost']:.2f}")
        
        if input("Add this Strangle? (y/n): ").lower().startswith('y'):
            strangle = Strangle(
                symbol=symbol,
                call_strike=data['call_strike'],
                put_strike=data['put_strike'],
                current_price=current_price,
                expiration=expiration,
                call_premium=data['call_premium'],
                put_premium=data['put_premium']
            )
            
            self.trading_engine.add_strategy(strangle)
            print("✓ Strangle added!")
            
    def _add_single_option(self):
        """Add a single option"""
        try:
            symbol = input("Underlying Symbol (e.g., AAPL): ").strip().upper()
            option_type = input("Type (PUT/CALL): ").strip().upper()
            strike = float(input("Strike Price: "))
            expiration = input("Expiration Date (YYYY-MM-DD): ").strip()
            premium = float(input("Premium: "))
            
            option = Option(
                symbol=symbol,
                option_type=option_type,
                strike=strike,
                expiration=datetime.strptime(expiration, "%Y-%m-%d").date(),
                premium=premium,
                current_price=strike  # Default to strike, can be updated
            )
            
            self.trading_engine.add_option(option)
            print(f"✓ Added {option_type} option: {symbol} ${strike} exp {expiration}")
            
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
            
    def _add_iron_condor(self):
        """Add an iron condor strategy"""
        try:
            symbol = input("Underlying Symbol (e.g., AAPL): ").strip().upper()
            current_price = float(input("Current Stock Price: "))
            expiration = input("Expiration Date (YYYY-MM-DD): ").strip()
            
            # Iron condor: sell call spread + sell put spread
            short_call_strike = float(input("Short Call Strike: "))
            long_call_strike = float(input("Long Call Strike: "))
            short_put_strike = float(input("Short Put Strike: "))
            long_put_strike = float(input("Long Put Strike: "))
            
            net_credit = float(input("Net Credit Received: "))
            
            iron_condor = IronCondor(
                symbol=symbol,
                current_price=current_price,
                expiration=datetime.strptime(expiration, "%Y-%m-%d").date(),
                short_call_strike=short_call_strike,
                long_call_strike=long_call_strike,
                short_put_strike=short_put_strike,
                long_put_strike=long_put_strike,
                net_credit=net_credit
            )
            
            self.trading_engine.add_strategy(iron_condor)
            print(f"✓ Added Iron Condor: {symbol} exp {expiration}")
            
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
            
    def _add_straddle(self):
        """Add a straddle strategy"""
        try:
            symbol = input("Underlying Symbol (e.g., AAPL): ").strip().upper()
            strike = float(input("Strike Price: "))
            current_price = float(input("Current Stock Price: "))
            expiration = input("Expiration Date (YYYY-MM-DD): ").strip()
            call_premium = float(input("Call Premium: "))
            put_premium = float(input("Put Premium: "))
            
            straddle = Straddle(
                symbol=symbol,
                strike=strike,
                current_price=current_price,
                expiration=datetime.strptime(expiration, "%Y-%m-%d").date(),
                call_premium=call_premium,
                put_premium=put_premium
            )
            
            self.trading_engine.add_strategy(straddle)
            print(f"✓ Added Straddle: {symbol} ${strike} exp {expiration}")
            
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
            
    def _add_strangle(self):
        """Add a strangle strategy"""
        try:
            symbol = input("Underlying Symbol (e.g., AAPL): ").strip().upper()
            call_strike = float(input("Call Strike Price: "))
            put_strike = float(input("Put Strike Price: "))
            current_price = float(input("Current Stock Price: "))
            expiration = input("Expiration Date (YYYY-MM-DD): ").strip()
            call_premium = float(input("Call Premium: "))
            put_premium = float(input("Put Premium: "))
            
            strangle = Strangle(
                symbol=symbol,
                call_strike=call_strike,
                put_strike=put_strike,
                current_price=current_price,
                expiration=datetime.strptime(expiration, "%Y-%m-%d").date(),
                call_premium=call_premium,
                put_premium=put_premium
            )
            
            self.trading_engine.add_strategy(strangle)
            print(f"✓ Added Strangle: {symbol} exp {expiration}")
            
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
            
    def analyze_strategy(self):
        """Analyze current strategies"""
        if not self.trading_engine.strategies:
            print("❌ No strategies to analyze. Add some options data first.")
            return
            
        print("\n--- Strategy Analysis ---")
        
        for i, strategy in enumerate(self.trading_engine.strategies, 1):
            print(f"\nStrategy {i}: {strategy.__class__.__name__}")
            
            # Update current price if using live data
            if self.config.use_live_data and LIVE_DATA_AVAILABLE:
                current_price = self.data_fetcher.get_stock_price(strategy.symbol)
                if current_price > 0:
                    strategy.current_price = current_price
                    print(f"  Updated {strategy.symbol} price: ${current_price:.2f}")
            
            analysis = self.analyzer.analyze_strategy(strategy)
            
            print(f"  Symbol: {strategy.symbol}")
            print(f"  Current Price: ${strategy.current_price:.2f}")
            print(f"  Expiration: {strategy.expiration}")
            print(f"  Days to Expiration: {strategy.days_to_expiration}")
            print(f"  Max Profit: ${analysis['max_profit']:.2f}")
            print(f"  Max Loss: ${analysis['max_loss']:.2f}")
            print(f"  Break-even Points: {analysis['break_even_points']}")
            print(f"  Risk/Reward Ratio: {analysis['risk_reward_ratio']:.2f}")
            print(f"  Recommendation: {analysis['recommendation']}")
            
    def run_simulation(self):
        """Run the trading simulation"""
        if not self.trading_engine.strategies:
            print("❌ No strategies to simulate. Add some options data first.")
            return
            
        print("\n--- Running Simulation ---")
        print(f"Simulating {self.config.simulation_days} days with ${self.config.initial_capital:,.2f} capital...")
        print(f"Using {'live' if self.config.use_live_data and LIVE_DATA_AVAILABLE else 'simulated'} data")
        
        results = self.trading_engine.run_simulation()
        
        print(f"\n✓ Simulation Complete!")
        print(f"  Final Portfolio Value: ${results['final_value']:,.2f}")
        print(f"  Total Return: {results['total_return']:.2f}%")
        print(f"  Total Trades: {results['total_trades']}")
        print(f"  Winning Trades: {results['winning_trades']}")
        print(f"  Losing Trades: {results['losing_trades']}")
        print(f"  Win Rate: {results['win_rate']:.1f}%")
        
    def view_portfolio(self):
        """View current portfolio"""
        portfolio = self.trading_engine.get_portfolio()
        
        print("\n--- Current Portfolio ---")
        print(f"Cash: ${portfolio['cash']:,.2f}")
        print(f"Total Value: ${portfolio['total_value']:,.2f}")
        print(f"Open Positions: {len(portfolio['positions'])}")
        
        if portfolio['positions']:
            print("\nOpen Positions:")
            for position in portfolio['positions']:
                print(f"  {position['symbol']} - {position['strategy_type']} - P&L: ${position['unrealized_pnl']:,.2f}")
                
    def view_trade_history(self):
        """View trade history"""
        history = self.trading_engine.get_trade_history()
        
        print("\n--- Trade History ---")
        if not history:
            print("No trades executed yet.")
            return
            
        for trade in history[-10:]:  # Show last 10 trades
            print(f"  {trade['date']} - {trade['symbol']} - {trade['action']} - P&L: ${trade['pnl']:,.2f}")
            
    def load_sample_data(self):
        """Load sample options data for testing"""
        print("\n--- Loading Sample Data ---")
        
        # Sample AAPL Iron Condor
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
        
        # Sample TSLA Straddle
        straddle = Straddle(
            symbol="TSLA",
            strike=200.0,
            current_price=200.0,
            expiration=(datetime.now() + timedelta(days=21)).date(),
            call_premium=15.0,
            put_premium=12.0
        )
        
        self.trading_engine.add_strategy(iron_condor)
        self.trading_engine.add_strategy(straddle)
        
        print("✓ Loaded sample AAPL Iron Condor and TSLA Straddle")
        
    def market_status(self):
        """Show market status"""
        if not LIVE_DATA_AVAILABLE:
            print("❌ Market status not available.")
            print("To enable market status, install: pip install yfinance numpy pandas")
            return
            
        print("\n--- Market Status ---")
        
        status = self.data_fetcher.get_market_status()
        
        print(f"Market State: {status['market_state']}")
        print(f"Market Open: {'Yes' if status['is_open'] else 'No'}")
        if status['last_update']:
            print(f"Last Update: {status['last_update']}")
            
        # Show some popular symbols
        popular_symbols = ['SPY', 'QQQ', 'AAPL', 'TSLA', 'MSFT']
        print(f"\nCurrent Prices:")
        for symbol in popular_symbols:
            price = self.data_fetcher.get_stock_price(symbol)
            if price > 0:
                print(f"  {symbol}: ${price:.2f}")
                
    def export_results(self):
        """Export simulation results to JSON"""
        results = {
            'config': asdict(self.config),
            'portfolio': self.trading_engine.get_portfolio(),
            'trade_history': self.trading_engine.get_trade_history(),
            'strategies': [asdict(strategy) for strategy in self.trading_engine.strategies]
        }
        
        filename = f"options_simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
            
        print(f"✓ Results exported to {filename}")
        
    def run(self):
        """Main application loop"""
        print("Welcome to Options Trading Simulator!")
        if LIVE_DATA_AVAILABLE:
            print("This tool helps you simulate options trading strategies with real-time market data.")
        else:
            print("This tool helps you simulate options trading strategies.")
            print("For live data features, install: pip install yfinance numpy pandas")
        
        # Show market status on startup if available
        if LIVE_DATA_AVAILABLE:
            self.market_status()
        
        while self.running:
            try:
                self.display_menu()
                choice = input("\nSelect an option (1-11): ").strip()
                
                if choice == "1":
                    self.configure_simulation()
                elif choice == "2":
                    self.add_options_data()
                elif choice == "3":
                    self.fetch_live_data()
                elif choice == "4":
                    self.analyze_strategy()
                elif choice == "5":
                    self.run_simulation()
                elif choice == "6":
                    self.view_portfolio()
                elif choice == "7":
                    self.view_trade_history()
                elif choice == "8":
                    self.load_sample_data()
                elif choice == "9":
                    self.market_status()
                elif choice == "10":
                    self.export_results()
                elif choice == "11":
                    print("Goodbye!")
                    self.running = False
                else:
                    print("❌ Invalid choice. Please select 1-11.")
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                self.running = False
            except Exception as e:
                print(f"❌ An error occurred: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Options Trading Simulator")
    parser.add_argument("--config", help="Load configuration from JSON file")
    parser.add_argument("--sample", action="store_true", help="Load sample data and exit")
    parser.add_argument("--live", action="store_true", help="Enable live data by default")
    
    args = parser.parse_args()
    
    simulator = OptionsSimulator()
    
    if args.live and LIVE_DATA_AVAILABLE:
        simulator.config.use_live_data = True
        
    if args.config:
        # Load configuration from file
        try:
            with open(args.config, 'r') as f:
                config_data = json.load(f)
                simulator.config = SimulationConfig(**config_data)
                simulator.trading_engine.set_config(simulator.config)
                print(f"✓ Loaded configuration from {args.config}")
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return 1
            
    if args.sample:
        simulator.load_sample_data()
        simulator.analyze_strategy()
        return 0
        
    simulator.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
