import sys
import customtkinter as ctk

class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget # El cuadro de texto donde escribiremos
        self.original_stdout = sys.stdout # Guardamos la salida original por si acaso

    def write(self, str):
        # Insertamos el texto al final del cuadro
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", str)
        self.text_widget.see("end") # Auto-scroll hacia abajo
        self.text_widget.configure(state="disabled") # Bloqueamos para que el usuario no borre

    def flush(self):
        pass # Necesario para cumplir con el protocolo de archivos de Python