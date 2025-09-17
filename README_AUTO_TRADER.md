# 🤖 Automated Options Trading System

A fully automated options trading system that uses AI to generate trading strategies and executes them automatically. Just run it and watch it trade!

## 🚀 Features

- **AI-Powered Strategy Generation**: Uses OpenAI GPT-4 to analyze market conditions and generate trading strategies
- **Real-Time Market Monitoring**: Continuously monitors market conditions and price movements
- **Automatic Trade Execution**: Executes trades automatically based on AI recommendations
- **Live Dashboard**: Real-time display of portfolio, positions, and performance
- **Risk Management**: Built-in position sizing and risk controls
- **Comprehensive Logging**: All activities logged to files for analysis

## 🎯 How It Works

1. **Market Monitoring**: Monitors market conditions every 5 minutes (VIX, SPY, trends)
2. **AI Analysis**: Uses OpenAI to analyze market conditions and generate trading strategies
3. **Strategy Execution**: Automatically executes recommended strategies
4. **Portfolio Management**: Manages positions, risk, and performance
5. **Real-Time Dashboard**: Displays live updates of all activities

## 📋 Quick Start

### 1. Set up OpenAI API Key (Optional)
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 2. Run the Automated Trader
```bash
# Simple start
./run_auto_trader.sh

# Or with Python directly
python3 auto_trader.py

# Demo mode (no real trades)
./run_auto_trader.sh --demo
```

### 3. Watch It Trade!
The system will:
- Display a real-time dashboard
- Monitor market conditions
- Generate AI strategies
- Execute trades automatically
- Log all activities

## ⚙️ Configuration

### Command Line Options
```bash
python3 auto_trader.py --help

Options:
  --api-key API_KEY        OpenAI API key
  --capital CAPITAL        Initial capital (default: 10000)
  --interval INTERVAL      Monitoring interval in seconds (default: 300)
  --trading-interval INT   Trading interval in seconds (default: 1800)
  --max-positions INT      Maximum concurrent positions (default: 5)
  --risk RISK             Risk per trade (default: 0.02 = 2%)
  --demo                  Run in demo mode
  --config CONFIG         Load configuration from JSON file
```

### Configuration File
Create `auto_trader_config.json`:
```json
{
  "symbols": ["SPY", "QQQ", "AAPL", "TSLA", "MSFT", "GOOGL"],
  "intervals": {
    "monitoring": 300,
    "trading": 1800
  },
  "risk": 0.02,
  "max_positions": 5,
  "capital": 10000.0
}
```

## 📊 Real-Time Dashboard

The system displays a live dashboard showing:

```
🤖 AUTOMATED OPTIONS TRADING SYSTEM
============================================================
⏰ Time: 2024-01-15 14:30:25
🔄 Status: RUNNING

💰 PORTFOLIO SUMMARY
   Cash: $8,450.00
   Total Value: $10,250.00
   Open Positions: 3

📊 PERFORMANCE METRICS
   Total Trades: 12
   Winning Trades: 8
   Losing Trades: 4
   Total P&L: $250.00

📈 CURRENT POSITIONS
   1. AAPL - Iron Condor
      P&L: $125.00
   2. TSLA - Straddle
      P&L: -$50.00
   3. SPY - Strangle
      P&L: $75.00

🤖 RECENT AI STRATEGIES
   AAPL - Iron Condor
      Risk: Medium | Confidence: 0.8
      High volatility environment favors income strategies...
   TSLA - Straddle
      Risk: High | Confidence: 0.6
      Earnings volatility expected, directional play...

🌐 MARKET CONDITIONS
   VIX: 28.5
   SPY: $425.50
   Trend: Neutral
   Volatility: 22.5%
```

## 🤖 AI Strategy Generation

The system uses OpenAI GPT-4 to:

1. **Analyze Market Conditions**:
   - VIX levels and volatility
   - Market trends and sentiment
   - Time of day and market hours
   - Current price levels

