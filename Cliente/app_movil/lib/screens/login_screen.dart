import 'package:flutter/material.dart';
import '../constants.dart';
import '../services/api_service.dart';
import 'home_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _ipController = TextEditingController();
  final TextEditingController _cedulaController = TextEditingController();
  final TextEditingController _passController = TextEditingController();
  final ApiService _api = ApiService();
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _cargarIpGuardada();
  }

  void _cargarIpGuardada() async {
    final ipGuardada = await _api.loadBaseUrl();
    if (ipGuardada != null && ipGuardada.isNotEmpty) {
      _ipController.text = ipGuardada;
    }
  }

  void _iniciarSesion() async {
    if (_ipController.text.isEmpty || _cedulaController.text.isEmpty) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Faltan datos")));
      return;
    }

    setState(() => _isLoading = true);

    // 1. Guardar IP (IMPORTANTE: Usamos trim() para quitar espacios)
    await _api.setServerIp(_ipController.text.trim());

    // 2. Login
    var resultado = await _api.login(
      _cedulaController.text.trim(),
      _passController.text.trim(),
    );

    setState(() => _isLoading = false);

    if (resultado.containsKey("id")) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => HomeScreen(usuario: resultado)),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(resultado["error"] ?? "Error desconocido"),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Center(
          child: SingleChildScrollView(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.lock_person, size: 80, color: kNavyBlue),
                SizedBox(height: 20),
                Text(
                  "SIGEP MÓVIL",
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: kNavyBlue,
                  ),
                ),
                SizedBox(height: 40),

                TextField(
                  controller: _ipController,
                  decoration: InputDecoration(
                    labelText: "IP del Servidor (Ver en PC)",
                    hintText: "Ej: 192.168.1.15",
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.wifi),
                  ),
                ),
                SizedBox(height: 15),

                TextField(
                  controller: _cedulaController,
                  keyboardType: TextInputType.number,
                  decoration: InputDecoration(
                    labelText: "Cédula",
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.person),
                  ),
                ),
                SizedBox(height: 15),

                TextField(
                  controller: _passController,
                  obscureText: true,
                  decoration: InputDecoration(
                    labelText: "Contraseña",
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.key),
                  ),
                ),
                SizedBox(height: 30),

                _isLoading
                    ? CircularProgressIndicator()
                    : ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: kNavyBlue,
                          minimumSize: Size(double.infinity, 50),
                        ),
                        onPressed: _iniciarSesion,
                        child: Text(
                          "INGRESAR",
                          style: TextStyle(color: Colors.white, fontSize: 16),
                        ),
                      ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
