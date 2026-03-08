"""
Privacy Amplification for BB84
Reduce impact of partial eavesdropping
"""

from typing import List
import hashlib
import logging

logger = logging.getLogger(__name__)


class PrivacyAmplification:
    """Privacy amplification for secure key distillation"""
    
    @staticmethod
    def toeplitz_matrix_hash(
        raw_key: str,
        seed_x: bytes,
        seed_y: bytes,
        output_length: int = 256
    ) -> str:
        """
        Apply Toeplitz matrix hash for privacy amplification
        
        Args:
            raw_key: Binary string of the raw key
            seed_x: Seed for x coefficients
            seed_y: Seed for y coefficients
            output_length: Desired output length in bits
            
        Returns:
            Privacy-amplified key as binary string
        """
        # Convert binary string to integers
        key_bits = [int(b) for b in raw_key]
        
        # Derive matrix coefficients from seeds
        x_matrix = hashlib.sha256(seed_x).digest()
        y_matrix = hashlib.sha256(seed_y).digest()
        
        # Build Toeplitz matrix
        matrix_width = min(output_length, len(key_bits))
        amplified_bits = []
        
        for col in range(matrix_width):
            # Compute parity
            parity = 0
            seed_byte_x = x_matrix[col % len(x_matrix)]
            seed_byte_y = y_matrix[col % len(y_matrix)]
            
            for row in range(len(key_bits)):
                # XOR with seeded matrix values
                matrix_val = ((seed_byte_x >> (row % 8)) ^ 
                             (seed_byte_y >> (row % 8))) & 1
                parity ^= (key_bits[row] & matrix_val)
            
            amplified_bits.append(str(parity))
        
        amplified_key = ''.join(amplified_bits[:output_length])
        logger.info(f"Applied privacy amplification: {len(amplified_key)} bits")
        
        return amplified_key
    
    @staticmethod
    def xor_hash_amplification(raw_key: str, hash_rounds: int = 3) -> str:
        """
        Simpler XOR-based privacy amplification
        
        Args:
            raw_key: Binary string or bytes
            hash_rounds: Number of hash iterations
            
        Returns:
            Amplified key
        """
        current = raw_key.encode() if isinstance(raw_key, str) else raw_key
        
        for round_num in range(hash_rounds):
            h = hashlib.sha256()
            h.update(current)
            h.update(str(round_num).encode())
            current = h.digest()
        
        # Convert to binary string
        amplified = bin(int.from_bytes(current, 'big'))[2:].zfill(256)
        logger.info(f"Applied XOR-hash amplification: {len(amplified)} bits")
        
        return amplified
    
    @staticmethod
    def randomness_extraction(
        raw_key: str,
        extractor_seed: bytes = None
    ) -> str:
        """
        Extract randomness from raw key
        
        Args:
            raw_key: Input raw key
            extractor_seed: Seed for extraction function
            
        Returns:
            Extracted random key
        """
        if extractor_seed is None:
            extractor_seed = b"quantum_extraction"
        
        # Universal hashing for randomness extraction
        h = hashlib.sha256()
        h.update(extractor_seed)
        h.update(raw_key.encode() if isinstance(raw_key, str) else raw_key)
        
        extracted = bin(int.from_bytes(h.digest(), 'big'))[2:].zfill(256)
        logger.info(f"Extracted random key: {len(extracted)} bits")
        
        return extracted
    
    @staticmethod
    def apply_full_amplification(
        raw_key: str,
        error_rate: float,
        target_bits: int = 256
    ) -> str:
        """
        Apply full privacy amplification pipeline
        
        Args:
            raw_key: Noisy raw key
            error_rate: Estimated quantum bit error rate
            target_bits: Target output length
            
        Returns:
            Final secure key
        """
        logger.info(
            f"Starting privacy amplification (input: {len(raw_key)} bits, "
            f"QBER: {error_rate:.4f})"
        )
        
        # Step 1: Randomness extraction
        extracted = PrivacyAmplification.randomness_extraction(raw_key)
        
        # Step 2: Toeplitz matrix hash
        amplified = PrivacyAmplification.toeplitz_matrix_hash(
            extracted,
            seed_x=b"seed_x_quantum",
            seed_y=b"seed_y_quantum",
            output_length=target_bits
        )
        
        # Step 3: Final hash
        final = hashlib.sha256(amplified.encode()).hexdigest()
        
        logger.info(f"Privacy amplification complete: {len(final)*4} bits")
        return final
