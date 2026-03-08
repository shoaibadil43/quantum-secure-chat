/// Application Constants
class AppConstants {
  // API Configuration
  static const String baseUrl = 'http://localhost:8000/api';
  static const String wsBaseUrl = 'ws://localhost:8000/api/ws';
  
  // API Endpoints
  static const String authRegister = '/auth/register';
  static const String authLogin = '/auth/login';
  static const String authRefresh = '/auth/refresh';
  static const String usersMe = '/users/me';
  static const String usersById = '/users';
  static const String messagesList = '/messages';
  static const String generateKey = '/ws/generate-key';
  
  // WebSocket
  static const String chatEndpoint = '/chat';
  static const int wsReconnectDelay = 3000; // ms
  static const int wsMaxReconnectAttempts = 10;
  
  // Storage Keys
  static const String storageKeyToken = 'access_token';
  static const String storageKeyRefreshToken = 'refresh_token';
  static const String storageKeyUser = 'user_data';
  static const String storageKeyTheme = 'theme_mode';
  
  // Message Constraints
  static const int maxMessageLength = 4096;
  static const int maxUsernameLength = 255;
  static const int minPasswordLength = 12;
  
  // UI Configuration
  static const Duration animationDuration = Duration(milliseconds: 300);
  static const double defaultPadding = 16.0;
  static const double defaultBorderRadius = 12.0;
  static const double smallBorderRadius = 8.0;
  
  // Timeouts
  static const Duration apiTimeout = Duration(seconds: 30);
  static const Duration dbTimeout = Duration(seconds: 10);
  
  // Pagination
  static const int pageSize = 50;
  static const int initialMessageCount = 20;
}

/// Default Configuration
class AppConfig {
  static const String appName = 'Quantum Secure Chat';
  static const String appVersion = '1.0.0';
  static const bool debugMode = true;
  static const bool enableLogging = true;
}
