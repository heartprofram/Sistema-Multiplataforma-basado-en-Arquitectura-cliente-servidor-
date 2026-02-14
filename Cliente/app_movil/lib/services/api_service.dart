import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  String _baseUrl = "";

  // 1. Cargar la IP guardada en memoria
  Future<String?> loadBaseUrl() async {
    final prefs = await SharedPreferences.getInstance();
    String? ip = prefs.getString('server_ip');
    // Si hay IP guardada, la usamos. Si no, cadena vacía.
    _baseUrl = ip != null ? "http://$ip:8000" : "";
    return ip;
  }

  // 2. Guardar una nueva IP
  Future<void> setServerIp(String ip) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('server_ip', ip);
    _baseUrl = "http://$ip:8000";
  }

  // 3. Función de Login
  Future<Map<String, dynamic>> login(String cedula, String password) async {
    await loadBaseUrl(); // <--- OBLIGATORIO: Cargar IP antes de conectar

    if (_baseUrl.isEmpty) return {"error": "Configura la IP primero"};

    final url = Uri.parse('$_baseUrl/login');

    try {
      final response = await http
          .post(
            url,
            headers: {"Content-Type": "application/json"},
            body: jsonEncode({"cedula": cedula, "password": password}),
          )
          .timeout(Duration(seconds: 10)); // Timeout aumentado a 10s

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        return {"error": "Credenciales incorrectas"};
      }
    } catch (e) {
      if (e.toString().contains("Timeout")) {
        return {"error": "Tiempo de espera agotado. Verifica tu conexión."};
      }
      return {"error": "No conecta. Revisa IP y Firewall. ($e)"};
    }
  }

  // 4. Obtener Detalle del Empleado
  Future<Map<String, dynamic>> obtenerDetalle(String cedula) async {
    await loadBaseUrl(); // <--- OBLIGATORIO

    if (_baseUrl.isEmpty) return {};

    final url = Uri.parse('$_baseUrl/empleado/$cedula/detalle');
    try {
      final response = await http.get(url).timeout(Duration(seconds: 5));
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return {};
    } catch (e) {
      print("Error obteniendo detalle: $e");
      return {};
    }
  }

  // 5. Registrar Asistencia
  Future<bool> marcarAsistencia(String cedula) async {
    await loadBaseUrl(); // <--- OBLIGATORIO

    if (_baseUrl.isEmpty) return false;

    final url = Uri.parse('$_baseUrl/marcar_asistencia');
    try {
      final response = await http
          .post(
            url,
            headers: {"Content-Type": "application/json"},
            body: jsonEncode({"cedula": cedula}),
          )
          .timeout(Duration(seconds: 5));

      return response.statusCode == 200;
    } catch (e) {
      print("Error marcando: $e");
      return false;
    }
  }
}
