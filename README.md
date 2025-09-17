# Options Trading Simulator

A Python console application for simulating options trading strategies without real money. This tool helps you test different options strategies, analyze their risk/reward profiles, and understand how they perform under various market conditions.

## Features

- **Multiple Options Strategies**: Support for Iron Condors, Straddles, Strangles, Call/Put Spreads, and Butterflies
- **Risk Management**: Configurable position sizing and risk per trade
- **Strategy Analysis**: Comprehensive analysis including Greeks, probability of profit, and expected value
- **Simulation Engine**: Backtest strategies with realistic price movements
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
2. **Add Options Data**: Input options data manually or load sample data
3. **Analyze Strategy**: View detailed analysis of your strategies
4. **Run Simulation**: Execute the trading simulation
5. **View Results**: Check portfolio performance and trade history

### Command Line Options

```bash
# Run with sample data
python main.py --sample

# Load configuration from file
python main.py --config config.json
```

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
├── main.py                 # Main application
├── options_models.py       # Options and strategy models
├── trading_engine.py       # Simulation engine
├── strategy_analyzer.py    # Strategy analysis
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
└── README.md              # This file
```

## Example Workflow

1. **Start the application**:
   ```bash
   docker-compose up
   ```

2. **Load sample data** (Option 7 in menu)

3. **Analyze strategies** (Option 3 in menu)

4. **Configure simulation** (Option 1 in menu)

5. **Run simulation** (Option 4 in menu)

6. **View results** (Options 5-6 in menu)

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