2. **Generate Trading Strategies**:
   - Iron Condors (income strategies)
   - Straddles (volatility plays)
   - Strangles (directional bets)
   - Call/Put Spreads (defined risk)

3. **Risk Assessment**:
   - Strategy risk levels
   - Confidence scores
   - Probability of profit
   - Maximum loss calculations

## 📈 Supported Strategies

### Iron Condor
- **When**: High volatility, range-bound markets
- **AI Logic**: "High VIX suggests premium collection opportunity"
- **Risk**: Limited profit, limited loss

### Straddle
- **When**: Expected volatility, earnings, events
- **AI Logic**: "Earnings week, expect large moves"
- **Risk**: Unlimited profit, limited loss

### Strangle
- **When**: Moderate volatility, directional bias
- **AI Logic**: "Trending market with volatility"
- **Risk**: Unlimited profit, limited loss

### Call/Put Spreads
- **When**: Directional bias, defined risk
- **AI Logic**: "Strong trend, limited risk preferred"
- **Risk**: Limited profit, limited loss

## 🔧 Technical Details

### Architecture
- **Multi-threaded**: Separate threads for monitoring, trading, and dashboard
- **Event-driven**: Responds to market conditions and time intervals
- **Modular**: Separate components for AI, trading, and analysis
- **Robust**: Error handling and fallback strategies

### Data Sources
- **Market Data**: Yahoo Finance API for real-time prices
- **AI Analysis**: OpenAI GPT-4 for strategy generation
- **Risk Management**: Built-in position sizing and risk controls

### Logging
- **Trading Log**: All trades and strategies logged to `trading.log`
- **Performance Metrics**: Real-time tracking of P&L and performance
- **AI Decisions**: All AI reasoning and recommendations logged

## 🛡️ Risk Management

### Built-in Protections
- **Position Limits**: Maximum number of concurrent positions
- **Risk per Trade**: Configurable percentage of capital at risk
- **Stop Losses**: Automatic position management
- **Diversification**: Multiple symbols and strategies

### Safety Features
- **Demo Mode**: Test without real money
- **Fallback Strategies**: Works without AI if needed
- **Error Handling**: Graceful handling of API failures
- **Manual Override**: Stop trading at any time

## 📁 File Structure

```
bot-trader/
├── auto_trader.py              # Main automated trading application
├── automated_trader.py         # Core trading engine
├── ai_strategy_generator.py    # AI strategy generation
├── run_auto_trader.sh          # Startup script
├── auto_trader_config.json     # Configuration file
├── test_auto_trader.py         # Test script
├── trading.log                 # Trading activity log
└── README_AUTO_TRADER.md       # This file
```

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install openai yfinance numpy pandas
```

### 2. Set API Key (Optional)
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Run the System
```bash
./run_auto_trader.sh
```

### 4. Watch It Trade!
The system will start automatically and begin:
- Monitoring markets
- Generating AI strategies
- Executing trades
- Displaying real-time updates

## 🎮 Demo Mode

Run in demo mode to test without real trades:
```bash
./run_auto_trader.sh --demo
```

## �� Performance Monitoring

The system tracks:
- **Total Trades**: Number of strategies executed
- **Win Rate**: Percentage of profitable trades
- **Total P&L**: Overall profit/loss
- **Risk Metrics**: Maximum drawdown, Sharpe ratio
- **AI Performance**: Strategy success rates

## 🔍 Troubleshooting

### Common Issues

1. **No OpenAI API Key**:
   - System will use fallback strategies
   - Set `OPENAI_API_KEY` environment variable

2. **Missing Dependencies**:
   - Run: `pip install openai yfinance numpy pandas`

3. **Market Data Issues**:
   - System will use simulated data
   - Check internet connection

4. **High API Usage**:
   - Adjust intervals in configuration
   - Use demo mode for testing

## ⚠️ Disclaimer

This is a simulation tool for educational purposes only. It does not provide financial advice and should not be used for actual trading decisions. Options trading involves significant risk and may not be suitable for all investors.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Ready to start automated trading? Just run `./run_auto_trader.sh` and watch the AI trade!** 🚀
