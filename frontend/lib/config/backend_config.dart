/// Backend Configuration
/// Manages API endpoints and can be updated based on environment

class BackendConfig {
  /// Get API URL - can be updated for different environments
  static String get apiUrl {
    // For development: local backend
    const String devUrl = 'http://192.168.29.109:8000/api';
    
    // For production: Firebase or deployed backend
    const String prodUrl = 'http://192.168.29.109:8000/api';
    
    // Use development URL for now
    return devUrl;
  }

  /// Get WebSocket URL
  static String get wsUrl {
    // Development WebSocket URL
    const String devUrl = 'ws://192.168.29.109:8000/api/ws/chat';
    
    // Production WebSocket URL
    const String prodUrl = 'ws://192.168.29.109:8000/api/ws/chat';
    
    return devUrl;
  }

  /// Update API URL for production deployment
  static void setProductionUrl(String apiUrl, String wsUrl) {
    print('Backend API URL would be updated to: $apiUrl');
    print('WebSocket URL would be updated to: $wsUrl');
  }
}
