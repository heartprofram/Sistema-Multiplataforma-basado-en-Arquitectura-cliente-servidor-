import sys
import os
from cx_Freeze import setup, Executable

# Definir archivos a incluir
files = [
    ("servidor.ico", "servidor.ico"),
    ("config.py", "config.py"),
    ("gui/", "gui/"),
    ("database/", "database/"),
    ("services/", "services/"),
    # Incluir requirements.txt si es necesario para referencia, pero no es crítico para el exe
]

# Dependencias adicionales
build_exe_options = {
    "packages": [
        "os", "sys", "ctypes", "logging", "threading", 
        "customtkinter", "PIL", "pystray", "sqlalchemy", 
        "fastapi", "uvicorn", "matplotlib", "openpyxl", "reportlab"
    ],
    "include_files": files,
    "excludes": ["tkinter.test", "unittest"], # Excluir tests para reducir tamaño
    "include_msvcr": True, # Incluir runtime de VC++ si es necesario
}

# Configuración del ejecutable
base = None
if sys.platform == "win32":
    base = "Win32GUI" # Ocultar consola en Windows

target = Executable(
    script="main.py",
    base=base,
    icon="servidor.ico",
    target_name="SIGEP_Server.exe" if sys.platform == "win32" else "SIGEP_Server"
)

setup(
    name="SIGEP_Server",
    version="1.0.0",
    description="Sistema Integral de Gestión de Personal",
    options={"build_exe": build_exe_options},
    executables=[target]
)
