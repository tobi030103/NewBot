"""
BuddyAI NEXTGEN - Interface Module

This module provides all user interfaces for controlling and monitoring BuddyAI.
It includes web dashboard, GUI application, Telegram bot, and CLI interfaces.

The goal is to make EVERYTHING controllable through interfaces without touching code.
"""

from .web_dashboard import WebDashboard
from .gui_application import GUIApplication
from .telegram_bot import TelegramBot
from .cli_interface import CLIInterface
from .api_server import APIServer

__all__ = [
    'WebDashboard',
    'GUIApplication',
    'TelegramBot',
    'CLIInterface',
    'APIServer'
]
