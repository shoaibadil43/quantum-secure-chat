"""
API Documentation
"""

# Quantum Secure Chat - API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
All endpoints (except /auth/*) require a valid JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### POST /auth/register
Register a new user account.

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-string",
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-02-26T12:00:00Z"
}
```

**Error (400 Bad Request):**
```json
{
  "detail": "Invalid email format" | "Username must be 3+ characters" | "Password not strong enough"
}
```

---

### POST /auth/login
Authenticate user and receive tokens.

**Request:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Error (401 Unauthorized):**
```json
{
  "detail": "Invalid credentials"
}
```

---

### POST /auth/refresh
Refresh expired access token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

## User Endpoints

### GET /users/me
Get current user profile.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "avatar_url": "https://...",
  "is_active": true,
  "created_at": "2024-02-26T12:00:00Z"
}
```

---

### GET /users/{user_id}
Get user by ID.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "id": "user-id",
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-02-26T12:00:00Z"
}
```

---

### GET /users
List all active users.

**Authentication:** Required

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 50, max: 100)

**Response (200 OK):**
```json
[
  {
    "id": "uuid-string",
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2024-02-26T12:00:00Z"
  }
]
```

---

## Message Endpoints

### GET /messages/session/{session_id}
Get messages from a chat session.

**Authentication:** Required

**Query Parameters:**
- `skip`: Number of messages to skip (default: 0)
- `limit`: Number of messages to return (default: 50)

**Response (200 OK):**
```json
[
  {
    "id": "message-id",
    "sender_id": "user-id",
    "session_id": "session-id",
    "content": "Hello everyone!",
    "encrypted_content": "encrypted-blob",
    "is_delivered": true,
    "is_read": true,
    "created_at": "2024-02-26T12:00:00Z"
  }
]
```

---

### POST /messages/{message_id}/read
Mark message as read.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "status": "marked_read"
}
```

---

### DELETE /messages/{message_id}
Delete a message (sender only).

**Authentication:** Required

**Response (200 OK):**
```json
{
  "status": "deleted"
}
```

---

## WebSocket Endpoints

### WS /ws/chat/{room_id}?token={access_token}
WebSocket connection for real-time chat.

**Authentication:** Required (via query parameter)

**Message Types Sent:**

**Message:**
```json
{
  "type": "message",
  "content": "Hello there!"
}
```

**Typing Indicator:**
```json
{
  "type": "typing"
}
```

**Stop Typing:**
```json
{
  "type": "stop_typing"
}
```

**Received Messages:**

**New Message:**
```json
{
  "type": "message",
  "message_id": "msg-id",
  "sender_id": "user-id",
  "username": "john_doe",
  "content": "Hello there!",
  "timestamp": "2024-02-26T12:00:00Z"
}
```

**User Joined:**
```json
{
  "type": "user_joined",
  "user_id": "user-id",
  "username": "john_doe",
  "timestamp": "2024-02-26T12:00:00Z"
}
```

**User Left:**
```json
{
  "type": "user_left",
  "user_id": "user-id",
  "username": "john_doe",
  "timestamp": "2024-02-26T12:00:00Z"
}
```

**User Typing:**
```json
{
  "type": "typing",
  "user_id": "user-id",
  "username": "john_doe"
}
```

**Stop Typing:**
```json
{
  "type": "stop_typing",
  "user_id": "user-id"
}
```

---

### POST /ws/generate-key/{room_id}
Generate BB84 quantum key for a room.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "status": "success",
  "key_generated": true,
  "key_length": 512,
  "qber": 0.0087,
  "security_message": "Secure - No eavesdropping detected"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Rate limits are enforced on all endpoints:
- **Authentication endpoints**: 5 requests per minute
- **Other endpoints**: 100 requests per minute

Headers returned:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1708940460
```

---

## WebSocket Connection Example (JavaScript)

```javascript
const token = 'your-access-token';
const roomId = 'room-123';
const ws = new WebSocket(`ws://localhost:8000/api/ws/chat/${roomId}?token=${token}`);

ws.onopen = () => {
  console.log('Connected');
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Received:', message);
};

ws.onerror = (error) => {
  console.error('Error:', error);
};

// Send message
ws.send(JSON.stringify({
  type: 'message',
  content: 'Hello!'
}));

// Send typing indicator
ws.send(JSON.stringify({
  type: 'typing'
}));
```

---

## Common Use Cases

### Complete Signup Flow
1. `POST /auth/register` - Register user
2. `POST /auth/login` - Login user
3. Store access_token and refresh_token
4. Use access_token in Authorization header

### Sending a Message
1. `WS /ws/chat/{room_id}` - Connect to room
2. Send message via WebSocket
3. `POST /messages/{message_id}/read` - Mark as read

### Generating Quantum Key
1. `POST /ws/generate-key/{room_id}` - Generate key
2. Use returned key for AES-256 encryption
3. Send encrypted messages via WebSocket

---

## Versioning

Current API Version: `1.0.0`

Future changes will maintain backward compatibility within major versions.
