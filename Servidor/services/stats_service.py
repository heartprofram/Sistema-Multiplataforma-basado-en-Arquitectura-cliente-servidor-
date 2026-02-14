from datetime import datetime, timedelta
from database.models import get_db_session, Empleado, Asistencia

class StatsService:
    @staticmethod
    def calculate_stats(start_str: str, end_str: str):
        """
        Calcula la efectividad de asistencia para todos los empleados en un rango de fechas.
        start_str, end_str: "YYYY-MM-DD"
        """
        try:
            start_date = datetime.strptime(start_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        except ValueError:
            return {"error": "Formato de fecha incorrecto. Use YYYY-MM-DD"}

        # Calcular días hábiles (Lunes a Viernes) en el rango
        business_days = 0
        current = start_date
        while current <= end_date:
            if current.weekday() < 5: # 0=Lunes, 4=Viernes
                business_days += 1
            current += timedelta(days=1)

        if business_days == 0:
            return {"error": "No hay días hábiles en el rango seleccionado"}

        stats = []

        with get_db_session() as db:
            empleados = db.query(Empleado).all()
            
            for emp in empleados:
                # Contar asistencias únicas por día en el rango
                # (Si marca entrada y salida el mismo día, cuenta como 1 asistencia para la efectividad)
                attendance_count = db.query(Asistencia).filter(
                    Asistencia.empleado_id == emp.id,
                    Asistencia.fecha_hora >= start_date,
                    Asistencia.fecha_hora <= end_date
                ).count()

                # Ajuste simple: Asumimos 1 marca por día para asistencia perfecta
                # Si el sistema requiere entrada y salida, se podría dividir por 2 o buscar días únicos
                # Para este MVP, contamos registros crudos pero limitados a business_days para no exceder 100%
                # Una mejor aproximación es contar DÍAS únicos con asistencia
                
                days_attended = db.query(Asistencia.fecha_hora).filter(
                    Asistencia.empleado_id == emp.id,
                    Asistencia.fecha_hora >= start_date,
                    Asistencia.fecha_hora <= end_date
                ).distinct().count()
                
                # Sin embargo, SQLite con SQLAlchemy a veces complica el distinct de fechas
                # Hacemos una consulta cruda de todos los registros y filtramos en python por set de fechas
                raw_records = db.query(Asistencia.fecha_hora).filter(
                    Asistencia.empleado_id == emp.id,
                    Asistencia.fecha_hora >= start_date,
                    Asistencia.fecha_hora <= end_date
                ).all()
                
                unique_days = set(r.fecha_hora.date() for r in raw_records)
                days_present = len(unique_days)

                effectiveness = (days_present / business_days) * 100
                effectiveness = min(effectiveness, 100.0) # Cap al 100%

                stats.append({
                    "id": emp.id,
                    "nombre": emp.nombre,
                    "cargo": emp.cargo_rel.nombre if emp.cargo_rel else "Sin Cargo",
                    "dias_habiles": business_days,
                    "asistencias": days_present,
                    "efectividad": round(effectiveness, 1)
                })

        return stats
