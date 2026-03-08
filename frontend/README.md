# Flutter Frontend - Quantum Secure Chat

Cross-platform Flutter UI for quantum-secure chat application.

## Directory Structure

```
frontend/
├── lib/
│   ├── main.dart               # App entry point
│   ├── config/
│   │   ├── app_config.dart    # Theme configuration
│   │   ├── colors.dart         # Color palette
│   │   └── constants.dart      # App constants
│   ├── models/
│   │   ├── user.dart           # User data model
│   │   ├── message.dart        # Message model
│   │   └── chat.dart           # Chat session model
│   ├── screens/
│   │   ├── auth/
│   │   │   ├── login_screen.dart
│   │   │   └── signup_screen.dart
│   │   ├── chat/
│   │   │   ├── chat_list_screen.dart
│   │   │   └── conversation_screen.dart
│   │   └── widgets/
│   │       ├── message_bubble.dart
│   │       ├── typing_indicator.dart
│   │       ├── message_input.dart
│   │       └── app_drawer.dart
│   └── services/
│       ├── api_service.dart    # HTTP API client
│       ├── encryption_service.dart
│       └── websocket_service.dart
├── pubspec.yaml                # Dependencies
├── pubspec.lock
└── README.md
```

## Features

### UI Components
- **Authentication Screens**: Login & Sign-up with validation
- **Chat List**: List of all conversations
- **Conversation Screen**: Real-time messaging interface
- **Message Bubbles**: User-friendly message display
- **Typing Indicator**: Shows when other user is typing
- **Message Input**: Rich text input with emoji support

### State Management
- **Provider**: For simple state management
- **Riverpod**: Alternative for more complex scenarios

### Real-time Communication
- **WebSocket**: Live message synchronization
- **Message Queue**: Offline message handling
- **Typing Indicators**: Real-time typing notification

### Security Features
- **Secure Storage**: Encrypted key storage
- **Local Encryption**: Flutter secure storage for tokens
- **BB84 Integration**: Support for quantum keys
- **AES-256**: Client-side message encryption

### User Experience
- **Dark Mode**: Full dark theme support
- **Material Design 3**: Modern UI components
- **Animations**: Smooth transitions and interactions
- **Offline Support**: Message caching and sync

## Setup & Installation

```bash
# Install dependencies
flutter pub get

# Run app
flutter run

# Build release
flutter build apk      # Android
flutter build ipa      # iOS
flutter build web      # Web
```

## Usage

### Authentication
```dart
// Login
await apiService.login(email: 'user@example.com', password: 'pass');

// Register
await apiService.register(
  username: 'john_doe',
  email: 'john@example.com',
  password: 'SecurePass123!'
);
```

### Real-time Chat
```dart
// Connect to chat room
await wsService.connect(roomId, token);

// Send message
await wsService.sendMessage(content, encryptionKeyId);

// Listen to messages
wsService.onMessage.listen((message) {
  // Update UI with message
});
```

### Encryption
```dart
// Generate BB84 key
final key = await encryptionService.generateBB84Key();

// Encrypt message
final encrypted = await encryptionService.encryptAES256(message, key);

// Decrypt message
final decrypted = await encryptionService.decryptAES256(encrypted, key);
```

## Architecture

### MVVM Pattern
- **Models**: Data classes (User, Message, ChatSession)
- **Views**: UI screens and widgets
- **ViewModels**: Business logic providers

### Service Layer
- **APIService**: HTTP client for REST endpoints
- **WebSocketService**: Real-time communication
- **EncryptionService**: Cryptographic operations
- **StorageService**: Local data persistence

## Testing

```bash
# Run unit tests
flutter test

# Run integration tests
flutter test integration_test/
```

## Performance Optimization

- ImageCaching for network images
- ListView builder for large lists
- Pagination for message history
- Connection pooling for WebSocket
- Local caching with hive/sqflite

## Future Enhancements

- Video/Audio calls
- File sharing
- Voice messages
- Message reactions
- Read receipts improvement
- Group chat management
- User profiles & status
- Message search
- Backup & restore
