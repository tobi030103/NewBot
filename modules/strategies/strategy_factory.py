"""
Strategy Factory for NewBot

Creates trading strategy instances based on configuration
"""

from utils.logging.logger import Logger


class StrategyFactory:
    """
    Factory class for creating strategy instances
    """
    
    @staticmethod
    def create_strategy(strategy_name: str, parameters: dict):
        """
        Create a strategy instance
        
        Args:
            strategy_name: Name of the strategy
            parameters: Strategy parameters
            
        Returns:
            Strategy instance
        """
        strategy_name = strategy_name.lower()
        
        if strategy_name == 'moving_average_crossover':
            from modules.strategies.moving_average_crossover import MovingAverageCrossover
            return MovingAverageCrossover(parameters)
        
        elif strategy_name == 'rsi_strategy':
            from modules.strategies.rsi_strategy import RSIStrategy
            return RSIStrategy(parameters)
        
        elif strategy_name == 'trend_following':
            from modules.strategies.trend_following import TrendFollowing
            return TrendFollowing(parameters)
        
        else:
            raise ValueError(f"Unsupported strategy: {strategy_name}")


class BaseStrategy:
    """
    Base class for all trading strategies
    """
    
    def __init__(self, parameters: dict):
        """
        Initialize strategy
        
        Args:
            parameters: Strategy-specific parameters
        """
        self.parameters = parameters
        self.logger = Logger(self.__class__.__name__)
    
    def generate_signal(self, market_data: dict) -> str:
        """
        Generate trading signal based on market data
        
        Args:
            market_data: Market data (OHLCV)
            
        Returns:
            Signal: 'BUY', 'SELL', or 'HOLD'
        """
        raise NotImplementedError("Subclass must implement generate_signal()")
    
    def validate_parameters(self) -> bool:
        """
        Validate strategy parameters
        
        Returns:
            True if parameters are valid, False otherwise
        """
        return True
