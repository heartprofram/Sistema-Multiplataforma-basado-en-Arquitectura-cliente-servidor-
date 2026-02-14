import sys
from cx_Freeze import setup, Executable

# --- CONFIGURACIÓN ---
base = None
if sys.platform == "win32":
    base = "gui"

# Lista de librerías a incluir
build_exe_options = {
    "packages": ["os", "sys", "customtkinter", "openpyxl", "sqlalchemy", "reportlab"],
    "include_files": [],
    # Excluimos numpy porque da error en Python 3.14 y no lo necesitamos
    "excludes": ["numpy"] 
}

# --- DEFINICIÓN DEL EJECUTABLE ---
target = Executable(
    script="main.py",
    base=base,
    target_name="SIGEP_Admin.exe",
    icon=None
)

setup(
    name="SIGEP_Admin",
    version="1.0",
    description="Sistema de Control de Asistencia",
    options={"build_exe": build_exe_options},
    executables=[target]
)