import customtkinter as ctk
# Importa la nueva pestaña y la de gestión anterior
from gui.tab_nomina import NominaTab
from gui.tab_gestion import GestionTab 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SIGEP 2.0 - Gestión Integral")
        self.geometry("1100x700")

        # Configurar Grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Crear Panel de Pestañas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # --- AÑADIR PESTAÑAS ---
        self.tabview.add("Personal y Nómina")
        self.tabview.add("Monitor Asistencia")

        # --- CONECTAR LAS VISTAS ---
        
        # Pestaña 1: Gestión de Empleados (NUEVA)
        self.tab_nomina = NominaTab(master=self.tabview.tab("Personal y Nómina"))
        self.tab_nomina.pack(fill="both", expand=True)

        # Pestaña 2: Monitor de Asistencia (LA QUE YA TENÍAS)
        self.tab_gestion = GestionTab(master=self.tabview.tab("Monitor Asistencia"))
        self.tab_gestion.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()