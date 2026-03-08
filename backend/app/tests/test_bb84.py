"""
BB84 Algorithm Tests
"""

import unittest
from app.security.bb84.bb84 import BB84, run_simple_bb84
from app.security.bb84.key_sifting import KeySifting
from app.security.bb84.privacy_amplification import PrivacyAmplification


class TestBB84(unittest.TestCase):
    """Test BB84 quantum key distribution"""
    
    def setUp(self):
        self.bb84 = BB84(qubit_count=1024)
    
    def test_random_bit_generation(self):
        """Test random bit generation"""
        bits = self.bb84.generate_random_bits()
        self.assertEqual(len(bits), 1024)
        self.assertTrue(all(b in [0, 1] for b in bits))
    
    def test_random_basis_generation(self):
        """Test random basis generation"""
        bases = self.bb84.generate_random_bases()
        self.assertEqual(len(bases), 1024)
        self.assertTrue(all(b in [0, 1] for b in bases))
    
    def test_qubit_encoding(self):
        """Test qubit encoding"""
        self.bb84.generate_random_bits()
        self.bb84.generate_random_bases()
        encoded = self.bb84.encode_qubits()
        self.assertEqual(len(encoded), 1024)
    
    def test_measurement(self):
        """Test qubit measurement"""
        self.bb84.generate_random_bits()
        self.bb84.generate_random_bases()
        measured, bases = self.bb84.receiver_measure_qubits()
        self.assertEqual(len(measured), 1024)
        self.assertEqual(len(bases), 1024)
    
    def test_key_sifting(self):
        """Test key sifting"""
        self.bb84.generate_random_bits()
        self.bb84.generate_random_bases()
        self.bb84.receiver_measure_qubits()
        sifted = self.bb84.sift_keys()
        self.assertGreater(len(sifted), 0)
        self.assertTrue(all(b in ['0', '1'] for b in sifted))
    
    def test_complete_protocol(self):
        """Test complete BB84 protocol"""
        result = self.bb84.run_bb84_protocol()
        self.assertIn("success", result)
        self.assertIn("final_key", result)
        self.assertIn("qber", result)
        self.assertGreater(result["final_key_length"], 0)


class TestKeySifting(unittest.TestCase):
    """Test key sifting"""
    
    def test_sift_keys(self):
        """Test sifting functionality"""
        sender_bases = [0, 1, 0, 1, 0]
        receiver_bases = [0, 1, 1, 1, 0]
        sender_bits = [0, 1, 0, 1, 0]
        
        sifted, indices = KeySifting.sift_keys(
            sender_bases, receiver_bases, sender_bits
        )
        
        # Matching indices: 0, 1, 4
        self.assertEqual(len(indices), 3)
        self.assertEqual(sifted, "010")


class TestPrivacyAmplification(unittest.TestCase):
    """Test privacy amplification"""
    
    def test_xor_hash_amplification(self):
        """Test XOR hash amplification"""
        raw_key = "0" * 256
        amplified = PrivacyAmplification.xor_hash_amplification(raw_key)
        self.assertEqual(len(amplified), 256)
    
    def test_randomness_extraction(self):
        """Test randomness extraction"""
        raw_key = "01010101" * 32
        extracted = PrivacyAmplification.randomness_extraction(raw_key)
        self.assertEqual(len(extracted), 256)


if __name__ == "__main__":
    unittest.main()
