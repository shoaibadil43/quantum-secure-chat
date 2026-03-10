/// Backend Configuration
/// Manages API endpoints and can be updated based on environment

class BackendConfig {
  /// Get API URL - can be updated for different environments
  static String get apiUrl {
    // For production: Use Render backend
    const String prodUrl = 'https://quantum-secure-chat-backend.onrender.com/api';
    
    // For development: local backend
    const String devUrl = 'http://192.168.29.109:8000/api';
    
    // Use production URL (change to devUrl during development)
    return prodUrl;
  }

  /// Get WebSocket URL
  static String get wsUrl {
    // Production WebSocket URL
    const String prodUrl = 'wss://quantum-secure-chat-backend.onrender.com/api/ws/chat';
    
    // Development WebSocket URL
    const String devUrl = 'ws://192.168.29.109:8000/api/ws/chat';
    
    return prodUrl;
  }

  /// Update API URL for production deployment
  static void setProductionUrl(String apiUrl, String wsUrl) {
    print('Backend API URL would be updated to: $apiUrl');
    print('WebSocket URL would be updated to: $wsUrl');
  }
}
