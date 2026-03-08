"""
Security Threat Model Analysis
"""

# Security Threat Model - Quantum Secure Chat

## Executive Summary

This document analyzes security threats for a quantum-secure chat application combining BB84 quantum key distribution with AES-256 encryption. The analysis covers eavesdropping, active attacks, infrastructure failures, and mitigation strategies.

---

## 1. Man-in-the-Middle (MITM) Attacks

### Threat Description
Attacker intercepts and modifies communication between Alice and Bob without detection.

### Threat Scenarios

#### 1.1 Network MITM
**Attack Vector**: ARP spoofing, DNS hijacking, BGP hijacking
```
Alice --> [Eve intercepts] --> Bob
Message modified during transmission
```

**Impact**: 
- Message contents revealed
- Message contents modified
- Authentication bypass

**BB84 Protection**:
- Quantum channel provides detection
- Eve's measurement causes QBER increase > 11%
- Protocol aborts, preventing shared key compromise
- Alice and Bob detect eavesdropping

**AES-256 Protection**:
- Even if Eve intercepts ciphertext without BB84 key, decryption impossible
- Computational infeasibility with current technology

**Mitigation**:
```python
# 1. Use TLS 1.3 for all connections
# Certificate pinning to prevent MITM certificates
# HSTS headers to prevent downgrade attacks

# 2. BB84 deployment
if qber > error_threshold:
    abort_key_exchange()
    alert_users()
    # Force re-authentication

# 3. Message authentication codes
hmac = compute_hmac(message, shared_key)
send(message, hmac)

# 4. Forward secrecy
# Each message uses unique derived key from BB84 key
message_key = derive_key(bb84_key, message_number, salt)
```

#### 1.2 SSL/TLS MITM
**Attack Vector**: Rogue certificate, compromised CA
```
Attacker issues fake certificate for quantum-secure-chat.com
Intercepts HTTPS traffic
```

**Mitigation**:
- Certificate pinning in mobile app
- PKPK (Public Key Pinning) headers
- Certificate transparency validation
- OCSP stapling

```python
# Certificate pinning
PINNED_CERTIFICATES = [
    "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
    "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB="
]

def verify_certificate(cert_chain):
    for cert in cert_chain:
        public_key_hash = sha256(cert.public_key)
        if public_key_hash not in PINNED_CERTIFICATES:
            raise CertificateVerificationError()
```

---

## 2. Replay Attacks

### Threat Description
Attacker captures and re-transmits valid messages at different times.

### Threat Scenarios

#### 2.1 Message Replay
```
Attacker: "Transfer $1000" (encrypted with Alice's key)
Eve captures: message_1 = encrypt("Transfer", key)
Eve replays: Same message 10 times
Bob receives same message 10 times = $10,000 transferred
```

**Impact**:
- Duplicate transactions
- Unintended message repetition
- State inconsistency

**Mitigation**:
```python
class ReplayProtection:
    def __init__(self):
        self.message_nonce_cache = {}  # {nonce -> timestamp}
        self.nonce_ttl = 3600  # 1 hour
    
    def create_message(self, content):
        # Include nonce in message
        nonce = os.urandom(16)
        timestamp = int(time.time())
        
        message = {
            "content": content,
            "nonce": nonce.hex(),
            "timestamp": timestamp,
            "seq": self.message_seq_counter
        }
        
        return encrypt(json.dumps(message), key)
    
    def verify_message(self, encrypted_msg, key):
        msg = decrypt(encrypted_msg, key)
        
        # Check nonce hasn't been seen
        if msg["nonce"] in self.message_nonce_cache:
            raise ReplayAttackDetected()
        
        # Check timestamp freshness
        age = int(time.time()) - msg["timestamp"]
        if age > self.nonce_ttl:
            raise ReplayAttackDetected()
        
        # Store nonce
        self.message_nonce_cache[msg["nonce"]] = time.time()
        
        # Verify sequence number
        if msg["seq"] != self.expected_seq:
            raise OutOfOrderMessage()
        
        return msg
```

