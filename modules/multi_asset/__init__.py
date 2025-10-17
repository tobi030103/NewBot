"""
BuddyAI NEXTGEN - Multi-Asset Module

Handle trading across all asset classes: Forex, Crypto, Stocks, Indices,
Commodities, ETFs, Options, Futures, and more.
"""

from .asset_manager import AssetManager
from .asset_selector import AssetSelector
from .market_scanner import MarketScanner
from .cross_asset_analyzer import CrossAssetAnalyzer

__all__ = [
    'AssetManager',
    'AssetSelector',
    'MarketScanner',
    'CrossAssetAnalyzer'
]
