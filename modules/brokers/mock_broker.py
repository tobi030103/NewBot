"""
Mock Broker Implementation

Mock broker for testing without connecting to real exchanges
"""

import random
from typing import Optional
from modules.brokers.broker_factory import BaseBroker


class MockBroker(BaseBroker):
    """
    Mock broker for testing and development
    """
    
    def __init__(self, api_key: str, api_secret: str, sandbox: bool = True):
        """Initialize mock broker"""
        super().__init__(api_key, api_secret, sandbox)
        self.connected = True
        self.positions = []
        self.orders = []
        self.order_counter = 0
        self.logger.info("Mock broker initialized")
    
    def reconnect(self):
        """Reconnect to mock broker"""
        self.connected = True
        self.logger.info("Mock broker reconnected")
    
    def get_positions(self) -> list:
        """Get all open positions"""
        return self.positions
    
    def get_open_orders(self) -> list:
        """Get all open orders"""
        return [o for o in self.orders if o['status'] == 'open']
    
    def get_order_status(self, order_id: str) -> str:
        """Get order status"""
        for order in self.orders:
            if order['id'] == order_id:
                return order['status']
        return 'unknown'
    
    def get_market_data(self, symbol: str, timeframe: str, limit: int = 100) -> dict:
        """Get mock market data"""
        # Generate fake OHLCV data
        data = []
        base_price = 50000.0
        
        for i in range(limit):
            open_price = base_price + random.uniform(-1000, 1000)
            high = open_price + random.uniform(0, 500)
            low = open_price - random.uniform(0, 500)
            close = open_price + random.uniform(-500, 500)
            volume = random.uniform(100, 1000)
            
            data.append([
                i * 3600000,  # timestamp
                open_price,
                high,
                low,
                close,
                volume
            ])
        
        return {
            'symbol': symbol,
            'timeframe': timeframe,
            'data': data
        }
    
    def get_current_price(self, symbol: str) -> float:
        """Get mock current price"""
        return 50000.0 + random.uniform(-1000, 1000)
    
    def place_order(self, symbol: str, side: str, amount: float,
                   order_type: str = 'market', price: Optional[float] = None) -> dict:
        """Place a mock order"""
        self.order_counter += 1
        order_id = f"mock_order_{self.order_counter}"
        
        order = {
            'id': order_id,
            'symbol': symbol,
            'side': side,
            'amount': amount,
            'type': order_type,
            'price': price or self.get_current_price(symbol),
            'status': 'filled' if order_type == 'market' else 'open',
            'filled': amount if order_type == 'market' else 0
        }
        
        self.orders.append(order)
        self.logger.info(f"Mock order placed: {order_id}")
        
        return order
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel a mock order"""
        for order in self.orders:
            if order['id'] == order_id:
                order['status'] = 'cancelled'
                self.logger.info(f"Mock order cancelled: {order_id}")
                return True
        return False
