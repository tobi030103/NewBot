"""
Notification system for NewBot

Sends alerts via multiple channels (email, webhooks, etc.)
"""

import requests
from typing import Optional
from datetime import datetime

from config import config
from utils.logging.logger import Logger


class Notifier:
    """
    Multi-channel notification system
    """
    
    def __init__(self):
        """Initialize notifier"""
        self.logger = Logger('Notifier')
        self.enabled = config.get('notifications.enabled', True)
    
    def send_notification(self, title: str, message: str, priority: str = 'low'):
        """
        Send notification through configured channels
        
        Args:
            title: Notification title
            message: Notification message
            priority: Priority level ('low', 'medium', 'high')
        """
        if not self.enabled:
            return
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        full_message = f"[{timestamp}] [{priority.upper()}]\n{title}\n\n{message}"
        
        # Log notification
        self.logger.info(f"Notification: {title} - {message}")
        
        # Send via email
        if config.get('notifications.email.enabled', False):
            self._send_email(title, full_message)
        
        # Send via webhook
        if config.get('notifications.webhook.enabled', False):
            self._send_webhook(title, full_message, priority)
    
    def _send_email(self, subject: str, message: str):
        """
        Send email notification
        
        Args:
            subject: Email subject
            message: Email message
        """
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            smtp_server = config.get('notifications.email.smtp_server')
            smtp_port = config.get('notifications.email.smtp_port', 587)
            from_address = config.get('notifications.email.from_address')
            to_address = config.get('notifications.email.to_address')
            password = config.get('notifications.email.password')
            
            msg = MIMEMultipart()
            msg['From'] = from_address
            msg['To'] = to_address
            msg['Subject'] = f"NewBot: {subject}"
            
            msg.attach(MIMEText(message, 'plain'))
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(from_address, password)
                server.send_message(msg)
            
            self.logger.info(f"Email sent to {to_address}")
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
    
    def _send_webhook(self, title: str, message: str, priority: str):
        """
        Send webhook notification
        
        Args:
            title: Notification title
            message: Notification message
            priority: Priority level
        """
        try:
            webhook_url = config.get('notifications.webhook.url')
            
            payload = {
                'title': title,
                'message': message,
                'priority': priority,
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            self.logger.info("Webhook notification sent")
            
        except Exception as e:
            self.logger.error(f"Failed to send webhook: {e}")
