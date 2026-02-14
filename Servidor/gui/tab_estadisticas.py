import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta
from services.stats_service import StatsService
from services.export_service import ExportService

# Matplotlib integration
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EstadisticasTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, fg_color="transparent")
        
        self.service = StatsService()
        self.current_stats = [] # Store data for export
        
        # Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Table
        self.grid_rowconfigure(2, weight=1) # Chart

        # --- CONTROLES SUPERIORES ---
        self.controls_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        self.controls_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        ctk.CTkLabel(self.controls_frame, text="Rango de Fechas:", font=("Roboto", 14, "bold"), text_color="#333").pack(side="left", padx=20, pady=15)
        
        # Entradas de Fecha (YYYY-MM-DD)
        today = datetime.now()
        first_day = today.replace(day=1)

        self.entry_start = ctk.CTkEntry(self.controls_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.entry_start.pack(side="left", padx=5)
        self.entry_start.insert(0, first_day.strftime("%Y-%m-%d"))

        ctk.CTkLabel(self.controls_frame, text="a", text_color="#333").pack(side="left", padx=5)

        self.entry_end = ctk.CTkEntry(self.controls_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.entry_end.pack(side="left", padx=5)
        self.entry_end.insert(0, today.strftime("%Y-%m-%d"))

        self.btn_calc = ctk.CTkButton(
            self.controls_frame, 
            text="CALCULAR EFECTIVIDAD",
            fg_color="#1976D2", hover_color="#1565C0",
            command=self.calcular_estadisticas
        )
        self.btn_calc.pack(side="left", padx=20)

        self.btn_export = ctk.CTkButton(
            self.controls_frame, 
            text="EXPORTAR EXCEL",
            fg_color="#2E7D32", hover_color="#1B5E20",
            image=None, # Todo: Add icon
            command=self.exportar_excel
        )
        self.btn_export.pack(side="right", padx=20)


        # --- TABLA DE RESULTADOS ---
        self.tree_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tree_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))

        columns = ("id", "nombre", "cargo", "dias_habiles", "asistencias", "efectividad")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", height=8)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Empleado")
        self.tree.heading("cargo", text="Cargo")
        self.tree.heading("dias_habiles", text="Días Hábiles")
        self.tree.heading("asistencias", text="Asistencias")
        self.tree.heading("efectividad", text="Efectividad %")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=200)
        self.tree.column("cargo", width=150)
        self.tree.column("dias_habiles", width=100, anchor="center")
        self.tree.column("asistencias", width=100, anchor="center")
        self.tree.column("efectividad", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Estilos simples
        self.tree.tag_configure("low", background="#FFEBEE") # Rojo claro
        self.tree.tag_configure("high", background="#E8F5E9") # Verde claro

        # --- GRÁFICO ---
        self.chart_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        self.chart_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))
        
        # Placeholder del gráfico
        self.fig, self.ax = plt.subplots(figsize=(8, 3), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        self.ax.set_title("Efectividad por Empleado")
        self.ax.set_ylabel("Carga (%)")


    def calcular_estadisticas(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        start = self.entry_start.get()
        end = self.entry_end.get()

        # Llamar al servicio
        stats = self.service.calculate_stats(start, end)

        if isinstance(stats, dict) and "error" in stats:
            messagebox.showerror("Error", stats["error"])
            return

        self.current_stats = stats # Save for export

        nombres = []
        efectividades = []

        for s in stats:
            # Color coding para efectividad
            tags = ()
            if s["efectividad"] < 50:
                tags = ("low",)
            elif s["efectividad"] >= 90:
                tags = ("high",)

            self.tree.insert("", "end", values=(
                s["id"], s["nombre"], s["cargo"], 
                s["dias_habiles"], s["asistencias"], f"{s['efectividad']}%"
            ), tags=tags)
            
            nombres.append(s["nombre"].split(" ")[0]) # Solo primer nombre
            efectividades.append(s["efectividad"])

        self.actualizar_grafico(nombres, efectividades)

    def actualizar_grafico(self, nombres, efectividades):
        self.ax.clear()
        
        colors = ['#EF5350' if x < 50 else '#66BB6A' if x >= 90 else '#42A5F5' for x in efectividades]
        
        bars = self.ax.bar(nombres, efectividades, color=colors)
        
        self.ax.set_title("Efectividad de Asistencia (%)")
        self.ax.set_ylim(0, 100)
        self.ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Añadir etiquetas en las barras
        for bar in bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}%',
                    ha='center', va='bottom')

        self.fig.tight_layout()
        self.canvas.draw()

    def exportar_excel(self):
        if not self.current_stats:
            messagebox.showwarning("Atención", "No hay datos para exportar. Calcula primero.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Guardar Informe"
        )

        if filename:
            success, msg = ExportService.export_stats_to_excel(self.current_stats, filename)
            if success:
                messagebox.showinfo("Éxito", msg)
            else:
                messagebox.showerror("Error", msg)
