
import sys
import os
import traceback

print("Testing initialization...")

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.append(script_dir)
    
    print(f"Script dir: {script_dir}")
    print(f"Files in dir: {os.listdir(script_dir)}")

    from gestor_db import GestorConPresupuesto
    print("Import successful")

    db_path = os.path.join(script_dir, "FinanzasPro.db")
    mi_gestor = GestorConPresupuesto(db_path, 5000)
    print("Gestor initialized successfully")
    print(f"Total: {mi_gestor.obtener_total()}")

except Exception:
    traceback.print_exc()
