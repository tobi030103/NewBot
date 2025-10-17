# NewBot Architecture

This document describes the architectural design and implementation of NewBot trading bot.

## Overview

NewBot follows a modular, layered architecture designed for extensibility, maintainability, and security.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         bot.py                              │
│                    (Main Application)                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├─────────────────┐
                              │                 │
                              ▼                 ▼
┌──────────────────────────────────┐  ┌─────────────────────┐
│         config.py                │  │   utils/            │
│   (Configuration Management)     │  │   - logging/        │
└──────────────────────────────────┘  │   - security/       │
                                      │   - backup/         │
                                      │   - network/        │
                                      └─────────────────────┘
                              │
                ┌─────────────┴───────────────┐
                │                             │
                ▼                             ▼
┌────────────────────────────┐  ┌────────────────────────────┐
│      modules/brokers/      │  │    modules/strategies/     │
│  - BrokerFactory           │  │  - StrategyFactory         │
│  - BaseBroker              │  │  - BaseStrategy            │
│  - BinanceBroker           │  │  - MA Crossover            │
│  - MockBroker              │  │  - RSI Strategy            │
│  - BitpandaBroker          │  │  - Trend Following         │
└────────────────────────────┘  └────────────────────────────┘
                │                             │
                │                             │
                ▼                             ▼
┌────────────────────────────┐  ┌────────────────────────────┐
│   modules/notifications/   │  │    modules/indicators/     │
│  - Notifier                │  │  - RSI                     │
│  - Email                   │  │  - Moving Averages         │
│  - Webhook                 │  │  - Bollinger Bands         │
└────────────────────────────┘  └────────────────────────────┘
```

## Core Components

### 1. Main Application (bot.py)

The central orchestrator that coordinates all components:

- **Initialization**: Sets up all subsystems (broker, strategy, logging, backup, notifications)
- **Trading Loop**: Continuous market monitoring and trade execution
- **Order Management**: Monitors and manages open orders
- **Position Management**: Tracks and adjusts open positions
- **Risk Management**: Implements stop-loss and take-profit mechanisms
- **Signal Handler**: Graceful shutdown on system signals

**Key Methods:**
- `start()`: Starts the bot
- `_trading_loop()`: Main execution loop
- `_execute_buy()` / `_execute_sell()`: Trade execution with risk management
- `_monitor_orders()` / `_monitor_positions()`: Order and position tracking

### 2. Configuration Management (config.py)

Centralized configuration handling with:

- **YAML-based configuration**: Human-readable config files
- **Environment variables**: Secure credential storage
- **Default values**: Sensible defaults for all settings
- **Validation**: Configuration integrity checks
- **Dynamic updates**: Runtime configuration changes

**Configuration Structure:**
- Trading parameters (mode, currency pairs, amounts)
- Risk management settings (SL/TP percentages, limits)
- Broker credentials and settings
- Strategy selection and parameters
- Notification preferences
- Logging and backup settings

### 3. Broker Module

Abstract broker interface with multiple implementations:

**Base Class: `BaseBroker`**
- Defines common interface for all brokers
- Standard methods for market data, orders, positions

**Implementations:**
- **BinanceBroker**: Full Binance integration via CCXT
- **MockBroker**: Simulation for testing
- **BitpandaBroker**: Placeholder for future implementation

**Factory Pattern:**
- `BrokerFactory.create_broker()` instantiates brokers dynamically
- Easy to add new broker integrations

**Key Methods:**
- `get_market_data()`: Retrieve OHLCV data
- `place_order()`: Execute trades
- `get_positions()`: Query open positions
- `cancel_order()`: Cancel pending orders

### 4. Strategy Module

Pluggable trading strategies:

**Base Class: `BaseStrategy`**
- Common interface for all strategies
- Parameter management
- Signal generation contract

**Available Strategies:**
- **Moving Average Crossover**: Trend following using MA crossovers
- **RSI Strategy**: Mean reversion based on RSI
- **Trend Following**: EMA-based trend identification

**Factory Pattern:**
- `StrategyFactory.create_strategy()` for dynamic instantiation
- Easy to add custom strategies

**Signal Types:**
- `BUY`: Enter long position
- `SELL`: Exit position or enter short
- `HOLD`: No action

### 5. Indicators Module

Technical analysis indicators:

**Available Indicators:**
- **RSI**: Relative Strength Index
- **Moving Averages**: SMA, EMA, WMA, MACD
- **Bollinger Bands**: Volatility bands

**Design:**
- Pure functions taking pandas Series
- Composable and reusable
- Can be used in any strategy

### 6. Utilities

Supporting services:

**Logging (`utils/logging/logger.py`):**
- File rotation (size-based)
- Multiple log levels
- Console and file output
- Structured logging with timestamps

**Security (`utils/security/credential_manager.py`):**
- Fernet encryption for credentials
- Secure key storage
- Encrypted credential file
- Restricted file permissions

**Backup (`utils/backup/backup_manager.py`):**
- Automatic scheduled backups
- JSON-based backup format
- Backup rotation (max count)
- State recovery

**Network (`utils/network/network_manager.py`):**
- Connection monitoring
- Automatic reconnection
- Router management (planned)

**Notifications (`modules/notifications/notifier.py`):**
- Multi-channel alerts (email, webhook)
- Priority levels
- Event-based triggering
- Configurable delivery

## Data Flow

### Trading Loop Cycle

```
1. Check Market
   ├─> Test broker connection
   └─> Reconnect if needed

