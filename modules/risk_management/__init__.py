"""
BuddyAI NEXTGEN - Risk Management Module

Comprehensive risk management system for protecting capital and managing exposure.
Dynamic position sizing, stop losses, correlation analysis, and portfolio risk control.
"""

from .position_sizer import PositionSizer
from .risk_calculator import RiskCalculator
from .drawdown_manager import DrawdownManager
from .correlation_analyzer import CorrelationAnalyzer
from .volatility_manager import VolatilityManager

__all__ = [
    'PositionSizer',
    'RiskCalculator',
    'DrawdownManager',
    'CorrelationAnalyzer',
    'VolatilityManager'
]
