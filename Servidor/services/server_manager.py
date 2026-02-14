import threading
import uvicorn
import time
from server.api import app
import config

class ServerThread(threading.Thread):
    def __init__(self, host=config.SERVER_HOST, port=config.SERVER_PORT):
        super().__init__()
        self.host = host
        self.port = port
        self.server = None
        self.daemon = True # Se cierra si cierras la app

    def run(self):
        # Configuración especial para tener control sobre el servidor
        config = uvicorn.Config(app, host=self.host, port=self.port, log_level="info")
        self.server = uvicorn.Server(config)
        
        # Evitamos que Uvicorn capture Ctrl+C, dejamos que Tkinter mande
        self.server.install_signal_handlers = lambda: None
        
        print("⚡ Servidor Iniciando...")
        self.server.run()

    def stop(self):
        if self.server:
            self.server.should_exit = True # Señal de apagado suave
            print("🛑 Deteniendo servidor...")