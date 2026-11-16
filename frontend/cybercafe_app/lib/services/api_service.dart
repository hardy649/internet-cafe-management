
import 'dart:convert';
import 'package:http/http.dart' as http;

import '../models/computer.dart';
import 'auth_service.dart';

class ApiService {
  static const String baseUrl =
      'http://127.0.0.1:8000/api';

  static Future<List<Computer>> getComputers() async {
    final token = await AuthService.storage.read(
      key: 'access',
    );

    if (token == null) {
      throw Exception('Эхлээд нэвтэрнэ үү');
    }

    final response = await http.get(
      Uri.parse('$baseUrl/computers/'),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 401) {
      throw Exception(
        'Нэвтрэх хугацаа дууссан. Дахин нэвтэрнэ үү.',
      );
    }

    if (response.statusCode != 200) {
      throw Exception(
        'Компьютерийн мэдээлэл авахад алдаа гарлаа: '
        '${response.statusCode}',
      );
    }

    final List<dynamic> data = jsonDecode(response.body);

    return data
        .map((item) => Computer.fromJson(item))
        .toList();
  }
}
