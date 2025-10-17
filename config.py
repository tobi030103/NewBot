"""
Configuration management for NewBot Trading Bot

This module handles all configuration settings including:
- Trading parameters
- Risk management settings
- Broker connections
- Notification settings
- Security settings
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Main configuration class for the trading bot"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration
        
        Args:
            config_file: Path to YAML configuration file (optional)
        """
        self.config_file = config_file or os.getenv('CONFIG_FILE', 'config.yaml')
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file or use defaults"""
        config_path = Path(self.config_file)
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f) or {}
        else:
            # Use default configuration
            self.config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'trading': {
                'mode': 'paper',  # 'paper' or 'live'
                'base_currency': 'EUR',
                'quote_currency': 'BTC',
                'trade_amount': 100.0,
                'max_positions': 5,
            },
            'risk_management': {
                'stop_loss_percent': 2.0,
                'take_profit_percent': 5.0,
                'use_trailing_stop': True,
                'trailing_stop_percent': 1.5,
                'use_guaranteed_stop_loss': False,
                'max_risk_per_trade': 2.0,
                'max_daily_loss': 5.0,
            },
            'broker': {
                'name': 'binance',  # 'binance', 'bitpanda', etc.
                'sandbox': True,
                'api_key': os.getenv('BROKER_API_KEY', ''),
                'api_secret': os.getenv('BROKER_API_SECRET', ''),
            },
            'strategy': {
                'name': 'moving_average_crossover',
                'parameters': {
                    'fast_period': 10,
                    'slow_period': 30,
                    'signal_threshold': 0.001,
                }
            },
            'notifications': {
                'enabled': True,
                'email': {
                    'enabled': False,
                    'smtp_server': '',
                    'smtp_port': 587,
                    'from_address': '',
                    'to_address': '',
                    'password': os.getenv('EMAIL_PASSWORD', ''),
                },
                'webhook': {
                    'enabled': False,
                    'url': '',
                }
            },
            'logging': {
                'level': 'INFO',
                'log_to_file': True,
                'log_file': 'logs/newbot.log',
                'max_file_size_mb': 10,
                'backup_count': 5,
            },
            'backup': {
                'enabled': True,
                'interval_hours': 6,
                'backup_dir': 'backups',
                'max_backups': 10,
            },
            'monitoring': {
                'check_interval_seconds': 60,
                'network_timeout_seconds': 30,
                'max_api_retries': 3,
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key path
        
        Args:
            key: Dot-separated key path (e.g., 'trading.mode')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set configuration value by key path
        
        Args:
            key: Dot-separated key path (e.g., 'trading.mode')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, config_file: Optional[str] = None):
        """
        Save configuration to file
        
        Args:
            config_file: Path to save configuration (optional)
        """
        save_path = config_file or self.config_file
        
        # Create directory if it doesn't exist
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(save_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def validate(self) -> bool:
        """
        Validate configuration
        
        Returns:
            True if configuration is valid, False otherwise
        """
        required_keys = [
            'trading.mode',
            'broker.name',
            'risk_management.stop_loss_percent',
            'risk_management.take_profit_percent',
        ]
        
        for key in required_keys:
            if self.get(key) is None:
                print(f"Missing required configuration: {key}")
                return False
        
        return True


# Global configuration instance
config = Config()
