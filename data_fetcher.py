"""
Data fetcher for live options and stock data using Yahoo Finance
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YahooFinanceDataFetcher:
    """Fetches live data from Yahoo Finance"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = 60  # Cache for 1 minute
        
    def get_stock_price(self, symbol: str) -> float:
        """Get current stock price"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            
            if current_price == 0:
                # Fallback to historical data
                hist = ticker.history(period="1d")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    
            logger.info(f"Fetched {symbol} price: ${current_price:.2f}")
            return float(current_price)
            
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            return 0.0
            
    def get_options_chain(self, symbol: str, expiration_date: Optional[date] = None) -> Dict:
        """Get options chain for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get available expiration dates
            expirations = ticker.options
            if not expirations:
                logger.warning(f"No options data available for {symbol}")
                return {}
                
            # Use provided expiration or closest one
            if expiration_date:
                target_exp = expiration_date.strftime('%Y-%m-%d')
                if target_exp in expirations:
                    exp_date = target_exp
                else:
                    # Find closest expiration
                    exp_date = min(expirations, key=lambda x: abs(
                        datetime.strptime(x, '%Y-%m-%d').date() - expiration_date
                    ))
            else:
                # Use closest expiration
                exp_date = expirations[0]
                
            # Get options chain
            options_chain = ticker.option_chain(exp_date)
            
            logger.info(f"Fetched options chain for {symbol} exp {exp_date}")
            return {
                'calls': options_chain.calls,
                'puts': options_chain.puts,
                'expiration': exp_date
            }
            
        except Exception as e:
            logger.error(f"Error fetching options chain for {symbol}: {e}")
            return {}
            
    def get_option_price(self, symbol: str, strike: float, option_type: str, 
                        expiration: date) -> float:
        """Get specific option price"""
        try:
            options_chain = self.get_options_chain(symbol, expiration)
            if not options_chain:
                return 0.0
                
            if option_type.upper() == 'CALL':
                options_df = options_chain['calls']
            else:
                options_df = options_chain['puts']
                
            # Find closest strike
            closest_strike = options_df.iloc[(options_df['strike'] - strike).abs().argsort()[:1]]
            
            if not closest_strike.empty:
                price = closest_strike['lastPrice'].iloc[0]
                logger.info(f"Fetched {symbol} {option_type} ${strike} price: ${price:.2f}")
                return float(price)
                
        except Exception as e:
            logger.error(f"Error fetching option price for {symbol} {option_type} ${strike}: {e}")
            
        return 0.0
        
    def get_available_expirations(self, symbol: str) -> List[date]:
        """Get available expiration dates for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            expirations = ticker.options
            
            if not expirations:
                return []
                
            # Convert to date objects and sort
            exp_dates = [datetime.strptime(exp, '%Y-%m-%d').date() for exp in expirations]
            exp_dates.sort()
            
            return exp_dates
            
        except Exception as e:
            logger.error(f"Error fetching expirations for {symbol}: {e}")
            return []
            
    def get_iron_condor_data(self, symbol: str, current_price: float, 
                           expiration: date) -> Dict:
        """Get data for iron condor strategy"""
        try:
            options_chain = self.get_options_chain(symbol, expiration)
            if not options_chain:
                return {}
                
            calls = options_chain['calls']
            puts = options_chain['puts']
            
            # Find strikes around current price
            call_strikes = calls[calls['strike'] > current_price].sort_values('strike')
            put_strikes = puts[puts['strike'] < current_price].sort_values('strike', ascending=False)
            
            if len(call_strikes) < 2 or len(put_strikes) < 2:
                logger.warning(f"Not enough strikes for iron condor on {symbol}")
                return {}
                
            # Select strikes (simplified selection)
            short_call_strike = call_strikes.iloc[0]['strike']
            long_call_strike = call_strikes.iloc[1]['strike']
            short_put_strike = put_strikes.iloc[0]['strike']
            long_put_strike = put_strikes.iloc[1]['strike']
            
            # Get premiums
            short_call_premium = call_strikes.iloc[0]['lastPrice']
            long_call_premium = call_strikes.iloc[1]['lastPrice']
            short_put_premium = put_strikes.iloc[0]['lastPrice']
            long_put_premium = put_strikes.iloc[1]['lastPrice']
            
            net_credit = (short_call_premium + short_put_premium) - (long_call_premium + long_put_premium)
            
            return {
                'short_call_strike': short_call_strike,
                'long_call_strike': long_call_strike,
                'short_put_strike': short_put_strike,
                'long_put_strike': long_put_strike,
                'net_credit': net_credit,
                'short_call_premium': short_call_premium,
                'long_call_premium': long_call_premium,
                'short_put_premium': short_put_premium,
                'long_put_premium': long_put_premium
            }
            
        except Exception as e:
            logger.error(f"Error fetching iron condor data for {symbol}: {e}")
            return {}
            
    def get_straddle_data(self, symbol: str, current_price: float, 
                         expiration: date) -> Dict:
        """Get data for straddle strategy"""
        try:
            options_chain = self.get_options_chain(symbol, expiration)
            if not options_chain:
                return {}
                
            calls = options_chain['calls']
            puts = options_chain['puts']
            
            # Find ATM strikes
            atm_call = calls.iloc[(calls['strike'] - current_price).abs().argsort()[:1]]
            atm_put = puts.iloc[(puts['strike'] - current_price).abs().argsort()[:1]]
            
            if atm_call.empty or atm_put.empty:
                logger.warning(f"No ATM options for straddle on {symbol}")
                return {}
                
            strike = atm_call.iloc[0]['strike']
            call_premium = atm_call.iloc[0]['lastPrice']
            put_premium = atm_put.iloc[0]['lastPrice']
            
            return {
                'strike': strike,
                'call_premium': call_premium,
                'put_premium': put_premium,
                'total_cost': call_premium + put_premium
            }
            
        except Exception as e:
            logger.error(f"Error fetching straddle data for {symbol}: {e}")
            return {}
            
    def get_strangle_data(self, symbol: str, current_price: float, 
                         expiration: date) -> Dict:
        """Get data for strangle strategy"""
        try:
            options_chain = self.get_options_chain(symbol, expiration)
            if not options_chain:
                return {}
                
            calls = options_chain['calls']
            puts = options_chain['puts']
            
            # Find OTM strikes
            otm_calls = calls[calls['strike'] > current_price].sort_values('strike')
            otm_puts = puts[puts['strike'] < current_price].sort_values('strike', ascending=False)
            
            if otm_calls.empty or otm_puts.empty:
                logger.warning(f"No OTM options for strangle on {symbol}")
                return {}
                
            call_strike = otm_calls.iloc[0]['strike']
            put_strike = otm_puts.iloc[0]['strike']
            call_premium = otm_calls.iloc[0]['lastPrice']
            put_premium = otm_puts.iloc[0]['lastPrice']
            
            return {
                'call_strike': call_strike,
                'put_strike': put_strike,
                'call_premium': call_premium,
                'put_premium': put_premium,
                'total_cost': call_premium + put_premium
            }
            
        except Exception as e:
            logger.error(f"Error fetching strangle data for {symbol}: {e}")
            return {}
            
    def get_historical_data(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """Get historical price data"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            logger.info(f"Fetched {len(hist)} days of historical data for {symbol}")
            return hist
            
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            return pd.DataFrame()
            
    def get_volatility(self, symbol: str, period: str = "1mo") -> float:
        """Calculate historical volatility"""
        try:
            hist = self.get_historical_data(symbol, period)
            if hist.empty:
                return 0.0
                
            # Calculate daily returns
            returns = hist['Close'].pct_change().dropna()
            
            # Calculate annualized volatility
            volatility = returns.std() * (252 ** 0.5)  # 252 trading days per year
            
            logger.info(f"Calculated volatility for {symbol}: {volatility:.2%}")
            return float(volatility)
            
        except Exception as e:
            logger.error(f"Error calculating volatility for {symbol}: {e}")
            return 0.0
            
    def search_symbols(self, query: str) -> List[str]:
        """Search for symbols by name or ticker"""
        try:
            # This is a simplified search - in practice you might use a more comprehensive API
            # For now, we'll return common symbols that match the query
            common_symbols = [
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX',
                'SPY', 'QQQ', 'IWM', 'VIX', 'GLD', 'SLV', 'TLT', 'HYG'
            ]
            
            matches = [symbol for symbol in common_symbols if query.upper() in symbol.upper()]
            return matches
            
        except Exception as e:
            logger.error(f"Error searching symbols: {e}")
            return []
            
    def get_market_status(self) -> Dict:
        """Get current market status"""
        try:
            # Check if market is open by looking at SPY
            spy = yf.Ticker("SPY")
            info = spy.info
            
            market_state = info.get('marketState', 'UNKNOWN')
            regular_market_time = info.get('regularMarketTime', 0)
            
            return {
                'market_state': market_state,
                'is_open': market_state == 'REGULAR',
                'last_update': datetime.fromtimestamp(regular_market_time) if regular_market_time else None
            }
            
        except Exception as e:
            logger.error(f"Error getting market status: {e}")
            return {'market_state': 'UNKNOWN', 'is_open': False, 'last_update': None}
