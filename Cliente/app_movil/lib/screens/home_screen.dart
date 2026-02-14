import 'package:flutter/material.dart';
import 'package:flutter/services.dart'; // Necesario para errores de plataforma
import 'package:local_auth/local_auth.dart'; // <--- Importamos Seguridad
import '../services/api_service.dart';
import 'login_screen.dart';

class HomeScreen extends StatefulWidget {
  final Map<String, dynamic> usuario;

  HomeScreen({required this.usuario});

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ApiService _api = ApiService();
  final LocalAuthentication auth =
      LocalAuthentication(); // <--- Instancia de Seguridad

  Map<String, dynamic>? _detalle;
  bool _cargando = true;

  @override
  void initState() {
    super.initState();
    _cargarDatosCompletos();
  }

  void _cargarDatosCompletos() async {
    String cedula = widget.usuario['cedula'] ?? "1234";
    var datos = await _api.obtenerDetalle(cedula);

    if (mounted) {
      setState(() {
        _detalle = datos;
        _cargando = false;
      });
    }
  }

  // --- NUEVA FUNCIÓN CON SEGURIDAD ---
  void _intentarMarcarAsistencia() async {
    bool autenticado = false;

    try {
      // 1. Verificar si el celular puede usar biometría
      final bool puedeVerificar =
          await auth.canCheckBiometrics || await auth.isDeviceSupported();

      if (!puedeVerificar) {
        // Si el celular es muy viejo o no tiene seguridad configurada,
        // dejamos pasar o mostramos error (decisión tuya).
        // Aquí dejamos pasar para no bloquear, pero avisamos.
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              "⚠️ Dispositivo sin seguridad biométrica. Se marcará directo.",
            ),
          ),
        );
        autenticado = true;
      } else {
        // 2. Pedir Huella o PIN
        autenticado = await auth.authenticate(
          localizedReason:
              'Escanea tu huella o usa tu PIN para confirmar asistencia',
          options: const AuthenticationOptions(
            stickyAuth:
                true, // Mantiene la ventana abierta si la app se minimiza
            biometricOnly: false, // false = Permite PIN si falla la huella
          ),
        );
      }
    } on PlatformException catch (e) {
      print("Error de seguridad: $e");
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Error en seguridad: $e")));
      return;
    }

    // 3. Si pasó la seguridad, llamamos al servidor
    if (autenticado) {
      _enviarDatosAlServidor();
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("❌ Autenticación cancelada"),
          backgroundColor: Colors.orange,
        ),
      );
    }
  }

  void _enviarDatosAlServidor() async {
    String cedula = widget.usuario['cedula'] ?? "";

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text("📡 Conectando..."),
        duration: Duration(milliseconds: 500),
      ),
    );

    bool exito = await _api.marcarAsistencia(cedula);

    if (exito) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("✅ ASISTENCIA CONFIRMADA"),
          backgroundColor: Colors.green,
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("❌ Error de Conexión"),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Panel del Empleado"),
        backgroundColor: Colors.indigo,
        actions: [
          IconButton(
            icon: Icon(Icons.exit_to_app, color: Colors.white),
            onPressed: () {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(builder: (_) => LoginScreen()),
              );
            },
          ),
        ],
      ),
      body: _cargando
          ? Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Card(
                    color: Colors.indigo.shade50,
                    child: ListTile(
                      leading: CircleAvatar(
                        backgroundColor: Colors.indigo,
                        child: Icon(Icons.person, color: Colors.white),
                      ),
                      title: Text(
                        widget.usuario['nombre'] ?? "Empleado",
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: Text(widget.usuario['tipo'] ?? "Personal"),
                    ),
                  ),
                  SizedBox(height: 20),

                  // BOTÓN CON SEGURIDAD
                  Center(
                    child: ElevatedButton.icon(
                      onPressed:
                          _intentarMarcarAsistencia, // <--- CAMBIADO A LA NUEVA FUNCIÓN
                      icon: Icon(
                        Icons.fingerprint,
                        size: 40,
                        color: Colors.white,
                      ),
                      label: Text(
                        "MARCAR ASISTENCIA",
                        style: TextStyle(fontSize: 18, color: Colors.white),
                      ),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.green,
                        padding: EdgeInsets.symmetric(
                          horizontal: 40,
                          vertical: 20,
                        ),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(30),
                        ),
                      ),
                    ),
                  ),
                  SizedBox(height: 30),

                  Text(
                    "Mi Información",
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  Divider(),

                  if (_detalle != null && _detalle!.isNotEmpty) ...[
                    _buildInfoCard("📅 Horario & Académico", Icons.calendar_today, [
                      "Cargo: ${_detalle!['cargo']}",
                      "Horario: ${_detalle!['academico']['horario_horas'] ?? 'No definido'}",
                      "Materias: ${_detalle!['academico']['materias'] ?? 'N/A'}",
                    ]),
                  ] else
                    Text("No se pudo cargar la info detallada."),
                ],
              ),
            ),
    );
  }

  Widget _buildInfoCard(
    String titulo,
    IconData icono,
    List<String> lineas, {
    bool esNomina = false,
  }) {
    return Card(
      margin: EdgeInsets.symmetric(vertical: 10),
      elevation: 3,
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icono, color: Colors.indigo),
                SizedBox(width: 10),
                Text(
                  titulo,
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
              ],
            ),
            Divider(),
            ...lineas
                .map(
                  (l) => Padding(
                    padding: const EdgeInsets.symmetric(vertical: 4),
                    child: Text(
                      l,
                      style: TextStyle(
                        fontSize: 15,
                        fontWeight: esNomina && l.startsWith("TOTAL")
                            ? FontWeight.bold
                            : FontWeight.normal,
                        color: esNomina && l.startsWith("TOTAL")
                            ? Colors.green.shade800
                            : Colors.black87,
                      ),
                    ),
                  ),
                )
                .toList(),
          ],
        ),
      ),
    );
  }
}
