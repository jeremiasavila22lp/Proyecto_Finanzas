from fastapi import FastAPI
from gestor_db import GestorConPresupuesto
from pydantic import BaseModel, Field

class Gasto(BaseModel):
    id: int
    fecha: str
    categoria: str
    monto: float = Field(gt=0)
    descripcion: str = "Sin descripcion"

app = FastAPI(title="FinanzasPro API")
mi_gestor = GestorConPresupuesto("FinanzasPro.db")

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la API de FinanzasPro"}

@app.get("/gastos")
def listar_gastos():
    try:
        datos = mi_gestor.obtener_todos_los_gastos()
        return datos
    except Exception as e:
        return {"error": str(e)}

@app.post("/gastos")
def crear_gasto(gasto: Gasto):
    try:
        resultado = mi_gestor.agregar_gasto(
            gasto.fecha,
            gasto.categoria, 
            gasto.monto, 
            gasto.descripcion)
        return {"mensaje": "Gasto agregado correctamente"}
    except Exception as e:
        import logging
        logging.error(f"Error al agregar gasto: {e}")
        return {"error": "No se pudo agregar el gasto"}