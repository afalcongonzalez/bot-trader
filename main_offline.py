#!/usr/bin/env python3
"""
Options Trading Simulator (Offline Version)
A console application for simulating options trading strategies without external dependencies
"""

import sys
import json
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import argparse

from options_models import Option, OptionsStrategy, IronCondor, Straddle, Strangle
from trading_engine import TradingEngine
from strategy_analyzer_safe import StrategyAnalyzer


@dataclass
class SimulationConfig:
    """Configuration for trading simulation"""
    initial_capital: float = 10000.0
    risk_per_trade: float = 0.02  # 2% of capital per trade
    max_concurrent_trades: int = 5
    simulation_days: int = 30
    use_live_data: bool = False  # Always False for offline version


class OptionsSimulator:
    """Main application class for options trading simulation (offline version)"""
    
    def __init__(self):
        self.trading_engine = TradingEngine()
        self.analyzer = StrategyAnalyzer()
        self.config = SimulationConfig()
        self.running = True
        
    def display_menu(self):
        """Display main menu options"""
        print("\n" + "="*60)
        print("    OPTIONS TRADING SIMULATOR (OFFLINE MODE)")
        print("="*60)
        print("1. Configure Simulation")
        print("2. Add Options Data")
        print("3. Analyze Strategy")
        print("4. Run Simulation")
        print("5. View Portfolio")
        print("6. View Trade History")
        print("7. Load Sample Data")
        print("8. Export Results")
        print("9. Exit")
        print("="*60)
        
    def configure_simulation(self):
        """Configure simulation parameters"""
        print("\n--- Simulation Configuration ---")
        
        try:
            capital = float(input(f"Initial Capital (current: ${self.config.initial_capital:,.2f}): ") or self.config.initial_capital)
            risk = float(input(f"Risk per Trade % (current: {self.config.risk_per_trade*100:.1f}%): ") or self.config.risk_per_trade*100) / 100
            max_trades = int(input(f"Max Concurrent Trades (current: {self.config.max_concurrent_trades}): ") or self.config.max_concurrent_trades)
            days = int(input(f"Simulation Days (current: {self.config.simulation_days}): ") or self.config.simulation_days)
            
            self.config = SimulationConfig(capital, risk, max_trades, days, False)
            self.trading_engine.set_config(self.config)
            
            print(f"\n✓ Configuration updated:")
            print(f"  Initial Capital: ${self.config.initial_capital:,.2f}")
            print(f"  Risk per Trade: {self.config.risk_per_trade*100:.1f}%")
            print(f"  Max Concurrent Trades: {self.config.max_concurrent_trades}")
            print(f"  Simulation Days: {self.config.simulation_days}")
            print(f"  Use Live Data: False (Offline Mode)")
            
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
        print("Using simulated data (offline mode)")
        
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
        print("Welcome to Options Trading Simulator (Offline Mode)!")
        print("This tool helps you simulate options trading strategies.")
        print("For live data features, install: pip install yfinance numpy pandas")
        
        while self.running:
            try:
                self.display_menu()
                choice = input("\nSelect an option (1-9): ").strip()
                
                if choice == "1":
                    self.configure_simulation()
                elif choice == "2":
                    self.add_options_data()
                elif choice == "3":
                    self.analyze_strategy()
                elif choice == "4":
                    self.run_simulation()
                elif choice == "5":
                    self.view_portfolio()
                elif choice == "6":
                    self.view_trade_history()
                elif choice == "7":
                    self.load_sample_data()
                elif choice == "8":
                    self.export_results()
                elif choice == "9":
                    print("Goodbye!")
                    self.running = False
                else:
                    print("❌ Invalid choice. Please select 1-9.")
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                self.running = False
            except Exception as e:
                print(f"❌ An error occurred: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Options Trading Simulator (Offline)")
    parser.add_argument("--config", help="Load configuration from JSON file")
    parser.add_argument("--sample", action="store_true", help="Load sample data and exit")
    
    args = parser.parse_args()
    
    simulator = OptionsSimulator()
        
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
