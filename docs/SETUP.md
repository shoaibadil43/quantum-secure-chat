"""
Setup and Getting Started Guide
"""

# Quantum Secure Chat - Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 18+ (for Flutter Web)
- Flutter SDK 3.0+ (for mobile app)
- Docker & Docker Compose (optional)
- Git

## Quick Start with Docker

### 1. Clone Repository
```bash
git clone <repository-url>
cd quantum-secure-chat
```

### 2. Configure Environment
```bash
cp backend/.env.example backend/.env

# Edit backend/.env with your settings
# At minimum, update:
# - SECRET_KEY
# - MASTER_KEY
# - DATABASE_URL
```

### 3. Start Services
```bash
docker-compose up -d

# Verify services running
docker-compose ps
```

### 4. Access Application
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

---

## Manual Setup (Without Docker)

### Backend Setup

#### 1. Create Python Virtual Environment
```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Configure Environment
```bash
cp .env.example .env

# Edit .env and set:
# - DATABASE_URL (PostgreSQL)
# - REDIS_URL (Redis)
# - SECRET_KEY (JWT secret)
# - MASTER_KEY (Encryption key)
```

#### 4. Setup Database
```bash
# Install PostgreSQL if not present
# Create database:
createdb quantum_chat

# Run migrations (if using Alembic)
# alembic upgrade head
```

#### 5. Start Redis
```bash
# On Windows with WSL:
wsl redis-server

# On macOS:
brew services start redis

# On Linux:
sudo systemctl start redis-server
```

#### 6. Run Backend Server
```bash
python -m app.main

# Server should be available at http://localhost:8000
```

---

### Frontend Setup (Flutter)

#### 1. Install Flutter Dependencies
```bash
cd frontend
flutter pub get
```

#### 2. Run App
```bash
# Development
flutter run -d chrome  # For web
flutter run -d emulator  # For Android emulator
flutter run -d ios  # For iOS (macOS only)
```

#### 3. Build Release
```bash
# Android APK
flutter build apk --release

# iOS IPA
flutter build ipa

# Web
flutter build web
```

---

### Mobile App Setup

#### Android

1. Install Android SDK 21+
2. Configure Android emulator
3. Run app:
   ```bash
   flutter run
   ```

#### iOS (macOS only)

1. Install Xcode and Command Line Tools
2. Install CocoaPods:
   ```bash
   sudo gem install cocoapods
   ```
3. Run app:
   ```bash
   flutter run
   ```

#### Web

1. Install Chrome browser
2. Run app:
   ```bash
   flutter run -d chrome
   ```

---

## Testing

### Backend Tests
```bash
# Unit tests
python -m pytest app/tests/

# Specific test file
python -m pytest app/tests/test_bb84.py -v

# Coverage report
python -m pytest --cov=app app/tests/
```

### Frontend Tests
```bash
# Unit tests
flutter test

# Integration tests
flutter test integration_test/
```

---

## API Usage Examples

### Authentication

#### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Generate Quantum Key
```bash
curl -X POST http://localhost:8000/api/ws/generate-key/room_123 \
  -H "Authorization: Bearer <your-token>"
```

### WebSocket Connection (Node.js example)
```javascript
const WebSocket = require('ws');
const token = 'your-access-token';
const roomId = 'room_123';

const ws = new WebSocket(
  `ws://localhost:8000/api/ws/chat/${roomId}?token=${token}`
);

ws.on('open', () => {
  console.log('Connected');
  ws.send(JSON.stringify({
    type: 'message',
    content: 'Hello everyone!'
  }));
});

ws.on('message', (data) => {
  console.log('Received:', JSON.parse(data));
});
```

---

## Database Setup

### PostgreSQL

#### Windows
1. Download PostgreSQL installer from https://www.postgresql.org/download/windows/
2. Run installer with default settings
3. Remember the password you set

#### macOS
```bash
brew install postgresql
brew services start postgresql
```

#### Linux
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### Create Database
```bash
psql -U postgres
CREATE USER quantum_user WITH PASSWORD 'quantum_pass';
CREATE DATABASE quantum_chat OWNER quantum_user;
```

---

## Redis Setup

### Installation

#### Windows
Download from: https://github.com/microsoftarchive/redis/releases

#### macOS
```bash
brew install redis
brew services start redis
```

#### Linux
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

---

## Configuration Guide

### Backend Configuration (.env)

```env
# Server
DEBUG=False
APP_VERSION=1.0.0

# Database
DATABASE_URL=postgresql://quantum_user:quantum_pass@localhost:5432/quantum_chat

# Redis
REDIS_URL=redis://localhost:6379

# JWT Security
SECRET_KEY=your-super-secret-key-min-32-chars-required
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Encryption Master Key (32 bytes base64)
MASTER_KEY=base64-encoded-32-byte-key

# BB84 Configuration
BB84_QUBIT_COUNT=4096
BB84_ERROR_THRESHOLD=0.11
BB84_SIFT_RATIO=0.5

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Security
MAX_FAILED_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=15
```

### Generate Secure Keys
```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate MASTER_KEY (base64 encoded)
python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"
```

---

## Troubleshooting

### Database Connection Error
```
Error: could not translate host name "postgres" to address
```
**Solution**: Ensure PostgreSQL is running and connection string is correct.

### Redis Connection Error
```
Error: Connection refused at 127.0.0.1:6379
```
**Solution**: Start Redis server:
```bash
redis-server  # macOS/Linux
redis-cli     # Windows
```

### WebSocket Connection Failed
**Solution**: 
- Check token is valid
- Verify room ID exists
- Check firewall/network settings

### Migration Errors
```
Error: relation "users" already exists
```
**Solution**: Drop and recreate database:
```bash
dropdb quantum_chat
createdb quantum_chat
# Then restart backend
```

---

## Performance Tuning

### Database
- Enable connection pooling: `pool_size=20, max_overflow=0`
- Create indexes on frequently queried columns
- Use prepared statements

### Redis
- Enable persistence: `appendonly yes`
- Set appropriate eviction policy: `maxmemory-policy allkeys-lru`

### Backend
- Enable gzip compression
- Use async/await throughout
- Implement caching for frequently accessed data

---

## Production Deployment

### Pre-deployment Checklist
- [ ] Update SECRET_KEY and MASTER_KEY
- [ ] Configure PostgreSQL with backups
- [ ] Setup Redis with persistence
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Setup monitoring and logging
- [ ] Implement rate limiting
- [ ] Setup CI/CD pipeline

### AWS Deployment
```bash
# Push image to ECR
aws ecr get-login-password | docker login ...
docker tag quantum-chat:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/quantum-chat:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/quantum-chat:latest

# Deploy to ECS
aws ecs create-service ...
```

### Kubernetes Deployment
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

---

## Monitoring

### Application Logs
```bash
# Backend logs
docker logs quantum-chat-api -f

# Frontend logs
docker logs quantum-chat-frontend -f
```

### Health Checks
```bash
# API health
curl http://localhost:8000/health

# Database
curl http://localhost:8000/api/users/me -H "Authorization: Bearer {token}"
```

### Metrics
- Access metrics at: http://localhost:8000/metrics (if Prometheus enabled)
- Monitor with Grafana dashboard

---

For more information, see:
- [Architecture Documentation](./ARCHITECTURE.md)
- [API Documentation](./API_DOCUMENTATION.md)
- [Security Threat Model](./SECURITY_THREAT_MODEL.md)
- [Database Schema](./DATABASE_SCHEMA.md)
