"""
Automated Trading Engine with AI Strategy Generation
"""

import time
import threading
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional
import logging
import json

from options_models import IronCondor, Straddle, Strangle, CallSpread, PutSpread
from trading_engine import TradingEngine
from strategy_analyzer_safe import StrategyAnalyzer
from ai_strategy_generator import AIStrategyGenerator

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AutomatedTrader:
    """Automated trading engine that monitors markets and executes trades"""
    
    def __init__(self, api_key: Optional[str] = None, initial_capital: float = 10000.0):
        self.trading_engine = TradingEngine()
        self.analyzer = StrategyAnalyzer()
        self.ai_generator = AIStrategyGenerator(api_key)
        self.running = False
        self.monitoring_interval = 300  # 5 minutes
        self.trading_interval = 1800  # 30 minutes
        self.symbols_to_monitor = ['SPY', 'QQQ', 'AAPL', 'TSLA', 'MSFT', 'GOOGL']
        self.max_positions = 5
        self.risk_per_trade = 0.02  # 2%
        
        # Set up trading engine
        from trading_engine import SimulationConfig
        config = SimulationConfig(
            initial_capital=initial_capital,
            risk_per_trade=self.risk_per_trade,
            max_concurrent_trades=self.max_positions,
            simulation_days=365,
            use_live_data=True
        )
        self.trading_engine.set_config(config)
        
        # Trading history
        self.trade_log = []
        self.performance_metrics = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_pnl': 0.0,
            'max_drawdown': 0.0,
            'sharpe_ratio': 0.0
        }
        
    def start_trading(self):
        """Start the automated trading system"""
        logger.info("🚀 Starting Automated Trading System")
        self.running = True
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        monitor_thread.start()
        
        # Start trading thread
        trading_thread = threading.Thread(target=self._trading_loop, daemon=True)
        trading_thread.start()
        
        # Start dashboard thread
        dashboard_thread = threading.Thread(target=self._dashboard_loop, daemon=True)
        dashboard_thread.start()
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Stopping Automated Trading System")
            self.running = False
    
    def _monitoring_loop(self):
        """Monitor market conditions and update data"""
        while self.running:
            try:
                logger.info("📊 Monitoring market conditions...")
                
                # Get market data
                market_data = self._get_market_data()
                
                # Log market status
                self._log_market_status(market_data)
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def _trading_loop(self):
        """Main trading loop that generates and executes strategies"""
        while self.running:
            try:
                logger.info("🤖 AI Strategy Generation and Execution")
                
                # Get current market data
                market_data = self._get_market_data()
                
                # Check if we should trade
                if self._should_trade():
                    # Generate AI strategy
                    strategy_recommendation = self._generate_ai_strategy(market_data)
                    
                    if strategy_recommendation:
                        # Execute the strategy
                        self._execute_strategy(strategy_recommendation)
                
                time.sleep(self.trading_interval)
                
            except Exception as e:
                logger.error(f"Error in trading loop: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying
    
    def _dashboard_loop(self):
        """Display real-time dashboard"""
        while self.running:
            try:
                self._display_dashboard()
                time.sleep(10)  # Update every 10 seconds
            except Exception as e:
                logger.error(f"Error in dashboard loop: {e}")
                time.sleep(10)
    
    def _get_market_data(self) -> Dict:
        """Get current market data"""
        try:
            # This would normally fetch real data
            # For now, we'll simulate market data
            import random
            
            market_data = {
                'vix': random.uniform(15, 35),
                'spy_price': random.uniform(400, 450),
                'trend': random.choice(['Bullish', 'Bearish', 'Neutral']),
                'volatility': random.uniform(0.15, 0.35),
                'time_of_day': datetime.now().strftime('%H:%M'),
                'market_open': True
            }
            
            return market_data
            
        except Exception as e:
            logger.error(f"Error getting market data: {e}")
            return {
                'vix': 20,
                'spy_price': 425,
                'trend': 'Neutral',
                'volatility': 0.20,
                'time_of_day': datetime.now().strftime('%H:%M'),
                'market_open': True
            }
    
    def _should_trade(self) -> bool:
        """Determine if we should generate new trades"""
        # Check if we have room for more positions
        current_positions = len(self.trading_engine.positions)
        if current_positions >= self.max_positions:
            return False
        
        # Check if market is open (simplified)
        current_hour = datetime.now().hour
        if current_hour < 9 or current_hour > 16:  # Outside market hours
            return False
        
        return True
    
    def _generate_ai_strategy(self, market_data: Dict) -> Optional[Dict]:
        """Generate AI strategy recommendation"""
        try:
            # Select a symbol to trade
            symbol = self._select_trading_symbol()
            if not symbol:
                return None
            
            # Get current price (simulated)
            current_price = self._get_symbol_price(symbol)
            
            # Generate AI recommendation
            recommendation = self.ai_generator.get_strategy_recommendation(
                symbol, market_data, current_price
            )
            
            logger.info(f"🎯 AI Strategy Generated for {symbol}")
            logger.info(f"   Strategy: {recommendation['strategy']['strategy_type']}")
            logger.info(f"   Reasoning: {recommendation['strategy']['reasoning']}")
            logger.info(f"   Risk Level: {recommendation['strategy']['risk_level']}")
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error generating AI strategy: {e}")
            return None
    
    def _select_trading_symbol(self) -> Optional[str]:
        """Select a symbol to trade based on current positions"""
        # Avoid symbols we already have positions in
        current_symbols = [pos.symbol for pos in self.trading_engine.positions]
        
        available_symbols = [s for s in self.symbols_to_monitor if s not in current_symbols]
        
        if available_symbols:
            import random
            return random.choice(available_symbols)
        
        return None
    
    def _get_symbol_price(self, symbol: str) -> float:
        """Get current price for a symbol (simulated)"""
        # This would normally fetch real price data
        import random
        
        base_prices = {
            'SPY': 425,
            'QQQ': 380,
            'AAPL': 150,
            'TSLA': 200,
            'MSFT': 300,
            'GOOGL': 140
        }
        
        base_price = base_prices.get(symbol, 100)
        # Add some random movement
        price = base_price * (1 + random.uniform(-0.02, 0.02))
        
        return round(price, 2)
    
    def _execute_strategy(self, recommendation: Dict):
        """Execute the AI-recommended strategy"""
        try:
            strategy = recommendation['strategy']
            symbol = strategy['symbol']
            strategy_type = strategy['strategy_type']
            parameters = strategy['parameters']
            
            # Create the strategy object
            strategy_obj = self._create_strategy_object(
                symbol, strategy_type, parameters
            )
            
            if strategy_obj:
                # Add to trading engine
                self.trading_engine.add_strategy(strategy_obj)
                
                # Log the trade
                trade_log = {
                    'timestamp': datetime.now().isoformat(),
                    'symbol': symbol,
                    'strategy_type': strategy_type,
                    'reasoning': strategy['reasoning'],
                    'risk_level': strategy['risk_level'],
                    'confidence': strategy.get('confidence', 0.5),
                    'parameters': parameters
                }
                
                self.trade_log.append(trade_log)
                self.performance_metrics['total_trades'] += 1
                
                logger.info(f"✅ Strategy Executed: {symbol} {strategy_type}")
                
        except Exception as e:
            logger.error(f"Error executing strategy: {e}")
    
    def _create_strategy_object(self, symbol: str, strategy_type: str, parameters: Dict):
        """Create a strategy object from AI parameters"""
        try:
            current_price = self._get_symbol_price(symbol)
            expiration = date.today() + timedelta(days=parameters.get('expiration_days', 30))
            
            if strategy_type == 'Iron Condor':
                strikes = parameters.get('strikes', {})
                return IronCondor(
                    symbol=symbol,
                    current_price=current_price,
                    expiration=expiration,
                    short_call_strike=strikes.get('short_call', current_price * 1.05),
                    long_call_strike=strikes.get('long_call', current_price * 1.10),
                    short_put_strike=strikes.get('short_put', current_price * 0.95),
                    long_put_strike=strikes.get('long_put', current_price * 0.90),
                    net_credit=parameters.get('net_credit', 2.0)
                )
            
            elif strategy_type == 'Straddle':
                strike = parameters.get('strikes', {}).get('strike', current_price)
                return Straddle(
                    symbol=symbol,
                    strike=strike,
                    current_price=current_price,
                    expiration=expiration,
                    call_premium=parameters.get('premiums', {}).get('call', 10.0),
                    put_premium=parameters.get('premiums', {}).get('put', 8.0)
                )
            
            elif strategy_type == 'Strangle':
                strikes = parameters.get('strikes', {})
                return Strangle(
                    symbol=symbol,
                    call_strike=strikes.get('call', current_price * 1.05),
                    put_strike=strikes.get('put', current_price * 0.95),
                    current_price=current_price,
                    expiration=expiration,
                    call_premium=parameters.get('premiums', {}).get('call', 8.0),
                    put_premium=parameters.get('premiums', {}).get('put', 6.0)
                )
            
            # Add more strategy types as needed
            
        except Exception as e:
            logger.error(f"Error creating strategy object: {e}")
            return None
    
    def _display_dashboard(self):
        """Display real-time trading dashboard"""
        try:
            # Clear screen (works on most terminals)
            print('\033[2J\033[H', end='')
            
            print("🤖 AUTOMATED OPTIONS TRADING SYSTEM")
            print("=" * 60)
            print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"🔄 Status: {'RUNNING' if self.running else 'STOPPED'}")
            print()
            
            # Portfolio Summary
            portfolio = self.trading_engine.get_portfolio()
            print("💰 PORTFOLIO SUMMARY")
            print(f"   Cash: ${portfolio['cash']:,.2f}")
            print(f"   Total Value: ${portfolio['total_value']:,.2f}")
            print(f"   Open Positions: {len(portfolio['positions'])}")
            print()
            
            # Performance Metrics
            print("📊 PERFORMANCE METRICS")
            print(f"   Total Trades: {self.performance_metrics['total_trades']}")
            print(f"   Winning Trades: {self.performance_metrics['winning_trades']}")
            print(f"   Losing Trades: {self.performance_metrics['losing_trades']}")
            print(f"   Total P&L: ${self.performance_metrics['total_pnl']:,.2f}")
            print()
            
            # Current Positions
            if portfolio['positions']:
                print("📈 CURRENT POSITIONS")
                for i, position in enumerate(portfolio['positions'][:5], 1):
                    print(f"   {i}. {position['symbol']} - {position['strategy_type']}")
                    print(f"      P&L: ${position['unrealized_pnl']:,.2f}")
                print()
            
            # Recent Trades
            if self.trade_log:
                print("📋 RECENT AI STRATEGIES")
                for trade in self.trade_log[-3:]:
                    print(f"   {trade['symbol']} - {trade['strategy_type']}")
                    print(f"      Risk: {trade['risk_level']} | Confidence: {trade['confidence']:.1%}")
                    print(f"      {trade['reasoning'][:50]}...")
                print()
            
            # Market Data
            market_data = self._get_market_data()
            print("🌐 MARKET CONDITIONS")
            print(f"   VIX: {market_data['vix']:.1f}")
            print(f"   SPY: ${market_data['spy_price']:.2f}")
            print(f"   Trend: {market_data['trend']}")
            print(f"   Volatility: {market_data['volatility']:.1%}")
            print()
            
            print("Press Ctrl+C to stop...")
            
        except Exception as e:
            logger.error(f"Error displaying dashboard: {e}")
    
    def _log_market_status(self, market_data: Dict):
        """Log current market status"""
        logger.info(f"📊 Market Status - VIX: {market_data['vix']:.1f}, "
                   f"SPY: ${market_data['spy_price']:.2f}, "
                   f"Trend: {market_data['trend']}")
    
    def stop_trading(self):
        """Stop the automated trading system"""
        self.running = False
        logger.info("🛑 Automated trading system stopped")
    
    def get_performance_report(self) -> Dict:
        """Get detailed performance report"""
        portfolio = self.trading_engine.get_portfolio()
        trade_history = self.trading_engine.get_trade_history()
        
        # Calculate additional metrics
        if trade_history:
            winning_trades = [t for t in trade_history if t['pnl'] > 0]
            losing_trades = [t for t in trade_history if t['pnl'] < 0]
            
            self.performance_metrics['winning_trades'] = len(winning_trades)
            self.performance_metrics['losing_trades'] = len(losing_trades)
            self.performance_metrics['total_pnl'] = sum(t['pnl'] for t in trade_history)
        
        return {
            'portfolio': portfolio,
            'performance_metrics': self.performance_metrics,
            'trade_log': self.trade_log,
            'trade_history': trade_history
        }
