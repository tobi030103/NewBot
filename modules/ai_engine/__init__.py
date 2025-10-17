"""
BuddyAI NEXTGEN - AI Engine Module

This module contains the core artificial intelligence engine that powers BuddyAI.
It is responsible for autonomous decision-making, self-learning, strategy generation,
and continuous optimization.

The AI Engine is the brain of BuddyAI NEXTGEN - it learns from market data,
generates and tests trading strategies, and continuously improves its performance
without human intervention.

Components:
-----------
- StrategyGenerator: Creates and tests new trading strategies autonomously
- MetaLearner: Learns from past strategies and generates new ones
- DecisionEngine: Makes real-time trading decisions based on multiple factors
- PerformanceOptimizer: Continuously optimizes strategy parameters
- SelfHealing: Detects and fixes issues automatically
"""

from .strategy_generator import StrategyGenerator
from .meta_learner import MetaLearner
from .decision_engine import DecisionEngine
from .performance_optimizer import PerformanceOptimizer
from .self_healing import SelfHealingEngine

__all__ = [
    'StrategyGenerator',
    'MetaLearner',
    'DecisionEngine',
    'PerformanceOptimizer',
    'SelfHealingEngine'
]
