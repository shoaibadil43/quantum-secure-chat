import json
from firebase_functions import https_fn, options
from firebase_admin import initialize_app, firestore, auth
import bcrypt
from cryptography.fernet import Fernet
import secrets
import uuid
from datetime import datetime
import base64

# Initialize Firebase
initialize_app()
db = firestore.client()

# Encryption setup
MASTER_KEY = secrets.token_bytes(32)
cipher = Fernet(base64.urlsafe_b64encode(MASTER_KEY))

# CORS options
cors_options = options.CorsOptions(
    cors_origins=["*"],  # Update with your frontend URL
    cors_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
)

# Helper functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data: str) -> str:
    return cipher.decrypt(data.encode()).decode()

# API Routes
@https_fn.on_request(cors=cors_options)
def api(req: https_fn.Request) -> https_fn.Response:
    """Main API handler for Firebase Functions"""

    # Handle CORS preflight
    if req.method == "OPTIONS":
        return https_fn.Response("", status=204, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        })

    try:
        # Parse request
        path = req.path.strip("/")
        method = req.method

        # Route handling
        if path == "auth/register" and method == "POST":
            return register_user(req)
        elif path == "auth/login" and method == "POST":
            return login_user(req)
        elif path.startswith("users/") and method == "GET":
            return get_user(req, path.split("/")[-1])
        elif path == "messages" and method == "GET":
            return get_messages(req)
        elif path.startswith("messages/") and method == "POST":
            return send_message(req, path.split("/")[-1])
        else:
            return https_fn.Response(
                json.dumps({"error": "Endpoint not found"}),
                status=404,
                content_type="application/json"
            )

    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=500,
            content_type="application/json"
        )

def register_user(req: https_fn.Request) -> https_fn.Response:
    """Register a new user"""
    try:
        data = json.loads(req.data.decode())

        # Validate required fields
        if not all(k in data for k in ["username", "email", "password"]):
            return https_fn.Response(
                json.dumps({"error": "Missing required fields"}),
                status=400,
                content_type="application/json"
            )

        # Check if user exists
        existing = db.collection('users').where('email', '==', data['email']).get()
        if existing:
            return https_fn.Response(
                json.dumps({"error": "User already exists"}),
                status=400,
                content_type="application/json"
            )

        # Create user
        user_id = str(uuid.uuid4())
        user_data = {
            'id': user_id,
            'username': data['username'],
            'email': data['email'],
            'hashed_password': hash_password(data['password']),
            'created_at': datetime.utcnow().isoformat(),
        }

        db.collection('users').document(user_id).set(user_data)

        return https_fn.Response(
            json.dumps({"message": "User created successfully", "user_id": user_id}),
            status=201,
            content_type="application/json"
        )

    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=500,
            content_type="application/json"
        )

def login_user(req: https_fn.Request) -> https_fn.Response:
    """Authenticate user"""
    try:
        data = json.loads(req.data.decode())

        # Find user
        users = db.collection('users').where('email', '==', data['email']).get()

        if not users:
            return https_fn.Response(
                json.dumps({"error": "Invalid credentials"}),
                status=401,
                content_type="application/json"
            )

        user = users[0].to_dict()

        # Verify password
        if not verify_password(data['password'], user['hashed_password']):
            return https_fn.Response(
                json.dumps({"error": "Invalid credentials"}),
                status=401,
                content_type="application/json"
            )

        # Generate simple token (in production, use proper JWT)
        token = str(uuid.uuid4())

        return https_fn.Response(
            json.dumps({
                "access_token": token,
                "token_type": "bearer",
                "user": {
                    "id": user['id'],
                    "username": user['username'],
                    "email": user['email']
                }
            }),
            status=200,
            content_type="application/json"
        )

    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=500,
            content_type="application/json"
        )

def get_user(req: https_fn.Request, user_id: str) -> https_fn.Response:
    """Get user information"""
    try:
        user = db.collection('users').document(user_id).get()

        if not user.exists:
            return https_fn.Response(
                json.dumps({"error": "User not found"}),
                status=404,
                content_type="application/json"
            )

        user_data = user.to_dict()
        # Remove sensitive data
        user_data.pop('hashed_password', None)

        return https_fn.Response(
            json.dumps(user_data),
            status=200,
            content_type="application/json"
        )

    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=500,
            content_type="application/json"
        )

def get_messages(req: https_fn.Request) -> https_fn.Response:
    """Get messages for a room"""
    try:
        room_id = req.args.get('room_id')
        if not room_id:
            return https_fn.Response(
                json.dumps({"error": "room_id required"}),
                status=400,
                content_type="application/json"
            )

        messages = db.collection('rooms').document(room_id).collection('messages')\
                    .order_by('timestamp').get()

        messages_data = []
        for msg in messages:
            msg_data = msg.to_dict()
            messages_data.append(msg_data)

        return https_fn.Response(
            json.dumps(messages_data),
            status=200,
            content_type="application/json"
        )

    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=500,
            content_type="application/json"
        )

def send_message(req: https_fn.Request, room_id: str) -> https_fn.Response:
    """Send a message to a room"""
    try:
        data = json.loads(req.data.decode())

        message_data = {
            'id': str(uuid.uuid4()),
            'room_id': room_id,
            'sender_id': data['sender_id'],
            'content': encrypt_data(data['content']),  # Encrypt message
            'timestamp': datetime.utcnow().isoformat(),
            'message_type': data.get('message_type', 'text')
        }

        # Save to Firestore
        db.collection('rooms').document(room_id).collection('messages')\
          .document(message_data['id']).set(message_data)

        return https_fn.Response(
            json.dumps({"message": "Message sent", "message_id": message_data['id']}),
            status=201,
            content_type="application/json"
        )

    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=500,
            content_type="application/json"
        )