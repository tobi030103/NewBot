"""
Moving Average Crossover Strategy

A classic trend-following strategy based on two moving averages:
- Fast MA (short period)
- Slow MA (long period)

Buy when fast MA crosses above slow MA
Sell when fast MA crosses below slow MA
"""

import pandas as pd
from modules.strategies.strategy_factory import BaseStrategy


class MovingAverageCrossover(BaseStrategy):
    """
    Moving Average Crossover trading strategy
    """
    
    def __init__(self, parameters: dict):
        """
        Initialize strategy
        
        Args:
            parameters: Must contain 'fast_period' and 'slow_period'
        """
        super().__init__(parameters)
        self.fast_period = parameters.get('fast_period', 10)
        self.slow_period = parameters.get('slow_period', 30)
        self.signal_threshold = parameters.get('signal_threshold', 0.001)
        
        self.last_signal = 'HOLD'
        
        self.logger.info(f"MA Crossover initialized (fast={self.fast_period}, slow={self.slow_period})")
    
    def generate_signal(self, market_data: dict) -> str:
        """
        Generate trading signal based on MA crossover
        
        Args:
            market_data: Market data with OHLCV
            
        Returns:
            Signal: 'BUY', 'SELL', or 'HOLD'
        """
        try:
            ohlcv_data = market_data.get('data', [])
            
            if len(ohlcv_data) < self.slow_period:
                self.logger.warning("Insufficient data for MA calculation")
                return 'HOLD'
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # Calculate moving averages
            df['fast_ma'] = df['close'].rolling(window=self.fast_period).mean()
            df['slow_ma'] = df['close'].rolling(window=self.slow_period).mean()
            
            # Get last two rows for crossover detection
            current = df.iloc[-1]
            previous = df.iloc[-2]
            
            # Check for crossover
            if pd.isna(current['fast_ma']) or pd.isna(current['slow_ma']):
                return 'HOLD'
            
            # Bullish crossover (buy signal)
            if (previous['fast_ma'] <= previous['slow_ma'] and 
                current['fast_ma'] > current['slow_ma']):
                
                # Check if crossover is significant
                diff = (current['fast_ma'] - current['slow_ma']) / current['slow_ma']
                if diff >= self.signal_threshold:
                    self.logger.info("Bullish crossover detected - BUY signal")
                    self.last_signal = 'BUY'
                    return 'BUY'
            
            # Bearish crossover (sell signal)
            elif (previous['fast_ma'] >= previous['slow_ma'] and 
                  current['fast_ma'] < current['slow_ma']):
                
                # Check if crossover is significant
                diff = abs(current['fast_ma'] - current['slow_ma']) / current['slow_ma']
                if diff >= self.signal_threshold:
                    self.logger.info("Bearish crossover detected - SELL signal")
                    self.last_signal = 'SELL'
                    return 'SELL'
            
            return 'HOLD'
            
        except Exception as e:
            self.logger.error(f"Signal generation failed: {e}")
            return 'HOLD'
