import customtkinter as ctk
from services.server_manager import ServerThread
from services.ip_scanner import obtener_ip_local
import threading
import config

class ServerTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, fg_color="transparent")
        
        self.server_thread = None 
        self.is_running = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Console expands

        # --- 1. CABECERA: DASHBOARD DE ESTADO ---
        self.status_card = ctk.CTkFrame(self, fg_color="white", corner_radius=15, border_width=2, border_color="#E0E0E0")
        self.status_card.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.status_card.grid_columnconfigure(1, weight=1)

        # Indicador Visual (Círculo)
        self.status_canvas = ctk.CTkCanvas(self.status_card, width=20, height=20, bg="white", highlightthickness=0)
        self.status_circle = self.status_canvas.create_oval(2, 2, 18, 18, fill="#9E9E9E", outline="") # Inicial: Gris
        self.status_canvas.grid(row=0, column=0, padx=(20, 10), pady=20)

        # Texto de Estado
        self.lbl_status = ctk.CTkLabel(
            self.status_card, text="SERVIDOR APAGADO", 
            font=("Roboto", 20, "bold"), text_color="#757575"
        )
        self.lbl_status.grid(row=0, column=1, sticky="w")

        # Info de Red (Derecha)
        ip = obtener_ip_local()
        self.info_frame = ctk.CTkFrame(self.status_card, fg_color="transparent")
        self.info_frame.grid(row=0, column=2, padx=20, pady=15)

        ctk.CTkLabel(self.info_frame, text=f"IP: {ip}", font=("Roboto", 14, "bold"), text_color="#1A237E").pack(anchor="e")
        ctk.CTkLabel(self.info_frame, text=f"Puerto: {config.SERVER_PORT}", font=("Roboto", 12), text_color="#424242").pack(anchor="e")

        # --- 2. BOTONES DE CONTROL ---
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=1, column=0, padx=20, pady=(0, 20))

        self.btn_start = ctk.CTkButton(
            self.btn_frame, text="▶ INICIAR SERVIDOR", 
            fg_color="#2E7D32", hover_color="#1B5E20", # Verde
            height=55, width=220, corner_radius=10,
            font=("Roboto", 14, "bold"),
            command=self.iniciar_servidor
        )
        self.btn_start.pack(side="left", padx=10)

        self.btn_stop = ctk.CTkButton(
            self.btn_frame, text="⏹ DETENER SERVIDOR", 
            fg_color="#D32F2F", hover_color="#B71C1C", # Rojo
            height=55, width=220, corner_radius=10,
            font=("Roboto", 14, "bold"),
            state="disabled",
            command=self.detener_servidor
        )
        self.btn_stop.pack(side="left", padx=10)

        # --- 3. CONSOLA DE LOGS ---
        self.log_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.log_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")

        ctk.CTkLabel(self.log_frame, text="Registro de Eventos (Logs):", font=("Roboto", 12, "bold"), text_color="#424242").pack(anchor="w", pady=(0,5))

        self.console = ctk.CTkTextbox(
            self.log_frame, 
            font=("Consolas", 11), 
            fg_color="#FAFAFA", text_color="#212121",
            border_width=1, border_color="#BDBDBD",
            corner_radius=5
        )
        self.console.pack(fill="both", expand=True)
        self.console.insert("0.0", ">> Sistema listo. Esperando comando de inicio...\n")

    # --- LÓGICA DE CONTROL ---

    def iniciar_servidor(self):
        if self.is_running: return

        self.log(">> Iniciando servicios del servidor...")
        
        self.server_thread = ServerThread()
        self.server_thread.start()
        
        self.is_running = True
        self.actualizar_ui(True)
        self.log(">> Servidor EN LÍNEA y escuchando conexiones.")

    def detener_servidor(self):
        if not self.is_running or not self.server_thread: return

        self.log(">> Deteniendo servicios...")
        
        self.server_thread.stop()
        
        self.is_running = False
        self.actualizar_ui(False)
        self.log(">> Servidor APAGADO correctamente.")

    def actualizar_ui(self, activo):
        if activo:
             # Estado ONLINE
            self.status_card.configure(border_color="#43A047") # Borde Verde
            self.status_canvas.itemconfig(self.status_circle, fill="#43A047") # Círculo Verde
            self.lbl_status.configure(text="SERVIDOR EN LÍNEA", text_color="#2E7D32")
            
            self.btn_start.configure(state="disabled", fg_color="#E0E0E0", text_color="#9E9E9E")
            self.btn_stop.configure(state="normal", fg_color="#D32F2F")
        else:
            # Estado OFFLINE
            self.status_card.configure(border_color="#E0E0E0") # Borde Gris
            self.status_canvas.itemconfig(self.status_circle, fill="#9E9E9E") # Círculo Gris
            self.lbl_status.configure(text="SERVIDOR APAGADO", text_color="#757575")
            
            self.btn_start.configure(state="normal", fg_color="#2E7D32", text_color="white")
            self.btn_stop.configure(state="disabled", fg_color="#E0E0E0", text_color="#9E9E9E")

    def log(self, mensaje):
        self.console.insert("end", f"{mensaje}\n")
        self.console.see("end")