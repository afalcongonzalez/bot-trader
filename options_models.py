"""
Options data models and strategy classes
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
import math


@dataclass
class Option:
    """Represents a single option contract"""
    symbol: str
    option_type: str  # "PUT" or "CALL"
    strike: float
    expiration: date
    premium: float
    current_price: float
    volume: int = 0
    open_interest: int = 0
    
    @property
    def days_to_expiration(self) -> int:
        """Calculate days until expiration"""
        return (self.expiration - date.today()).days
    
    @property
    def is_expired(self) -> bool:
        """Check if option is expired"""
        return self.days_to_expiration <= 0
    
    @property
    def intrinsic_value(self) -> float:
        """Calculate intrinsic value"""
        if self.option_type == "CALL":
            return max(0, self.current_price - self.strike)
        else:  # PUT
            return max(0, self.strike - self.current_price)
    
    @property
    def time_value(self) -> float:
        """Calculate time value"""
        return self.premium - self.intrinsic_value
    
    def calculate_payoff(self, stock_price: float) -> float:
        """Calculate payoff at expiration for given stock price"""
        if self.option_type == "CALL":
            return max(0, stock_price - self.strike) - self.premium
        else:  # PUT
            return max(0, self.strike - stock_price) - self.premium


class OptionsStrategy(ABC):
    """Abstract base class for options strategies"""
    
    def __init__(self, symbol: str, current_price: float, expiration: date):
        self.symbol = symbol
        self.current_price = current_price
        self.expiration = expiration
        self.entry_date = date.today()
        
    @property
    def days_to_expiration(self) -> int:
        """Calculate days until expiration"""
        return (self.expiration - date.today()).days
    
    @property
    def is_expired(self) -> bool:
        """Check if strategy is expired"""
        return self.days_to_expiration <= 0
    
    @abstractmethod
    def calculate_payoff(self, stock_price: float) -> float:
        """Calculate payoff at expiration for given stock price"""
        pass
    
    @abstractmethod
    def get_max_profit(self) -> float:
        """Calculate maximum possible profit"""
        pass
    
    @abstractmethod
    def get_max_loss(self) -> float:
        """Calculate maximum possible loss"""
        pass
    
    @abstractmethod
    def get_break_even_points(self) -> List[float]:
        """Calculate break-even points"""
        pass
    
    def get_profit_loss_range(self, price_range: List[float]) -> Dict[float, float]:
        """Calculate P&L for a range of stock prices"""
        return {price: self.calculate_payoff(price) for price in price_range}


class IronCondor(OptionsStrategy):
    """Iron Condor strategy: sell call spread + sell put spread"""
    
    def __init__(self, symbol: str, current_price: float, expiration: date,
                 short_call_strike: float, long_call_strike: float,
                 short_put_strike: float, long_put_strike: float,
                 net_credit: float):
        super().__init__(symbol, current_price, expiration)
        self.short_call_strike = short_call_strike
        self.long_call_strike = long_call_strike
        self.short_put_strike = short_put_strike
        self.long_put_strike = long_put_strike
        self.net_credit = net_credit
        
    def calculate_payoff(self, stock_price: float) -> float:
        """Calculate payoff at expiration"""
        # Call spread payoff
        call_spread_payoff = 0
        if stock_price > self.short_call_strike:
            call_spread_payoff = min(stock_price - self.short_call_strike, 
                                   self.long_call_strike - self.short_call_strike)
        
        # Put spread payoff
        put_spread_payoff = 0
        if stock_price < self.short_put_strike:
            put_spread_payoff = min(self.short_put_strike - stock_price,
                                  self.short_put_strike - self.long_put_strike)
        
        # Total payoff = net credit - (call spread loss + put spread loss)
        total_loss = call_spread_payoff + put_spread_payoff
        return self.net_credit - total_loss
    
    def get_max_profit(self) -> float:
        """Maximum profit is the net credit received"""
        return self.net_credit
    
    def get_max_loss(self) -> float:
        """Maximum loss is the width of the spreads minus the credit"""
        call_spread_width = self.long_call_strike - self.short_call_strike
        put_spread_width = self.short_put_strike - self.long_put_strike
        max_loss = max(call_spread_width, put_spread_width) - self.net_credit
        return max_loss
    
    def get_break_even_points(self) -> List[float]:
        """Calculate break-even points"""
        # Upper break-even: short call strike + net credit
        upper_be = self.short_call_strike + self.net_credit
        # Lower break-even: short put strike - net credit
        lower_be = self.short_put_strike - self.net_credit
        return [lower_be, upper_be]


class Straddle(OptionsStrategy):
    """Straddle strategy: buy call + buy put at same strike"""
    
    def __init__(self, symbol: str, strike: float, current_price: float,
                 expiration: date, call_premium: float, put_premium: float):
        super().__init__(symbol, current_price, expiration)
        self.strike = strike
        self.call_premium = call_premium
        self.put_premium = put_premium
        self.total_cost = call_premium + put_premium
        
    def calculate_payoff(self, stock_price: float) -> float:
        """Calculate payoff at expiration"""
        call_payoff = max(0, stock_price - self.strike) - self.call_premium
        put_payoff = max(0, self.strike - stock_price) - self.put_premium
        return call_payoff + put_payoff
    
    def get_max_profit(self) -> float:
        """Maximum profit is unlimited (theoretically)"""
        return float('inf')
    
    def get_max_loss(self) -> float:
        """Maximum loss is the total premium paid"""
        return self.total_cost
    
    def get_break_even_points(self) -> List[float]:
        """Calculate break-even points"""
        upper_be = self.strike + self.total_cost
        lower_be = self.strike - self.total_cost
        return [lower_be, upper_be]


class Strangle(OptionsStrategy):
    """Strangle strategy: buy call + buy put at different strikes"""
    
    def __init__(self, symbol: str, call_strike: float, put_strike: float,
                 current_price: float, expiration: date,
                 call_premium: float, put_premium: float):
        super().__init__(symbol, current_price, expiration)
        self.call_strike = call_strike
        self.put_strike = put_strike
        self.call_premium = call_premium
        self.put_premium = put_premium
        self.total_cost = call_premium + put_premium
        
    def calculate_payoff(self, stock_price: float) -> float:
        """Calculate payoff at expiration"""
        call_payoff = max(0, stock_price - self.call_strike) - self.call_premium
        put_payoff = max(0, self.put_strike - stock_price) - self.put_premium
        return call_payoff + put_payoff
    
    def get_max_profit(self) -> float:
        """Maximum profit is unlimited (theoretically)"""
        return float('inf')
    
    def get_max_loss(self) -> float:
        """Maximum loss is the total premium paid"""
        return self.total_cost
    
    def get_break_even_points(self) -> List[float]:
        """Calculate break-even points"""
        upper_be = self.call_strike + self.total_cost
        lower_be = self.put_strike - self.total_cost
        return [lower_be, upper_be]


class CallSpread(OptionsStrategy):
    """Call Spread strategy: buy call + sell call at higher strike"""
    
    def __init__(self, symbol: str, buy_strike: float, sell_strike: float,
                 current_price: float, expiration: date,
                 buy_premium: float, sell_premium: float):
        super().__init__(symbol, current_price, expiration)
        self.buy_strike = buy_strike
        self.sell_strike = sell_strike
        self.buy_premium = buy_premium
        self.sell_premium = sell_premium
        self.net_debit = buy_premium - sell_premium
        
    def calculate_payoff(self, stock_price: float) -> float:
        """Calculate payoff at expiration"""
        if stock_price <= self.buy_strike:
            return -self.net_debit
        elif stock_price <= self.sell_strike:
            return (stock_price - self.buy_strike) - self.net_debit
        else:
            return (self.sell_strike - self.buy_strike) - self.net_debit
    
    def get_max_profit(self) -> float:
        """Maximum profit is the spread width minus net debit"""
        return (self.sell_strike - self.buy_strike) - self.net_debit
    
    def get_max_loss(self) -> float:
        """Maximum loss is the net debit paid"""
        return self.net_debit
    
    def get_break_even_points(self) -> List[float]:
        """Calculate break-even point"""
        return [self.buy_strike + self.net_debit]


class PutSpread(OptionsStrategy):
    """Put Spread strategy: buy put + sell put at lower strike"""
    
    def __init__(self, symbol: str, buy_strike: float, sell_strike: float,
                 current_price: float, expiration: date,
                 buy_premium: float, sell_premium: float):
        super().__init__(symbol, current_price, expiration)
        self.buy_strike = buy_strike
        self.sell_strike = sell_strike
        self.buy_premium = buy_premium
        self.sell_premium = sell_premium
        self.net_debit = buy_premium - sell_premium
        
    def calculate_payoff(self, stock_price: float) -> float:
        """Calculate payoff at expiration"""
        if stock_price >= self.buy_strike:
            return -self.net_debit
        elif stock_price >= self.sell_strike:
            return (self.buy_strike - stock_price) - self.net_debit
        else:
            return (self.buy_strike - self.sell_strike) - self.net_debit
    
    def get_max_profit(self) -> float:
        """Maximum profit is the spread width minus net debit"""
        return (self.buy_strike - self.sell_strike) - self.net_debit
    
    def get_max_loss(self) -> float:
        """Maximum loss is the net debit paid"""
        return self.net_debit
    
    def get_break_even_points(self) -> List[float]:
        """Calculate break-even point"""
        return [self.buy_strike - self.net_debit]


class Butterfly(OptionsStrategy):
    """Butterfly strategy: buy 1 ITM, sell 2 ATM, buy 1 OTM"""
    
    def __init__(self, symbol: str, low_strike: float, middle_strike: float,
                 high_strike: float, current_price: float, expiration: date,
                 low_premium: float, middle_premium: float, high_premium: float):
        super().__init__(symbol, current_price, expiration)
        self.low_strike = low_strike
        self.middle_strike = middle_strike
        self.high_strike = high_strike
        self.low_premium = low_premium
        self.middle_premium = middle_premium
        self.high_premium = high_premium
        self.net_debit = low_premium - (2 * middle_premium) + high_premium
        
    def calculate_payoff(self, stock_price: float) -> float:
        """Calculate payoff at expiration"""
        if stock_price <= self.low_strike:
            return -self.net_debit
        elif stock_price <= self.middle_strike:
            return (stock_price - self.low_strike) - self.net_debit
        elif stock_price <= self.high_strike:
            return (self.middle_strike - self.low_strike) - (stock_price - self.middle_strike) - self.net_debit
        else:
            return -self.net_debit
    
    def get_max_profit(self) -> float:
        """Maximum profit occurs at middle strike"""
        return (self.middle_strike - self.low_strike) - self.net_debit
    
    def get_max_loss(self) -> float:
        """Maximum loss is the net debit paid"""
        return self.net_debit
    
    def get_break_even_points(self) -> List[float]:
        """Calculate break-even points"""
        lower_be = self.low_strike + self.net_debit
        upper_be = self.high_strike - self.net_debit
        return [lower_be, upper_be]
