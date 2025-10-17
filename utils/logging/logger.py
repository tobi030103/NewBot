"""
Logging utility for NewBot

Provides comprehensive logging functionality with file rotation,
multiple log levels, and proper formatting.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

from config import config


class Logger:
    """Enhanced logger with file rotation and formatting"""
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        """
        Initialize logger
        
        Args:
            name: Logger name (usually module/class name)
            log_file: Optional custom log file path
        """
        self.logger = logging.getLogger(name)
        
        # Get log level from config
        log_level = config.get('logging.level', 'INFO')
        self.logger.setLevel(getattr(logging, log_level))
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers(log_file)
    
    def _setup_handlers(self, log_file: Optional[str] = None):
        """Setup logging handlers"""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (if enabled)
        if config.get('logging.log_to_file', True):
            log_file_path = log_file or config.get('logging.log_file', 'logs/newbot.log')
            
            # Create log directory
            Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Rotating file handler
            max_bytes = config.get('logging.max_file_size_mb', 10) * 1024 * 1024
            backup_count = config.get('logging.backup_count', 5)
            
            file_handler = RotatingFileHandler(
                log_file_path,
                maxBytes=max_bytes,
                backupCount=backup_count
            )
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
