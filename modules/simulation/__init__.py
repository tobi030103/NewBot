"""
BuddyAI NEXTGEN - Simulation & Backtesting Module

Comprehensive backtesting, walk-forward analysis, and shadow trading capabilities.
"""

from .backtest_engine import BacktestEngine
from .walk_forward import WalkForwardOptimizer
from .shadow_trader import ShadowTrader
from .monte_carlo import MonteCarloSimulator

__all__ = [
    'BacktestEngine',
    'WalkForwardOptimizer',
    'ShadowTrader',
    'MonteCarloSimulator'
]
