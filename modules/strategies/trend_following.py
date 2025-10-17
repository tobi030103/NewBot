"""
Trend Following Strategy

Identifies and follows market trends using multiple indicators
"""

import pandas as pd
from modules.strategies.strategy_factory import BaseStrategy


class TrendFollowing(BaseStrategy):
    """
    Trend following strategy using EMA and price action
    """
    
    def __init__(self, parameters: dict):
        """
        Initialize strategy
        
        Args:
            parameters: Strategy parameters
        """
        super().__init__(parameters)
        self.ema_period = parameters.get('ema_period', 50)
        self.trend_threshold = parameters.get('trend_threshold', 0.02)
        
        self.logger.info(f"Trend Following initialized (ema_period={self.ema_period})")
    
    def generate_signal(self, market_data: dict) -> str:
        """
        Generate trading signal based on trend
        
        Args:
            market_data: Market data with OHLCV
            
        Returns:
            Signal: 'BUY', 'SELL', or 'HOLD'
        """
        try:
            ohlcv_data = market_data.get('data', [])
            
            if len(ohlcv_data) < self.ema_period:
                return 'HOLD'
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # Calculate EMA
            df['ema'] = df['close'].ewm(span=self.ema_period, adjust=False).mean()
            
            # Get current values
            current_price = df['close'].iloc[-1]
            current_ema = df['ema'].iloc[-1]
            
            if pd.isna(current_ema):
                return 'HOLD'
            
            # Calculate price position relative to EMA
            price_diff = (current_price - current_ema) / current_ema
            
            # Strong uptrend - Buy
            if price_diff > self.trend_threshold:
                self.logger.info(f"Uptrend detected ({price_diff:.2%}) - BUY signal")
                return 'BUY'
            
            # Strong downtrend - Sell
            elif price_diff < -self.trend_threshold:
                self.logger.info(f"Downtrend detected ({price_diff:.2%}) - SELL signal")
                return 'SELL'
            
            return 'HOLD'
            
        except Exception as e:
            self.logger.error(f"Signal generation failed: {e}")
            return 'HOLD'