#### 2.2 Authentication Token Replay
```
Eve captures: JWT token = "eyJhbGciOiJIUzI1NiI..."
Eve uses token repeatedly to access Bob's account
```

**JWT Token Protections**:
```python
class TokenReplayProtection:
    def __init__(self):
        self.token_jti_cache = set()  # JTI = JWT ID
    
    def create_token(self, user_id):
        jti = str(uuid.uuid4())
        token_data = {
            "sub": user_id,
            "jti": jti,  # Unique token ID
            "iat": int(time.time()),  # Issued at
            "exp": int(time.time()) + 1800,  # Expires
            "nbf": int(time.time())  # Not before
        }
        return jwt.encode(token_data, SECRET_KEY)
    
    def verify_token(self, token):
        payload = jwt.decode(token, SECRET_KEY)
        
        # Check if JTI already used (revoked)
        if payload["jti"] in self.token_jti_cache:
            raise TokenRevokedException()
        
        # Check token freshness
        age = int(time.time()) - payload["iat"]
        if age > 3600:  # 1 hour max age
            raise TokenExpiredException()
        
        # Mark as used
        self.token_jti_cache.add(payload["jti"])
        
        return payload
```

---

## 3. Key Leakage Scenarios

### Threat Description
Shared encryption keys are compromised, allowing decryption of messages.

### Threat Scenarios

#### 3.1 Database Breach
```
Attacker gains access to database
Retrieves encrypted keys and key_material column
```

**Impact**:
- All messages encrypted with compromised keys become readable
- Future messages vulnerable if keys not rotated

**Mitigation**:
```python
class KeyManager:
    def __init__(self):
        self.master_key = os.getenv("MASTER_KEY")  # From secure env
        self.key_rotation_interval = 604800  # 7 days
    
    def encrypt_key_for_storage(self, bb84_key):
        """
        Encrypt BB84 key before storing in database
        Uses master key from HSM
        """
        cipher = Cipher(
            algorithms.AES(self.master_key),
            modes.GCM(os.urandom(12)),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Encrypt the key
        ciphertext = encryptor.update(bb84_key) + encryptor.finalize()
        
        return {
            "encrypted_key": ciphertext,
            "iv": encryptor.iv,
            "tag": encryptor.tag
        }
    
    def rotate_keys(self, session_id):
        """
        Rotate encryption key for session
        Re-encrypt old messages with new key
        """
        # Generate new BB84 key
        new_key = run_bb84_protocol()
        
        # Re-encrypt all messages in session
        messages = db.query(Message).filter(
            Message.session_id == session_id
        ).all()
        
        for msg in messages:
            # Decrypt with old key
            old_message = decrypt_message(msg.encrypted_content, old_key)
            
            # Re-encrypt with new key
            msg.encrypted_content = encrypt_message(old_message, new_key)
        
        db.commit()
```

#### 3.2 Memory Dump Attack
```
Attacker obtains memory dump from running application
Keys in memory are readable
```

**Mitigation**:
```python
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

class SecureKeyStorage:
    def __init__(self):
        self.key = None
        self.key_lock = threading.Lock()
    
    def load_key(self):
        """Load key into memory with protection"""
        with self.key_lock:
            # Load from secure enclave if available
            if has_secure_enclave():
                return load_from_secure_enclave()
            
            # Otherwise load from encrypted file
            with open("/secure/key.enc", "rb") as f:
                encrypted_key = f.read()
            
            master_key = load_master_key()
            key = decrypt_key(encrypted_key, master_key)
            
            return key
    
    def use_key(self, callback):
        """Use key in callback, ensure cleared after"""
        key = self.load_key()
        try:
            return callback(key)
        finally:
            # Securely clear from memory
            key.clear()
            del key
            gc.collect()
    
    @staticmethod
    def constant_time_compare(a, b):
        """Prevent timing attacks"""
        return secrets.compare_digest(a, b)
```