2. Monitor Positions
   ├─> Get open positions
   ├─> Adjust trailing stops
   └─> Log position status

3. Monitor Orders
   ├─> Check order status
   ├─> Notify on fills/cancels
   └─> Update internal state

4. Evaluate Signals
   ├─> Get market data
   ├─> Run strategy
   ├─> Generate signal (BUY/SELL/HOLD)
   └─> Execute if conditions met

5. Execute Trade (if signal)
   ├─> Validate constraints
   ├─> Place entry order
   ├─> Place SL/TP orders
   └─> Send notifications

6. Backup
   └─> Auto-backup if interval elapsed

7. Sleep (check_interval_seconds)
```

### Order Execution Flow

```
Signal Generated (BUY/SELL)
    │
    ├─> Validate (max positions, risk limits)
    │
    ├─> Calculate SL/TP prices
    │
    ├─> Place market order
    │       │
    │       ├─> Success: Order filled
    │       │       │
    │       │       ├─> Place SL order
    │       │       ├─> Place TP order
    │       │       ├─> Record position
    │       │       └─> Send notification
    │       │
    │       └─> Failure: Log error & notify
    │
    └─> Continue monitoring
```

## Security Features

### 1. Credential Protection
- Encrypted storage using Fernet (symmetric encryption)
- API keys never stored in plain text
- Environment variable support
- Restricted file permissions (0600)

### 2. Configuration Security
- Sensitive data in .env (excluded from git)
- config.yaml template without secrets
- Runtime credential injection

### 3. Safe Defaults
- Paper trading mode by default
- Sandbox mode for brokers
- Conservative risk limits
- Mock broker for testing

## Risk Management

### Multi-Level Protection

**Trade Level:**
- Stop-loss on every trade
- Take-profit targets
- Position size limits

**Portfolio Level:**
- Maximum concurrent positions
- Daily loss limits
- Risk per trade percentage

**System Level:**
- Connection monitoring
- Automatic reconnection
- Backup and recovery
- Emergency notifications

## Extensibility

### Adding New Brokers

1. Create new broker class extending `BaseBroker`
2. Implement required methods (connect, orders, data)
3. Register in `BrokerFactory`

Example:
```python
class NewBroker(BaseBroker):
    def __init__(self, api_key, api_secret, sandbox):
        super().__init__(api_key, api_secret, sandbox)
        # Initialize broker connection
```

### Adding New Strategies

1. Create strategy class extending `BaseStrategy`
2. Implement `generate_signal()` method
3. Register in `StrategyFactory`

Example:
```python
class MyStrategy(BaseStrategy):
    def generate_signal(self, market_data: dict) -> str:
        # Analyze data
        return 'BUY' | 'SELL' | 'HOLD'
```

### Adding New Indicators

Simply add functions that take pandas Series and return calculated values:

```python
def calculate_my_indicator(prices: pd.Series, period: int) -> pd.Series:
    # Calculate indicator
    return result
```

## Performance Considerations

### Optimization Strategies

1. **Efficient Data Handling**
   - pandas for vectorized operations
   - Limited data fetch (only needed periods)
   - Caching where appropriate

2. **API Rate Limiting**
   - CCXT built-in rate limiting
   - Configurable check intervals
   - Retry mechanisms

3. **Resource Management**
   - Log file rotation
   - Backup file limits
   - Memory-efficient data structures

## Testing Strategy

### Test Hierarchy

1. **Unit Tests**: Individual components
2. **Integration Tests**: Component interactions
3. **Mock Trading**: Full system with fake broker
4. **Sandbox Trading**: Real broker, test environment
5. **Live Trading**: Production environment

### Test Tools

- `test_modules.py`: Automated test suite
- `demo.py`: Interactive demonstration
- Mock broker for safe testing
- Configurable test mode

## Deployment Options

### Local Deployment
- Run on personal computer
- Full control
- Subject to local network

### Cloud Deployment
- VPS (Digital Ocean, AWS EC2, etc.)
- 24/7 operation
- Better uptime
- Remote access

### Container Deployment
- Docker containerization (planned)
- Easy scaling
- Consistent environment

## Future Enhancements

### Planned Features

1. **GUI Interface**: Web-based dashboard
2. **Backtesting**: Historical strategy testing
3. **Advanced Analytics**: Performance metrics, charts
4. **Machine Learning**: Adaptive strategies
5. **Portfolio Management**: Multi-asset trading
6. **Social Features**: Strategy sharing
7. **Mobile App**: iOS/Android monitoring
8. **Advanced Orders**: Conditional, basket orders
9. **Market Making**: Liquidity provision strategies
10. **Arbitrage**: Cross-exchange opportunities

### Architecture Evolution

- Microservices architecture for scaling
- Event-driven architecture with message queues
- Time-series database for historical data
- Redis for caching and real-time data
- WebSocket for live updates

## Conclusion

NewBot's architecture prioritizes:
- **Modularity**: Easy to extend and modify
- **Security**: Protected credentials and safe defaults
- **Reliability**: Robust error handling and recovery
- **Usability**: Clear interfaces and good documentation
- **Performance**: Efficient data processing and API usage

This design enables both novice users to get started quickly and advanced users to customize deeply.
