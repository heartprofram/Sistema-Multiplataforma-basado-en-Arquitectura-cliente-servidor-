from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import config
from contextlib import contextmanager

# 1. Configuración de la Base de Datos
# connect_args es necesario para SQLite en aplicaciones multihilo (como esta)
engine = create_engine(config.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Context Manager para manejar sesiones de forma segura
@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close() # Asegura que la sesión se cierre siempre

# --- NUEVOS MODELOS NORMALIZADOS ---

class Cargo(Base):
    __tablename__ = "cargos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False) # Ej: Docente, Administrativo
    descripcion = Column(String, nullable=True)
    
    empleados = relationship("Empleado", back_populates="cargo_rel")

class Horario(Base):
    __tablename__ = "horarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False) # Ej: "Matutino A"
    entrada = Column(String, nullable=False) # "08:00"
    salida = Column(String, nullable=False) # "12:00"
    dias = Column(String, nullable=False) # "L-V"
    
    empleados = relationship("Empleado", back_populates="horario_rel")

# 2. Modelo de Empleado (Perfil Completo - Normalizado)
class Empleado(Base):
    __tablename__ = "empleados"
    
    # --- Identificación y Acceso ---
    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    password = Column(String, nullable=False, default="1234") 
    
    # --- Datos Personales (Nuevos) ---
    telefono = Column(String, nullable=True)
    email = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    
    # Nuevos campos personales
    fecha_nacimiento = Column(String, nullable=True)
    lugar_nacimiento = Column(String, nullable=True)
    estado_civil = Column(String, nullable=True) # Soltero, Casado...
    genero = Column(String, nullable=True) # M, F
    nacionalidad = Column(String, nullable=True) # V, E
    
    # --- Datos Laborales ---
    departamento = Column(String, nullable=True) # Ej: "Ciencias", "RRHH"
    tipo_personal = Column(String, nullable=False) # "Docente", "Obrero" (Categoría macro)
    
    # Relaciones Foreign Keys
    cargo_id = Column(Integer, ForeignKey("cargos.id"), nullable=True)
    horario_id = Column(Integer, ForeignKey("horarios.id"), nullable=True)
    
    # Datos Académicos (Texto libre para detalles extra - MANTENIDO POR COMPATIBILIDAD)
    materias_asignadas = Column(Text, nullable=True) 
    
    fecha_registro = Column(DateTime, default=datetime.now)

    # --- Relaciones ORM ---
    cargo_rel = relationship("Cargo", back_populates="empleados")
    horario_rel = relationship("Horario", back_populates="empleados")
    asistencias = relationship("Asistencia", back_populates="empleado")
    
    # Nueva relación 1 a 1 con detalles de docente
    detalle_docente = relationship("DetalleDocente", uselist=False, back_populates="empleado", cascade="all, delete-orphan")

# 2.1 Modelo Detalle Docente (Nuevo)
class DetalleDocente(Base):
    __tablename__ = "detalles_docente"
    
    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(Integer, ForeignKey("empleados.id"), unique=True, nullable=False)
    
    # Campos solicitados
    nucleo_extension = Column(String, nullable=True)
    fecha_ingreso = Column(String, nullable=True) # Guardamos como string por facilidad "dd-mm-yyyy"
    perfil_academico = Column(String, nullable=True)
    categoria_actual = Column(String, nullable=True) # Instructor, Asistente, Agregado...
    condicion_dedicacion = Column(String, nullable=True) # Contratado/TC, Ordinario/TV...
    cargo_colateral = Column(String, nullable=True)
    carrera = Column(String, nullable=True)
    semestre = Column(String, nullable=True)
    horas_academicas = Column(Integer, nullable=True)
    asignaturas = Column(Text, nullable=True) # Lista larga
    observaciones = Column(Text, nullable=True)
    
    # Relación inversa
    empleado = relationship("Empleado", back_populates="detalle_docente")

# 3. Modelo de Asistencia (Sin cambios mayores)
class Asistencia(Base):
    __tablename__ = "asistencias"

    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(Integer, ForeignKey("empleados.id"))
    fecha_hora = Column(DateTime, default=datetime.now)
    
    # Relación inversa
    empleado = relationship("Empleado", back_populates="asistencias")

# 4. Función de Inicialización
def init_db():
    """Crea las tablas en la base de datos si no existen"""
    Base.metadata.create_all(bind=engine)
