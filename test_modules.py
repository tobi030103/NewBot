#!/usr/bin/env python
"""
Quick test script to validate NewBot functionality

This script runs basic tests on the core modules to ensure
everything is working correctly.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("NewBot Module Tests")
print("=" * 60)
print()

# Test 1: Configuration
print("1. Testing Configuration Module...")
try:
    from config import config
    assert config.get('trading.mode') == 'paper'
    broker_name = config.get('broker.name')
    print("   ✓ Configuration loaded successfully")
    print(f"   - Trading mode: {config.get('trading.mode')}")
    print(f"   - Broker: {broker_name}")
except Exception as e:
    print(f"   ✗ Configuration test failed: {e}")
    sys.exit(1)

print()

# Test 2: Logger
print("2. Testing Logger Module...")
try:
    from utils.logging.logger import Logger
    logger = Logger('TestLogger')
    logger.info("Logger test message")
    print("   ✓ Logger working correctly")
except Exception as e:
    print(f"   ✗ Logger test failed: {e}")
    sys.exit(1)

print()

# Test 3: Credential Manager
print("3. Testing Credential Manager...")
try:
    from utils.security.credential_manager import CredentialManager
    cm = CredentialManager()
    cm.set_credential('test', 'value')
    assert cm.get_credential('test') == 'value'
    print("   ✓ Credential manager working correctly")
except Exception as e:
    print(f"   ✗ Credential manager test failed: {e}")
    sys.exit(1)

print()

# Test 4: Mock Broker
print("4. Testing Mock Broker...")
try:
    from modules.brokers.mock_broker import MockBroker
    broker = MockBroker('api_key', 'api_secret', sandbox=True)
    assert broker.is_connected()
    
    # Test getting market data
    data = broker.get_market_data('BTC/EUR', '1h')
    assert data['symbol'] == 'BTC/EUR'
    assert len(data['data']) > 0
    
    # Test placing order
    order = broker.place_order('BTC/EUR', 'buy', 0.01, 'market')
    assert order['status'] == 'filled'
    
    print("   ✓ Mock broker working correctly")
    print(f"   - Connected: {broker.is_connected()}")
    print(f"   - Market data points: {len(data['data'])}")
    print(f"   - Test order placed: {order['id']}")
except Exception as e:
    print(f"   ✗ Mock broker test failed: {e}")
    sys.exit(1)

print()

# Test 5: Strategy
print("5. Testing Trading Strategy...")
try:
    from modules.strategies.moving_average_crossover import MovingAverageCrossover
    
    strategy = MovingAverageCrossover({
        'fast_period': 10,
        'slow_period': 30,
        'signal_threshold': 0.001
    })
    
    # Test with mock data
    market_data = broker.get_market_data('BTC/EUR', '1h')
    signal = strategy.generate_signal(market_data)
    assert signal in ['BUY', 'SELL', 'HOLD']
    
    print("   ✓ Strategy working correctly")
    print(f"   - Generated signal: {signal}")
except Exception as e:
    print(f"   ✗ Strategy test failed: {e}")
    sys.exit(1)

print()

# Test 6: Indicators
print("6. Testing Technical Indicators...")
try:
    import pandas as pd
    from modules.indicators.rsi import calculate_rsi
    from modules.indicators.moving_averages import calculate_sma, calculate_ema
    
    # Create sample data
    prices = pd.Series([100, 102, 101, 103, 105, 104, 106, 108, 107, 109,
                       110, 108, 109, 111, 112, 111, 113, 115, 114, 116])
    
    rsi = calculate_rsi(prices, period=14)
    sma = calculate_sma(prices, period=10)
    ema = calculate_ema(prices, period=10)
    
    assert not rsi.isna().all()
    assert not sma.isna().all()
    assert not ema.isna().all()
    
    print("   ✓ Indicators working correctly")
    print(f"   - RSI last value: {rsi.iloc[-1]:.2f}")
    print(f"   - SMA last value: {sma.iloc[-1]:.2f}")
    print(f"   - EMA last value: {ema.iloc[-1]:.2f}")
except Exception as e:
    print(f"   ✗ Indicators test failed: {e}")
    sys.exit(1)

print()

# Test 7: Backup Manager
print("7. Testing Backup Manager...")
try:
    from utils.backup.backup_manager import BackupManager
    
    backup_mgr = BackupManager()
    backup_file = backup_mgr.create_backup({'test': 'data'})
    
    # Verify backup exists
    assert Path(backup_file).exists()
    
    # Test restore
    restored = backup_mgr.restore_backup(backup_file)
    assert 'config' in restored
    assert 'timestamp' in restored
    
    print("   ✓ Backup manager working correctly")
    print(f"   - Backup created: {Path(backup_file).name}")
except Exception as e:
    print(f"   ✗ Backup manager test failed: {e}")
    sys.exit(1)

print()

# Test 8: Notifier
print("8. Testing Notifier...")
try:
    from modules.notifications.notifier import Notifier
    
    notifier = Notifier()
    notifier.send_notification("Test", "Test message", priority="low")
    
    print("   ✓ Notifier working correctly")
except Exception as e:
    print(f"   ✗ Notifier test failed: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("All tests passed! ✓")
print("=" * 60)
print()
print("NewBot is ready to use!")
print("Run 'python bot.py' to start the trading bot.")
print()
