"""
BuddyAI NEXTGEN - Machine Learning Module

Advanced machine learning models for market prediction, strategy optimization,
and intelligent decision making.
"""

from .model_manager import ModelManager
from .feature_engineering import FeatureEngineer
from .model_trainer import ModelTrainer
from .reinforcement_learning import RLAgent

__all__ = [
    'ModelManager',
    'FeatureEngineer', 
    'ModelTrainer',
    'RLAgent'
]
