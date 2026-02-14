from database.models import get_db_session, Asistencia, Empleado
from sqlalchemy.orm import joinedload
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AttendanceService:
    @staticmethod
    def register_attendance(cedula):
        with get_db_session() as db:
            empleado = db.query(Empleado).filter(Empleado.cedula == cedula).first()
            
            if not empleado:
                logger.warning(f"Intento de asistencia fallido: Cédula {cedula} no encontrada.")
                raise ValueError("Empleado no encontrado")

            nueva_asistencia = Asistencia(empleado_id=empleado.id)
            db.add(nueva_asistencia)
            db.commit()
            db.refresh(nueva_asistencia)

            logger.info(f"Asistencia registrada: {empleado.nombre} - {datetime.now()}")
            
            return {
                "empleado": empleado.nombre, 
                "hora": nueva_asistencia.fecha_hora.strftime("%H:%M:%S")
            }

    @staticmethod
    def get_recent_attendance(limit=50):
        with get_db_session() as db:
            # Usamos joinedload para cargar la relación 'empleado' y sus sub-relaciones ansiosamente
            return db.query(Asistencia).options(
                joinedload(Asistencia.empleado).joinedload(Empleado.cargo_rel)
            ).order_by(Asistencia.fecha_hora.desc()).limit(limit).all()
    
    @staticmethod
    def get_todays_attendance():
        start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        with get_db_session() as db:
            return db.query(Asistencia).options(joinedload(Asistencia.empleado)).filter(Asistencia.fecha_hora >= start_of_day).all()
