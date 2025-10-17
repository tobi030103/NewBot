"""
Broker Factory for NewBot

Creates broker instances based on configuration
"""

from typing import Optional
from utils.logging.logger import Logger


class BrokerFactory:
    """
    Factory class for creating broker instances
    """
    
    @staticmethod
    def create_broker(broker_name: str, api_key: str, api_secret: str, sandbox: bool = True):
        """
        Create a broker instance
        
        Args:
            broker_name: Name of the broker (e.g., 'binance', 'bitpanda')
            api_key: API key
            api_secret: API secret
            sandbox: Use sandbox/testnet mode
            
        Returns:
            Broker instance
        """
        broker_name = broker_name.lower()
        
        if broker_name == 'binance':
            from modules.brokers.binance_broker import BinanceBroker
            return BinanceBroker(api_key, api_secret, sandbox)
        
        elif broker_name == 'bitpanda':
            from modules.brokers.bitpanda_broker import BitpandaBroker
            return BitpandaBroker(api_key, api_secret, sandbox)
        
        elif broker_name == 'mock':
            from modules.brokers.mock_broker import MockBroker
            return MockBroker(api_key, api_secret, sandbox)
        
        else:
            raise ValueError(f"Unsupported broker: {broker_name}")


class BaseBroker:
    """
    Base class for all broker implementations
    """
    
    def __init__(self, api_key: str, api_secret: str, sandbox: bool = True):
        """
        Initialize broker
        
        Args:
            api_key: API key
            api_secret: API secret
            sandbox: Use sandbox/testnet mode
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.sandbox = sandbox
        self.logger = Logger(self.__class__.__name__)
        self.connected = False
    
    def is_connected(self) -> bool:
        """Check if broker is connected"""
        return self.connected
    
    def reconnect(self):
        """Reconnect to broker"""
        raise NotImplementedError("Subclass must implement reconnect()")
    
    def get_positions(self) -> list:
        """Get all open positions"""
        raise NotImplementedError("Subclass must implement get_positions()")
    
    def get_open_orders(self) -> list:
        """Get all open orders"""
        raise NotImplementedError("Subclass must implement get_open_orders()")
    
    def get_order_status(self, order_id: str) -> str:
        """Get order status"""
        raise NotImplementedError("Subclass must implement get_order_status()")
    
    def get_market_data(self, symbol: str, timeframe: str) -> dict:
        """Get market data (OHLCV)"""
        raise NotImplementedError("Subclass must implement get_market_data()")
    
    def get_current_price(self, symbol: str) -> float:
        """Get current market price"""
        raise NotImplementedError("Subclass must implement get_current_price()")
    
    def place_order(self, symbol: str, side: str, amount: float, 
                   order_type: str = 'market', price: Optional[float] = None) -> dict:
        """Place an order"""
        raise NotImplementedError("Subclass must implement place_order()")
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        raise NotImplementedError("Subclass must implement cancel_order()")
