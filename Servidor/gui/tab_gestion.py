import customtkinter as ctk
from tkinter import ttk, messagebox
import logging
from services.attendance_service import AttendanceService
from services.excel_manager import exportar_excel
from services.pdf_generator import generar_pdf
import config

logger = logging.getLogger(__name__)

class GestionTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, fg_color="transparent")

        # 1. Título y Botonera
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=20, padx=10)

        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame, 
            text="📋 Asistencia en Tiempo Real", 
            font=("Roboto", 24, "bold"),
            text_color="#1A237E" # Azul Oscuro
        )
        self.lbl_titulo.pack(side="left", padx=10)

        # --- ÁREA DE BOTONES DE REPORTE ---
        self.btn_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.btn_frame.pack(side="right")

        # Botón Excel
        self.btn_excel = ctk.CTkButton(
            self.btn_frame, text="📗 Excel", width=90, height=36,
            fg_color="#2E7D32", hover_color="#1B5E20", # Verde Excel
            corner_radius=8, font=("Roboto", 12, "bold"),
            command=self.accion_excel
        )
        self.btn_excel.pack(side="left", padx=5)

        # Botón PDF
        self.btn_pdf = ctk.CTkButton(
            self.btn_frame, text="📕 PDF", width=90, height=36,
            fg_color="#D32F2F", hover_color="#B71C1C", # Rojo PDF
            corner_radius=8, font=("Roboto", 12, "bold"),
            command=self.accion_pdf
        )
        self.btn_pdf.pack(side="left", padx=5)

        # Botón Actualizar
        self.btn_refresh = ctk.CTkButton(
            self.btn_frame, text="🔄 Actualizar", width=110, height=36,
            fg_color="#1976D2", hover_color="#1565C0", # Azul Google
            corner_radius=8, font=("Roboto", 12, "bold"),
            command=self.cargar_datos
        )
        self.btn_refresh.pack(side="left", padx=5)
        # ----------------------------------

        # 2. ESTILO DE LA TABLA (Clonado de Nómina para consistencia)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure(
            "Treeview", 
            background="white", 
            foreground="#212121", 
            rowheight=32, 
            fieldbackground="white", 
            font=("Roboto", 10)
        )
        self.style.map('Treeview', background=[('selected', '#E3F2FD')], foreground=[('selected', 'black')])
        
        self.style.configure(
            "Treeview.Heading", 
            font=("Roboto", 11, "bold"), 
            background="#1976D2", 
            foreground="white", 
            relief="flat"
        )

        # 3. Construcción de la Tabla
        columns = ("id", "empleado", "cedula", "cargo", "fecha", "hora")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("empleado", text="Colaborador")
        self.tree.heading("cedula", text="Cédula")
        self.tree.heading("cargo", text="Cargo")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora Entrada")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("empleado", width=220)
        self.tree.column("cedula", width=100, anchor="center")
        self.tree.column("cargo", width=150)
        self.tree.column("fecha", width=100, anchor="center")
        self.tree.column("hora", width=100, anchor="center")

        scrollbar = ctk.CTkScrollbar(self, command=self.tree.yview, fg_color="transparent")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 4. Iniciar Datos
        self.cargar_datos()
        self.iniciar_auto_refresco()

    def cargar_datos(self):
        try:
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            registros = AttendanceService.get_recent_attendance(limit=50)
            
            for reg in registros:
                nombre_emp = reg.empleado.nombre if reg.empleado else "Eliminado"
                cedula_emp = reg.empleado.cedula if reg.empleado else "---"
                
                cargo_emp = "---"
                if reg.empleado and reg.empleado.cargo_rel:
                    cargo_emp = reg.empleado.cargo_rel.nombre
                
                self.tree.insert("", "end", values=(
                    reg.id, nombre_emp, cedula_emp,
                    cargo_emp, reg.fecha_hora.strftime("%d/%m/%Y"),
                    reg.fecha_hora.strftime("%H:%M:%S")
                ))
        except Exception as e:
            logger.error(f"Error al cargar datos en la tabla: {e}")
            print(f"Error UI: {e}")

    def iniciar_auto_refresco(self):
        try:
            self.cargar_datos()
        except Exception as e:
            logger.error(f"Error en auto-refresco: {e}")
        
        # Se programa la siguiente ejecución pase lo que pase
        self.after(config.REFRESH_INTERVAL_MS, self.iniciar_auto_refresco)

    # --- FUNCIONES DE LOS BOTONES ---
    def accion_excel(self):
        resultado = exportar_excel()
        messagebox.showinfo("Exportar Excel", resultado)

    def accion_pdf(self):
        resultado = generar_pdf()
        messagebox.showinfo("Exportar PDF", resultado)