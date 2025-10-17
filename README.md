# NewBot - Advanced Trading Bot

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

NewBot is a professional, modular trading bot designed for automated trading across multiple exchanges and asset classes. Built with security, flexibility, and extensibility in mind, it provides comprehensive risk management and is suitable for both beginners and advanced traders.

## 🚀 Key Features

### Automated Trading
- **Autonomous Trading**: Make automated buy/sell decisions based on configurable strategies
- **Technical Analysis**: Built-in indicators including RSI, MACD, Bollinger Bands, and Moving Averages
- **Real-time Market Data**: Continuous market monitoring and analysis
- **Multiple Strategies**: Trend following, MA crossover, RSI-based, and custom strategies

### Broker Integration
- **Multi-Exchange Support**: Binance, Bitpanda, and more (via CCXT library)
- **Unified API**: Consistent interface across all brokers
- **Sandbox Mode**: Test strategies without risking real money
- **Modular Design**: Easy to add new broker integrations

### Risk Management
- ✅ **Stop-Loss & Take-Profit**: Automatic risk management on every trade
- ✅ **Trailing Stop**: Dynamic stop-loss adjustment to lock in profits
- ✅ **Guaranteed Stop-Loss**: Protection against extreme market movements (when supported)
- ✅ **OCO Orders**: One-Cancels-Other order mechanism for risk control
- ✅ **Position Limits**: Maximum position and daily loss limits

### Security
- 🔒 **Encrypted Credentials**: API keys and passwords stored with encryption
- 🔒 **Secure Configuration**: Sensitive data never exposed in plain text
- 🔒 **Environment Variables**: Support for .env files
- 🔒 **File Permissions**: Automatic permission restrictions on sensitive files

### Monitoring & Alerts
- 📧 **Email Notifications**: Get alerts for important events
- 🔔 **Webhook Integration**: Send notifications to custom endpoints
- 📊 **Comprehensive Logging**: All actions logged with rotation
- 🔍 **Order Monitoring**: Real-time tracking of all open orders

### Backup & Recovery
- 💾 **Automatic Backups**: Regular backups of configuration and state
- 🔄 **Disaster Recovery**: Restore from backups after system failures
- 📁 **Backup Rotation**: Automatic cleanup of old backups

### Advanced Features
- ☁️ **Cloud-Ready**: Run in cloud environments for 24/7 operation
- 🌐 **Network Management**: Automatic connection monitoring
- 📈 **Backtesting**: Test strategies with historical data (planned)
- 🤖 **AI Integration**: Machine learning support (planned)

