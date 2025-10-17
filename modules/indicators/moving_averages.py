"""
Moving Average Indicators

Various moving average calculations
"""

import pandas as pd


def calculate_sma(prices: pd.Series, period: int) -> pd.Series:
    """
    Calculate Simple Moving Average (SMA)
    
    Args:
        prices: Series of prices
        period: Moving average period
        
    Returns:
        Series of SMA values
    """
    return prices.rolling(window=period).mean()


def calculate_ema(prices: pd.Series, period: int) -> pd.Series:
    """
    Calculate Exponential Moving Average (EMA)
    
    Args:
        prices: Series of prices
        period: Moving average period
        
    Returns:
        Series of EMA values
    """
    return prices.ewm(span=period, adjust=False).mean()


def calculate_wma(prices: pd.Series, period: int) -> pd.Series:
    """
    Calculate Weighted Moving Average (WMA)
    
    Args:
        prices: Series of prices
        period: Moving average period
        
    Returns:
        Series of WMA values
    """
    weights = pd.Series(range(1, period + 1))
    
    def weighted_mean(x):
        return (x * weights).sum() / weights.sum()
    
    return prices.rolling(window=period).apply(weighted_mean, raw=True)


def calculate_macd(prices: pd.Series, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> tuple:
    """
    Calculate MACD (Moving Average Convergence Divergence)
    
    Args:
        prices: Series of closing prices
        fast_period: Fast EMA period
        slow_period: Slow EMA period
        signal_period: Signal line period
        
    Returns:
        Tuple of (MACD line, Signal line, Histogram)
    """
    # Calculate EMAs
    fast_ema = calculate_ema(prices, fast_period)
    slow_ema = calculate_ema(prices, slow_period)
    
    # MACD line
    macd_line = fast_ema - slow_ema
    
    # Signal line
    signal_line = calculate_ema(macd_line, signal_period)
    
    # Histogram
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram
