import customtkinter as ctk
import sys
import os
import logging
import config

# Ajuste de rutas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.models import init_db
from gui.tab_nomina import NominaTab
from gui.tab_gestion import GestionTab
from gui.tab_server import ServerTab 
from gui.tab_estadisticas import EstadisticasTab

# Configuración de Logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(config.APP_TITLE)
        self.geometry(config.APP_GEOMETRY)
        ctk.set_appearance_mode(config.THEME)
        
        logger.info("Inicializando Base de Datos...")
        init_db()
        
        # Sembrar datos por defecto (Cargos, Horarios)
        from services.employee_service import EmployeeService
        EmployeeService.seed_data()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # --- AÑADIR PESTAÑAS ---
        # 1. Pestaña de Conexión
        self.tabview.add("Conexion") # Removed emoji
        self.tab_server = ServerTab(master=self.tabview.tab("Conexion"))
        self.tab_server.pack(fill="both", expand=True)

        # 2. Pestaña de Nómina
        self.tabview.add("Personal") # Removed emoji
        self.tab_nomina = NominaTab(master=self.tabview.tab("Personal"))
        self.tab_nomina.pack(fill="both", expand=True)

        # 3. Pestaña de Monitor
        self.tabview.add("Asistencia") # Removed emoji
        self.tab_gestion = GestionTab(master=self.tabview.tab("Asistencia"))
        self.tab_gestion.pack(fill="both", expand=True)

        # 4. Pestaña de Estadísticas (NUEVO)
        self.tabview.add("Estadisticas")
        self.tab_estadisticas = EstadisticasTab(master=self.tabview.tab("Estadisticas"))
        self.tab_estadisticas.pack(fill="both", expand=True)

        logger.info("Aplicacion iniciada correctamente")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()