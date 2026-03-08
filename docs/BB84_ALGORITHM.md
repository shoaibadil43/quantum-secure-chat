"""
BB84 Quantum Key Distribution Algorithm Documentation
"""

# BB84 Quantum Key Distribution Algorithm

## Overview

BB84 is a quantum key distribution (QKD) protocol developed by Charles Bennett and Gilles Brassard in 1984. It provides theoretically unconditional security against eavesdropping based on quantum mechanical principles.

## How It Works

### Step 1: Random Bit Generation
Alice (sender) generates a random sequence of bits:
```
Bits: [0, 1, 0, 1, 1, 0, 1, 0, ...]
```

### Step 2: Random Basis Selection
Alice randomly chooses a basis for each bit:
```
Rectilinear (+): Vertical/Horizontal polarization
Diagonal (×): Diagonal/Anti-diagonal polarization

Bases: [+, ×, +, ×, +, ×, +, +, ...]
```

### Step 3: Qubit Encoding & Transmission
Alice encodes bits using selected bases and sends qubits through quantum channel:
```
Bit 0 in + basis: Vertical polarization ↑
Bit 1 in + basis: Horizontal polarization →
Bit 0 in × basis: Diagonal polarization ↗
Bit 1 in × basis: Anti-diagonal polarization ↖
```

### Step 4: Random Measurement
Bob (receiver) randomly chooses bases for measurement:
```
Receiver Bases: [×, ×, +, ×, ×, +, +, ×, ...]
```

Key quantum principle: If Bob measures with wrong basis, result is random.

### Step 5: Sifting
Alice and Bob publicly compare bases (NOT bits) and keep only matches:
```
Alice Bits:          [0, 1, 0, 1, 1, 0, 1, 0]
Alice Bases:         [+, ×, +, ×, +, ×, +, +]
Bob Bases:           [×, ×, +, ×, +, +, +, ×]
                      ✗  ✓  ✓  ✓  ✗  ✗  ✓  ✗

Sifted Key:          [1, 0, 1, 0, 1, 0]
```

Sifting efficiency: ~50% of qubits retained

### Step 6: Error Detection (QBER Estimation)
Alice and Bob publicly compare a random subset of sifted bits:
```
Theoretical error rate: ~0% (perfect channel)
Due to quantum noise: ~1% (noisy channel)
Evidence of eavesdropping: > 11% error rate
```

### Step 7: Privacy Amplification
Apply randomness extraction and universal hashing to final key to remove partial information an eavesdropper might have:
```
Raw sifted key: [1, 0, 1, 0, 1, 0, ...]
After amplification: [Privacy-amplified random bits]
```

## Security Properties

### Unconditional Security
- Security independent of computational power
- Based on laws of physics, not mathematical assumptions
- No key recovery possible even with quantum computer

### Eavesdropping Detection
If Eve (eavesdropper) tries to intercept qubits:
1. She must measure without knowing correct basis
2. Wrong basis measurement gives random result
3. Sending random qubit to Bob causes detectable errors
4. QBER increases above threshold ~11%
5. Alice and Bob abort protocol

```
Normal transmission QBER: ~1% (quantum noise)
Eve eavesdropping QBER: ~25% (information gain + noise)
```

### Key Rate
- Input: 4096 qubits
- After sifting: ~2048 bits
- After sacrificing for QBER: ~1024 bits
- Final key after amplification: 256-512 bits

## Implementation Details

### Protocol Parameters
```python
BB84_QUBIT_COUNT = 4096           # Number of qubits
BB84_ERROR_THRESHOLD = 0.11        # Max acceptable QBER
BB84_SIFT_RATIO = 0.5              # Expected sift ratio
BB84_KEY_LENGTH = 256              # Final key in bits
```

### Rectilinear Basis (+)
```
Bit 0: |0⟩ (vertical polarization)
Bit 1: |1⟩ (horizontal polarization)
```

### Diagonal Basis (×)
```
Bit 0: |+⟩ = (|0⟩ + |1⟩)/√2
Bit 1: |-⟩ = (|0⟩ - |1⟩)/√2
```

### Measurement Rules
```
If measured with correct basis: 100% correct
If measured with wrong basis: 50% correct, 50% wrong
Average information per qubit: 0.5 bits
```

## Limitations

### Practical Challenges
1. **Quantum Channel Requirements**
   - Long-distance transmission difficult
   - Photon loss over distance
   - Quantum noise degrades signal

2. **Implementation Security**
   - Realistic detectors have vulnerabilities
   - Timing attacks possible
   - Side-channel attacks

3. **Speed**
   - Slower than classical key distribution
   - Dependent on quantum hardware

### Modern Variants
- **E91 (Ekert 1991)**: Uses entangled photons
- **Decoy State BB84**: Extended range
- **Twin-Field QKD**: Record distances

## In Our Application

### Integration with AES-256
```python
# BB84 generates ~512-bit key
bb84_key = run_bb84_protocol(qubit_count=4096)

# Derive AES-256 key from quantum key
aes_key = derive_key_from_bb84(
    bb84_key,
    desired_length=32  # 256 bits
)

# Use for message encryption
encrypted = encrypt_aes256(message, aes_key)
```

### Key Exchange Protocol
```
1. Alice: Generate BB84 key (offline)
2. Alice: Transmit qubits through quantum channel
3. Bob: Measure and record results
4. Alice & Bob: Public basis comparison
5. Alice & Bob: Sift keys (basis matching)
6. Alice & Bob: Estimate QBER (error detection)
7. Alice & Bob: Privacy amplification (randomness extraction)
8. Result: Shared 256-512 bit key for AES-256
```

## Mathematical Foundations

### Information Gain for Eve
```
If Eve intercepts and measures correctly (knows basis):
I(E:final key | Eve) = 0  (Eve has perfect knowledge)

If Eve intercepts but doesn't know basis:
I(E:final key | Eve) ≈ 0  (Privacy amplification removes info)
```

### QBER Calculation
```
QBER = Number of bit errors / Number of sifted bit positions

Normal: QBER ≈ 0.01 (1% quantum noise)
Eve present: QBER ≈ 0.25 (25% error increase)
Threshold: QBER_max = 0.11 (11%)
```

### Key Rate Formula
```
R = {(1 - 2H(QBER)) × P_sift × n × R_key}

Where:
H(QBER) = Binary entropy function
P_sift = Sifting probability (~0.5)
n = Number of qubits
R_key = Privacy amplification efficiency
```

## References
- Bennett, C. H., & Brassard, G. (1984). "Quantum cryptography: Public key distribution and coin tossing"
- https://en.wikipedia.org/wiki/BB84
- https://qiskit.org/textbook/ch-algorithms/quantum-key-distribution.html
