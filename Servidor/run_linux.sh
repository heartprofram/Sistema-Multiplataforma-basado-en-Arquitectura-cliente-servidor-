#!/bin/bash

echo "=== Iniciando SIGEP Server para Linux ==="

# 1. Verificar si Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado."
    echo "Por favor instálalo con: sudo apt install python3 python3-venv python3-tk"
    exit 1
fi

# 2. Crear entorno virtual si no existe
if [ ! -d "venv_linux" ]; then
    echo "Creando entorno virtual (venv_linux)..."
    python3 -m venv venv_linux
fi

# 3. Activar entorno virtual
source venv_linux/bin/activate

# 4. Instalar dependencias si es necesario
# Verificamos si existe el directorio de site-packages o un archivo centinela
if [ ! -f "venv_linux/.installed" ]; then
    echo "Instalando dependencias desde requirements.txt..."
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        touch venv_linux/.installed
    else
        echo "Error instalando dependencias. Asegúrate de tener las librerías de desarrollo instaladas."
        echo "En Debian/LocOS/Ubuntu: sudo apt install python3-dev python3-tk"
        exit 1
    fi
fi

# 5. Ejecutar la aplicación
echo "Ejecutando SIGEP Server..."
python main.py
