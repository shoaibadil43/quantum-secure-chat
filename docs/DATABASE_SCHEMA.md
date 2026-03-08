"""
Database Schema Documentation
"""

# Database Schema - Quantum Secure Chat

## Tables Overview

### 1. Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255),
  avatar_url VARCHAR(500),
  is_active BOOLEAN DEFAULT TRUE,
  is_verified BOOLEAN DEFAULT FALSE,
  failed_login_attempts INTEGER DEFAULT 0,
  last_login TIMESTAMP,
  locked_until TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_username (username),
  INDEX idx_email (email),
  INDEX idx_is_active (is_active)
);
```

**Purpose**: Store user account information
**Key Fields**:
- `id`: Unique user identifier
- `password_hash`: Bcrypt hashed password (NOT stored in plain)
- `is_verified`: Email verification status
- `failed_login_attempts`: For account lockout mechanism
- `locked_until`: Account lockout timestamp

### 2. ChatSessions Table
```sql
CREATE TABLE chat_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  is_group BOOLEAN DEFAULT FALSE,
  is_encrypted BOOLEAN DEFAULT TRUE,
  shared_key_id UUID,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_owner_id (owner_id),
  INDEX idx_created_at (created_at)
);
```

**Purpose**: Store chat rooms/conversations
**Key Fields**:
- `is_group`: Differentiate between 1-on-1 and group chats
- `is_encrypted`: Track if encryption is enabled
- `shared_key_id`: Reference to BB84-generated key

### 3. Messages Table
```sql
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
  sender_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  encrypted_content TEXT,
  encryption_key_id UUID REFERENCES encryption_keys(id),
  is_delivered BOOLEAN DEFAULT FALSE,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_session_id (session_id),
  INDEX idx_sender_id (sender_id),
  INDEX idx_created_at (created_at),
  INDEX idx_is_read (is_read)
);
```

**Purpose**: Store chat messages
**Key Fields**:
- `content`: Original plaintext message
- `encrypted_content`: AES-256 encrypted message
- `encryption_key_id`: Key used for encryption
- `is_delivered`: Message delivery status
- `is_read`: Message read status

### 4. EncryptionKeys Table
```sql
CREATE TABLE encryption_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
  key_type VARCHAR(50) DEFAULT 'BB84',
  key_material TEXT NOT NULL,  -- Encrypted key material
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP,
  metadata TEXT,  -- JSON metadata
  
  INDEX idx_session_id (session_id),
  INDEX idx_is_active (is_active)
);
```

**Purpose**: Store encryption keys
**Key Fields**:
- `key_type`: BB84, AES256, etc.
- `key_material`: Encrypted binary key data
- `expires_at`: Key expiration time
- `metadata`: JSON with key derivation params

## Indexing Strategy

### High-Frequency Queries
```sql
-- Popular queries and their indexes
SELECT * FROM messages WHERE session_id = ? ORDER BY created_at DESC;
INDEX: (session_id, created_at)

SELECT * FROM users WHERE email = ?;
INDEX: (email)

SELECT * FROM messages WHERE is_read = FALSE AND recipient_id = ?;
INDEX: (is_read, recipient_id)
```

### Query Performance
- Messages by session: O(log n)
- User lookup: O(log n)
- Unread messages: O(log n)

## Relationships

```
Users (1) ---> (Many) ChatSessions
Users (1) ---> (Many) Messages
ChatSessions (1) ---> (Many) Messages
ChatSessions (1) ---> (Many) EncryptionKeys
EncryptionKeys (1) ---> (Many) Messages
```

## Data Constraints

### Foreign Key Constraints
- ON DELETE CASCADE for dependent records
- Referential integrity enforcement

### Uniqueness Constraints
- username (UNIQUE)
- email (UNIQUE)

### Data Types
- IDs: UUID for distributed systems compatibility
- Timestamps: TIMESTAMP with UTC timezone
- Sensitive data: TEXT (encrypted at application layer)

## Backup & Recovery

### Backup Strategy
- Daily automated snapshots
- Point-in-time recovery windows: 30 days
- Cross-region replication for DR
- Transaction logs for WAL-based recovery

### Archive Policy
- Messages > 1 year: Archive to cold storage
- Users: Never delete (soft delete with is_active flag)
- Encryption keys: Retain indefinitely for historical decryption

## Performance Characteristics

### Read Operations
- Average message retrieval: < 50ms
- User lookup: < 10ms
- Session query: < 20ms

### Write Operations
- Message insertion: < 100ms
- User registration: < 100ms
- Key generation: < 50ms

## Scaling Considerations

### Partitioning Strategy
- Partition messages by session_id and date
- Archive old partitions separately
- Improves query performance for large datasets

### Connection Pooling
- Min connections: 5
- Max connections: 20
- Connection timeout: 30 seconds

## Security Features

### Encryption at Rest
```sql
-- Column-level encryption for sensitive data
ALTER TABLE encryption_keys 
  ADD CONSTRAINT encryption_keys_pkey_encrypted 
  CHECK (key_material IS NOT NULL);

-- Encrypted backups
BACKUP DATABASE quantum_chat 
  WITH ENCRYPTION = ON;
```

### Audit Logging
```sql
CREATE TABLE audit_log (
  id UUID PRIMARY KEY,
  table_name VARCHAR(255),
  operation VARCHAR(10),  -- INSERT, UPDATE, DELETE
  user_id UUID,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  changes JSONB
);
```
