"""
Encryption Tests
"""

import unittest
from app.security.encryption import EncryptionManager


class TestEncryption(unittest.TestCase):
    """Test AES-256 encryption"""
    
    def setUp(self):
        self.manager = EncryptionManager()
        self.key = self.manager.generate_key()
        self.test_message = "Hello, Quantum Secure Chat!"
    
    def test_key_generation(self):
        """Test key generation"""
        key = self.manager.generate_key()
        self.assertEqual(len(key), 32)  # 256 bits
    
    def test_iv_generation(self):
        """Test IV generation"""
        iv = self.manager.generate_iv()
        self.assertEqual(len(iv), 16)  # 128 bits
    
    def test_encrypt_decrypt(self):
        """Test encryption and decryption"""
        ciphertext, iv, _ = self.manager.encrypt_aes256(
            self.test_message,
            self.key
        )
        
        decrypted = self.manager.decrypt_aes256(ciphertext, self.key, iv)
        self.assertEqual(decrypted, self.test_message)
    
    def test_encrypt_message(self):
        """Test message encryption package"""
        encrypted_pkg = self.manager.encrypt_message(self.test_message, self.key)
        self.assertIn("ciphertext", encrypted_pkg)
        self.assertIn("iv", encrypted_pkg)
        self.assertIn("algorithm", encrypted_pkg)
    
    def test_decrypt_message(self):
        """Test message decryption from package"""
        encrypted_pkg = self.manager.encrypt_message(self.test_message, self.key)
        decrypted = self.manager.decrypt_message(encrypted_pkg, self.key)
        self.assertEqual(decrypted, self.test_message)
    
    def test_derive_key_from_bb84(self):
        """Test deriving AES key from BB84"""
        bb84_key = "a" * 64  # Hex string
        aes_key = self.manager.derive_key_from_bb84(bb84_key, 32)
        self.assertEqual(len(aes_key), 32)


if __name__ == "__main__":
    unittest.main()
