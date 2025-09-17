"""
Strategy analyzer for options trading strategies
"""

import math
from typing import Dict, List
from datetime import date
import numpy as np

from options_models import OptionsStrategy


class StrategyAnalyzer:
    """Analyzes options trading strategies"""
    
    def __init__(self):
        self.price_range_percent = 0.3  # Analyze ±30% price movement
        
    def analyze_strategy(self, strategy: OptionsStrategy) -> Dict:
        """Comprehensive analysis of a strategy"""
        analysis = {
            'max_profit': strategy.get_max_profit(),
            'max_loss': strategy.get_max_loss(),
            'break_even_points': strategy.get_break_even_points(),
            'risk_reward_ratio': self._calculate_risk_reward_ratio(strategy),
            'probability_of_profit': self._calculate_probability_of_profit(strategy),
            'expected_value': self._calculate_expected_value(strategy),
            'greeks': self._calculate_greeks(strategy),
            'profit_loss_curve': self._generate_profit_loss_curve(strategy),
            'recommendation': self._get_recommendation(strategy)
        }
        
        return analysis
        
    def _calculate_risk_reward_ratio(self, strategy: OptionsStrategy) -> float:
        """Calculate risk/reward ratio"""
        max_profit = strategy.get_max_profit()
        max_loss = abs(strategy.get_max_loss())
        
        if max_loss == 0:
            return float('inf') if max_profit > 0 else 0
            
        return max_profit / max_loss if max_profit != float('inf') else 0
        
    def _calculate_probability_of_profit(self, strategy: OptionsStrategy) -> float:
        """Calculate probability of profit (simplified)"""
        # This is a simplified calculation
        # In reality, you'd use Black-Scholes or similar models
        
        current_price = strategy.current_price
        break_even_points = strategy.get_break_even_points()
        
        if len(break_even_points) == 1:
            # Single break-even point
            be_point = break_even_points[0]
            if current_price > be_point:
                return 0.6  # Simplified: 60% chance if above BE
            else:
                return 0.4  # Simplified: 40% chance if below BE
        elif len(break_even_points) == 2:
            # Two break-even points (like straddle)
            lower_be, upper_be = break_even_points
            if lower_be <= current_price <= upper_be:
                return 0.3  # Between BEs, lower probability
            else:
                return 0.7  # Outside BEs, higher probability
        else:
            return 0.5  # Default 50%
            
    def _calculate_expected_value(self, strategy: OptionsStrategy) -> float:
        """Calculate expected value of the strategy"""
        # Simplified expected value calculation
        prob_profit = self._calculate_probability_of_profit(strategy)
        max_profit = strategy.get_max_profit()
        max_loss = strategy.get_max_loss()
        
        if max_profit == float('inf'):
            # For unlimited profit strategies, use a reasonable estimate
            max_profit = abs(max_loss) * 2
            
        expected_value = (prob_profit * max_profit) + ((1 - prob_profit) * max_loss)
        return expected_value
        
    def _calculate_greeks(self, strategy: OptionsStrategy) -> Dict[str, float]:
        """Calculate simplified Greeks"""
        # This is a very simplified calculation
        # Real Greeks require Black-Scholes model
        
        current_price = strategy.current_price
        days_to_exp = strategy.days_to_expiration
        
        # Delta: price sensitivity
        delta = self._estimate_delta(strategy, current_price)
        
        # Gamma: delta sensitivity
        gamma = self._estimate_gamma(strategy, current_price)
        
        # Theta: time decay
        theta = self._estimate_theta(strategy, days_to_exp)
        
        # Vega: volatility sensitivity
        vega = self._estimate_vega(strategy, days_to_exp)
        
        return {
            'delta': delta,
            'gamma': gamma,
            'theta': theta,
            'vega': vega
        }
        
    def _estimate_delta(self, strategy: OptionsStrategy, current_price: float) -> float:
        """Estimate delta for the strategy"""
        # Very simplified delta calculation
        price_change = 0.01
        current_payoff = strategy.calculate_payoff(current_price)
        new_payoff = strategy.calculate_payoff(current_price + price_change)
        
        return (new_payoff - current_payoff) / price_change
        
    def _estimate_gamma(self, strategy: OptionsStrategy, current_price: float) -> float:
        """Estimate gamma for the strategy"""
        # Very simplified gamma calculation
        price_change = 0.01
        delta1 = self._estimate_delta(strategy, current_price)
        delta2 = self._estimate_delta(strategy, current_price + price_change)
        
        return (delta2 - delta1) / price_change
        
    def _estimate_theta(self, strategy: OptionsStrategy, days_to_exp: int) -> float:
        """Estimate theta (time decay) for the strategy"""
        if days_to_exp <= 0:
            return 0
            
        # Simplified theta calculation
        # Time decay accelerates as expiration approaches
        time_decay_factor = 1 / math.sqrt(days_to_exp) if days_to_exp > 0 else 0
        
        # For strategies that benefit from time decay (like iron condors)
        if hasattr(strategy, 'net_credit'):
            return time_decay_factor * 0.1  # Positive theta
        else:
            return -time_decay_factor * 0.1  # Negative theta
            
    def _estimate_vega(self, strategy: OptionsStrategy, days_to_exp: int) -> float:
        """Estimate vega (volatility sensitivity) for the strategy"""
        if days_to_exp <= 0:
            return 0
            
        # Simplified vega calculation
        # Vega is higher for longer-dated options
        vega_factor = math.sqrt(days_to_exp / 365.0)
        
        # For strategies that benefit from volatility (like straddles)
        if hasattr(strategy, 'total_cost'):
            return vega_factor * 0.2  # Positive vega
        else:
            return -vega_factor * 0.1  # Negative vega
            
    def _generate_profit_loss_curve(self, strategy: OptionsStrategy) -> Dict[str, List[float]]:
        """Generate profit/loss curve for different stock prices"""
        current_price = strategy.current_price
        price_range = current_price * self.price_range_percent
        
        # Generate price points
        min_price = max(0.01, current_price - price_range)
        max_price = current_price + price_range
        price_points = np.linspace(min_price, max_price, 50)
        
        # Calculate payoffs
        payoffs = [strategy.calculate_payoff(price) for price in price_points]
        
        return {
            'prices': price_points.tolist(),
            'payoffs': payoffs
        }
        
    def _get_recommendation(self, strategy: OptionsStrategy) -> str:
        """Get trading recommendation based on analysis"""
        risk_reward = self._calculate_risk_reward_ratio(strategy)
        prob_profit = self._calculate_probability_of_profit(strategy)
        expected_value = self._calculate_expected_value(strategy)
        
        if expected_value > 0 and risk_reward > 1.5 and prob_profit > 0.6:
            return "STRONG BUY"
        elif expected_value > 0 and risk_reward > 1.0 and prob_profit > 0.5:
            return "BUY"
        elif expected_value > 0:
            return "WEAK BUY"
        elif expected_value < -abs(strategy.get_max_loss()) * 0.5:
            return "AVOID"
        else:
            return "HOLD"
            
    def compare_strategies(self, strategies: List[OptionsStrategy]) -> Dict:
        """Compare multiple strategies"""
        comparison = {}
        
        for i, strategy in enumerate(strategies):
            analysis = self.analyze_strategy(strategy)
            comparison[f"Strategy_{i+1}"] = {
                'name': strategy.__class__.__name__,
                'symbol': strategy.symbol,
                'expected_value': analysis['expected_value'],
                'risk_reward_ratio': analysis['risk_reward_ratio'],
                'probability_of_profit': analysis['probability_of_profit'],
                'recommendation': analysis['recommendation']
            }
            
        # Rank strategies by expected value
        ranked_strategies = sorted(
            comparison.items(),
            key=lambda x: x[1]['expected_value'],
            reverse=True
        )
        
        comparison['ranking'] = [item[0] for item in ranked_strategies]
        
        return comparison
        
    def analyze_market_conditions(self, strategies: List[OptionsStrategy]) -> Dict:
        """Analyze overall market conditions for strategies"""
        if not strategies:
            return {}
            
        total_expected_value = sum(self._calculate_expected_value(s) for s in strategies)
        avg_prob_profit = sum(self._calculate_probability_of_profit(s) for s in strategies) / len(strategies)
        
        # Market sentiment based on strategy performance
        if total_expected_value > 0 and avg_prob_profit > 0.6:
            sentiment = "BULLISH"
        elif total_expected_value < 0 and avg_prob_profit < 0.4:
            sentiment = "BEARISH"
        else:
            sentiment = "NEUTRAL"
            
        return {
            'total_expected_value': total_expected_value,
            'average_probability_of_profit': avg_prob_profit,
            'market_sentiment': sentiment,
            'strategy_count': len(strategies)
        }
