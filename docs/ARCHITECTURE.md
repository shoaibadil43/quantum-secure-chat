"""
Production Architecture Documentation
"""

# Quantum-Secure Chat Application - Production Architecture

## System Overview

### Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│                    Flutter UI Layer                 │
│  (iOS, Android, Web with Material Design 3)         │
└──────────────────┬──────────────────────────────────┘
                   │ HTTPS/WSS
┌──────────────────┼──────────────────────────────────┐
│              API Gateway / Load Balancer             │
│          (Nginx reverse proxy, TLS termination)     │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────┼──────────────────────────────────┐
│         FastAPI Backend (Uvicorn ASGI Server)       │
│  - Authentication & Authorization                   │
│  - Message Routing & Processing                     │
│  - WebSocket Management                             │
└──────────────┬───────────────┬──────────────────────┘
               │               │
    ┌──────────┴─┐      ┌──────┴───────────┐
    │            │      │                  │
┌───┴────────────▼──┐  ┌┴────────────┐  ┌─┴───────────────┐
│  PostgreSQL DB    │  │  Redis      │  │  Message Queue  │
│  (Persistent      │  │  (Cache &   │  │  (RabbitMQ/     │
│   Storage)        │  │   Pub/Sub)  │  │   Celery)       │
└───────────────────┘  └─────────────┘  └─────────────────┘
```

## Component Details

### Frontend (Flutter)
- **Platforms**: iOS, Android, Web, Desktop
- **UI Framework**: Flutter Material Design 3
- **State Management**: Provider + Riverpod
- **WebSocket**: web_socket_channel, socket_io_client
- **Encryption**: flutter_secure_storage for local keys
- **Features**:
  - Offline message queue
  - Local message caching
  - End-to-end encryption
  - Dark mode support

### Backend (FastAPI)
- **Server**: Uvicorn ASGI server
- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis for session & message caching
- **Message Queue**: Celery with Redis broker
- **WebSocket**: Native FastAPI WebSocket support
- **Features**:
  - Async/await throughout
  - Connection pooling
  - Database indexing
  - Rate limiting

### Security Layer
- **Quantum Key Distribution**: BB84 protocol
  - Algorithm: Bennett-Brassard 1984
  - Key length: 512-bits minimum
  - QBER threshold: 11%
  - Privacy amplification: Toeplitz matrix hashing
  
- **Encryption**:
  - AES-256-CBC for message encryption
  - PBKDF2 key derivation
  - Random IV per message
  
- **Authentication**:
  - JWT with HS256
  - Token expiration: 30 minutes
  - Refresh tokens with 7-day expiry
  - Bcrypt password hashing (rounds=12)

- **Authorization**:
  - Role-based access control
  - Room-level permissions
  - User isolation

### Database Schema

```sql
-- Users Table
CREATE TABLE users (
  id UUID PRIMARY KEY,
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
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat Sessions Table
CREATE TABLE chat_sessions (
  id UUID PRIMARY KEY,
  owner_id UUID NOT NULL REFERENCES users(id),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  is_group BOOLEAN DEFAULT FALSE,
  is_encrypted BOOLEAN DEFAULT TRUE,
  shared_key_id UUID,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Messages Table
CREATE TABLE messages (
  id UUID PRIMARY KEY,
  session_id UUID NOT NULL REFERENCES chat_sessions(id),
  sender_id UUID NOT NULL REFERENCES users(id),
  content TEXT NOT NULL,
  encrypted_content TEXT,
  encryption_key_id UUID,
  is_delivered BOOLEAN DEFAULT FALSE,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Encryption Keys Table
CREATE TABLE encryption_keys (
  id UUID PRIMARY KEY,
  session_id UUID NOT NULL REFERENCES chat_sessions(id),
  key_type VARCHAR(50) DEFAULT 'BB84',
  key_material TEXT NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP,
  metadata TEXT
);
```

## Deployment Architecture

### Cloud Deployment (AWS Example)
```
┌─────────────────────────────────────────────────┐
│              CloudFront CDN                      │
│        (Static assets distribution)              │
└──────────────────┬────────────────────────────────┘
                   │
┌──────────────────┴────────────────────────────────┐
│         Application Load Balancer (ALB)           │
│          - HTTPS/WSS termination                  │
│          - Route optimization                     │
└──────────────────┬────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────┴──────┐    ┌─────────┴─────────┐
│ ECS Cluster  │    │  ECS Cluster      │
│ (Production) │    │  (Backup/DR)      │
└────┬─────────┘    └────────┬──────────┘
     │                       │
     └───────────┬───────────┘
                 │
        ┌────────┴─────────┐
        │                  │
    ┌───┴────────┐  ┌──────┴──────┐
    │ RDS Aurora │  │ ElastiCache │
    │ PostgreSQL │  │   Redis     │
    └────────────┘  └─────────────┘
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: quantum-chat-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: quantum-chat-api
  template:
    metadata:
      labels:
        app: quantum-chat-api
    spec:
      containers:
      - name: api
        image: quantum-chat:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: redis-config
              key: url
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

## Scalability Strategy

### Horizontal Scaling
- **API Servers**: Stateless FastAPI instances behind load balancer
- **Database**: PostgreSQL with read replicas
- **Cache**: Redis cluster with sentinel for HA
- **WebSocket**: Redis pub/sub for cross-instance communication

### Vertical Scaling
- Instance types for CPU/Memory requirements
- Connection pooling optimization
- Query optimization and caching

### Performance Optimization
- Database query indexing
- Redis caching for frequently accessed data
- Message batching
- Websocket frame compression

## Monitoring & Observability

### Metrics Collection
- Prometheus for metrics scraping
- Grafana for visualization
- Application Performance Monitoring (APM)

### Logging
- Centralized logging (ELK Stack / CloudWatch)
- Structured JSON logs
- Log levels: INFO, WARNING, ERROR, CRITICAL

### Health Checks
- `/health` endpoint for load balancer
- Database connectivity checks
- Redis connectivity checks
- Message queue health

## Security Best Practices

1. **Network Security**
   - TLS 1.3 for all connections
   - WSS (WebSocket Secure) for real-time communication
   - VPC isolation
   - Security groups for traffic control

2. **Data Security**
   - Encryption at rest (database)
   - Encryption in transit (TLS)
   - Encryption in application layer (AES-256)
   - Key rotation policies

3. **Application Security**
   - Input validation for all endpoints
   - SQL injection prevention (ORM)
   - CSRF protection
   - Rate limiting
   - Account lockout mechanisms

4. **Infrastructure Security**
   - Secrets management (AWS Secrets Manager)
   - IAM roles and policies
   - Regular security audits
   - Dependency scanning

## Disaster Recovery

### Backup Strategy
- Daily database snapshots
- Point-in-time recovery capability
- Cross-region replication
- Message queue persistence

### Recovery Time Objectives (RTO)
- Critical services: < 15 minutes
- Non-critical services: < 1 hour

### Recovery Point Objectives (RPO)
- Database: < 1 hour
- Messages: < 5 minutes
