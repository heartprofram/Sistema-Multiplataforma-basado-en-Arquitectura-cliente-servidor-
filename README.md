# Sistema Multiplataforma Basado en Arquitectura Cliente/Servidor (SIGEP)

![Version](https://img.shields.io/github/v/release/heartprofram/Sistema-Multiplataforma-basado-en-Arquitectura-cliente-servidor-?style=flat-square)
![License](https://img.shields.io/github/license/heartprofram/Sistema-Multiplataforma-basado-en-Arquitectura-cliente-servidor-?style=flat-square)
![Python](https://img.shields.io/badge/Backend-Python%20%7C%20FastAPI-blue?style=flat-square&logo=python)
![Flutter](https://img.shields.io/badge/Frontend-Flutter-02569B?style=flat-square&logo=flutter)

Este proyecto es un sistema integral diseñado para la gestión de talento humano (**SIGEP**). Opera bajo una arquitectura Cliente-Servidor segura y eficiente, ideal para entornos de Intranet corporativa o institucional.

---

## 📥 Descarga y Uso Inmediato (v1.0.0)

¡Empieza a usar el sistema ahora mismo sin necesidad de programar!

| Componente | Archivo | Descripción |
| :--- | :---: | :--- |
| **📱 App Móvil** | [![Descargar APK](https://img.shields.io/badge/⬇️_Descargar_APK_Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)](https://github.com/heartprofram/Sistema-Multiplataforma-basado-en-Arquitectura-cliente-servidor-/releases/download/v1.0.0/SIGEP_App_v1.0.apk) | Instalar en teléfonos de los empleados. |
| **🖥️ Servidor PC** | [![Descargar Servidor](https://img.shields.io/badge/⬇️_Descargar_Servidor_(ZIP)-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/heartprofram/Sistema-Multiplataforma-basado-en-Arquitectura-cliente-servidor-/releases/tag/v1.0.0) | Panel de control para el Administrador. |

### 📋 Instrucciones rápidas:
1.  **Móvil:** Descarga el APK e instálalo (acepta orígenes desconocidos). Conéctate al Wi-Fi del servidor.
2.  **PC:** Descarga el ZIP, descomprímelo y ejecuta `SIGEP_Server.exe`. Si Windows protege la PC, da clic en *"Más información" > "Ejecutar de todas formas"*.

---

## 🏗️ Arquitectura del Sistema

El sistema se compone de dos módulos principales que se comunican entre sí:

* **🖥️ Servidor (Escritorio):**
    * Desarrollado en **Python** (**FastAPI** + **CustomTkinter**).
    * Gestiona la base de datos SQLite y expone una API REST local.
* **📱 Cliente (Móvil):**
    * Desarrollado en **Flutter** (Dart).
    * Permite al personal interactuar con el sistema (consultas, marcar asistencia) mediante dispositivos Android.

## 🚀 Características Principales

### Servidor (Panel Administrativo)
* ✅ **Gestión de Personal:** CRUD completo de empleados, cargos y horarios.
* ✅ **Nómina:** Visualización detallada de datos personales y laborales.
* ✅ **Control de Asistencia:** Monitoreo en tiempo real de entradas y salidas.
* ✅ **Reportes:** Cálculo de efectividad y exportación a **Excel/PDF**.
* ✅ **API REST:** Servicio optimizado para conexión fluida con la app móvil.

### Cliente (App Móvil)
* ✅ **Autenticación Segura:** Inicio de sesión con soporte para biometría (huella/rostro).
* ✅ **Conexión Inteligente:** Detección automática de la IP del servidor.
* ✅ **Marcaje de Asistencia:** Registro de entrada/salida validado por red local.
* ✅ **Dashboard Personal:** Acceso a perfil, carga académica y recibos.

## 📂 Estructura del Proyecto

```text
.
├── Cliente/          # Código fuente de la App Móvil (Flutter)
├── Servidor/         # Código fuente del Servidor (Python/FastAPI)
├── LICENSE           # Licencia Apache 2.0
├── README.md         # Documentación del proyecto
└── .gitignore        # Archivos ignorados por Git
