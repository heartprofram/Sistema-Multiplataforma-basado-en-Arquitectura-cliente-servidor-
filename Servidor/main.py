import customtkinter as ctk
import sys
import os
import logging
import threading
import config
from PIL import Image
import pystray

# Ajuste de rutas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.models import init_db
from gui.tab_nomina import NominaTab
from gui.tab_gestion import GestionTab
from gui.tab_server import ServerTab 
from gui.tab_estadisticas import EstadisticasTab
from gui.tab_configuracion import ConfiguracionTab

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

        self.tabview = ctk.CTkTabview(
            self,
            segmented_button_selected_color="#1565C0",
            segmented_button_selected_hover_color="#0D47A1",
            segmented_button_unselected_color="#B0BEC5",
            segmented_button_unselected_hover_color="#78909C"
        )
        self.tabview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # --- AÑADIR PESTAÑAS ---
        # 1. Pestaña de Conexión
        self.tabview.add("Conexion")
        self.tab_server = ServerTab(master=self.tabview.tab("Conexion"))
        self.tab_server.pack(fill="both", expand=True)

        # 2. Pestaña de Nómina
        self.tabview.add("Personal")
        self.tab_nomina = NominaTab(master=self.tabview.tab("Personal"))
        self.tab_nomina.pack(fill="both", expand=True)

        # 3. Pestaña de Monitor
        self.tabview.add("Asistencia")
        self.tab_gestion = GestionTab(master=self.tabview.tab("Asistencia"))
        self.tab_gestion.pack(fill="both", expand=True)

        # 4. Pestaña de Estadísticas
        self.tabview.add("Estadisticas")
        self.tab_estadisticas = EstadisticasTab(master=self.tabview.tab("Estadisticas"))
        self.tab_estadisticas.pack(fill="both", expand=True)

        # 5. Pestaña de Configuración (NUEVO)
        self.tabview.add("Configuracion")
        self.tab_config = ConfiguracionTab(master=self.tabview.tab("Configuracion"))
        self.tab_config.pack(fill="both", expand=True)

        logger.info("Aplicacion iniciada correctamente")
        
        # Tray Icon setup
        self.tray_icon = None
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Check config for background mode
        bg_mode = getattr(config, "BACKGROUND_MODE", True)
        
        if bg_mode:
            self.withdraw() # Hide window
            self.show_tray_icon()
        else:
            self.quit_app()

    def show_tray_icon(self):
        if self.tray_icon:
            return
            
        try:
            if os.path.exists("servidor.ico"):
                image = Image.open("servidor.ico")
            else:
                # Create a simple colored block if icon missing
                image = Image.new('RGB', (64, 64), color = (21, 101, 192))
                
            menu = (
                pystray.MenuItem("Restaurar", self.restore_window),
                pystray.MenuItem("Salir", self.quit_app)
            )
            self.tray_icon = pystray.Icon("SIGEP", image, "SIGEP Server", menu)
            
            # Run in a separate thread so it doesn't block
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Error creating tray icon: {e}")
            self.quit_app()

    def restore_window(self, icon, item):
        try:
            icon.stop()
            self.tray_icon = None
            self.after(0, self.deiconify)
        except Exception as e:
            logger.error(f"Error restoring window: {e}")

    def quit_app(self, icon=None, item=None):
        if self.tray_icon:
            self.tray_icon.stop()
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()