# Sistema Multiplataforma Basado en Arquitectura Cliente/Servidor (SIGEP)

![Version](https://img.shields.io/github/v/release/heartprofram/Sistema-Multiplataforma-basado-en-Arquitectura-cliente-servidor-?style=flat-square)
![License](https://img.shields.io/github/license/heartprofram/Sistema-Multiplataforma-basado-en-Arquitectura-cliente-servidor-?style=flat-square)
![Python](https://img.shields.io/badge/Backend-Python%20%7C%20FastAPI-blue?style=flat-square&logo=python)
![Flutter](https://img.shields.io/badge/Frontend-Flutter-02569B?style=flat-square&logo=flutter)

Este proyecto es un sistema integral diseñado para la gestión de talento humano (**SIGEP**). Opera bajo una arquitectura Cliente-Servidor segura y eficiente, ideal para entornos de Intranet corporativa o institucional.

---

## 📥 Descarga y Uso Inmediato

¿No quieres compilar el código? ¡No hay problema! Hemos generado los ejecutables listos para usar.

Puedes encontrar la última versión estable (**v1.0.0**) en nuestra sección de **Releases**:

[![Descargar v1.0.0](https://img.shields.io/badge/⬇️_Descargar_Ejecutables_(v1.0.0)-2ea44f?style=for-the-badge)](https://github.com/heartprofram/Sistema-Multiplataforma-basado-en-Arquitectura-cliente-servidor-/releases/tag/v1.0.0)

### 📦 Contenido de la descarga:
1.  **📱 Cliente Móvil (`.apk`):** Instálalo en cualquier dispositivo Android.
    * *Nota:* Asegúrate de estar conectado a la misma red Wi-Fi que el servidor.
2.  **💻 Servidor (`.zip` / `.exe`):** Descomprime y ejecuta `SIGEP_Server.exe` en Windows para iniciar el panel de control y la base de datos.

---

## 🏗️ Arquitectura del Sistema

El sistema se compone de dos módulos principales que se comunican entre sí:

* **🖥️ Servidor (Escritorio):** * Desarrollado en **Python**.
    * Usa **FastAPI** para el backend y **CustomTkinter** para la interfaz administrativa moderna.
    * Gestiona la base de datos SQLite y expone una API REST local.
* **📱 Cliente (Móvil):** * Desarrollado en **Flutter** (Dart).
    * Permite al personal interactuar con el sistema (consultas, marcar asistencia) mediante dispositivos Android.

## 🚀 Características Principales

### Servidor (Panel Administrativo)
* ✅ **Gestión de Personal:** CRUD completo de empleados, cargos y horarios.
* ✅ **Nómina:** Visualización detallada de datos personales y laborales.
* ✅ **Control de Asistencia:** Monitoreo en tiempo real de entradas y salidas.
* ✅ **Reportes y Estadísticas:** Cálculo de efectividad y generación de reportes en **Excel/PDF**.
* ✅ **API REST:** Servicio optimizado para conexión fluida con la app móvil.

### Cliente (App Móvil)
* ✅ **Autenticación Segura:** Inicio de sesión con soporte para biometría (huella/rostro).
* ✅ **Conexión Inteligente:** Detección automática de la IP del servidor.
* ✅ **Marcaje de Asistencia:** Registro de entrada/salida validado por red local.
* ✅ **Dashboard Personal:** Acceso a perfil, carga académica y recibos de pago.

## 📂 Estructura del Proyecto

```text
.
├── Cliente/          # Código fuente de la App Móvil (Flutter)
├── Servidor/         # Código fuente del Servidor (Python/FastAPI)
├── LICENSE           # Licencia Apache 2.0
├── README.md         # Documentación del proyecto
└── .gitignore        # Archivos ignorados por Git

## 🛠️ Requisitos e Instalación

### 1. Servidor (Python)

**Requisitos:**
*   Python 3.8 o superior.

**Instalación:**
1.  Navega a la carpeta del servidor:
    ```bash
    cd Servidor
    ```
2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Ejecuta la aplicación:
    ```bash
    python main.py
    ```

### 1. Generar Ejecutables (Windows/Linux)

El proyecto incluye un script de construcción (`setup_build.py`) para crear ejecutables independientes.

**Windows (.exe):**
1.  Asegúrate de tener instalado `cx_Freeze`:
    ```bash
    pip install cx_Freeze
    ```
2.  Ejecuta el script de construcción:
    ```bash
    cd Servidor
    python setup_build.py build
    ```
3.  El ejecutable se generará en la carpeta `build/exe.win-amd64-3.x/SIGEP_Server.exe`.

**Linux:**
1.  Copia el proyecto a tu entorno Linux.
2.  Instala las dependencias y `cx_Freeze`.
3.  Ejecuta el mismo comando:
    ```bash
    python setup_build.py build
    ```
4.  El ejecutable compilado para Linux aparecerá en la carpeta `build/exe.linux-x86_64-3.x/`.
5.  Para distribuir, puedes comprimir esta carpeta:
    ```bash
    tar -czvf SIGEP_Server_Linux.tar.gz -C build/exe.linux-x86_64-3.x .
    ```

**Requisitos:**
*   Flutter SDK instalado y configurado.
*   Dispositivo Android/iOS o Emulador.

**Instalación:**
1.  Navega a la carpeta del cliente:
    ```bash
    cd Cliente
    ```
2.  Obtén las dependencias:
    ```bash
    flutter pub get
    ```
3.  Ejecuta la aplicación:
    ```bash
    flutter run
    ```

## 📄 Licencia

Este proyecto está bajo la Licencia **Apache 2.0**. Ver el archivo [LICENSE](LICENSE) para más detalles.
