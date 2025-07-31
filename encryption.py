#!/usr/bin/env python3
"""
Encryption Module for Bluetooth Chat
Provides secure message encryption and decryption using Fernet symmetric encryption.
"""

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from colorama import Fore, Style

class ChatEncryption:
    def __init__(self, password=None):
        """Initialize encryption with a password"""
        self.fernet = None
        if password:
            self.setup_encryption(password)
    
    def setup_encryption(self, password):
        """Setup encryption using a password"""
        try:
            # Generate a salt for key derivation
            salt = b'bluetooth_chat_salt_2024'  # Fixed salt for simplicity
            
            # Derive a key from the password
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            self.fernet = Fernet(key)
            return True
        except Exception as e:
            print(f"{Fore.RED}Error setting up encryption: {e}{Style.RESET_ALL}")
            return False
    
    def encrypt_message(self, message):
        """Encrypt a message"""
        if not self.fernet:
            return message  # Return plaintext if no encryption setup
        
        try:
            encrypted = self.fernet.encrypt(message.encode('utf-8'))
            # Encode to base64 for safe transmission
            return base64.b64encode(encrypted).decode('ascii')
        except Exception as e:
            print(f"{Fore.RED}Encryption error: {e}{Style.RESET_ALL}")
            return message
    
    def decrypt_message(self, encrypted_message):
        """Decrypt a message"""
        if not self.fernet:
            return encrypted_message  # Return as-is if no encryption setup
        
        try:
            # Decode from base64 first
            encrypted_bytes = base64.b64decode(encrypted_message.encode('ascii'))
            decrypted = self.fernet.decrypt(encrypted_bytes)
            return decrypted.decode('utf-8')
        except Exception as e:
            print(f"{Fore.RED}Decryption error: {e}{Style.RESET_ALL}")
            return encrypted_message
    
    def is_encrypted(self):
        """Check if encryption is enabled"""
        return self.fernet is not None

def get_chat_password():
    """Get password from user for encryption"""
    print(f"{Fore.CYAN}═══════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.CYAN}       Secure Chat Setup               {Style.RESET_ALL}")
    print(f"{Fore.CYAN}═══════════════════════════════════════{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Choose your security option:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  1. Enable encryption (recommended){Style.RESET_ALL}")
    print(f"{Fore.RED}  2. No encryption (messages in plaintext){Style.RESET_ALL}")
    print()
    
    while True:
        try:
            choice = input(f"{Fore.CYAN}Enter your choice (1 or 2): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                print()
                print(f"{Fore.YELLOW}Important: Both devices must use the same password!{Style.RESET_ALL}")
                password = input(f"{Fore.CYAN}Enter encryption password: {Style.RESET_ALL}")
                if password.strip():
                    return password
                else:
                    print(f"{Fore.RED}Password cannot be empty!{Style.RESET_ALL}")
                    
            elif choice == '2':
                print(f"{Fore.YELLOW}⚠️  Warning: Messages will be sent without encryption!{Style.RESET_ALL}")
                confirm = input(f"{Fore.CYAN}Are you sure? (y/n): {Style.RESET_ALL}").lower()
                if confirm == 'y':
                    return None
                    
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Setup cancelled by user.{Style.RESET_ALL}")
            return None

def test_encryption():
    """Test the encryption functionality"""
    print(f"{Fore.CYAN}Testing encryption functionality...{Style.RESET_ALL}")
    
    # Test with password
    crypto = ChatEncryption("test_password_123")
    
    test_message = "Hello, this is a secret message!"
    print(f"{Fore.YELLOW}Original: {test_message}{Style.RESET_ALL}")
    
    encrypted = crypto.encrypt_message(test_message)
    print(f"{Fore.MAGENTA}Encrypted: {encrypted}{Style.RESET_ALL}")
    
    decrypted = crypto.decrypt_message(encrypted)
    print(f"{Fore.GREEN}Decrypted: {decrypted}{Style.RESET_ALL}")
    
    if decrypted == test_message:
        print(f"{Fore.GREEN}✓ Encryption test passed!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Encryption test failed!{Style.RESET_ALL}")

if __name__ == "__main__":
    test_encryption()
