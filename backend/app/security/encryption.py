"""
Encryption and Decryption Module
AES-256 encryption with BB84 keys
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os
import logging
from typing import Tuple
import json
from base64 import b64encode, b64decode

logger = logging.getLogger(__name__)


class EncryptionManager:
    """Manages AES-256 encryption/decryption"""
    
    BACKEND = default_backend()
    ALGORITHM = algorithms.AES
    KEY_SIZE = 32  # 256 bits
    IV_SIZE = 16   # 128 bits
    
    @staticmethod
    def generate_key() -> bytes:
        """Generate a random 256-bit AES key"""
        return os.urandom(EncryptionManager.KEY_SIZE)
    
    @staticmethod
    def generate_iv() -> bytes:
        """Generate a random 128-bit IV"""
        return os.urandom(EncryptionManager.IV_SIZE)
    
    @staticmethod
    def derive_key_from_bb84(bb84_key: str, desired_length: int = 32) -> bytes:
        """
        Derive AES key from BB84 quantum key
        
        Args:
            bb84_key: BB84 output key (hex string or binary)
            desired_length: Desired key length in bytes
            
        Returns:
            Derived key bytes
        """
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        
        # Convert BB84 key to bytes if needed
        if isinstance(bb84_key, str):
            key_bytes = bb84_key.encode() if len(bb84_key) != 64 else bytes.fromhex(bb84_key)
        else:
            key_bytes = bb84_key
        
        # Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=desired_length,
            salt=b"quantum_chat_salt",
            iterations=100000,
            backend=EncryptionManager.BACKEND
        )

        derived = kdf.derive(key_bytes)
        logger.info(f"Derived {len(derived)} byte key from BB84 key")
        return derived
    
    @staticmethod
    def encrypt_aes256(
        plaintext: str,
        key: bytes,
        iv: bytes = None
    ) -> Tuple[bytes, bytes, bytes]:
        """
        Encrypt plaintext using AES-256-CBC
        
        Args:
            plaintext: Text to encrypt
            key: 32-byte AES key
            iv: 16-byte IV (generated if not provided)
            
        Returns:
            Tuple of (ciphertext, iv, tag) for authentication
        """
        if len(key) != EncryptionManager.KEY_SIZE:
            raise ValueError(f"Key must be {EncryptionManager.KEY_SIZE} bytes")
        
        if iv is None:
            iv = EncryptionManager.generate_iv()
        elif len(iv) != EncryptionManager.IV_SIZE:
            raise ValueError(f"IV must be {EncryptionManager.IV_SIZE} bytes")
        
        # Use CBC mode with PKCS7 padding
        cipher = Cipher(
            EncryptionManager.ALGORITHM(key),
            modes.CBC(iv),
            backend=EncryptionManager.BACKEND
        )
        encryptor = cipher.encryptor()
        
        # Add PKCS7 padding
        plaintext_bytes = plaintext.encode()
        padding_length = 16 - (len(plaintext_bytes) % 16)
        padded = plaintext_bytes + bytes([padding_length] * padding_length)
        
        # Encrypt
        ciphertext = encryptor.update(padded) + encryptor.finalize()
        
        logger.info(f"Encrypted {len(plaintext)} chars -> {len(ciphertext)} bytes")
        return ciphertext, iv, ciphertext[:16]  # tag is first 16 bytes
    
    @staticmethod
    def decrypt_aes256(
        ciphertext: bytes,
        key: bytes,
        iv: bytes
    ) -> str:
        """
        Decrypt ciphertext using AES-256-CBC
        
        Args:
            ciphertext: Encrypted data
            key: 32-byte AES key
            iv: 16-byte IV used during encryption
            
        Returns:
            Decrypted plaintext
        """
        if len(key) != EncryptionManager.KEY_SIZE:
            raise ValueError(f"Key must be {EncryptionManager.KEY_SIZE} bytes")
        if len(iv) != EncryptionManager.IV_SIZE:
            raise ValueError(f"IV must be {EncryptionManager.IV_SIZE} bytes")
        
        cipher = Cipher(
            EncryptionManager.ALGORITHM(key),
            modes.CBC(iv),
            backend=EncryptionManager.BACKEND
        )
        decryptor = cipher.decryptor()
        
        # Decrypt
        padded = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove PKCS7 padding
        padding_length = padded[-1]
        plaintext_bytes = padded[:-padding_length]
        plaintext = plaintext_bytes.decode()
        
        logger.info(f"Decrypted {len(ciphertext)} bytes -> {len(plaintext)} chars")
        return plaintext
    
    @staticmethod
    def encrypt_message(
        message: str,
        key: bytes
    ) -> dict:
        """
        Encrypt message and return encrypted package
        
        Args:
            message: Message to encrypt
            key: AES key
            
        Returns:
            Dict with encrypted data and IV (base64 encoded)
        """
        iv = EncryptionManager.generate_iv()
        ciphertext, _, _ = EncryptionManager.encrypt_aes256(message, key, iv)
        
        return {
            "ciphertext": b64encode(ciphertext).decode(),
            "iv": b64encode(iv).decode(),
            "algorithm": "AES-256-CBC"
        }
    
    @staticmethod
    def decrypt_message(encrypted_data: dict, key: bytes) -> str:
        """
        Decrypt message from encrypted package
        
        Args:
            encrypted_data: Dict with 'ciphertext' and 'iv' (base64)
            key: AES key
            
        Returns:
            Decrypted message
        """
        ciphertext = b64decode(encrypted_data["ciphertext"])
        iv = b64decode(encrypted_data["iv"])
        
        return EncryptionManager.decrypt_aes256(ciphertext, key, iv)


encryption_manager = EncryptionManager()
