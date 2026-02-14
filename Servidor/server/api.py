from fastapi import FastAPI, HTTPException, Depends
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
import socket
from database.models import init_db
from services.attendance_service import AttendanceService
from services.employee_service import EmployeeService
import config

app = FastAPI(title=config.APP_TITLE)

# Aseguramos que la BD exista al arrancar
init_db()

# --- MODELOS DE DATOS (Lo que llega del celular) ---
class LoginRequest(BaseModel):
    cedula: str
    password: str

class AsistenciaRequest(BaseModel):
    cedula: str

# ==========================================
# RUTAS DEL SISTEMA
# ==========================================

@app.get("/")
def home():
    return {"mensaje": "Servidor SIGEP Activo"}

@app.get("/config/ip")
def get_server_ip():
    try:
        # Truco para obtener IP real
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return {"ip": ip}
    except:
        return {"ip": "127.0.0.1"}

# ==========================================
# RUTAS DE LA APP MÓVIL
# ==========================================

@app.post("/login")
def login(data: LoginRequest):
    """ Valida usuario y contraseña """
    # Usamos el servicio de empleados
    empleado = EmployeeService.get_employee_by_cedula(data.cedula)
    
    # Verificamos si existe y si la contraseña coincide
    if not empleado or empleado.password != data.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    return {
        "status": "ok",
        "id": empleado.id,
        "nombre": empleado.nombre,
        "cedula": empleado.cedula,  # <--- IMPORTANTE: Devolvemos la cédula
        "tipo": empleado.tipo_personal
    }

@app.post("/marcar_asistencia")
def marcar(data: AsistenciaRequest):
    """ Registra la entrada/salida """
    try:
        resultado = AttendanceService.register_attendance(data.cedula)
        return {"status": "exito", **resultado}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/empleado/{cedula}/detalle")
def obtener_detalle(cedula: str):
    """ Datos para la pantalla Home del celular """
    empleado = EmployeeService.get_employee_by_cedula(cedula)
    if not empleado:
        raise HTTPException(404, "No encontrado")
    
    cargo_nombre = empleado.cargo_rel.nombre if empleado.cargo_rel else "Sin Cargo"
    horario_nombre = empleado.horario_rel.nombre if empleado.horario_rel else "Sin Horario"
    horario_detalles = f"{empleado.horario_rel.entrada} - {empleado.horario_rel.salida} ({empleado.horario_rel.dias})" if empleado.horario_rel else "Por definir"

    return {
        "nombre": empleado.nombre,
        "cedula": empleado.cedula,
        "tipo": empleado.tipo_personal,
        "cargo": cargo_nombre,
        "departamento": empleado.departamento or "General",
        "informacion_personal": {
            "telefono": empleado.telefono,
            "email": empleado.email,
            "direccion": empleado.direccion
        },
        "academico": {
            "materias": empleado.materias_asignadas,
            "horario_nombre": horario_nombre,
            "horario_horas": horario_detalles
        }
    }
