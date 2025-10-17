"""
RSI (Relative Strength Index) Strategy

Trading strategy based on RSI indicator:
- Oversold condition (RSI < 30): Buy signal
- Overbought condition (RSI > 70): Sell signal
"""

import pandas as pd
from modules.strategies.strategy_factory import BaseStrategy
from modules.indicators.rsi import calculate_rsi


class RSIStrategy(BaseStrategy):
    """
    RSI-based trading strategy
    """
    
    def __init__(self, parameters: dict):
        """
        Initialize strategy
        
        Args:
            parameters: Must contain 'period', 'oversold', 'overbought'
        """
        super().__init__(parameters)
        self.period = parameters.get('period', 14)
        self.oversold = parameters.get('oversold', 30)
        self.overbought = parameters.get('overbought', 70)
        
        self.logger.info(f"RSI Strategy initialized (period={self.period}, oversold={self.oversold}, overbought={self.overbought})")
    
    def generate_signal(self, market_data: dict) -> str:
        """
        Generate trading signal based on RSI
        
        Args:
            market_data: Market data with OHLCV
            
        Returns:
            Signal: 'BUY', 'SELL', or 'HOLD'
        """
        try:
            ohlcv_data = market_data.get('data', [])
            
            if len(ohlcv_data) < self.period + 1:
                self.logger.warning("Insufficient data for RSI calculation")
                return 'HOLD'
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # Calculate RSI
            df['rsi'] = calculate_rsi(df['close'], self.period)
            
            # Get current RSI
            current_rsi = df['rsi'].iloc[-1]
            
            if pd.isna(current_rsi):
                return 'HOLD'
            
            # Generate signals
            if current_rsi < self.oversold:
                self.logger.info(f"RSI oversold ({current_rsi:.2f}) - BUY signal")
                return 'BUY'
            
            elif current_rsi > self.overbought:
                self.logger.info(f"RSI overbought ({current_rsi:.2f}) - SELL signal")
                return 'SELL'
            
            return 'HOLD'
            
        except Exception as e:
            self.logger.error(f"Signal generation failed: {e}")
            return 'HOLD'