---

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Strategies](#strategies)
- [Brokers](#brokers)
- [Development](#development)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/tobi030103/NewBot.git
cd NewBot
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Configuration
```bash
# Copy example configuration (you'll need to create this)
cp config.yaml.example config.yaml

# Edit configuration with your settings
nano config.yaml
```

---

## 🚀 Quick Start

### Using Mock Broker (Testing)
```bash
# Run with mock broker for testing
python bot.py
```

The default configuration uses a mock broker, so you can test the bot without connecting to real exchanges.

### Using Real Broker
1. Get API credentials from your chosen exchange (e.g., Binance)
2. Update `config.yaml` or use environment variables:
   ```bash
   export BROKER_API_KEY="your_api_key"
   export BROKER_API_SECRET="your_api_secret"
   ```
3. Update configuration to use real broker:
   ```yaml
   broker:
     name: binance
     sandbox: true  # Use testnet first!
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

---

## ⚙️ Configuration

NewBot uses a YAML configuration file (`config.yaml`) for all settings. Here's an example:

```yaml
trading:
  mode: paper              # 'paper' or 'live'
  base_currency: EUR
  quote_currency: BTC
  trade_amount: 100.0
  max_positions: 5

risk_management:
  stop_loss_percent: 2.0
  take_profit_percent: 5.0
  use_trailing_stop: true
  trailing_stop_percent: 1.5
  max_risk_per_trade: 2.0

broker:
  name: mock              # 'binance', 'bitpanda', 'mock'
  sandbox: true

strategy:
  name: moving_average_crossover
  parameters:
    fast_period: 10
    slow_period: 30

notifications:
  enabled: true
  email:
    enabled: false
  webhook:
    enabled: false

logging:
  level: INFO
  log_to_file: true

backup:
  enabled: true
  interval_hours: 6
```

### Environment Variables
Sensitive data should be stored in `.env` file:
```
BROKER_API_KEY=your_key_here
BROKER_API_SECRET=your_secret_here
EMAIL_PASSWORD=your_email_password
```

---

## 📖 Usage

### Starting the Bot
```bash
python bot.py
```

### Monitoring
- Logs are written to `logs/newbot.log`
- Console output shows important events
- Email/webhook notifications for critical events

### Stopping the Bot
- Press `Ctrl+C` for graceful shutdown
- Bot will save state and perform final backup

---

## 📁 Project Structure

```
NewBot/
├── bot.py                      # Main application entry point
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
│
├── modules/                    # Core modules
│   ├── brokers/               # Broker integrations
│   │   ├── broker_factory.py
│   │   ├── binance_broker.py
│   │   ├── bitpanda_broker.py
│   │   └── mock_broker.py
│   │
│   ├── strategies/            # Trading strategies
│   │   ├── strategy_factory.py
│   │   ├── moving_average_crossover.py
│   │   ├── rsi_strategy.py
│   │   └── trend_following.py
│   │
│   ├── indicators/            # Technical indicators
│   │   ├── rsi.py
│   │   ├── moving_averages.py
│   │   └── bollinger_bands.py
│   │
│   └── notifications/         # Notification system
│       └── notifier.py
│
└── utils/                     # Utility functions
    ├── logging/               # Logging utilities
    │   └── logger.py
    ├── security/              # Security utilities
    │   └── credential_manager.py
    ├── backup/                # Backup management
    │   └── backup_manager.py
    └── network/               # Network utilities
        └── network_manager.py
```

---

## 📊 Strategies

NewBot includes several built-in strategies:

### 1. Moving Average Crossover
Classic trend-following strategy using fast and slow moving averages.
- **Buy**: When fast MA crosses above slow MA
- **Sell**: When fast MA crosses below slow MA

### 2. RSI Strategy
Momentum-based strategy using the Relative Strength Index.
- **Buy**: When RSI < 30 (oversold)
- **Sell**: When RSI > 70 (overbought)

### 3. Trend Following
Follows market trends using EMA and price action.
- **Buy**: Price significantly above EMA (uptrend)
- **Sell**: Price significantly below EMA (downtrend)

### Creating Custom Strategies
Extend `BaseStrategy` and implement the `generate_signal()` method:

```python
from modules.strategies.strategy_factory import BaseStrategy

class MyStrategy(BaseStrategy):
    def generate_signal(self, market_data: dict) -> str:
        # Your strategy logic here
        return 'BUY' | 'SELL' | 'HOLD'
```

---

## 🏦 Brokers

### Supported Brokers
- **Binance**: Full support via CCXT
- **Bitpanda**: Planned
- **Mock**: For testing without real money

### Adding New Brokers
1. Create new file in `modules/brokers/`
2. Extend `BaseBroker` class
3. Implement required methods
4. Add to `BrokerFactory`

---

## 🛠️ Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
# Format code
black .

# Lint code
flake8 .
```

### Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 🗺️ Roadmap

### Phase 1: Core Features ✅
- [x] Basic bot structure
- [x] Broker integration (Binance, Mock)
- [x] Trading strategies
- [x] Risk management (SL/TP)
- [x] Logging and monitoring
- [x] Backup system

### Phase 2: Enhanced Features 🚧
- [ ] GUI interface
- [ ] Backtesting framework
- [ ] More broker integrations
- [ ] Advanced order types
- [ ] Performance analytics

### Phase 3: Advanced Features 📋
- [ ] Machine learning integration
- [ ] Portfolio management
- [ ] Social trading features
- [ ] Mobile app
- [ ] API for external integrations

---

## ⚠️ Disclaimer

**Trading involves risk. Past performance is not indicative of future results.**

This bot is provided as-is for educational and research purposes. The authors are not responsible for any financial losses incurred through the use of this software. Always test thoroughly with paper trading before using real money.

**Key Recommendations:**
- Start with paper trading (sandbox mode)
- Never invest more than you can afford to lose
- Always use stop-loss orders
- Monitor your bot regularly
- Keep your API keys secure

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/tobi030103/NewBot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tobi030103/NewBot/discussions)
- **Email**: [Support Email]

---

## 🙏 Acknowledgments

- [CCXT](https://github.com/ccxt/ccxt) - Cryptocurrency trading library
- [pandas](https://pandas.pydata.org/) - Data analysis library
- [TA-Lib](https://github.com/mrjbq7/ta-lib) - Technical analysis library

---

**Made with ❤️ by the NewBot Team**