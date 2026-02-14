import sys
import os
import unittest
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'Desktop', 'Sistema Multiplataforma base', 'Sistema Multiplataforma', 'Servidor')))

try:
    from services.employee_service import EmployeeService
    from services.attendance_service import AttendanceService
    from database.models import init_db, Empleado
    import config
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

# Configure logging to console for checking
logging.basicConfig(level=logging.INFO)

class TestSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n--- Setting up Test Environment ---")
        # Use a test database if possible, but for now we'll use the main one carefully or just verify connections
        # Initialize DB
        init_db()
        print("Database initialized.")

    def test_01_config(self):
        print("\n--- Testing Configuration ---")
        self.assertTrue(hasattr(config, 'DATABASE_URL'))
        self.assertTrue(hasattr(config, 'SERVER_PORT'))
        print(f"Database URL: {config.DATABASE_URL}")

    def test_02_employee_crud(self):
        print("\n--- Testing Employee CRUD ---")
        # Create
        data = {
            "cedula": "99999999",
            "nombre": "Test User",
            "password": "123",
            "tipo_personal": "Docente",
            # Cargo and Horario are optional, testing without them first or with defaults if seeded
            "departamento": "Testing",
            "email": "test@example.com"
        }
        
        # Clean up if exists
        existing = EmployeeService.get_employee_by_cedula("99999999")
        if existing:
            EmployeeService.delete_employee(existing.id)

        emp = EmployeeService.create_employee(data)
        self.assertIsNotNone(emp.id)
        self.assertEqual(emp.nombre, "Test User")
        self.assertEqual(emp.email, "test@example.com")
        print("Employee created.")

        # Read
        emp_read = EmployeeService.get_employee_by_id(emp.id)
        self.assertEqual(emp_read.cedula, "99999999")
        print("Employee read.")

        # Update
        emp_updated = EmployeeService.update_employee(emp.id, {"nombre": "Updated Test User", "telefono": "555-0000"})
        self.assertEqual(emp_updated.nombre, "Updated Test User")
        self.assertEqual(emp_updated.telefono, "555-0000")
        print("Employee updated.")

        # Delete
        result = EmployeeService.delete_employee(emp.id)
        self.assertTrue(result)
        
        emp_deleted = EmployeeService.get_employee_by_id(emp.id)
        self.assertIsNone(emp_deleted)
        print("Employee deleted.")

    def test_03_attendance(self):
        print("\n--- Testing Attendance ---")
        # Clean up if exists
        existing = EmployeeService.get_employee_by_cedula("88888888")
        if existing:
            EmployeeService.delete_employee(existing.id)

        # Need an employee first
        data = {
            "cedula": "88888888",
            "nombre": "Attendance Tester",
            "password": "123",
            "tipo_personal": "Obrero",
            # Cargo removed
            "departamento": "Maintenance"
        }
        emp = EmployeeService.create_employee(data)

        # Register Attendance
        result = AttendanceService.register_attendance("88888888")
        self.assertEqual(result['empleado'], "Attendance Tester")
        print("Attendance registered.")

        # Get Recent
        recent = AttendanceService.get_recent_attendance(10)
        self.assertTrue(len(recent) > 0)
        found = False
        for reg in recent:
            if reg.empleado.cedula == "88888888":
                found = True
                break
        self.assertTrue(found)
        print("Attendance found in recent logs.")

        # Cleanup
        EmployeeService.delete_employee(emp.id)
        # Note: Attendance records remain, which is expected behavior for logs

if __name__ == '__main__':
    unittest.main()
