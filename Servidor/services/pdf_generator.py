from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
from database.models import SessionLocal, Asistencia
import os

def generar_pdf():
    db = SessionLocal()
    try:
        # 1. Consultar datos MIENTRAS la sesión está abierta
        registros = db.query(Asistencia).order_by(Asistencia.fecha_hora.desc()).all()

        if not registros:
            return "No hay datos para generar PDF."

        # Crear nombre de archivo
        nombre_archivo = f"ficha_asistencia_{datetime.now().strftime('%H%M%S')}.pdf"
        
        # 2. Crear el Canvas (La hoja en blanco)
        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        width, height = letter # Tamaño carta
        
        # 3. Encabezado
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Reporte Oficial de Asistencias - SIGEP")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 70, f"Generado el: {datetime.now().strftime('%d/%m/%Y a las %H:%M')}")
        
        # Línea separadora
        c.line(50, height - 80, width - 50, height - 80)

        # 4. Listar Datos
        y = height - 110 # Posición vertical inicial
        c.setFont("Courier", 10) 
        
        # Encabezados de columna
        header = f"{'FECHA':<12} {'HORA':<10} {'CÉDULA':<12} {'NOMBRE EMPLEADO'}"
        c.drawString(50, y, header)
        y -= 20 # Bajar renglón

        for reg in registros:
            if y < 50: # Si se acaba la hoja, crear nueva página
                c.showPage()
                y = height - 50
                c.setFont("Courier", 10)

            # AQUI OCURRÍA EL ERROR ANTES:
            # Ahora la sesión sigue viva, así que podemos leer 'reg.empleado.nombre' sin problemas
            fecha = reg.fecha_hora.strftime("%d/%m/%Y")
            hora = reg.fecha_hora.strftime("%H:%M:%S")
            if reg.empleado:
                nombre = reg.empleado.nombre
                cedula = reg.empleado.cedula
            else:
                nombre = "Desconocido"
                cedula = "---"
            
            linea = f"{fecha:<12} {hora:<10} {cedula:<12} {nombre}"
            c.drawString(50, y, linea)
            y -= 15 

        # 5. Guardar PDF
        c.save()
        
        # Obtener ruta absoluta para decirle al usuario dónde quedó
        return os.path.abspath(nombre_archivo)
        
    except Exception as e:
        return f"❌ Error al generar PDF: {e}"
    
    finally:
        # 6. ¡AHORA SÍ CERRAMOS LA CONEXIÓN! (Al final de todo)
        db.close()