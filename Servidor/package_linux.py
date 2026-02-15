import os
import zipfile
import shutil

def package_for_linux():
    source_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = "SIGEP_Server_Linux_Portable.zip"
    
    # Archivos y carpetas a incluir
    includes = [
        "main.py",
        "config.py",
        "requirements.txt",
        "run_linux.sh",
        "servidor.ico",
        "gui",
        "database",
        "services"
    ]
    
    # Archivos a excluir dentro de las carpetas incluidas
    excludes_extensions = [".pyc", ".pyo", ".pyd", ".DS_Store"]
    excludes_dirs = ["__pycache__"]

    print(f"Empaquetando para Linux en: {output_filename}...")

    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in includes:
            item_path = os.path.join(source_dir, item)
            
            if os.path.isfile(item_path):
                zipf.write(item_path, arcname=item)
                print(f"  Añadido: {item}")
            
            elif os.path.isdir(item_path):
                for root, dirs, files in os.walk(item_path):
                    # Filtrar directorios excluidos
                    dirs[:] = [d for d in dirs if d not in excludes_dirs]
                    
                    for file in files:
                        if any(file.endswith(ext) for ext in excludes_extensions):
                            continue
                            
                        file_path = os.path.join(root, file)
                        # Calcular ruta relativa para el zip
                        rel_path = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arcname=rel_path)
                        print(f"  Añadido: {rel_path}")
            else:
                print(f"  Advertencia: No se encontró {item}")

    print("\n¡Empaquetado completado!")
    print(f"Archivo generado: {os.path.join(source_dir, output_filename)}")

if __name__ == "__main__":
    package_for_linux()