#### 3.3 Master Key Compromise
```
Attacker obtains HSM/master key
Can decrypt all stored keys
```

**Mitigation**:
- Hardware Security Module (HSM) for key storage
- Key sharding (Shamir Secret Sharing)
- Multi-factor approval for key access
- Audit logging of all key access

```python
class HSMKeyManager:
    def __init__(self):
        self.hsm = HSMClient()  # CloudHSM, Thales, etc.
    
    def store_key_sharded(self, key, threshold=3, shares=5):
        """
        Use Shamir Secret Sharing
        Any threshold shares can reconstruct key
        Attacker needs threshold shares (harder)
        """
        from secrets import randbelow
        from polynomial import generate_polynomial
        
        # Create polynomial with key as constant term
        poly = generate_polynomial(key, threshold - 1)
        
        # Generate shares
        shares = []
        for x in range(1, shares + 1):
            y = poly.evaluate(x)
            shares.append((x, y))
        
        # Store shares in different locations
        for i, (x, y) in enumerate(shares):
            self.hsm.store_share(f"share_{i}", (x, y))
```

---

## 4. Server Compromise

### Threat Description
Attacker gains control of backend server.

### Threat Scenarios

#### 4.1 Full Server Compromise
```
Attacker: Root access to FastAPI server
Attacker: Can read all memory, files, databases
```

**Impact**:
- All user credentials
- All message keys
- All message contents
- User privacy compromised

**Mitigation**:
<file_endblock/>

```python
class ServerCompromiseDefense:
    
    # 1. Zero-knowledge architecture
    # Server doesn't know plaintext messages
    def handle_message(self, encrypted_message, key_id):
        # Server never decrypts
        # Just routes encrypted blobs
        return self.route_encrypted_message(encrypted_message, key_id)
    
    # 2. Cryptographic proof of integrity
    def verify_message_integrity(self, message, signature, public_key):
        try:
            public_key.verify(signature, message, ec.ECDSA(SHA256()))
            return True
        except InvalidSignature:
            return False
    
    # 3.Continuous monitoring
    def detect_compromise(self):
        suspicious_indicators = {
            "unusual_process_count": psutil.process_count() > BASELINE + 10,
            "unusual_memory": psutil.virtual_memory().percent > 90,
            "unauthorized_file_access": self.check_file_access_logs(),
            "unexpected_network": self.check_network_connections(),
            "process_injection": self.detect_process_injection()
        }
        
        if any(suspicious_indicators.values()):
            self.trigger_incident_response()
            self.failover_to_backup_server()
```

---

## 5. Side-Channel Attacks

### Threat Description
Exploit implementation vulnerabilities rather than algorithmic weaknesses.

#### 5.1 Timing Attack
```
Measure time to verify password/token
Attacker learns bit-by-bit information
```

**Attack Example**:
```
Time took to reject password: 5ms
Time took to accept password: 45ms
Attacker knows first char is correct if takes longer
```

**Mitigation**:
```python
def constant_time_compare(user_input, stored_hash):
    """Always take same time regardless of match position"""
    result = 0
    for x, y in zip(user_input, stored_hash):
        result |= ord(x) ^ ord(y)
    return result == 0

# Instead of naive comparison which returns early on first mismatch
def vulnerable_compare(a, b):
    if len(a) != len(b):  # Timing leak!
        return False
    for x, y in zip(a, b):
        if x != y:
            return False  # Timing leak - early return
    return True
```

#### 5.2 Power Analysis
```
Monitor power consumption during cryptographic operations
Different operations consume different power
Attacker learns bits being processed
```

**Mitigation**:
- Constant-time implementations
- Power noise injection
- Masking techniques

---

## 6. Quantum Computing Threat (Post-Quantum)

### Threat Description
Future quantum computers can break RSA/ECDSA in polynomial time.

