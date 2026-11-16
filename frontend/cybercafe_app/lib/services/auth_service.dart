
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthService {
  static const String baseUrl = 'http://127.0.0.1:8000/api';

  static const storage = FlutterSecureStorage();

  static Future<void> login(
    String username,
    String password,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'password': password,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Нэвтрэх нэр эсвэл нууц үг буруу');
    }

    final data = jsonDecode(response.body);

    await storage.write(
      key: 'access',
      value: data['access'],
    );

    await storage.write(
      key: 'refresh',
      value: data['refresh'],
    );
  }

  static Future<void> register({
    required String username,
    required String email,
    required String password,
    required String phone,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/register/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'email': email,
        'password': password,
        'phone': phone,
      }),
    );

    if (response.statusCode != 201) {
      throw Exception('Бүртгэл амжилтгүй: ${response.body}');
    }

    final data = jsonDecode(response.body);

    await storage.write(
      key: 'access',
      value: data['access'],
    );

    await storage.write(
      key: 'refresh',
      value: data['refresh'],
    );
  }

  static Future<Map<String, dynamic>> getProfile() async {
    final token = await storage.read(key: 'access');

    if (token == null) {
      throw Exception('Нэвтрээгүй байна');
    }

    final response = await http.get(
      Uri.parse('$baseUrl/profile/'),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode != 200) {
      throw Exception('Профайл авахад алдаа гарлаа');
    }

    return jsonDecode(response.body);
  }

  static Future<bool> isLoggedIn() async {
    final token = await storage.read(key: 'access');
    return token != null;
  }

  static Future<void> logout() async {
    await storage.delete(key: 'access');
    await storage.delete(key: 'refresh');
  }
}
