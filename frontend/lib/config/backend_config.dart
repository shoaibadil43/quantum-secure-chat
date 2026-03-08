/// Backend Configuration
/// Manages API endpoints and can be updated based on environment

class BackendConfig {
  /// Get API URL - can be updated for different environments
  /// 
  /// For development: Uses local PC IP (192.168.29.109:8000)
  /// For production: Use your deployed backend URL
  /// 
  /// To change: Update the URL below or set via environment variable during build
  static String get apiUrl {
    // Development URL
    const String devUrl = 'http://192.168.29.109:8000/api';
    
    // Production URL - Replace with your actual deployed backend
    // When you deploy, update this to your Render/Railway URL
    const String prodUrl = 'https://your-backend-url.onrender.com/api';
    
    // Check if running in production environment
    // For now, we'll use the dev URL
    // In production, you would set this via environment variable
    return devUrl;
  }

  static String get wsUrl {
    // Development WebSocket URL
    const String devUrl = 'ws://192.168.29.109:8000/api/ws/chat';
    
    // Production WebSocket URL (use wss:// for HTTPS)
    // When you deploy, update this to your Render/Railway URL
    const String prodUrl = 'wss://your-backend-url.onrender.com/api/ws/chat';
    
    return devUrl;
  }

  /// Update API URL for production deployment
  /// Call this method after deployment to change the API endpoint
  static void setProductionUrl(String apiUrl, String wsUrl) {
    print('Backend API URL would be updated to: $apiUrl');
    print('This is where you would implement runtime configuration');
  }
}
