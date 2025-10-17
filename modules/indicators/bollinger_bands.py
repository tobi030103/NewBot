"""
Bollinger Bands Indicator

Calculates Bollinger Bands for volatility analysis
"""

import pandas as pd


def calculate_bollinger_bands(prices: pd.Series, period: int = 20, num_std: float = 2.0) -> tuple:
    """
    Calculate Bollinger Bands
    
    Args:
        prices: Series of closing prices
        period: Moving average period
        num_std: Number of standard deviations
        
    Returns:
        Tuple of (Upper Band, Middle Band, Lower Band)
    """
    # Calculate middle band (SMA)
    middle_band = prices.rolling(window=period).mean()
    
    # Calculate standard deviation
    std_dev = prices.rolling(window=period).std()
    
    # Calculate upper and lower bands
    upper_band = middle_band + (std_dev * num_std)
    lower_band = middle_band - (std_dev * num_std)
    
    return upper_band, middle_band, lower_band


def calculate_bandwidth(prices: pd.Series, period: int = 20, num_std: float = 2.0) -> pd.Series:
    """
    Calculate Bollinger Band Width
    
    Args:
        prices: Series of closing prices
        period: Moving average period
        num_std: Number of standard deviations
        
    Returns:
        Series of bandwidth values
    """
    upper, middle, lower = calculate_bollinger_bands(prices, period, num_std)
    bandwidth = (upper - lower) / middle
    return bandwidth


def calculate_percent_b(prices: pd.Series, period: int = 20, num_std: float = 2.0) -> pd.Series:
    """
    Calculate %B (Percent B) indicator
    
    Shows where price is relative to the bands
    
    Args:
        prices: Series of closing prices
        period: Moving average period
        num_std: Number of standard deviations
        
    Returns:
        Series of %B values
    """
    upper, middle, lower = calculate_bollinger_bands(prices, period, num_std)
    percent_b = (prices - lower) / (upper - lower)
    return percent_b
