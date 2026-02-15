from PIL import Image
import os

ico_path = r"c:\Users\Edwin Medina\Desktop\Sistema Multiplataforma base\Sistema Multiplataforma\Cliente\cliente.ico"
png_path = r"c:\Users\Edwin Medina\Desktop\Sistema Multiplataforma base\Sistema Multiplataforma\Cliente\app_movil\assets\icon\icon.png"

try:
    img = Image.open(ico_path)
    img.save(png_path, format='PNG')
    print(f"Successfully converted {ico_path} to {png_path}")
except Exception as e:
    print(f"Error converting icon: {e}")
