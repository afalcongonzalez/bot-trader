# Options Trading Simulator with Live Data

A Python console application for simulating options trading strategies with real-time market data from Yahoo Finance. This tool helps you test different options strategies, analyze their risk/reward profiles, and understand how they perform under various market conditions using live data.

## 🚀 New Features

- **Live Market Data**: Real-time stock prices and options data from Yahoo Finance
- **Automatic Data Fetching**: Fetch options chains, expirations, and premiums automatically
- **Market Status**: Check if markets are open and get current market conditions
- **Real-time Analysis**: Update strategy analysis with current market prices
- **Live Simulation**: Run simulations with real market data updates

## Features

- **Multiple Options Strategies**: Support for Iron Condors, Straddles, Strangles, Call/Put Spreads, and Butterflies
- **Live Data Integration**: Real-time data from Yahoo Finance API
- **Risk Management**: Configurable position sizing and risk per trade
- **Strategy Analysis**: Comprehensive analysis including Greeks, probability of profit, and expected value
- **Simulation Engine**: Backtest strategies with realistic price movements or live data
- **Portfolio Tracking**: Monitor positions, P&L, and trade history
- **Dockerized**: Easy deployment with Docker and Docker Compose

## Supported Strategies

### Iron Condor
- Sell call spread + sell put spread
- Limited profit, limited risk
- Benefits from low volatility and time decay

### Straddle
- Buy call + buy put at same strike
- Unlimited profit potential
- Benefits from high volatility

### Strangle
- Buy call + buy put at different strikes
- Unlimited profit potential
- Benefits from high volatility

### Call/Put Spreads
- Limited risk, limited reward
- Directional strategies

### Butterfly
- Buy 1 ITM, sell 2 ATM, buy 1 OTM
- Limited risk, limited reward
- Benefits from low volatility

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd bot-trader
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

3. To run with Jupyter notebook support:
```bash
docker-compose --profile jupyter up --build
```

### Local Installation

1. Install Python 3.11 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### Basic Usage

1. **Configure Simulation**: Set initial capital, risk per trade, and simulation parameters
2. **Fetch Live Data**: Get real-time options data for any symbol
3. **Add Options Data**: Input strategies manually or use live data
4. **Analyze Strategy**: View detailed analysis with current market prices
5. **Run Simulation**: Execute the trading simulation with live or simulated data
6. **View Results**: Check portfolio performance and trade history

### Command Line Options

```bash
# Run with sample data
python main.py --sample

# Run with live data enabled by default
python main.py --live

# Load configuration from file
python main.py --config config.json
```

### Live Data Features

#### Fetch Live Options Data
- Enter any stock symbol (AAPL, TSLA, SPY, etc.)
- Automatically fetch current stock price
- Get available expiration dates
- Fetch options chain data for Iron Condors, Straddles, and Strangles
- Real-time premium prices

#### Market Status
- Check if markets are open
- View current market state
- Get last update timestamps
- Display current prices for popular symbols

#### Real-time Analysis
- Update strategy analysis with current market prices
- Calculate live P&L for open positions
- Monitor portfolio value in real-time

### Sample Data

The application includes sample data for testing:
- AAPL Iron Condor (30 days to expiration)
- TSLA Straddle (21 days to expiration)

## Configuration

### Simulation Parameters

- **Initial Capital**: Starting amount for simulation
- **Risk per Trade**: Percentage of capital to risk per trade (default: 2%)
- **Max Concurrent Trades**: Maximum number of open positions
- **Simulation Days**: Number of days to simulate
- **Use Live Data**: Enable/disable live data fetching

### Strategy Analysis

The analyzer provides:
- Maximum profit and loss
- Break-even points
- Risk/reward ratio
- Probability of profit
- Expected value
- Greeks (Delta, Gamma, Theta, Vega)
- Trading recommendations

## File Structure

```
bot-trader/
├── main.py                 # Main application with live data integration
├── options_models.py       # Options and strategy models
├── trading_engine.py       # Simulation engine with live data support
├── strategy_analyzer.py    # Strategy analysis
├── data_fetcher.py         # Yahoo Finance data fetcher
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── test_live_data.py      # Test script for live data
├── run.sh                 # Easy startup script
└── README.md              # This file
```

## Example Workflow

1. **Start the application**:
   ```bash
   docker-compose up
   ```

2. **Check market status** (Option 9 in menu)

3. **Fetch live data** (Option 3 in menu):
   - Enter symbol (e.g., AAPL)
   - Choose expiration date
   - Select strategy (Iron Condor, Straddle, Strangle)
   - Review and add the strategy

4. **Analyze strategies** (Option 4 in menu)

5. **Configure simulation** (Option 1 in menu)

6. **Run simulation** (Option 5 in menu)

7. **View results** (Options 6-7 in menu)

## Data Sources

- **Yahoo Finance**: Real-time stock prices and options data
- **Market Data**: Current market status and trading hours
- **Historical Data**: For volatility calculations and backtesting

## Testing

Test the live data functionality:
```bash
python test_live_data.py
```

This will test:
- Stock price fetching
- Market status
- Options expirations
- Strategy data fetching
- Volatility calculations

## Risk Disclaimer

This is a simulation tool for educational purposes only. It does not provide financial advice and should not be used for actual trading decisions. Options trading involves significant risk and may not be suitable for all investors.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue on GitHub or contact the maintainers.
