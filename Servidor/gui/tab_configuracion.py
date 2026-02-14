import customtkinter as ctk
from tkinter import messagebox
import winreg
import os
import sys
import config

class ConfiguracionTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # Spacer at bottom

        # --- TITULO ---
        ctk.CTkLabel(self, text="Configuración del Sistema", font=("Roboto", 20, "bold")).grid(row=0, column=0, pady=20, sticky="w", padx=20)

        # --- SECCION SISTEMA ---
        self.frame_system = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        self.frame_system.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        ctk.CTkLabel(self.frame_system, text="Opciones del Sistema", font=("Roboto", 16, "bold"), text_color="#333").pack(anchor="w", padx=20, pady=15)

        # Checkbox: Iniciar con Windows
        self.var_startup = ctk.BooleanVar(value=self.check_startup())
        self.cb_startup = ctk.CTkCheckBox(self.frame_system, text="Iniciar automáticamente con Windows", 
                                          variable=self.var_startup, command=self.toggle_startup,
                                          text_color="#333", border_color="#1E88E5", fg_color="#1E88E5")
        self.cb_startup.pack(anchor="w", padx=20, pady=10)

        # Checkbox: Segundo Plano
        self.var_background = ctk.BooleanVar(value=getattr(config, "BACKGROUND_MODE", True))
        self.cb_background = ctk.CTkCheckBox(self.frame_system, text="Minimizar a la bandeja del sistema al cerrar", 
                                             variable=self.var_background, command=self.toggle_background,
                                             text_color="#333", border_color="#1E88E5", fg_color="#1E88E5")
        self.cb_background.pack(anchor="w", padx=20, pady=10)


    def toggle_background(self):
        val = self.var_background.get()
        self.update_config("BACKGROUND_MODE", val, quote=False)
        config.BACKGROUND_MODE = val

    def update_config(self, key, value, quote=False):
        try:
            # Construct absolute path to config.py
            # This file is in Servidor/gui/, config.py is in Servidor/
            current_dir = os.path.dirname(os.path.abspath(__file__))
            server_dir = os.path.dirname(current_dir)
            config_path = os.path.join(server_dir, "config.py")

            with open(config_path, "r") as f:
                lines = f.readlines()
            
            with open(config_path, "w") as f:
                found = False
                for line in lines:
                    if line.strip().startswith(f"{key} ="):
                        if quote:
                            f.write(f'{key} = "{value}"\n')
                        else:
                            f.write(f'{key} = {value}\n')
                        found = True
                    else:
                        f.write(line)
                
                if not found:
                    if quote:
                        f.write(f'\n{key} = "{value}"\n')
                    else:
                        f.write(f'\n{key} = {value}\n')
        except Exception as e:
            print(f"Error updating config: {e}")
            messagebox.showerror("Error de Configuración", f"No se pudo escribir en config.py:\n{str(e)}")

    def check_startup(self):
        """Verifica si la app está en el registro de inicio"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, "SIGEP_Server")
            winreg.CloseKey(key)
            return True
        except WindowsError:
            return False

    def toggle_startup(self):
        app_path = os.path.abspath(sys.argv[0])
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            if self.var_startup.get():
                # Agregar al registro
                winreg.SetValueEx(key, "SIGEP_Server", 0, winreg.REG_SZ, f'"{app_path}"')
                messagebox.showinfo("Inicio Automático", "Aplicación añadida al inicio de Windows.")
            else:
                # Quitar del registro
                try:
                    winreg.DeleteValue(key, "SIGEP_Server")
                    messagebox.showinfo("Inicio Automático", "Aplicación eliminada del inicio de Windows.")
                except WindowsError:
                    pass # No existía
            winreg.CloseKey(key)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el registro: {e}")
