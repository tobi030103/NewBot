"""
Credential Manager for secure API key and password storage

Uses encryption to protect sensitive data like API keys, passwords, etc.
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2


class CredentialManager:
    """
    Manages encrypted storage of credentials
    
    Credentials are encrypted using Fernet (symmetric encryption)
    and stored in a local file.
    """
    
    def __init__(self, credentials_file: str = 'credentials.json.enc'):
        """
        Initialize credential manager
        
        Args:
            credentials_file: Path to encrypted credentials file
        """
        self.credentials_file = credentials_file
        self.credentials: Dict[str, str] = {}
        self._cipher = self._init_cipher()
        self._load_credentials()
    
    def _init_cipher(self) -> Fernet:
        """
        Initialize encryption cipher
        
        Returns:
            Fernet cipher instance
        """
        # Get or generate encryption key
        key_file = '.encryption.key'
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            # Set restrictive permissions
            os.chmod(key_file, 0o600)
        
        return Fernet(key)
    
    def _load_credentials(self):
        """Load encrypted credentials from file"""
        if not os.path.exists(self.credentials_file):
            return
        
        try:
            with open(self.credentials_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt
            decrypted_data = self._cipher.decrypt(encrypted_data)
            self.credentials = json.loads(decrypted_data.decode())
            
        except Exception as e:
            print(f"Warning: Failed to load credentials: {e}")
            self.credentials = {}
    
    def _save_credentials(self):
        """Save credentials to encrypted file"""
        try:
            # Serialize and encrypt
            data = json.dumps(self.credentials).encode()
            encrypted_data = self._cipher.encrypt(data)
            
            # Write to file
            with open(self.credentials_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Set restrictive permissions
            os.chmod(self.credentials_file, 0o600)
            
        except Exception as e:
            print(f"Error: Failed to save credentials: {e}")
    
    def set_credential(self, key: str, value: str):
        """
        Store a credential
        
        Args:
            key: Credential identifier
            value: Credential value (will be encrypted)
        """
        self.credentials[key] = value
        self._save_credentials()
    
    def get_credential(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Retrieve a credential
        
        Args:
            key: Credential identifier
            default: Default value if credential not found
            
        Returns:
            Credential value or default
        """
        return self.credentials.get(key, default)
    
    def delete_credential(self, key: str):
        """
        Delete a credential
        
        Args:
            key: Credential identifier
        """
        if key in self.credentials:
            del self.credentials[key]
            self._save_credentials()
    
    def list_credentials(self) -> list:
        """
        List all stored credential keys (not values)
        
        Returns:
            List of credential keys
        """
        return list(self.credentials.keys())
