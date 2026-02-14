import customtkinter as ctk
from tkinter import ttk, messagebox
from services.employee_service import EmployeeService
from services.ip_scanner import obtener_ip_local

class NominaTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, fg_color="transparent") # Fondo transparente para integrarse

        # --- 1. CABECERA CON IP ---
        self.ip_frame = ctk.CTkFrame(self, fg_color="#283593", corner_radius=10, height=50) # Azul oscuro moderno
        self.ip_frame.pack(fill="x", padx=10, pady=10)
        
        ip_actual = obtener_ip_local()
        self.lbl_ip = ctk.CTkLabel(
            self.ip_frame, 
            text=f"📡 IP DEL SERVIDOR: {ip_actual} (Conectar App Móvil)", 
            font=("Roboto", 16, "bold"), text_color="white"
        )
        self.lbl_ip.pack(pady=12)

        # --- 2. LAYOUT PRINCIPAL (Izquierda: Formulario, Derecha: Tabla) ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=5, pady=5)

        # === PANEL IZQUIERDO: FORMULARIO ===
        self.form_frame = ctk.CTkScrollableFrame(self.main_container, width=380, label_text="Ficha del Empleado")
        self.form_frame.pack(side="left", fill="y", padx=5)

        # Variables de control
        self.var_id_empleado = None 
        self.cargos_map = {} 
        self.horarios_map = {} 

        # > Sección Identificación
        ctk.CTkLabel(self.form_frame, text="Datos Personales", font=("Roboto", 13, "bold"), text_color="#1A237E").pack(pady=(10,5), anchor="w")
        
        self.entry_nombre = ctk.CTkEntry(self.form_frame, placeholder_text="Nombre Completo", height=32)
        self.entry_nombre.pack(fill="x", pady=4)
        
        self.entry_cedula = ctk.CTkEntry(self.form_frame, placeholder_text="Cédula (Usuario)", height=32)
        self.entry_cedula.pack(fill="x", pady=4)
        
        self.entry_pass = ctk.CTkEntry(self.form_frame, placeholder_text="Contraseña App", show="*", height=32)
        self.entry_pass.pack(fill="x", pady=4)

        # > Información Personal (Nuevos Campos)
        self.entry_fecha_nac = ctk.CTkEntry(self.form_frame, placeholder_text="Fecha Nacimiento (DD-MM-AAAA)", height=32)
        self.entry_fecha_nac.pack(fill="x", pady=4)

        self.entry_lugar_nac = ctk.CTkEntry(self.form_frame, placeholder_text="Lugar de Nacimiento", height=32)
        self.entry_lugar_nac.pack(fill="x", pady=4)

        self.combo_genero = ctk.CTkComboBox(self.form_frame, values=["Masculino", "Femenino"], height=32)
        self.combo_genero.set("Masculino")
        self.combo_genero.pack(fill="x", pady=4)

        self.combo_estado_civil = ctk.CTkComboBox(self.form_frame, values=["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a", "Concubino/a"], height=32)
        self.combo_estado_civil.set("Soltero/a")
        self.combo_estado_civil.pack(fill="x", pady=4)

        self.combo_nacionalidad = ctk.CTkComboBox(self.form_frame, values=["V - Venezolano", "E - Extranjero"], height=32)
        self.combo_nacionalidad.set("V - Venezolano")
        self.combo_nacionalidad.pack(fill="x", pady=4)

        # Contacto
        ctk.CTkLabel(self.form_frame, text="Contacto", font=("Roboto", 12, "bold"), text_color="#424242").pack(pady=(10,2), anchor="w")
        self.entry_telefono = ctk.CTkEntry(self.form_frame, placeholder_text="Teléfono", height=32)
        self.entry_telefono.pack(fill="x", pady=4)
        
        self.entry_email = ctk.CTkEntry(self.form_frame, placeholder_text="Email", height=32)
        self.entry_email.pack(fill="x", pady=4)
        
        self.entry_direccion = ctk.CTkEntry(self.form_frame, placeholder_text="Dirección", height=32)
        self.entry_direccion.pack(fill="x", pady=4)

        # > Datos Laborales
        ctk.CTkLabel(self.form_frame, text="Datos Laborales", font=("Roboto", 13, "bold"), text_color="#1A237E").pack(pady=(15,5), anchor="w")

        self.msg_tipo = ctk.CTkLabel(self.form_frame, text="Tipo de Personal:", font=("Arial", 11))
        self.msg_tipo.pack(anchor="w")
        self.combo_tipo = ctk.CTkComboBox(self.form_frame, values=["Docente", "Administrativo", "Obrero", "Directivo"], command=self.toggle_docente_fields, height=32)
        self.combo_tipo.set("Docente")
        self.combo_tipo.pack(fill="x", pady=4)
        
        self.entry_departamento = ctk.CTkEntry(self.form_frame, placeholder_text="Departamento", height=32)
        self.entry_departamento.pack(fill="x", pady=4)

        self.msg_horario = ctk.CTkLabel(self.form_frame, text="Horario Asignado:", font=("Arial", 11))
        self.msg_horario.pack(anchor="w", pady=(5,0))
        self.combo_horario = ctk.CTkComboBox(self.form_frame, values=[], height=32)
        self.combo_horario.pack(fill="x", pady=4)

        # --- SECCIÓN DETALLES DOCENTE (Oculta por defecto si no es Docente) ---
        self.frame_docente = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        
        ctk.CTkLabel(self.frame_docente, text="--- Detalles del Docente ---", font=("Roboto", 12, "bold"), text_color="#1565C0").pack(pady=(15, 5))
        
        self.entry_nucleo = ctk.CTkEntry(self.frame_docente, placeholder_text="Núcleo / Extensión", height=32)
        self.entry_nucleo.pack(fill="x", pady=4)

        self.entry_ingreso = ctk.CTkEntry(self.frame_docente, placeholder_text="Fecha Ingreso (DD-MM-AAAA)", height=32)
        self.entry_ingreso.pack(fill="x", pady=4)

        self.entry_perfil = ctk.CTkEntry(self.frame_docente, placeholder_text="Perfil Académico", height=32)
        self.entry_perfil.pack(fill="x", pady=4)

        self.combo_categoria = ctk.CTkComboBox(self.frame_docente, values=["Instructor", "Asistente", "Agregado", "Asociado", "Titular"], height=32)
        self.combo_categoria.set("Instructor")
        self.combo_categoria.pack(fill="x", pady=4)

        self.combo_dedicacion = ctk.CTkComboBox(self.frame_docente, values=["Tiempo Completo (TC)", "Dedicación Exclusiva (DE)", "Tiempo Convencional (Tcv)", "Medio Tiempo (MT)", "Tiempo Variable (TV)"], height=32)
        self.combo_dedicacion.set("Tiempo Completo (TC)")
        self.combo_dedicacion.pack(fill="x", pady=4)

        self.entry_cargo_colateral = ctk.CTkEntry(self.frame_docente, placeholder_text="Cargo Colateral", height=32)
        self.entry_cargo_colateral.pack(fill="x", pady=4)
        
        self.entry_carrera = ctk.CTkEntry(self.frame_docente, placeholder_text="Carrera", height=32)
        self.entry_carrera.pack(fill="x", pady=4)
        
        self.entry_semestre = ctk.CTkEntry(self.frame_docente, placeholder_text="Semestre", height=32)
        self.entry_semestre.pack(fill="x", pady=4)

        self.entry_horas = ctk.CTkEntry(self.frame_docente, placeholder_text="Horas Académicas", height=32)
        self.entry_horas.pack(fill="x", pady=4)
        
        # Text Areas con borde suave
        ctk.CTkLabel(self.frame_docente, text="Asignaturas:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(8,2))
        self.txt_asignaturas = ctk.CTkTextbox(self.frame_docente, height=60, border_width=1, border_color="#BDBDBD")
        self.txt_asignaturas.pack(fill="x", pady=4)

        ctk.CTkLabel(self.frame_docente, text="Observaciones:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(8,2))
        self.txt_observaciones = ctk.CTkTextbox(self.frame_docente, height=60, border_width=1, border_color="#BDBDBD")
        self.txt_observaciones.pack(fill="x", pady=4)

        # Notas Adicionales (General)
        ctk.CTkLabel(self.form_frame, text="Notas Adicionales:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(15,2))
        self.txt_materias = ctk.CTkTextbox(self.form_frame, height=60, border_width=1, border_color="#BDBDBD")
        self.txt_materias.pack(fill="x", pady=4)

        # Botones de Acción - Estilo Mejorado
        self.btn_guardar = ctk.CTkButton(
            self.form_frame, text="💾 GUARDAR / ACTUALIZAR", 
            fg_color="#1E88E5", hover_color="#1565C0", # Azul Google
            height=36, corner_radius=8, font=("Roboto", 12, "bold"),
            command=self.guardar_empleado
        )
        self.btn_guardar.pack(fill="x", pady=(25, 8))

        self.btn_limpiar = ctk.CTkButton(
            self.form_frame, text="🧹 LIMPIAR FORMULARIO", 
            fg_color="#757575", hover_color="#616161", # Gris Material
            height=36, corner_radius=8, font=("Roboto", 11),
            command=self.limpiar_form
        )
        self.btn_limpiar.pack(fill="x", pady=5)

        self.btn_eliminar = ctk.CTkButton(
            self.form_frame, text="🗑️ ELIMINAR EMPLEADO", 
            fg_color="#D32F2F", hover_color="#B71C1C", # Rojo Material
            height=36, corner_radius=8, font=("Roboto", 11, "bold"),
            command=self.eliminar_empleado
        )
        self.btn_eliminar.pack(fill="x", pady=5)
        
        # === PANEL DERECHO: TABLA ===
        self.table_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.table_frame.pack(side="right", fill="both", expand=True, padx=(10,5))

        # Estilos de Tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
            rowheight=32, 
            font=("Roboto", 10),
            background="white", 
            fieldbackground="white",
            foreground="#212121"
        )
        style.configure("Treeview.Heading", 
            font=("Roboto", 11, "bold"), 
            background="#1976D2", 
            foreground="white",
            relief="flat"
        )
        style.map("Treeview", 
            background=[('selected', '#E3F2FD')], 
            foreground=[('selected', 'black')]
        )

        cols = ("ID", "Cédula", "Nombre", "Cargo", "Horario")
        self.tree = ttk.Treeview(self.table_frame, columns=cols, show="headings")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cédula", text="Cédula")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cargo", text="Cargo")
        self.tree.heading("Horario", text="Horario")

        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Cédula", width=100)
        self.tree.column("Nombre", width=180)
        self.tree.column("Cargo", width=120)
        self.tree.column("Horario", width=120)

        # Scrollbar para la tabla
        scrollbar = ctk.CTkScrollbar(self.table_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.pack(fill="both", expand=True)
        
        # Evento: Al hacer clic en la tabla, cargar datos en el formulario
        self.tree.bind("<<TreeviewSelect>>", self.cargar_seleccion)

        # Cargar datos iniciales
        self.cargar_combos()
        self.cargar_tabla()

    # --- LÓGICA DE NEGOCIO ---
    
    def cargar_combos(self):
        # Cargar Cargos (Para mapeo interno, ya no se muestra combo)
        cargos = EmployeeService.get_all_cargos()
        self.cargos_map = {c.nombre: c.id for c in cargos}

        # Cargar Horarios
        horarios = EmployeeService.get_all_horarios()
        self.horarios_map = {h.nombre: h.id for h in horarios}
        self.combo_horario.configure(values=list(self.horarios_map.keys()))
        if self.horarios_map:
            self.combo_horario.set(list(self.horarios_map.keys())[0])

    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        empleados = EmployeeService.get_all_employees()
        for emp in empleados:
            cargo_nombre = emp.cargo_rel.nombre if emp.cargo_rel else "Sin Cargo"
            horario_nombre = emp.horario_rel.nombre if emp.horario_rel else "Sin Horario"
            self.tree.insert("", "end", values=(emp.id, emp.cedula, emp.nombre, cargo_nombre, horario_nombre))

    def limpiar_form(self):
        self.var_id_empleado = None
        self.entry_nombre.delete(0, "end")
        self.entry_cedula.delete(0, "end")
        self.entry_pass.delete(0, "end")
        self.entry_pass.insert(0, "1234")
        
        self.entry_telefono.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_direccion.delete(0, "end")
        self.entry_lugar_nac.delete(0, "end")
        self.entry_fecha_nac.delete(0, "end")
        self.combo_estado_civil.set("Soltero/a")
        self.combo_genero.set("Masculino")
        self.combo_nacionalidad.set("V - Venezolano")

        self.entry_departamento.delete(0, "end")
        
        self.txt_materias.delete("1.0", "end")

        # Limpiar campos docente
        self.entry_nucleo.delete(0, "end")
        self.entry_ingreso.delete(0, "end")
        self.entry_perfil.delete(0, "end")
        self.entry_cargo_colateral.delete(0, "end")
        self.entry_carrera.delete(0, "end")
        self.entry_semestre.delete(0, "end")
        self.entry_horas.delete(0, "end")
        self.txt_asignaturas.delete("1.0", "end")
        self.txt_observaciones.delete("1.0", "end")
        
        self.combo_tipo.set("Docente")
        self.toggle_docente_fields("Docente")
    
    def guardar_empleado(self):
        # Recolectar datos
        nombre = self.entry_nombre.get()
        cedula = self.entry_cedula.get()
        
        if not nombre or not cedula:
            messagebox.showwarning("Faltan datos", "Nombre y Cédula son obligatorios.")
            return

        # Obtener IDs de Combos
        tipo_seleccionado = self.combo_tipo.get()
        horario_nombre = self.combo_horario.get()
        
        # Asignar Cargo ID basado en el Tipo de Personal (1:1)
        cargo_id = self.cargos_map.get(tipo_seleccionado)
        horario_id = self.horarios_map.get(horario_nombre)

        data = {
            "nombre": nombre,
            "cedula": cedula,
            "password": self.entry_pass.get(),
            "telefono": self.entry_telefono.get(),
            "email": self.entry_email.get(),
            "direccion": self.entry_direccion.get(),
            
            "lugar_nacimiento": self.entry_lugar_nac.get(),
            "fecha_nacimiento": self.entry_fecha_nac.get(),
            "estado_civil": self.combo_estado_civil.get(),
            "genero": self.combo_genero.get(),
            "nacionalidad": self.combo_nacionalidad.get().split(" ")[0],

            "departamento": self.entry_departamento.get(),
            "tipo_personal": tipo_seleccionado,
            "cargo_id": cargo_id,
            "horario_id": horario_id,
            "materias_asignadas": self.txt_materias.get("1.0", "end-1c")
        }

        # Recolectar datos de docente si aplica
        if self.combo_tipo.get() == "Docente":
            data["detalle_docente"] = {
                "nucleo_extension": self.entry_nucleo.get(),
                "fecha_ingreso": self.entry_ingreso.get(),
                "perfil_academico": self.entry_perfil.get(),
                "categoria_actual": self.combo_categoria.get(),
                "condicion_dedicacion": self.combo_dedicacion.get(),
                "cargo_colateral": self.entry_cargo_colateral.get(),
                "carrera": self.entry_carrera.get(),
                "semestre": self.entry_semestre.get(),
                "horas_academicas": int(self.entry_horas.get()) if self.entry_horas.get().isdigit() else 0,
                "asignaturas": self.txt_asignaturas.get("1.0", "end-1c"),
                "observaciones": self.txt_observaciones.get("1.0", "end-1c")
            }

        try:
            if self.var_id_empleado: # MODO EDICIÓN
                EmployeeService.update_employee(self.var_id_empleado, data)
                messagebox.showinfo("Éxito", "Empleado actualizado correctamente.")
            else: # MODO CREACIÓN
                EmployeeService.create_employee(data)
                messagebox.showinfo("Éxito", "Empleado registrado.")
            
            self.limpiar_form()
            self.cargar_tabla()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
    
    def cargar_seleccion(self, event):
        seleccion = self.tree.selection()
        if not seleccion: return
        
        item = self.tree.item(seleccion)
        id_emp = item['values'][0]
        
        emp = EmployeeService.get_employee_by_id(id_emp)
        
        if emp:
            self.limpiar_form() # Limpia primero
            self.var_id_empleado = emp.id # Marca que estamos editando
            
            self.entry_nombre.insert(0, emp.nombre)
            self.entry_cedula.insert(0, emp.cedula)
            self.entry_pass.delete(0, "end")
            self.entry_pass.insert(0, emp.password)
            
            # Nuevos campos
            if emp.telefono: self.entry_telefono.insert(0, emp.telefono)
            if emp.email: self.entry_email.insert(0, emp.email)
            if emp.direccion: self.entry_direccion.insert(0, emp.direccion)
            
            if emp.lugar_nacimiento: self.entry_lugar_nac.insert(0, emp.lugar_nacimiento)
            if emp.fecha_nacimiento: self.entry_fecha_nac.insert(0, emp.fecha_nacimiento)
            if emp.estado_civil: self.combo_estado_civil.set(emp.estado_civil)
            if emp.genero: self.combo_genero.set(emp.genero)
            if emp.nacionalidad:
                val = "V - Venezolano" if emp.nacionalidad == "V" else "E - Extranjero"
                self.combo_nacionalidad.set(val)

            if emp.departamento: self.entry_departamento.insert(0, emp.departamento)
            
            self.combo_tipo.set(emp.tipo_personal)
            
            if emp.horario_rel:
                self.combo_horario.set(emp.horario_rel.nombre)

            self.txt_materias.insert("1.0", emp.materias_asignadas or "")
            
            # Cargar detalle docente
            self.toggle_docente_fields(emp.tipo_personal)
            if emp.detalle_docente:
                d = emp.detalle_docente
                if d.nucleo_extension: self.entry_nucleo.insert(0, d.nucleo_extension)
                if d.fecha_ingreso: self.entry_ingreso.insert(0, d.fecha_ingreso)
                if d.perfil_academico: self.entry_perfil.insert(0, d.perfil_academico)
                if d.categoria_actual: self.combo_categoria.set(d.categoria_actual)
                if d.condicion_dedicacion: self.combo_dedicacion.set(d.condicion_dedicacion)
                if d.cargo_colateral: self.entry_cargo_colateral.insert(0, d.cargo_colateral)
                if d.carrera: self.entry_carrera.insert(0, d.carrera)
                if d.semestre: self.entry_semestre.insert(0, d.semestre)
                if d.horas_academicas: self.entry_horas.insert(0, str(d.horas_academicas))
                if d.asignaturas: self.txt_asignaturas.insert("1.0", d.asignaturas)
                if d.observaciones: self.txt_observaciones.insert("1.0", d.observaciones)
    
    def eliminar_empleado(self):
        if not self.var_id_empleado:
            messagebox.showwarning("Cuidado", "Selecciona un empleado de la tabla primero.")
            return
        
        confirmar = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar a este empleado?")
        if confirmar:
            if EmployeeService.delete_employee(self.var_id_empleado):
                messagebox.showinfo("Eliminado", "Empleado eliminado del sistema.")
                self.limpiar_form()
                self.cargar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo eliminar al empleado.")

    def toggle_docente_fields(self, eleccion):
        try:
            if eleccion == "Docente":
                self.frame_docente.pack(fill="x", pady=5, after=self.combo_horario)
            else:
                self.frame_docente.pack_forget()
        except Exception:
            pass
