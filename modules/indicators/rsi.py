"""
RSI (Relative Strength Index) Indicator

Calculates RSI values for price data
"""

import pandas as pd


def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate RSI (Relative Strength Index)
    
    Args:
        prices: Series of closing prices
        period: RSI period (default: 14)
        
    Returns:
        Series of RSI values
    """
    # Calculate price changes
    delta = prices.diff()
    
    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    # Calculate average gains and losses
    avg_gains = gains.rolling(window=period, min_periods=period).mean()
    avg_losses = losses.rolling(window=period, min_periods=period).mean()
    
    # Calculate RS (Relative Strength)
    rs = avg_gains / avg_losses
    
    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_stochastic_rsi(prices: pd.Series, period: int = 14, smooth_k: int = 3, smooth_d: int = 3) -> tuple:
    """
    Calculate Stochastic RSI
    
    Args:
        prices: Series of closing prices
        period: RSI period
        smooth_k: %K smoothing period
        smooth_d: %D smoothing period
        
    Returns:
        Tuple of (%K, %D) Series
    """
    # Calculate RSI
    rsi = calculate_rsi(prices, period)
    
    # Calculate Stochastic RSI
    rsi_min = rsi.rolling(window=period).min()
    rsi_max = rsi.rolling(window=period).max()
    
    stoch_rsi = (rsi - rsi_min) / (rsi_max - rsi_min)
    
    # Smooth %K
    k = stoch_rsi.rolling(window=smooth_k).mean() * 100
    
    # Calculate %D
    d = k.rolling(window=smooth_d).mean()
    
    return k, d
