import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../config/backend_config.dart';

/// WebSocket Service
class WebSocketService {
  static String get _baseUrl => BackendConfig.wsUrl;

  WebSocket? _socket;

  Future<void> connect(String roomId, String token) async {
    final url = '$_baseUrl/$roomId?token=$token';

    _socket = await WebSocket.connect(url);

    print("WebSocket connected: $url");

    _socket!.listen(
      (message) {
        print("Received message: $message");
      },
      onDone: () {
        print("WebSocket closed");
      },
      onError: (error) {
        print("WebSocket error: $error");
      },
    );
  }

  void sendMessage(String message) {
    _socket?.add(message);
  }

  Future<void> disconnect() async {
    await _socket?.close();
  }
}

/// API Service
class APIService {
  static String get _baseUrl => BackendConfig.apiUrl;
  static String? _authToken;

  /// Set auth token after login
  static void setAuthToken(String token) {
    _authToken = token;
  }

  /// Get auth token
  static String? getAuthToken() {
    return _authToken;
  }

  /// Register a new user
  Future<Map<String, dynamic>> register({
    required String username,
    required String email,
    required String password,
  }) async {
    try {
      final response = await http.post(
        Uri.parse("$_baseUrl/auth/register"),
        headers: {
          "Content-Type": "application/json",
        },
        body: jsonEncode({
          "username": username,
          "email": email,
          "password": password,
        }),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        return jsonDecode(response.body);
      } else {
        final errorBody = jsonDecode(response.body);
        throw Exception(errorBody['detail'] ?? 'Registration failed');
      }
    } catch (e) {
      throw Exception('Registration error: $e');
    }
  }

  /// Login user and get token
  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await http.post(
        Uri.parse("$_baseUrl/auth/login"),
        headers: {
          "Content-Type": "application/json",
        },
        body: jsonEncode({
          "email": email,
          "password": password,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _authToken = data['access_token'];
        return data;
      } else {
        final errorBody = jsonDecode(response.body);
        throw Exception(errorBody['detail'] ?? 'Login failed');
      }
    } catch (e) {
      throw Exception('Login error: $e');
    }
  }

  /// Get current user profile
  Future<Map<String, dynamic>> getCurrentUser() async {
    if (_authToken == null) {
      throw Exception('Not authenticated');
    }

    try {
      final response = await http.get(
        Uri.parse("$_baseUrl/users/me"),
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $_authToken",
        },
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get user profile');
      }
    } catch (e) {
      throw Exception('Get user error: $e');
    }
  }

  /// Get list of all users
  Future<List<Map<String, dynamic>>> getUsers({int skip = 0, int limit = 50}) async {
    try {
      final response = await http.get(
        Uri.parse("$_baseUrl/users?skip=$skip&limit=$limit"),
        headers: {
          "Content-Type": "application/json",
        },
      );

      if (response.statusCode == 200) {
        final List<dynamic> users = jsonDecode(response.body);
        return users.cast<Map<String, dynamic>>();
      } else {
        throw Exception('Failed to load users');
      }
    } catch (e) {
      throw Exception('Get users error: $e');
    }
  }

  /// Get specific user by ID
  Future<Map<String, dynamic>> getUser(String userId) async {
    try {
      final response = await http.get(
        Uri.parse("$_baseUrl/users/$userId"),
        headers: {
          "Content-Type": "application/json",
        },
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('User not found');
      }
    } catch (e) {
      throw Exception('Get user error: $e');
    }
  }

  /// Get messages for a conversation
  Future<List<dynamic>> getMessages(String sessionId) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/messages/$sessionId'),
      headers: {
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body) as List<dynamic>;
    } else {
      throw Exception('Failed to load messages: ${response.statusCode}');
    }
  }

  /// Logout user
  static void logout() {
    _authToken = null;
  }
}

/// Encryption Service
class EncryptionService {
  /// BB84 Quantum Key Distribution
  Future<String> generateBB84Key() async {
    // TODO: Implement BB84 protocol
    throw UnimplementedError();
  }

  /// AES-256 Encryption/Decryption
  Future<String> encryptAES256(String plaintext, String key) async {
    // TODO: Implement AES-256 encryption
    throw UnimplementedError();
  }

  Future<String> decryptAES256(String ciphertext, String key) async {
    // TODO: Implement AES-256 decryption
    throw UnimplementedError();
  }
}