**Current Status**:
- BB84-derived AES-256 keys are **quantum-resistant**
- Symmetric encryption secure even against quantum computers
- RSA/ECDSA signatures vulnerable

**Quantum Threat Timeline**:
```
2024: Limited quantum computers (<1000 qubits)
2030: Cryptographically relevant quantum computers possible
2040: RSA-2048 breakable in ~1 day

Protection: Use post-quantum algorithms now
- CRYSTALS-Kyber (Key encapsulation)
- CRYSTALS-Dilithium (Digital signatures)
- SPHINCS+ (Hash-based signatures)
```

**Future-Proofing**:
```python
class QuantumResistantCrypto:
    def sign_message_hybrid(self, message):
        """Use both classical and post-quantum signatures"""
        # Classical signature (for now)
        classical_sig = sign_with_ecdsa(message)
        
        # Post-quantum signature
        pq_sig = sign_with_dilithium(message)
        
        return {
            "message": message,
            "classical_sig": classical_sig,
            "pq_sig": pq_sig
        }
    
    def verify_signature_hybrid(self, message, signatures):
        """Verify both signatures"""
        classical_valid = verify_ecdsa(message, signatures["classical_sig"])
        pq_valid = verify_dilithium(message, signatures["pq_sig"])
        
        # Both must be valid
        return classical_valid and pq_valid
```

---

## 7. Threat Summary Table

| Threat | Severity | BB84 Protection | AES-256 Protection | Detection |
|--------|----------|-----------------|-------------------|-----------|
| MITM (Network) | HIGH | ✓ QBER detection | ✓ Encryption | ✓ Error rate increase |
| MITM (SSL/TLS) | HIGH | ✓ BB84 key | ✓ Encryption | ✓ Certificate pinning |
| Replay Attack | MEDIUM | ✓ Nonces | ✓ Sequence numbers | ✓ Duplicate detection |
| Database Breach | HIGH | ✓ Encrypted keys | ✓ Key encryption | ✗ After fact |
| Server Compromise | CRITICAL | Partial | ✓ No plaintext | ✓ Monitoring |
| Timing Attack | MEDIUM | ✓ Constant time | ✓ Constant time | ✓ Audit logs |
| Quantum Computing | LOW* | ✓ Future-proof | ✓ Secure | - |

*Timeline: 10+ years

---

## 8. Incident Response Plan

```python
class IncidentResponsePlan:
    
    def detect_compromise(self):
        """Continuous monitoring"""
        return {
            "qber_spike": qber > 0.15,
            "failed_auth_spike": failed_logins > 100 / hour,
            "unusual_api_calls": abnormal_endpoint_pattern(),
            "data_exfiltration": unusual_network_egress()
        }
    
    def immediate_response(self, incident_type):
        """Immediate actions"""
        if incident_type == "EAVESDROPPING_DETECTED":
            # QBER > threshold
            self.abort_key_exchange()
            self.notify_users()
            self.force_re_authentication()
            self.generate_new_keys()
        
        elif incident_type == "SERVER_COMPROMISE":
            # Suspicious activity detected
            self.isolate_server()
            self.failover_to_backup()
            self.shutdown_affected_services()
            self.preserve_logs()
    
    def post_incident(self):
        """Recovery actions"""
        self.conduct_forensics()
        self.identify_root_cause()
        self.patch_vulnerabilities()
        self.rotate_all_keys()
        self.notify_affected_users()
        self.audit_all_access()
        self.improve_monitoring()
```

---

## Conclusion

The quantum-secure chat application provides:
1. **Detection** of MITM attacks via BB84 QBER monitoring
2. **Prevention** of message decryption via AES-256
3. **Resistance** to quantum computers via symmetric cryptography
4. **Resilience** through monitoring and incident response

Residual risks:
- Server compromise at application layer
- Implementation vulnerabilities (side-channels)
- Physical compromise of HSM

These require defense-in-depth:
- Code review and testing
- Secure enclave usage
- Zero-knowledge architecture
- Continuous monitoring
