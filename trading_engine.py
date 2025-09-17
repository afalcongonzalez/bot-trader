"""
Trading engine for simulating options trades
"""

import random
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import math

from options_models import OptionsStrategy, Option


@dataclass
class Trade:
    """Represents a completed trade"""
    id: str
    symbol: str
    strategy_type: str
    entry_date: date
    exit_date: date
    entry_price: float
    exit_price: float
    quantity: int
    pnl: float
    action: str  # "BUY" or "SELL"


@dataclass
class Position:
    """Represents an open position"""
    id: str
    symbol: str
    strategy_type: str
    entry_date: date
    entry_price: float
    quantity: int
    current_price: float
    unrealized_pnl: float


@dataclass
class SimulationConfig:
    """Configuration for trading simulation"""
    initial_capital: float = 10000.0
    risk_per_trade: float = 0.02  # 2% of capital per trade
    max_concurrent_trades: int = 5
    simulation_days: int = 30


class TradingEngine:
    """Engine for simulating options trading"""
    
    def __init__(self):
        self.cash = 10000.0
        self.positions: List[Position] = []
        self.trades: List[Trade] = []
        self.strategies: List[OptionsStrategy] = []
        self.options: List[Option] = []
        self.config = SimulationConfig()
        self.current_date = date.today()
        self.trade_counter = 0
        
    def set_config(self, config: SimulationConfig):
        """Set simulation configuration"""
        self.config = config
        self.cash = config.initial_capital
        
    def add_strategy(self, strategy: OptionsStrategy):
        """Add a strategy to the engine"""
        self.strategies.append(strategy)
        
    def add_option(self, option: Option):
        """Add a single option to the engine"""
        self.options.append(option)
        
    def calculate_position_size(self, strategy: OptionsStrategy) -> int:
        """Calculate position size based on risk management"""
        max_risk_amount = self.cash * self.config.risk_per_trade
        max_loss = abs(strategy.get_max_loss())
        
        if max_loss <= 0:
            return 0
            
        position_size = int(max_risk_amount / max_loss)
        return min(position_size, 10)  # Cap at 10 contracts
    
    def should_enter_trade(self, strategy: OptionsStrategy) -> bool:
        """Determine if we should enter a trade based on strategy analysis"""
        # Check if we have enough cash
        position_size = self.calculate_position_size(strategy)
        if position_size <= 0:
            return False
            
        # Check if we're at max concurrent trades
        if len(self.positions) >= self.config.max_concurrent_trades:
            return False
            
        # Check if strategy is not expired
        if strategy.is_expired:
            return False
            
        # Simple entry criteria (can be enhanced)
        days_to_exp = strategy.days_to_expiration
        
        # For iron condors, prefer 30-45 days to expiration
        if isinstance(strategy, type(self.strategies[0])) and hasattr(strategy, 'net_credit'):
            return 30 <= days_to_exp <= 45
            
        # For straddles/strangles, prefer 15-30 days to expiration
        if hasattr(strategy, 'total_cost'):
            return 15 <= days_to_exp <= 30
            
        return True
        
    def should_exit_trade(self, position: Position, strategy: OptionsStrategy) -> bool:
        """Determine if we should exit a trade"""
        # Exit if expired
        if strategy.is_expired:
            return True
            
        # Exit if we've held for too long (50% of time to expiration)
        days_held = (self.current_date - position.entry_date).days
        if days_held >= strategy.days_to_expiration * 0.5:
            return True
            
        # Exit if we've made 50% of max profit
        current_pnl = position.unrealized_pnl
        max_profit = strategy.get_max_profit()
        if max_profit != float('inf') and current_pnl >= max_profit * 0.5:
            return True
            
        # Exit if we've lost 50% of max loss
        max_loss = strategy.get_max_loss()
        if current_pnl <= max_loss * 0.5:
            return True
            
        return False
        
    def simulate_price_movement(self, symbol: str, current_price: float, days: int) -> float:
        """Simulate stock price movement using random walk"""
        # Simple random walk with slight upward bias
        daily_return = random.normalvariate(0.0005, 0.02)  # 0.05% daily return, 2% volatility
        price_change = current_price * daily_return * days
        new_price = current_price + price_change
        
        # Ensure price doesn't go negative
        return max(new_price, 0.01)
        
    def execute_trade(self, strategy: OptionsStrategy, action: str) -> Optional[Trade]:
        """Execute a trade"""
        position_size = self.calculate_position_size(strategy)
        if position_size <= 0:
            return None
            
        # Calculate trade value
        if action == "BUY":
            trade_value = abs(strategy.get_max_loss()) * position_size
            if trade_value > self.cash:
                return None
            self.cash -= trade_value
        else:  # SELL
            trade_value = abs(strategy.get_max_profit()) * position_size
            self.cash += trade_value
            
        # Create trade record
        trade = Trade(
            id=f"T{self.trade_counter:04d}",
            symbol=strategy.symbol,
            strategy_type=strategy.__class__.__name__,
            entry_date=self.current_date,
            exit_date=self.current_date,
            entry_price=strategy.current_price,
            exit_price=strategy.current_price,
            quantity=position_size,
            pnl=0.0,
            action=action
        )
        
        self.trade_counter += 1
        return trade
        
    def update_positions(self):
        """Update all open positions with current market data"""
        for position in self.positions:
            # Find corresponding strategy
            strategy = next((s for s in self.strategies if s.symbol == position.symbol), None)
            if not strategy:
                continue
                
            # Update current price
            position.current_price = self.simulate_price_movement(
                position.symbol, position.current_price, 1
            )
            
            # Update unrealized P&L
            strategy.current_price = position.current_price
            position.unrealized_pnl = strategy.calculate_payoff(position.current_price) * position.quantity
            
    def close_position(self, position: Position) -> Trade:
        """Close a position and create a trade record"""
        # Find corresponding strategy
        strategy = next((s for s in self.strategies if s.symbol == position.symbol), None)
        if not strategy:
            return None
            
        # Calculate final P&L
        strategy.current_price = position.current_price
        pnl = strategy.calculate_payoff(position.current_price) * position.quantity
        
        # Update cash
        self.cash += pnl
        
        # Create trade record
        trade = Trade(
            id=f"T{self.trade_counter:04d}",
            symbol=position.symbol,
            strategy_type=position.strategy_type,
            entry_date=position.entry_date,
            exit_date=self.current_date,
            entry_price=position.entry_price,
            exit_price=position.current_price,
            quantity=position.quantity,
            pnl=pnl,
            action="SELL"
        )
        
        self.trade_counter += 1
        self.trades.append(trade)
        
        # Remove position
        self.positions.remove(position)
        
        return trade
        
    def run_simulation(self) -> Dict:
        """Run the complete trading simulation"""
        print("Starting simulation...")
        
        # Reset state
        self.cash = self.config.initial_capital
        self.positions = []
        self.trades = []
        self.current_date = date.today()
        
        # Run simulation for specified days
        for day in range(self.config.simulation_days):
            self.current_date = date.today() + timedelta(days=day)
            
            # Update existing positions
            self.update_positions()
            
            # Check for exits
            positions_to_close = []
            for position in self.positions:
                strategy = next((s for s in self.strategies if s.symbol == position.symbol), None)
                if strategy and self.should_exit_trade(position, strategy):
                    positions_to_close.append(position)
                    
            # Close positions
            for position in positions_to_close:
                trade = self.close_position(position)
                if trade:
                    print(f"Day {day+1}: Closed {trade.symbol} {trade.strategy_type} - P&L: ${trade.pnl:.2f}")
            
            # Check for new entries
            for strategy in self.strategies:
                if self.should_enter_trade(strategy):
                    # Check if we already have a position in this symbol
                    existing_position = next((p for p in self.positions if p.symbol == strategy.symbol), None)
                    if not existing_position:
                        # Enter new position
                        position_size = self.calculate_position_size(strategy)
                        if position_size > 0:
                            position = Position(
                                id=f"P{len(self.positions)+1:04d}",
                                symbol=strategy.symbol,
                                strategy_type=strategy.__class__.__name__,
                                entry_date=self.current_date,
                                entry_price=strategy.current_price,
                                quantity=position_size,
                                current_price=strategy.current_price,
                                unrealized_pnl=0.0
                            )
                            
                            self.positions.append(position)
                            print(f"Day {day+1}: Opened {strategy.symbol} {strategy.__class__.__name__}")
                            
        # Close any remaining positions
        for position in self.positions[:]:
            trade = self.close_position(position)
            if trade:
                print(f"Final: Closed {trade.symbol} {trade.strategy_type} - P&L: ${trade.pnl:.2f}")
        
        # Calculate results
        total_trades = len(self.trades)
        winning_trades = len([t for t in self.trades if t.pnl > 0])
        losing_trades = total_trades - winning_trades
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_return = ((self.cash - self.config.initial_capital) / self.config.initial_capital) * 100
        
        return {
            'final_value': self.cash,
            'total_return': total_return,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'trades': [asdict(trade) for trade in self.trades]
        }
        
    def get_portfolio(self) -> Dict:
        """Get current portfolio status"""
        total_value = self.cash
        for position in self.positions:
            total_value += position.unrealized_pnl
            
        return {
            'cash': self.cash,
            'total_value': total_value,
            'positions': [asdict(position) for position in self.positions]
        }
        
    def get_trade_history(self) -> List[Dict]:
        """Get trade history"""
        return [asdict(trade) for trade in self.trades]
