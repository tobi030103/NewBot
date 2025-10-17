"""
Backup Manager for NewBot

Handles automatic backups of configuration, positions, and orders
to enable recovery after system failures.
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from config import config
from utils.logging.logger import Logger


class BackupManager:
    """
    Manages automated backups of bot state and configuration
    """
    
    def __init__(self):
        """Initialize backup manager"""
        self.logger = Logger('BackupManager')
        self.backup_dir = config.get('backup.backup_dir', 'backups')
        self.max_backups = config.get('backup.max_backups', 10)
        self.last_backup_time = None
        
        # Create backup directory
        Path(self.backup_dir).mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, data: Dict[str, Any] = None) -> str:
        """
        Create a backup
        
        Args:
            data: Optional additional data to backup
            
        Returns:
            Path to backup file
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = Path(self.backup_dir) / f'backup_{timestamp}.json'
            
            # Collect data to backup
            backup_data = {
                'timestamp': timestamp,
                'config': config.config,
                'additional_data': data or {}
            }
            
            # Write backup
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            self.logger.info(f"Backup created: {backup_file}")
            self.last_backup_time = datetime.now()
            
            # Clean old backups
            self._cleanup_old_backups()
            
            return str(backup_file)
            
        except Exception as e:
            self.logger.error(f"Backup failed: {e}")
            raise
    
    def restore_backup(self, backup_file: str) -> Dict[str, Any]:
        """
        Restore from a backup
        
        Args:
            backup_file: Path to backup file
            
        Returns:
            Restored data
        """
        try:
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)
            
            self.logger.info(f"Backup restored from: {backup_file}")
            return backup_data
            
        except Exception as e:
            self.logger.error(f"Backup restoration failed: {e}")
            raise
    
    def list_backups(self) -> list:
        """
        List all available backups
        
        Returns:
            List of backup file paths
        """
        backup_path = Path(self.backup_dir)
        backups = sorted(backup_path.glob('backup_*.json'), reverse=True)
        return [str(b) for b in backups]
    
    def get_latest_backup(self) -> str:
        """
        Get the most recent backup
        
        Returns:
            Path to latest backup file or None
        """
        backups = self.list_backups()
        return backups[0] if backups else None
    
    def auto_backup(self):
        """
        Perform automatic backup based on configured interval
        """
        if not config.get('backup.enabled', True):
            return
        
        interval_hours = config.get('backup.interval_hours', 6)
        
        if self.last_backup_time is None:
            self.create_backup()
            return
        
        elapsed = (datetime.now() - self.last_backup_time).total_seconds() / 3600
        
        if elapsed >= interval_hours:
            self.create_backup()
    
    def _cleanup_old_backups(self):
        """Remove old backups exceeding max_backups limit"""
        backups = self.list_backups()
        
        if len(backups) > self.max_backups:
            # Remove oldest backups
            for backup_file in backups[self.max_backups:]:
                try:
                    os.remove(backup_file)
                    self.logger.info(f"Removed old backup: {backup_file}")
                except Exception as e:
                    self.logger.warning(f"Failed to remove old backup {backup_file}: {e}")
