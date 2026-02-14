import time
from database.models import crear_base_datos, SessionLocal, Empleado
from services.thread_manager import ServerThread
import requests # Para simular ser el celular

def main():
    print("--- INICIANDO PRUEBA DEL SISTEMA SIGEP ---")

    # 1. Crear Base de datos y Tablas
    crear_base_datos()
    
    # 2. Insertar un empleado de prueba (si no existe)
    db = SessionLocal()
    if not db.query(Empleado).filter(Empleado.cedula == "12345").first():
        emp = Empleado(nombre="Juan Perez", cedula="12345", cargo="Desarrollador")
        db.add(emp)
        db.commit()
        print("👤 Empleado de prueba creado: Juan Perez (CI: 12345)")
    db.close()

    # 3. Iniciar el Servidor en un Hilo
    server = ServerThread()
    server.start()
    
    # Damos un segundo para que arranque
    time.sleep(2)

    # 4. Simular petición del Celular (Cliente Flutter)
    print("\n📱 Simulando celular enviando asistencia...")
    url = "http://127.0.0.1:8000/marcar_asistencia"
    datos = {"cedula_empleado": "12345"}

    try:
        respuesta = requests.post(url, json=datos)
        if respuesta.status_code == 200:
            print("✅ RESPUESTA DEL SERVIDOR:", respuesta.json())
        else:
            print("❌ ERROR:", respuesta.text)
    except Exception as e:
        print(f"Error de conexión: {e}")

    print("\n--- PRUEBA FINALIZADA (Cierra con Ctrl+C) ---")
    # Mantener vivo el script para ver logs
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()