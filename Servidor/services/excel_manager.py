from openpyxl import Workbook
from datetime import datetime
from database.models import SessionLocal, Asistencia
import os

def exportar_excel():
    db = SessionLocal()
    try:
        registros = db.query(Asistencia).all()
        
        if not registros:
            return "No hay datos para exportar."

        # 1. Crear el libro de Excel y la hoja activa
        wb = Workbook()
        ws = wb.active
        ws.title = "Asistencias"

        # 2. Crear los Encabezados (Negrita no es estrictamente necesario, pero mantenemos simple)
        encabezados = ["ID Asistencia", "Empleado", "Cédula", "Cargo", "Fecha", "Hora"]
        ws.append(encabezados)

        # 3. Llenar los datos fila por fila
        for reg in registros:
            if reg.empleado:
                ws.append([
                    reg.id,
                    reg.empleado.nombre,
                    reg.empleado.cedula,
                    reg.empleado.cargo_rel.nombre if reg.empleado.cargo_rel else "Sin Cargo",
                    reg.fecha_hora.strftime("%d/%m/%Y"),
                    reg.fecha_hora.strftime("%H:%M:%S")
                ])
            else:
                ws.append([
                    reg.id,
                    "Desconocido",
                    "---",
                    "---",
                    reg.fecha_hora.strftime("%d/%m/%Y"),
                    reg.fecha_hora.strftime("%H:%M:%S")
                ])
        
        # 4. Guardar archivo
        nombre_archivo = f"reporte_asistencia_{datetime.now().strftime('%Y-%m-%d_%H%M')}.xlsx"
        wb.save(nombre_archivo)
        
        return os.path.abspath(nombre_archivo)

    except Exception as e:
        return f"❌ Error al guardar: {e}"
    finally:
        db.close()