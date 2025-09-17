"""
AI Strategy Generator using OpenAI
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not available. Install with: pip install openai")


class AIStrategyGenerator:
    """Generates trading strategies using OpenAI"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = None
        self.strategy_history = []
        
        if OPENAI_AVAILABLE and api_key:
            openai.api_key = api_key
            self.client = openai.OpenAI(api_key=api_key)
        elif OPENAI_AVAILABLE:
            # Try to get from environment
            import os
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.client = openai.OpenAI(api_key=api_key)
            else:
                logger.warning("No OpenAI API key provided. Set OPENAI_API_KEY environment variable.")
    
    def analyze_market_conditions(self, market_data: Dict) -> Dict:
        """Analyze current market conditions and generate trading insights"""
        if not self.client:
            return self._fallback_analysis(market_data)
            
        try:
            prompt = self._create_market_analysis_prompt(market_data)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert options trader and market analyst. Provide concise, actionable trading insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            analysis = response.choices[0].message.content
            return self._parse_analysis(analysis, market_data)
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            return self._fallback_analysis(market_data)
    
    def generate_strategy(self, symbol: str, market_data: Dict, current_price: float) -> Dict:
        """Generate a specific trading strategy for a symbol"""
        if not self.client:
            return self._fallback_strategy(symbol, market_data, current_price)
            
        try:
            prompt = self._create_strategy_prompt(symbol, market_data, current_price)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert options trader. Generate specific, executable trading strategies with exact parameters."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.6
            )
            
            strategy_text = response.choices[0].message.content
            return self._parse_strategy(strategy_text, symbol, current_price)
            
        except Exception as e:
            logger.error(f"Error generating strategy: {e}")
            return self._fallback_strategy(symbol, market_data, current_price)
    
    def _create_market_analysis_prompt(self, market_data: Dict) -> str:
        """Create prompt for market analysis"""
        prompt = f"""
        Analyze the current market conditions and provide trading insights:
        
        Market Data:
        - VIX: {market_data.get('vix', 'N/A')}
        - SPY Price: {market_data.get('spy_price', 'N/A')}
        - Market Trend: {market_data.get('trend', 'N/A')}
        - Volatility: {market_data.get('volatility', 'N/A')}
        - Time of Day: {market_data.get('time_of_day', 'N/A')}
        
        Provide:
        1. Market sentiment (Bullish/Bearish/Neutral)
        2. Recommended strategy types (Iron Condor, Straddle, etc.)
        3. Risk level (Low/Medium/High)
        4. Key factors to watch
        """
        return prompt
    
    def _create_strategy_prompt(self, symbol: str, market_data: Dict, current_price: float) -> str:
        """Create prompt for strategy generation"""
        prompt = f"""
        Generate a specific options trading strategy for {symbol}:
        
        Current Price: ${current_price:.2f}
        Market Conditions:
        - VIX: {market_data.get('vix', 'N/A')}
        - Trend: {market_data.get('trend', 'N/A')}
        - Volatility: {market_data.get('volatility', 'N/A')}
        
        Provide a JSON response with:
        {{
            "strategy_type": "Iron Condor|Straddle|Strangle|Call Spread|Put Spread",
            "reasoning": "Why this strategy",
            "parameters": {{
                "expiration_days": 30,
                "strikes": {{}},
                "premiums": {{}},
                "max_profit": 0,
                "max_loss": 0,
                "probability_of_profit": 0.0
            }},
            "risk_level": "Low|Medium|High",
            "confidence": 0.0
        }}
        """
        return prompt
    
    def _parse_analysis(self, analysis: str, market_data: Dict) -> Dict:
        """Parse AI analysis response"""
        return {
            'sentiment': self._extract_sentiment(analysis),
            'recommended_strategies': self._extract_strategies(analysis),
            'risk_level': self._extract_risk_level(analysis),
            'key_factors': self._extract_factors(analysis),
            'raw_analysis': analysis
        }
    
    def _parse_strategy(self, strategy_text: str, symbol: str, current_price: float) -> Dict:
        """Parse AI strategy response"""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', strategy_text, re.DOTALL)
            if json_match:
                strategy_data = json.loads(json_match.group())
                strategy_data['symbol'] = symbol
                strategy_data['current_price'] = current_price
                strategy_data['generated_at'] = datetime.now().isoformat()
                return strategy_data
        except:
            pass
        
        # Fallback parsing
        return self._fallback_strategy(symbol, {}, current_price)
    
    def _extract_sentiment(self, text: str) -> str:
        """Extract market sentiment from text"""
        text_lower = text.lower()
        if 'bullish' in text_lower:
            return 'Bullish'
        elif 'bearish' in text_lower:
            return 'Bearish'
        else:
            return 'Neutral'
    
    def _extract_strategies(self, text: str) -> List[str]:
        """Extract recommended strategies from text"""
        strategies = []
        text_lower = text.lower()
        
        if 'iron condor' in text_lower:
            strategies.append('Iron Condor')
        if 'straddle' in text_lower:
            strategies.append('Straddle')
        if 'strangle' in text_lower:
            strategies.append('Strangle')
        if 'call spread' in text_lower:
            strategies.append('Call Spread')
        if 'put spread' in text_lower:
            strategies.append('Put Spread')
            
        return strategies if strategies else ['Iron Condor']
    
    def _extract_risk_level(self, text: str) -> str:
        """Extract risk level from text"""
        text_lower = text.lower()
        if 'high risk' in text_lower or 'high' in text_lower:
            return 'High'
        elif 'low risk' in text_lower or 'low' in text_lower:
            return 'Low'
        else:
            return 'Medium'
    
    def _extract_factors(self, text: str) -> List[str]:
        """Extract key factors from text"""
        # Simple extraction - look for bullet points or numbered lists
        lines = text.split('\n')
        factors = []
        for line in lines:
            line = line.strip()
            if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                factors.append(line[1:].strip())
        return factors[:3]  # Limit to 3 factors
    
    def _fallback_analysis(self, market_data: Dict) -> Dict:
        """Fallback analysis when AI is not available"""
        vix = market_data.get('vix', 20)
        
        if vix > 30:
            sentiment = 'Bearish'
            strategies = ['Iron Condor', 'Put Spread']
            risk_level = 'High'
        elif vix < 15:
            sentiment = 'Bullish'
            strategies = ['Call Spread', 'Straddle']
            risk_level = 'Low'
        else:
            sentiment = 'Neutral'
            strategies = ['Iron Condor', 'Strangle']
            risk_level = 'Medium'
        
        return {
            'sentiment': sentiment,
            'recommended_strategies': strategies,
            'risk_level': risk_level,
            'key_factors': ['VIX level', 'Market volatility', 'Trend direction'],
            'raw_analysis': f'Fallback analysis: {sentiment} market with {risk_level} risk'
        }
    
    def _fallback_strategy(self, symbol: str, market_data: Dict, current_price: float) -> Dict:
        """Fallback strategy when AI is not available"""
        vix = market_data.get('vix', 20)
        
        if vix > 25:
            # High volatility - use Iron Condor
            strategy_type = 'Iron Condor'
            expiration_days = 30
            strikes = {
                'short_call': current_price * 1.05,
                'long_call': current_price * 1.10,
                'short_put': current_price * 0.95,
                'long_put': current_price * 0.90
            }
            max_profit = 2.0
            max_loss = 3.0
        else:
            # Low volatility - use Straddle
            strategy_type = 'Straddle'
            expiration_days = 21
            strikes = {
                'strike': current_price
            }
            max_profit = float('inf')
            max_loss = 15.0
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'strategy_type': strategy_type,
            'reasoning': f'Fallback strategy based on VIX level of {vix}',
            'parameters': {
                'expiration_days': expiration_days,
                'strikes': strikes,
                'max_profit': max_profit,
                'max_loss': max_loss,
                'probability_of_profit': 0.6
            },
            'risk_level': 'Medium',
            'confidence': 0.5,
            'generated_at': datetime.now().isoformat()
        }
    
    def get_strategy_recommendation(self, symbol: str, market_data: Dict, current_price: float) -> Dict:
        """Get a complete strategy recommendation"""
        # First analyze market conditions
        market_analysis = self.analyze_market_conditions(market_data)
        
        # Then generate specific strategy
        strategy = self.generate_strategy(symbol, market_data, current_price)
        
        # Combine results
        recommendation = {
            'market_analysis': market_analysis,
            'strategy': strategy,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store in history
        self.strategy_history.append(recommendation)
        
        return recommendation
