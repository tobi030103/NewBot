# NewBot - Quick Start Guide

This guide will help you get NewBot up and running in minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/tobi030103/NewBot.git
cd NewBot
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Setup Wizard

```bash
python setup.py
```

The setup wizard will:
- Check your Python version
- Create necessary directories
- Create configuration files
- Check dependencies
- Help you configure trading mode and broker

### 5. Test Your Installation

```bash
python test_modules.py
```

All 8 tests should pass ✓

### 6. Try the Demo

```bash
python demo.py
```

This demonstrates the bot's capabilities without real trading.

## Running the Bot

### With Mock Broker (Recommended for First Time)

```bash
python bot.py
```

The default configuration uses the mock broker, which simulates trading without connecting to real exchanges.

### With Real Broker (After Testing)

1. Get API credentials from your broker (e.g., Binance)
2. Add them to `.env` file:
   ```
   BROKER_API_KEY=your_key_here
   BROKER_API_SECRET=your_secret_here
   ```
3. Edit `config.yaml`:
   ```yaml
   broker:
     name: binance
     sandbox: true  # Use testnet first!
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

## Configuration

The bot is configured via `config.yaml`. Key settings:

### Trading Mode
```yaml
trading:
  mode: paper  # 'paper' for simulation, 'live' for real trading
```

### Risk Management
```yaml
risk_management:
  stop_loss_percent: 2.0      # Stop loss at 2% below entry
  take_profit_percent: 5.0    # Take profit at 5% above entry
  use_trailing_stop: true     # Enable trailing stop
```

### Strategy Selection
```yaml
strategy:
  name: moving_average_crossover
  parameters:
    fast_period: 10
    slow_period: 30
```

Available strategies:
- `moving_average_crossover`: MA crossover strategy
- `rsi_strategy`: RSI-based momentum strategy
- `trend_following`: EMA-based trend strategy

### Broker Configuration
```yaml
broker:
  name: mock      # 'mock', 'binance', 'bitpanda'
  sandbox: true   # Use testnet/sandbox mode
```

## Safety Tips

⚠️ **IMPORTANT**: Always follow these safety guidelines:

1. **Start with Paper Trading**: Use `mode: paper` until you're comfortable
2. **Use Sandbox Mode**: Enable `sandbox: true` when testing with real brokers
3. **Start Small**: Begin with small amounts you can afford to lose
4. **Monitor Regularly**: Check the bot's activity daily
5. **Keep Keys Secure**: Never share your API keys
6. **Use Stop Losses**: The bot sets them automatically, don't disable
7. **Test Thoroughly**: Run extensive tests before live trading

## Monitoring

### Logs
- Console output shows important events
- Detailed logs in `logs/newbot.log`
- Log rotation keeps files manageable

### Notifications
Configure email or webhook notifications in `config.yaml`:

```yaml
notifications:
  enabled: true
  email:
    enabled: true
    smtp_server: smtp.gmail.com
    to_address: your_email@gmail.com
```

### Backups
Automatic backups are created every 6 hours (configurable):

```yaml
backup:
  enabled: true
  interval_hours: 6
  backup_dir: backups
```

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "Invalid configuration" errors
Check your `config.yaml` file or run `python setup.py` again.

### Broker connection issues
- Verify API keys in `.env`
- Check if sandbox mode is enabled
- Test network connectivity

### Permission errors
```bash
# On Linux/Mac, ensure proper permissions:
chmod 600 .env
chmod 600 .encryption.key  # if it exists
```

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
3. Check [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute
4. Join the community for support and discussions

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/tobi030103/NewBot/issues)
- **Documentation**: [README.md](README.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)

## License

NewBot is open-source software licensed under the MIT License.

---

**Happy Trading! 🚀**

Remember: *Past performance is not indicative of future results. Trade responsibly.*
