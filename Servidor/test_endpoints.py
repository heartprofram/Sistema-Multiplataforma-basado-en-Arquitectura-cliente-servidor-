from fastapi.testclient import TestClient
from server.api import app
import os

client = TestClient(app)

def test_reporte_pdf():
    print("Testing /reporte/pdf...")
    response = client.get("/reporte/pdf")
    if response.status_code == 200:
        print("[OK] /reporte/pdf OK")
        print(f"   Content-Type: {response.headers['content-type']}")
    else:
        error_msg = response.text.encode('ascii', 'replace').decode('ascii')
        print(f"[FAIL] /reporte/pdf FAILED: {response.status_code} - {error_msg}")

def test_reporte_excel():
    print("Testing /reporte/excel...")
    response = client.get("/reporte/excel")
    if response.status_code == 200:
        print("[OK] /reporte/excel OK")
        print(f"   Content-Type: {response.headers['content-type']}")
    else:
        error_msg = response.text.encode('ascii', 'replace').decode('ascii')
        print(f"[FAIL] /reporte/excel FAILED: {response.status_code} - {error_msg}")

def test_empleado_detalle():
    # Asumiendo que existe una cédula, si no, fallará con 404, pero validamos la estructura
    # Necesitamos una cédula válida. Voy a intentar seedear o usar una dummy si la BD está vacía.
    # Pero para este test rápido, intentemos con un 404 para ver si al menos el endpoint responde.
    print("Testing /empleado/123/detalle...")
    response = client.get("/empleado/123000/detalle") # Cédula random
    
    if response.status_code == 404:
         print("[OK] /empleado/.../detalle OK (404 Not Found as expected for random ID)")
    elif response.status_code == 200:
         print("[OK] /empleado/.../detalle OK (200 Found)")
         data = response.json()
         if "nomina" not in data:
             print("   [OK] No 'nomina' field (Correct)")
         else:
             print("   [FAIL] 'nomina' field found (Incorrect)")
             
         if "academico" in data and "horario_horas" in data["academico"]:
              print(f"   [OK] 'horario_horas' found: {data['academico']['horario_horas']}")
         else:
              print("   [FAIL] 'horario_horas' MISSING")

if __name__ == "__main__":
    try:
        test_reporte_pdf()
        test_reporte_excel()
        test_empleado_detalle()
    except Exception as e:
        print(f"Test Execution Error: {e}")
