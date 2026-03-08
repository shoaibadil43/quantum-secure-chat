# Quantum Secure Chat - Backend

Fast API backend for quantum-secure chat application with BB84 quantum key distribution.

## Directory Structure

```
backend/
├── app/
│   ├── auth/                    # Authentication module
│   │   ├── jwt_handler.py      # JWT token management
│   │   └── password_utils.py   # Password hashing & validation
│   ├── db/                      # Database module
│   │   ├── database.py         # SQLAlchemy setup & session management
│   │   └── schemas.py          # Pydantic validation schemas
│   ├── models/                  # SQLAlchemy ORM models
│   │   └── __init__.py         # User, Message, ChatSession models
│   ├── routes/                  # API routes
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── users.py            # User management endpoints
│   │   ├── messages.py         # Message endpoints
│   │   └── websocket.py        # WebSocket and real-time chat
│   ├── security/                # Security module
│   │   ├── bb84/               # BB84 quantum key distribution
│   │   │   ├── bb84.py         # BB84 protocol implementation
│   │   │   ├── key_sifting.py  # Key sifting and sacrifice
│   │   │   └── privacy_amplification.py
│   │   ├── encryption.py       # AES-256 encryption
│   │   └── redis_client.py     # Redis pub/sub & caching
│   ├── utils/                   # Utility functions
│   │   ├── logger.py           # Logging setup
│   │   └── validators.py       # Input validation
│   ├── tests/                   # Unit tests
│   ├── config.py               # Application configuration
│   ├── main.py                 # FastAPI app entry point
│   └── websocket_manager.py    # WebSocket connection management
├── requirements.txt            # Python dependencies
└── .env.example                # Example environment variables
```

## Features

- **BB84 Quantum Key Distribution**: Secure key exchange using quantum principles
- **AES-256 Encryption**: Military-grade message encryption
- **WebSocket Real-time Chat**: Live messaging with typing indicators
- **JWT Authentication**: Secure token-based authentication
- **Password Security**: Bcrypt hashing with strength requirements
- **Redis Pub/Sub**: Scalable message routing
- **Input Validation**: Comprehensive validation for all inputs
- **Database Persistence**: PostgreSQL with SQLAlchemy ORM
- **Error Handling**: Robust error handling and logging

## Setup & Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run database migrations (if applicable)
python -m alembic upgrade head

# Start server
python -m app.main
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token

### Users
- `GET /api/users/me` - Get current user profile
- `GET /api/users/{user_id}` - Get user by ID
- `GET /api/users` - List all users

### Messages
- `GET /api/messages/session/{session_id}` - Get session messages
- `POST /api/messages/{message_id}/read` - Mark as read
- `DELETE /api/messages/{message_id}` - Delete message

### WebSocket
- `WS /api/ws/chat/{room_id}` - Real-time chat
- `POST /api/ws/generate-key/{room_id}` - Generate BB84 key

## Configuration

Edit `.env` file for:
- Database URL
- Redis URL
- JWT secret key
- Encryption master key
- BB84 parameters
- CORS origins

## Testing

```bash
python -m pytest app/tests/
```

## Security Features

1. **Quantum Key Distribution (BB84)**
   - Theoretical immunity to eavesdropping
   - QBER (Quantum Bit Error Rate) monitoring
   - Key sifting and privacy amplification

2. **Encryption**
   - AES-256-CBC symmetric encryption
   - PBKDF2 key derivation from BB84 keys
   - Random IV generation

3. **Authentication**
   - JWT tokens with expiration
   - Bcrypt password hashing (rounds=12)
   - Account lockout after failed attempts

4. **Authorization**
   - Token-based access control
   - Room membership verification
   - User isolation

## Performance

- Async/await with FastAPI
- Connection pooling
- Redis caching
- Efficient WebSocket management
- Database indexing on key fields
