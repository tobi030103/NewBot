"""
NewBot - Advanced Trading Bot

Main application file containing the core trading logic and orchestration.
Handles automated trading, risk management, order monitoring, and system coordination.
"""

import time
import signal
import sys
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

from config import config
from modules.brokers.broker_factory import BrokerFactory
from modules.strategies.strategy_factory import StrategyFactory
from utils.logging.logger import Logger
from utils.security.credential_manager import CredentialManager
from utils.backup.backup_manager import BackupManager
from modules.notifications.notifier import Notifier


class NewBot:
    """
    Main trading bot class
    
    Coordinates all components including:
    - Trading execution
    - Strategy evaluation
    - Risk management
    - Order monitoring
    - Backup and recovery
    """
    
    def __init__(self):
        """Initialize the trading bot"""
        self.logger = Logger('NewBot')
        self.running = False
        self.positions: Dict = {}
        self.open_orders: List = []
        
        # Initialize components
        self._init_components()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info("NewBot initialized successfully")
    
    def _init_components(self):
        """Initialize all bot components"""
        try:
            # Validate configuration
            if not config.validate():
                raise ValueError("Invalid configuration")
            
            # Initialize credential manager
            self.credential_manager = CredentialManager()
            
            # Initialize broker connection
            broker_name = config.get('broker.name')
            api_key = config.get('broker.api_key')
            api_secret = config.get('broker.api_secret')
            sandbox = config.get('broker.sandbox', True)
            
            self.broker = BrokerFactory.create_broker(
                broker_name, 
                api_key, 
                api_secret, 
                sandbox
            )
            self.logger.info(f"Connected to broker: {broker_name}")
            
            # Initialize trading strategy
            strategy_name = config.get('strategy.name')
            strategy_params = config.get('strategy.parameters', {})
            
            self.strategy = StrategyFactory.create_strategy(
                strategy_name,
                strategy_params
            )
            self.logger.info(f"Loaded strategy: {strategy_name}")
            
            # Initialize notification system
            self.notifier = Notifier()
            
            # Initialize backup manager
            if config.get('backup.enabled', True):
                self.backup_manager = BackupManager()
                self.logger.info("Backup manager initialized")
            else:
                self.backup_manager = None
            
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {e}")
            raise
    
    def start(self):
        """Start the trading bot"""
        self.logger.info("Starting NewBot...")
        
        # Send startup notification
        self.notifier.send_notification(
            "NewBot Started",
            f"Trading bot started in {config.get('trading.mode')} mode"
        )
        
        self.running = True
        
        try:
            self._trading_loop()
        except Exception as e:
            self.logger.error(f"Critical error in trading loop: {e}")
            self.notifier.send_notification(
                "NewBot Error",
                f"Critical error: {e}",
                priority="high"
            )
            raise
        finally:
            self.stop()
    
    def _trading_loop(self):
        """Main trading loop"""
        check_interval = config.get('monitoring.check_interval_seconds', 60)
        
        while self.running:
            try:
                # Check market conditions
                self._check_market()
                
                # Monitor existing positions
                self._monitor_positions()
                
                # Monitor open orders
                self._monitor_orders()
                
                # Evaluate trading opportunities
                self._evaluate_trading_signals()
                
                # Perform backup if needed
                if self.backup_manager:
                    self.backup_manager.auto_backup()
                
                # Wait before next iteration
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                self.logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                self.logger.error(f"Error in trading loop: {e}")
                self.notifier.send_notification(
                    "NewBot Warning",
                    f"Trading loop error: {e}",
                    priority="medium"
                )
                time.sleep(check_interval)
    
    def _check_market(self):
        """Check market conditions and connectivity"""
        try:
            # Check broker connection
            if not self.broker.is_connected():
                self.logger.warning("Broker connection lost, attempting to reconnect...")
                self.broker.reconnect()
                self.notifier.send_notification(
                    "Connection Issue",
                    "Broker connection lost and reconnected",
                    priority="medium"
                )
        except Exception as e:
            self.logger.error(f"Market check failed: {e}")
    
    def _monitor_positions(self):
        """Monitor all open positions"""
        try:
            positions = self.broker.get_positions()
            
            for position in positions:
                # Check if stop-loss or take-profit needs adjustment
                self._adjust_risk_levels(position)
                
                # Log position status
                self.logger.debug(f"Position: {position}")
                
        except Exception as e:
            self.logger.error(f"Position monitoring failed: {e}")
    
    def _monitor_orders(self):
        """Monitor all open orders"""
        try:
            orders = self.broker.get_open_orders()
            
            for order in orders:
                # Check order status
                status = self.broker.get_order_status(order['id'])
                
                # Notify on filled orders
                if status == 'filled':
                    self.notifier.send_notification(
                        "Order Filled",
                        f"Order {order['id']} filled at {order.get('price', 'market')}",
                        priority="low"
                    )
                    self.logger.info(f"Order filled: {order['id']}")
                
                # Notify on cancelled orders
                elif status == 'cancelled':
                    self.notifier.send_notification(
                        "Order Cancelled",
                        f"Order {order['id']} was cancelled",
                        priority="low"
                    )
                    self.logger.info(f"Order cancelled: {order['id']}")
                    
        except Exception as e:
            self.logger.error(f"Order monitoring failed: {e}")
    
    def _evaluate_trading_signals(self):
        """Evaluate trading signals from strategy"""
        try:
            # Get market data
            symbol = f"{config.get('trading.quote_currency')}/{config.get('trading.base_currency')}"
            timeframe = config.get('strategy.timeframe', '1h')
            
            market_data = self.broker.get_market_data(symbol, timeframe)
            
            # Get trading signal from strategy
            signal = self.strategy.generate_signal(market_data)
            
            # Execute trades based on signal
            if signal == 'BUY':
                self._execute_buy(symbol)
            elif signal == 'SELL':
                self._execute_sell(symbol)
                
        except Exception as e:
            self.logger.error(f"Signal evaluation failed: {e}")
    
    def _execute_buy(self, symbol: str):
        """
        Execute a buy order with risk management
        
        Args:
            symbol: Trading pair symbol
        """
        try:
            # Check if we can open new position
            max_positions = config.get('trading.max_positions', 5)
            if len(self.positions) >= max_positions:
                self.logger.info("Max positions reached, skipping buy signal")
                return
            
            # Get trade amount
            amount = config.get('trading.trade_amount')
            
            # Calculate stop-loss and take-profit levels
            current_price = self.broker.get_current_price(symbol)
            stop_loss_pct = config.get('risk_management.stop_loss_percent', 2.0)
            take_profit_pct = config.get('risk_management.take_profit_percent', 5.0)
            
            stop_loss = current_price * (1 - stop_loss_pct / 100)
            take_profit = current_price * (1 + take_profit_pct / 100)
            
            # Place buy order with OCO (One-Cancels-Other) for SL/TP
            order = self.broker.place_order(
                symbol=symbol,
                side='buy',
                amount=amount,
                order_type='market'
            )
            
            # Place stop-loss and take-profit orders
            if order and order.get('status') == 'filled':
                self._place_risk_orders(symbol, order, stop_loss, take_profit)
                
                # Send notification
                self.notifier.send_notification(
                    "Buy Order Executed",
                    f"Bought {amount} {symbol} at {current_price}\nSL: {stop_loss}\nTP: {take_profit}",
                    priority="medium"
                )
                
                self.logger.info(f"Buy order executed: {symbol} at {current_price}")
                
        except Exception as e:
            self.logger.error(f"Buy execution failed: {e}")
            self.notifier.send_notification(
                "Buy Order Failed",
                f"Failed to execute buy order: {e}",
                priority="high"
            )
    
    def _execute_sell(self, symbol: str):
        """
        Execute a sell order
        
        Args:
            symbol: Trading pair symbol
        """
        try:
            # Check if we have position to sell
            if symbol not in self.positions:
                self.logger.info(f"No position to sell for {symbol}")
                return
            
            position = self.positions[symbol]
            amount = position.get('amount')
            
            # Place sell order
            order = self.broker.place_order(
                symbol=symbol,
                side='sell',
                amount=amount,
                order_type='market'
            )
            
            if order and order.get('status') == 'filled':
                current_price = self.broker.get_current_price(symbol)
                
                # Send notification
                self.notifier.send_notification(
                    "Sell Order Executed",
                    f"Sold {amount} {symbol} at {current_price}",
                    priority="medium"
                )
                
                self.logger.info(f"Sell order executed: {symbol} at {current_price}")
                
                # Remove position
                del self.positions[symbol]
                
        except Exception as e:
            self.logger.error(f"Sell execution failed: {e}")
            self.notifier.send_notification(
                "Sell Order Failed",
                f"Failed to execute sell order: {e}",
                priority="high"
            )
    
    def _place_risk_orders(self, symbol: str, entry_order: Dict, stop_loss: float, take_profit: float):
        """
        Place stop-loss and take-profit orders
        
        Args:
            symbol: Trading pair symbol
            entry_order: The entry order details
            stop_loss: Stop-loss price
            take_profit: Take-profit price
        """
        try:
            amount = entry_order.get('filled', entry_order.get('amount'))
            
            # Place stop-loss order
            sl_order = self.broker.place_order(
                symbol=symbol,
                side='sell',
                amount=amount,
                order_type='stop_loss',
                price=stop_loss
            )
            
            # Place take-profit order
            tp_order = self.broker.place_order(
                symbol=symbol,
                side='sell',
                amount=amount,
                order_type='take_profit',
                price=take_profit
            )
            
            # Store position with risk orders
            self.positions[symbol] = {
                'amount': amount,
                'entry_price': entry_order.get('price'),
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'sl_order_id': sl_order.get('id') if sl_order else None,
                'tp_order_id': tp_order.get('id') if tp_order else None,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to place risk orders: {e}")
    
    def _adjust_risk_levels(self, position: Dict):
        """
        Adjust stop-loss and take-profit levels (trailing stop)
        
        Args:
            position: Position details
        """
        try:
            if not config.get('risk_management.use_trailing_stop', False):
                return
            
            symbol = position.get('symbol')
            current_price = self.broker.get_current_price(symbol)
            entry_price = position.get('entry_price')
            trailing_pct = config.get('risk_management.trailing_stop_percent', 1.5)
            
            # Calculate new trailing stop
            new_stop_loss = current_price * (1 - trailing_pct / 100)
            
            # Only adjust if new stop is higher than current (for long positions)
            if new_stop_loss > position.get('stop_loss', 0):
                # Cancel old stop-loss order
                if position.get('sl_order_id'):
                    self.broker.cancel_order(position['sl_order_id'])
                
                # Place new stop-loss order
                sl_order = self.broker.place_order(
                    symbol=symbol,
                    side='sell',
                    amount=position['amount'],
                    order_type='stop_loss',
                    price=new_stop_loss
                )
                
                # Update position
                position['stop_loss'] = new_stop_loss
                position['sl_order_id'] = sl_order.get('id') if sl_order else None
                
                self.logger.info(f"Trailing stop adjusted for {symbol}: {new_stop_loss}")
                
        except Exception as e:
            self.logger.error(f"Failed to adjust risk levels: {e}")
    
    def stop(self):
        """Stop the trading bot gracefully"""
        self.logger.info("Stopping NewBot...")
        self.running = False
        
        # Perform final backup
        if self.backup_manager:
            self.backup_manager.create_backup()
        
        # Send shutdown notification
        self.notifier.send_notification(
            "NewBot Stopped",
            "Trading bot has been stopped",
            priority="medium"
        )
        
        self.logger.info("NewBot stopped successfully")
    
    def _signal_handler(self, signum, frame):
        """Handle system signals for graceful shutdown"""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)


def main():
    """Main entry point"""
    print("=" * 60)
    print("NewBot - Advanced Trading Bot")
    print("=" * 60)
    print()
    
    # Create logs directory
    Path('logs').mkdir(exist_ok=True)
    
    try:
        # Initialize and start bot
        bot = NewBot()
        bot.start()
        
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
