/// Backend Configuration
/// Manages API endpoints and can be updated based on environment

class BackendConfig {
  /// Get API URL - can be updated for different environments
  /// 
  /// For development: Uses local PC IP (192.168.29.109:8000)
  /// For production: Use your deployed Firebase Functions URL
  ///
  /// To change: Update the URL below or set via environment variable during build
  static String get apiUrl {
    // Development URL
    const String devUrl = 'http://192.168.29.109:8000/api';

    // Production URL - Firebase Functions
    // Replace 'your-project-id' with your actual Firebase project ID
    const String prodUrl = 'https://us-central1-quantum-secure-chat.cloudfunctions.net/api';

    // Check if running in production environment
    // For now, we'll use the prod URL for Firebase deployment
    return prodUrl;
    // Development WebSocket URL
    const String devUrl = 'ws://192.168.29.109:8000/api/ws/chat';
    
    // Production WebSocket URL (use wss:// for HTTPS)
    // Firebase Functions don't support WebSockets directly
    // For now, we'll use polling or Firebase Realtime Database
    const String prodUrl = 'wss://us-central1-quantum-secure-chat.cloudfunctions.net/ws';
    
    return prodUrl;
  }

  /// Update API URL for production deployment
  /// Call this method after deployment to change the API endpoint
  static void setProductionUrl(String apiUrl, String wsUrl) {
    print('Backend API URL would be updated to: $apiUrl');
    print('This is where you would implement runtime configuration');
  }
}
