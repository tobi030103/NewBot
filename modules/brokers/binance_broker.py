"""
Binance Broker Implementation

Handles integration with Binance exchange using CCXT library
"""

import ccxt
from typing import Optional
from modules.brokers.broker_factory import BaseBroker


class BinanceBroker(BaseBroker):
    """
    Binance broker implementation using CCXT
    """
    
    def __init__(self, api_key: str, api_secret: str, sandbox: bool = True):
        """Initialize Binance broker"""
        super().__init__(api_key, api_secret, sandbox)
        self._init_exchange()
    
    def _init_exchange(self):
        """Initialize CCXT exchange"""
        try:
            self.exchange = ccxt.binance({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',  # spot, margin, future
                }
            })
            
            if self.sandbox:
                self.exchange.set_sandbox_mode(True)
            
            # Test connection
            self.exchange.load_markets()
            self.connected = True
            self.logger.info("Connected to Binance")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to Binance: {e}")
            self.connected = False
    
    def reconnect(self):
        """Reconnect to Binance"""
        self._init_exchange()
    
    def get_positions(self) -> list:
        """Get all open positions"""
        try:
            balance = self.exchange.fetch_balance()
            positions = []
            
            for currency, amount in balance['total'].items():
                if amount > 0 and currency != 'EUR':
                    positions.append({
                        'symbol': f"{currency}/EUR",
                        'amount': amount,
                    })
            
            return positions
            
        except Exception as e:
            self.logger.error(f"Failed to get positions: {e}")
            return []
    
    def get_open_orders(self) -> list:
        """Get all open orders"""
        try:
            return self.exchange.fetch_open_orders()
        except Exception as e:
            self.logger.error(f"Failed to get open orders: {e}")
            return []
    
    def get_order_status(self, order_id: str) -> str:
        """Get order status"""
        try:
            order = self.exchange.fetch_order(order_id)
            return order['status']
        except Exception as e:
            self.logger.error(f"Failed to get order status: {e}")
            return 'unknown'
    
    def get_market_data(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> dict:
        """Get market data (OHLCV)"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return {
                'symbol': symbol,
                'timeframe': timeframe,
                'data': ohlcv
            }
        except Exception as e:
            self.logger.error(f"Failed to get market data: {e}")
            return {'symbol': symbol, 'timeframe': timeframe, 'data': []}
    
    def get_current_price(self, symbol: str) -> float:
        """Get current market price"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker['last']
        except Exception as e:
            self.logger.error(f"Failed to get current price: {e}")
            return 0.0
    
    def place_order(self, symbol: str, side: str, amount: float,
                   order_type: str = 'market', price: Optional[float] = None) -> dict:
        """Place an order"""
        try:
            if order_type == 'stop_loss':
                # Stop-loss order
                order = self.exchange.create_order(
                    symbol, 'stop_loss_limit', side, amount, price,
                    {'stopPrice': price}
                )
            elif order_type == 'take_profit':
                # Take-profit order
                order = self.exchange.create_order(
                    symbol, 'take_profit_limit', side, amount, price,
                    {'stopPrice': price}
                )
            else:
                # Regular order (market or limit)
                order = self.exchange.create_order(
                    symbol, order_type, side, amount, price
                )
            
            self.logger.info(f"Order placed: {order['id']}")
            return order
            
        except Exception as e:
            self.logger.error(f"Failed to place order: {e}")
            return {}
    
    def cancel_order(self, order_id: str, symbol: str = None) -> bool:
        """Cancel an order"""
        try:
            self.exchange.cancel_order(order_id, symbol)
            self.logger.info(f"Order cancelled: {order_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to cancel order: {e}")
            return False
