import threading
import uvicorn
from server.api import app

class ServerThread(threading.Thread):
    def __init__(self, host="0.0.0.0", port=8000):
        super().__init__()
        self.host = host
        self.port = port
        self.daemon = True # Esto hace que si cierras la ventana, el hilo muera también
        self.should_run = True

    def run(self):
        # Ejecutamos Uvicorn programáticamente
        print(f"🚀 Iniciando servidor en http://{self.host}:{self.port}")
        try:
            # log_config=None evita que uvicorn secuestre los logs de la consola
            uvicorn.run(app, host=self.host, port=self.port, log_config=None)
        except Exception as e:
            print(f"❌ Error en el servidor: {e}")

    def stop(self):
        # Detener uvicorn desde un hilo es complejo, pero al ser daemon=True,
        # cerrar la app principal es suficiente para la Fase 1.
        self.should_run = False