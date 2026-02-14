# Sistema Multiplataforma Basado en Arquitectura Cliente/Servidor

Este proyecto es un sistema integral diseñado para la gestión de talento humano (SIGEP). Opera bajo una arquitectura Cliente-Servidor segura y eficiente, ideal para entornos de Intranet.

## 🏗️ Arquitectura

El sistema se compone de dos módulos principales:

*   **Servidor (Escritorio)**: Desarrollado en **Python** con **FastAPI** para el backend y **CustomTkinter** para la interfaz administrativa. Gestiona la base de datos SQLite y expone una API REST.
*   **Cliente (Móvil)**: Desarrollado en **Flutter** (Dart). Permite al personal interactuar con el sistema (consultas, asistencia) mediante dispositivos móviles.

## 🚀 Características

### Servidor (Administrativo)
*   **Gestión de Personal**: CRUD completo de empleados, cargos y horarios.
*   **Nómina**: Cálculo y visualización de sueldos, bonos y deducciones.
*   **Control de Asistencia**: Monitoreo en tiempo real y generación de reportes (Excel/PDF).
*   **API REST**: Servicio local para conexión con la app móvil.

### Cliente (Móvil)
*   **Autenticación**: Inicio de sesión seguro y soporte para biometría.
*   **Marcaje de Asistencia**: Registro de entrada/salida con geolocalización/red local.
*   **Dashboard Personal**: Visualización de perfil, carga académica y recibos de pago.

## 📂 Estructura del Proyecto

```
.
├── Cliente/          # Código fuente de l App Móvil (Flutter)
├── Servidor/         # Código fuente del Servidor (Python)
├── LICENSE           # Licencia Apache 2.0
├── README.md         # Documentación del proyecto
└── .gitignore        # Archivos ignorados por Git
```

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

### 2. Cliente (Flutter)

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
