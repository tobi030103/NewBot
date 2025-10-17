#!/usr/bin/env python
"""
Demo script to show NewBot capabilities

This script demonstrates how to use NewBot without actually trading.
It uses the mock broker to simulate trading activities.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from modules.brokers.mock_broker import MockBroker
from modules.strategies.moving_average_crossover import MovingAverageCrossover
from utils.logging.logger import Logger

def demo():
    """Run a simple demo of NewBot capabilities"""
    
    print("=" * 70)
    print("NewBot Trading Bot - Demo")
    print("=" * 70)
    print()
    
    # Initialize logger
    logger = Logger('Demo')
    logger.info("Starting NewBot demo")
    
    # Show configuration
    print("Configuration:")
    print(f"  Trading Mode: {config.get('trading.mode')}")
    print(f"  Trade Amount: {config.get('trading.trade_amount')} {config.get('trading.base_currency')}")
    print(f"  Stop Loss: {config.get('risk_management.stop_loss_percent')}%")
    print(f"  Take Profit: {config.get('risk_management.take_profit_percent')}%")
    print()
    
    # Initialize mock broker
    print("Connecting to broker...")
    broker = MockBroker('demo_key', 'demo_secret', sandbox=True)
    logger.info("Connected to mock broker")
    print(f"  Status: {'Connected' if broker.is_connected() else 'Disconnected'}")
    print()
    
    # Get market data
    symbol = 'BTC/EUR'
    print(f"Fetching market data for {symbol}...")
    market_data = broker.get_market_data(symbol, '1h', limit=50)
    
    if market_data['data']:
        latest = market_data['data'][-1]
        print(f"  Latest Price: €{latest[4]:,.2f}")
        print(f"  24h High: €{max(candle[2] for candle in market_data['data'][-24:]):,.2f}")
        print(f"  24h Low: €{min(candle[3] for candle in market_data['data'][-24:]):,.2f}")
    print()
    
    # Initialize strategy
    print("Loading trading strategy...")
    strategy = MovingAverageCrossover({
        'fast_period': 10,
        'slow_period': 30,
        'signal_threshold': 0.001
    })
    logger.info("Strategy loaded: Moving Average Crossover")
    print("  Strategy: Moving Average Crossover")
    print("  Fast MA: 10 periods")
    print("  Slow MA: 30 periods")
    print()
    
    # Generate trading signal
    print("Analyzing market conditions...")
    signal = strategy.generate_signal(market_data)
    print(f"  Trading Signal: {signal}")
    print()
    
    # Simulate placing an order if signal is BUY
    if signal == 'BUY':
        print("Executing BUY order...")
        current_price = broker.get_current_price(symbol)
        amount = 0.01  # 0.01 BTC
        
        # Calculate SL/TP
        sl_pct = config.get('risk_management.stop_loss_percent', 2.0)
        tp_pct = config.get('risk_management.take_profit_percent', 5.0)
        
        stop_loss = current_price * (1 - sl_pct / 100)
        take_profit = current_price * (1 + tp_pct / 100)
        
        # Place order
        order = broker.place_order(symbol, 'buy', amount, 'market')
        
        if order and order.get('status') == 'filled':
            print(f"  ✓ Order filled at €{current_price:,.2f}")
            print(f"  Amount: {amount} BTC")
            print(f"  Stop Loss: €{stop_loss:,.2f}")
            print(f"  Take Profit: €{take_profit:,.2f}")
            
            # Place risk management orders
            sl_order = broker.place_order(symbol, 'sell', amount, 'stop_loss', stop_loss)
            tp_order = broker.place_order(symbol, 'sell', amount, 'take_profit', take_profit)
            
            print(f"  ✓ Stop Loss order placed: {sl_order['id']}")
            print(f"  ✓ Take Profit order placed: {tp_order['id']}")
            
            logger.info(f"Demo order executed: {amount} {symbol} at €{current_price:,.2f}")
    else:
        print(f"  No action taken (signal: {signal})")
    
    print()
    
    # Show open positions
    print("Current Positions:")
    positions = broker.get_positions()
    if positions:
        for pos in positions:
            print(f"  {pos}")
    else:
        print("  No open positions")
    print()
    
    # Show open orders
    print("Open Orders:")
    orders = broker.get_open_orders()
    if orders:
        for order in orders[:3]:  # Show first 3
            print(f"  {order['id']}: {order['side'].upper()} {order['amount']} @ {order.get('type', 'market')}")
        if len(orders) > 3:
            print(f"  ... and {len(orders) - 3} more")
    else:
        print("  No open orders")
    print()
    
    print("=" * 70)
    print("Demo completed successfully!")
    print()
    print("To run the actual bot with mock broker:")
    print("  1. Copy config.yaml.example to config.yaml")
    print("  2. Set broker.name to 'mock' in config.yaml")
    print("  3. Run: python bot.py")
    print()
    print("To run with a real broker:")
    print("  1. Get API credentials from your broker")
    print("  2. Set them in .env file or config.yaml")
    print("  3. Enable sandbox mode first!")
    print("  4. Run: python bot.py")
    print("=" * 70)
    print()

if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nDemo error: {e}")
        sys.exit(1)
