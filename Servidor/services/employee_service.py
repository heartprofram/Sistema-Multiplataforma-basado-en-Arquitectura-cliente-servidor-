from database.models import get_db_session, Empleado, Cargo, Horario, DetalleDocente
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger(__name__)

class EmployeeService:
    @staticmethod
    def get_all_employees():
        with get_db_session() as db:
            # Cargamos relaciones para mostrar nombres en UI
            return db.query(Empleado).options(
                joinedload(Empleado.cargo_rel), 
                joinedload(Empleado.horario_rel),
                joinedload(Empleado.detalle_docente)
            ).all()

    @staticmethod
    def get_employee_by_id(emp_id):
        with get_db_session() as db:
            return db.query(Empleado).options(
                joinedload(Empleado.cargo_rel), 
                joinedload(Empleado.horario_rel),
                joinedload(Empleado.detalle_docente)
            ).filter(Empleado.id == emp_id).first()

    @staticmethod
    def get_employee_by_cedula(cedula):
        with get_db_session() as db:
            return db.query(Empleado).options(
                joinedload(Empleado.cargo_rel), 
                joinedload(Empleado.horario_rel),
                joinedload(Empleado.detalle_docente)
            ).filter(Empleado.cedula == cedula).first()

    @staticmethod
    def create_employee(data):
        with get_db_session() as db:
            try:
                # Verificar si ya existe
                existing = db.query(Empleado).filter(Empleado.cedula == data['cedula']).first()
                if existing:
                    raise ValueError(f"Ya existe un empleado con la cédula {data['cedula']}")

                # Separar datos de detalle docente si existen
                detalle_data = data.pop('detalle_docente', None)

                new_emp = Empleado(**data)
                db.add(new_emp)
                db.commit()
                db.refresh(new_emp)
                
                # Crear detalle docente si corresponde
                if detalle_data and (new_emp.tipo_personal == "Docente" or detalle_data):
                    detalle = DetalleDocente(empleado_id=new_emp.id, **detalle_data)
                    db.add(detalle)
                    db.commit()

                logger.info(f"Empleado creado: {new_emp.nombre} ({new_emp.cedula})")
                return new_emp
            except IntegrityError as e:
                logger.error(f"Error de integridad al crear empleado: {e}")
                raise ValueError("Error de base de datos al crear empleado.")
            except Exception as e:
                logger.error(f"Error desconocido al crear empleado: {e}")
                raise

    @staticmethod
    def update_employee(emp_id, data):
        with get_db_session() as db:
            emp = db.query(Empleado).filter(Empleado.id == emp_id).first()
            if not emp:
                raise ValueError("Empleado no encontrado")

            # Separar y actualizar detalle docente
            detalle_data = data.pop('detalle_docente', None)
            
            for key, value in data.items():
                if hasattr(emp, key):
                    setattr(emp, key, value)
            
            if detalle_data:
                # Buscar si ya tiene detalle
                detalle = db.query(DetalleDocente).filter(DetalleDocente.empleado_id == emp.id).first()
                if detalle:
                    # Actualizar existente
                    for k, v in detalle_data.items():
                        if hasattr(detalle, k):
                            setattr(detalle, k, v)
                else:
                    # Crear nuevo
                    nuevo_detalle = DetalleDocente(empleado_id=emp.id, **detalle_data)
                    db.add(nuevo_detalle)

            db.commit()
            db.refresh(emp)
            logger.info(f"Empleado actualizado: {emp.nombre}")
            return emp

    @staticmethod
    def delete_employee(emp_id):
        with get_db_session() as db:
            emp = db.query(Empleado).filter(Empleado.id == emp_id).first()
            if emp:
                db.delete(emp)
                db.commit()
                logger.info(f"Empleado eliminado: ID {emp_id}")
                return True
            return False

    # --- MÉTODOS PARA CARGOS ---
    @staticmethod
    def get_all_cargos():
        with get_db_session() as db:
            return db.query(Cargo).all()

    @staticmethod
    def create_cargo(nombre, descripcion=None):
        with get_db_session() as db:
            if db.query(Cargo).filter(Cargo.nombre == nombre).first():
                return None # Ya existe
            
            nuevo_cargo = Cargo(nombre=nombre, descripcion=descripcion)
            db.add(nuevo_cargo)
            db.commit()
            db.refresh(nuevo_cargo)
            return nuevo_cargo

    # --- MÉTODOS PARA HORARIOS ---
    @staticmethod
    def get_all_horarios():
        with get_db_session() as db:
            return db.query(Horario).all()

    @staticmethod
    def create_horario(nombre, entrada, salida, dias):
        with get_db_session() as db:
            if db.query(Horario).filter(Horario.nombre == nombre).first():
                return None
            
            nuevo_horario = Horario(nombre=nombre, entrada=entrada, salida=salida, dias=dias)
            db.add(nuevo_horario)
            db.commit()
            db.refresh(nuevo_horario)
            return nuevo_horario

    @staticmethod
    def seed_data():
        """Crea datos por defecto si no existen"""
        if not EmployeeService.get_all_cargos():
            EmployeeService.create_cargo("Docente", "Personal de enseñanza")
            EmployeeService.create_cargo("Administrativo", "Personal de oficina")
            EmployeeService.create_cargo("Obrero", "Personal de mantenimiento")
            EmployeeService.create_cargo("Directivo", "Personal de dirección")
            
        if not EmployeeService.get_all_horarios():
            # Actualizado a Diurno y Nocturno por solicitud
            EmployeeService.create_horario("Diurno", "07:00", "12:00", "L-V")
            EmployeeService.create_horario("Nocturno", "18:00", "22:00", "L-V")
