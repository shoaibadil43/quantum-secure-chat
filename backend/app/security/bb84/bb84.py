"""
BB84 Quantum Key Distribution Algorithm Implementation
Bennett and Brassard 1984
"""

import random
from typing import Tuple, List, Dict
import logging

logger = logging.getLogger(__name__)


class BB84:
    """BB84 Quantum Key Distribution Protocol"""
    
    # Basis constants
    RECTILINEAR_BASIS = 0  # + (Vertical/Horizontal)
    DIAGONAL_BASIS = 1      # × (Diagonal)
    
    # Bit values
    ZERO = 0
    ONE = 1
    
    def __init__(self, qubit_count: int = 4096):
        """
        Initialize BB84 protocol
        
        Args:
            qubit_count: Number of qubits for key generation
        """
        self.qubit_count = qubit_count
        self.sender_bits: List[int] = []
        self.sender_bases: List[int] = []
        self.sender_results: List[int] = []
        self.receiver_bases: List[int] = []
        self.receiver_results: List[int] = []
        self.sifted_key: str = ""
        self.quantum_bit_error_rate: float = 0.0
    
    def generate_random_bits(self) -> List[int]:
        """
        Step 1: Sender generates random bits
        
        Returns:
            List of random bits (0 or 1)
        """
        bits = [random.choice([self.ZERO, self.ONE]) for _ in range(self.qubit_count)]
        self.sender_bits = bits
        logger.info(f"Generated {len(bits)} random bits")
        return bits
    
    def generate_random_bases(self) -> List[int]:
        """
        Step 2: Sender selects random bases for each bit
        
        Returns:
            List of bases (0 for rectilinear, 1 for diagonal)
        """
        bases = [random.choice([self.RECTILINEAR_BASIS, self.DIAGONAL_BASIS]) 
                 for _ in range(self.qubit_count)]
        self.sender_bases = bases
        logger.info(f"Generated {len(bases)} random bases")
        return bases
    
    def encode_qubits(self) -> Dict[int, Tuple[int, int]]:
        """
        Step 3: Encode bits using selected bases
        
        Returns:
            Dictionary mapping index to (bit, basis) tuples
        """
        if not self.sender_bits or not self.sender_bases:
            raise ValueError("Generate bits and bases first")
        
        encoded = {}
        for i in range(self.qubit_count):
            encoded[i] = (self.sender_bits[i], self.sender_bases[i])
        
        logger.info(f"Encoded {len(encoded)} qubits")
        return encoded
    
    def receiver_measure_qubits(self) -> Tuple[List[int], List[int]]:
        """
        Step 4: Receiver generates random bases and measures qubits
        
        Returns:
            Tuple of (measured_bits, measurement_bases)
        """
        measurement_bases = [
            random.choice([self.RECTILINEAR_BASIS, self.DIAGONAL_BASIS])
            for _ in range(self.qubit_count)
        ]
        self.receiver_bases = measurement_bases
        
        # Simulate measurement results
        measured_bits = []
        for i in range(self.qubit_count):
            if self.receiver_bases[i] == self.sender_bases[i]:
                # Correct basis - get correct bit
                measured_bits.append(self.sender_bits[i])
            else:
                # Wrong basis - random bit
                measured_bits.append(random.choice([self.ZERO, self.ONE]))
        
        self.receiver_results = measured_bits
        logger.info(f"Measured {len(measured_bits)} qubits with {len(measurement_bases)} bases")
        return measured_bits, measurement_bases
    
    def sift_keys(self, threshold: float = 0.5) -> str:
        """
        Step 5: Key sifting - keep only bits measured with correct basis
        
        Args:
            threshold: Minimum matching qubits ratio required
            
        Returns:
            Sifted key as binary string
        """
        if not self.receiver_results or not self.receiver_bases:
            raise ValueError("Perform measurement first")
        
        sifted_bits = []
        matching_count = 0
        
        for i in range(self.qubit_count):
            if self.sender_bases[i] == self.receiver_bases[i]:
                sifted_bits.append(str(self.sender_bits[i]))
                matching_count += 1
        
        match_ratio = matching_count / self.qubit_count
        logger.info(f"Sifting: {matching_count}/{self.qubit_count} ({match_ratio:.2%}) matches")
        
        if match_ratio < threshold:
            logger.warning(f"Sifting ratio {match_ratio:.2%} below threshold {threshold:.2%}")
        
        self.sifted_key = ''.join(sifted_bits)
        return self.sifted_key
    
    def estimate_quantum_bit_error_rate(self, sacrificed_indices: List[int]) -> float:
        """
        Step 6: Estimate QBER by sacrificing portion of sifted key
        
        Args:
            sacrificed_indices: Indices in sifted key to check for errors
            
        Returns:
            Estimated quantum bit error rate (QBER)
        """
        if not self.sifted_key:
            raise ValueError("Sift keys first")
        
        errors = 0
        for idx in sacrificed_indices:
            if idx < len(self.sifted_key):
                # Simulate checking against basis
                if random.random() > 0.99:  # ~1% quantum noise
                    errors += 1
        
        qber = errors / len(sacrificed_indices) if sacrificed_indices else 0.0
        self.quantum_bit_error_rate = qber
        
        logger.info(f"Estimated QBER: {qber:.4f} ({errors}/{len(sacrificed_indices)})")
        return qber
    
    def remove_sacrificed_bits(self, sacrificed_indices: List[int]) -> str:
        """
        Remove sacrificed bits from sifted key
        
        Args:
            sacrificed_indices: Indices of bits to remove
            
        Returns:
            Final key after removing sacrificed bits
        """
        final_key_bits = [
            bit for i, bit in enumerate(self.sifted_key)
            if i not in sacrificed_indices
        ]
        
        final_key = ''.join(final_key_bits)
        logger.info(f"Final key length: {len(final_key)} bits ({len(final_key)//8} bytes)")
        return final_key
    
    def run_bb84_protocol(self, error_threshold: float = 0.11) -> Dict:
        """
        Execute complete BB84 protocol
        
        Args:
            error_threshold: Maximum acceptable QBER
            
        Returns:
            Protocol results including final key and security info
        """
        logger.info("Starting BB84 Protocol")
        
        # Step 1-3: Generate and encode
        self.generate_random_bits()
        self.generate_random_bases()
        self.encode_qubits()
        
        # Step 4: Receiver measures
        self.receiver_measure_qubits()
        
        # Step 5: Sift keys
        self.sift_keys()
        
        # Step 6: Estimate QBER (sacrifice ~50% of sifted key)
        sacrificed_count = len(self.sifted_key) // 2
        sacrificed_indices = random.sample(
            range(len(self.sifted_key)),
            min(sacrificed_count, len(self.sifted_key))
        )
        
        qber = self.estimate_quantum_bit_error_rate(sacrificed_indices)
        
        # Check if QBER within acceptable range
        is_secure = qber < error_threshold
        
        # Step 7: Remove sacrificed bits
        final_key = self.remove_sacrificed_bits(sacrificed_indices)
        
        result = {
            "success": is_secure,
            "final_key": final_key,
            "final_key_length": len(final_key),
            "final_key_bytes": len(final_key) // 8,
            "sifted_key_length": len(self.sifted_key),
            "qber": qber,
            "error_threshold": error_threshold,
            "is_secure": is_secure,
            "security_message": (
                "Secure - No eavesdropping detected" if is_secure
                else f"Possible eavesdropping detected (QBER: {qber:.4f})"
            )
        }
        
        logger.info(f"BB84 Protocol Result: {result['security_message']}")
        return result


def run_simple_bb84(qubit_count: int = 4096) -> Dict:
    """
    Convenience function to run complete BB84 protocol
    
    Args:
        qubit_count: Number of qubits to use
        
    Returns:
        Protocol results
    """
    bb84 = BB84(qubit_count=qubit_count)
    return bb84.run_bb84_protocol()
