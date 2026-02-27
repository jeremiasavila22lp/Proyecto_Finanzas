from fastapi import FastAPI, HTTPException, Header, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from gestor_db import GestorConPresupuesto
from pydantic import BaseModel, Field
import logging
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from dotenv import load_dotenv
load_dotenv()

# Configuración de JWT
SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto_seguridad")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

def crear_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Genera un token JWT firmado"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Modelo para CREAR gastos (sin id ni fecha, se generan automáticamente)

class GastoCreate(BaseModel):
    monto: float = Field(gt=0, description="Monto del gasto, debe ser mayor a 0")
    categoria: str = Field(min_length=1, description="Categoría del gasto")
    descripcion: str = Field(default="Sin descripcion", description="Descripción opcional del gasto")

# Modelo para MOSTRAR gastos (con todos los campos)
class GastoResponse(BaseModel):
    id: int
    monto: float
    categoria: str
    fecha: str
    descripcion: str

# Modelo para el RESUMEN de gastos
class ResumenGastos(BaseModel):
    total_general: float
    por_categoria: dict[str, float]
    presupuesto_limite: float
    saldo_disponible: float
    porcentaje_usado: float
    nivel_alerta: str  # 'seguro', 'advertencia', 'peligro'
    balance_neto: float

# ============ MODELOS DE AUTENTICACIÓN ============

class UsuarioRegistro(BaseModel):
    nombre: str = Field(min_length=2, description="Nombre del usuario")
    email: str = Field(min_length=5, description="Email del usuario")
    password: str = Field(min_length=6, description="Contraseña (mínimo 6 caracteres)")

class UsuarioLogin(BaseModel):
    email: str
    password: str

class RespuestaAuth(BaseModel):
    mensaje: str
    token: str
    usuario: dict
    token_type: str = "bearer"

class PresupuestoUpdate(BaseModel):
    nuevo_limite: float = Field(gt=0, description="Nuevo límite de presupuesto mensual")


app = FastAPI(title="FinanzasPro API")
security = HTTPBearer()
DATABASE_NAME = os.getenv("DATABASE_URL", "FinanzasPro.db")
mi_gestor = GestorConPresupuesto(DATABASE_NAME)

@app.get("/")
def inicio():
    """Redirige a la interfaz web"""
    return RedirectResponse(url="/static/login.html")

# ============ ENDPOINTS DE AUTENTICACIÓN ============

@app.post("/auth/registro", status_code=201)
def registrar_usuario(datos: UsuarioRegistro):
    """
    Registra un nuevo usuario y devuelve un token JWT.
    """
    exito, resultado = mi_gestor.registrar_usuario(
        nombre=datos.nombre,
        email=datos.email,
        password=datos.password
    )
    
    if exito:
        # Generar token JWT con el ID del usuario
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = crear_access_token(
            data={"sub": str(resultado)}, 
            expires_delta=access_token_expires
        )
        
        usuario = mi_gestor.obtener_usuario_por_id(resultado)
        
        return {
            "mensaje": "Usuario registrado exitosamente",
            "token": token,
            "token_type": "bearer",
            "usuario": usuario
        }
    else:
        raise HTTPException(status_code=400, detail=resultado)

@app.post("/auth/login")
def login_usuario(datos: UsuarioLogin):
    """
    Inicia sesión y devuelve un token JWT.
    """
    exito, resultado = mi_gestor.verificar_login(
        email=datos.email,
        password=datos.password
    )
    
    if exito:
        # Generar token JWT
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = crear_access_token(
            data={"sub": str(resultado['id'])}, 
            expires_delta=access_token_expires
        )
        
        return {
            "mensaje": "Login exitoso",
            "token": token,
            "token_type": "bearer",
            "usuario": resultado
        }
    else:
        raise HTTPException(status_code=401, detail=resultado)

@app.post("/auth/logout")
def logout_usuario():
    """
    Con JWT el logout se maneja en el cliente (eliminando el token).
    Este endpoint es informativo.
    """
    return {"mensaje": "Para cerrar sesión, elimine el token del almacenamiento local"}

# ============ SEGURIDAD Y JWT ============

def obtener_usuario_actual(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """
    Dependencia para validar la identidad. 
    Soporta tanto Token JWT largo como Código Numérico Corto (6 dígitos).
    """
    token = credentials.credentials
    
    # 1. Intentar como Código Numérico Corto (6 dígitos)
    if token.isdigit() and len(token) == 6:
        user_id = mi_gestor.obtener_usuario_por_codigo(token)
        if user_id:
            return user_id
        raise HTTPException(status_code=401, detail="Código de acceso incorrecto o expirado")

    # 2. Intentar como Token JWT Estándar
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(status_code=401, detail="Token inválido: falta ID de usuario")
        return int(user_id_str)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido, expirado o formato incorrecto")
    except ValueError:
        raise HTTPException(status_code=401, detail="ID de usuario corrupto")

@app.put("/usuario/presupuesto", status_code=200)
def actualizar_presupuesto(datos: PresupuestoUpdate, user_id: int = Depends(obtener_usuario_actual)):
    """
    Actualiza el presupuesto mensual del usuario autenticado.
    """
    try:
        exito = mi_gestor.actualizar_presupuesto_usuario(user_id, datos.nuevo_limite)
        if exito:
            return {"mensaje": "Presupuesto actualizado correctamente", "nuevo_limite": datos.nuevo_limite}
        else:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el presupuesto")
    except Exception as e:
        logging.error(f"Error al actualizar presupuesto: {e}")
        raise HTTPException(status_code=500, detail="Error interno al actualizar el presupuesto")

# ============ ENDPOINTS DE GASTOS ============

@app.post("/gastos", status_code=201)
def crear_gasto(gasto: GastoCreate, user_id: int = Depends(obtener_usuario_actual)):
    """
    Crea un nuevo gasto en la base de datos.
    
    - **monto**: Cantidad gastada (debe ser mayor a 0)
    - **categoria**: Categoría del gasto (ej: comida, transporte)
    - **descripcion**: Descripción opcional del gasto
    """
    try:
        # Llamar al método con el ORDEN CORRECTO de parámetros
        exito = mi_gestor.agregar_gasto(
            monto=gasto.monto,
            categoria=gasto.categoria,
            descripcion=gasto.descripcion,
            usuario_id=user_id
        )
        
        if exito:
            return {
                "mensaje": "Gasto agregado correctamente",
                "datos": {
                    "monto": gasto.monto,
                    "categoria": gasto.categoria,
                    "descripcion": gasto.descripcion
                }
            }
        else:
            # Si agregar_gasto retorna False, es porque excedió el presupuesto
            raise HTTPException(
                status_code=400, 
                detail="No se pudo agregar el gasto. Posiblemente excede el presupuesto."
            )
    except HTTPException:
        # Re-lanzar las excepciones HTTP
        raise
    except Exception as e:
        logging.error(f"Error al agregar gasto: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Error interno al agregar el gasto"
        )


@app.delete("/gastos/{gasto_id}", status_code=200)
def eliminar_gasto(gasto_id: int, user_id: int = Depends(obtener_usuario_actual)):
    """
    Elimina un gasto específico por su ID.
    """
    try:
        exito = mi_gestor.eliminar_gasto(gasto_id, usuario_id=user_id)
        
        if exito:
            logging.info(f"API: Gasto {gasto_id} eliminado exitosamente por usuario {user_id}")
            return {
                "mensaje": f"Gasto con ID {gasto_id} ha sido eliminado",
                "id_eliminado": gasto_id
            }
        else:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró el gasto con ID {gasto_id} o no tienes permiso para eliminarlo"
            )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error al eliminar gasto {gasto_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno al eliminar el gasto"
        )

@app.put("/gastos/{gasto_id}", status_code=200)
def actualizar_gasto(gasto_id: int, gasto_actualizado: GastoCreate, user_id: int = Depends(obtener_usuario_actual)):
    """
    Actualiza un gasto existente.
    """
    try:
        # Primero obtener el gasto actual para mostrar qué cambió
        # NOTA: obtener_todos_los_gastos ahora filtra por usuario, así que esto también valida propiedad
        gastos_actuales = mi_gestor.obtener_todos_los_gastos(user_id)
        gasto_anterior = next((g for g in gastos_actuales if g['id'] == gasto_id), None)
        
        if not gasto_anterior:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró el gasto con ID {gasto_id} o no tienes permiso"
            )
        
        # Actualizar el gasto con fecha actual
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        exito = mi_gestor.actualizar_gasto(
            id_gasto=gasto_id,
            nuevo_monto=gasto_actualizado.monto,
            categoria=gasto_actualizado.categoria,
            descripcion=gasto_actualizado.descripcion,
            fecha=fecha_actual,
            usuario_id=user_id
        )
        
        if exito:
            logging.info(f"API: Gasto {gasto_id} actualizado exitosamente")
            return {
                "mensaje": f"Gasto {gasto_id} actualizado correctamente",
                "gasto_id": gasto_id,
                "datos_anteriores": {
                    "monto": gasto_anterior['monto'],
                    "categoria": gasto_anterior['categoria'],
                    "descripcion": gasto_anterior['descripcion'],
                    "fecha": gasto_anterior['fecha']
                },
                "datos_nuevos": {
                    "monto": gasto_actualizado.monto,
                    "categoria": gasto_actualizado.categoria,
                    "descripcion": gasto_actualizado.descripcion,
                    "fecha": fecha_actual
                }
            }
        else:
            raise HTTPException(
                status_code=400,
                detail="No se pudo actualizar el gasto"
            )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error al actualizar gasto {gasto_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno al actualizar el gasto"
        ) 

@app.get("/gastos", response_model=list[GastoResponse])
def listar_gastos(categorias: list[str] = Query(None, description="Categoría para filtrar los gastos"), user_id: int = Depends(obtener_usuario_actual)):
    """
    Obtiene los gastos de la base de datos del usuario autenticado.
    """
    try:
        # 1. Obtener solo los gastos del usuario autenticado
        todos_los_gastos = mi_gestor.obtener_todos_los_gastos(user_id)
        
        # 2. Si hay filtro, aplicarlo en memoria
        if categorias:
            # Filtramos la lista ignorando mayúsculas/minúsculas
            cats_mn = [c.lower() for c in categorias]
            gastos_filtrados = [
                gasto for gasto in todos_los_gastos if gasto['categoria'].lower() in cats_mn
            ]
            return gastos_filtrados
        
        # 3. Si no hay filtro, devolver todo
        return todos_los_gastos

    except Exception as e:
        logging.error(f"Error al listar gastos: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener los gastos")

@app.get("/gastos/exportar/csv")
def exportar_gastos_csv(user_id: int = Depends(obtener_usuario_actual)):
    """
    Exporta los gastos del usuario en formato CSV
    """
    from fastapi.responses import StreamingResponse
    import io
    import csv
    
    # Obtener gastos del usuario
    gastos = mi_gestor.obtener_todos_los_gastos(user_id)
    
    # Crear archivo CSV en memoria
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Escribir encabezados
    writer.writerow(['ID', 'Fecha', 'Descripción', 'Categoría', 'Monto'])
    
    # Escribir datos
    for gasto in gastos:
        writer.writerow([
            gasto['id'],
            gasto['fecha'],
            gasto['descripcion'],
            gasto['categoria'],
            f"${gasto['monto']:.2f}"
        ])
    
    # Preparar respuesta
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=gastos_{datetime.now().strftime('%Y%m%d')}.csv"
        }
    )

@app.get("/gastos/resumen", response_model=ResumenGastos)
def obtener_resumen(user_id: int = Depends(obtener_usuario_actual)):
    """
    Obtiene un resumen financiero completo del usuario autenticado.
    """
    try: 
        return mi_gestor.obtener_resumen(user_id)
    except Exception as e:
        logging.error(f"Error al obtener resumen: {e}")
        raise HTTPException(status_code=500, detail="Error al generar el resumen")

@app.get("/gastos/comparacion-presupuesto")
def obtener_comparacion(user_id: int = Depends(obtener_usuario_actual)):
    """
    Obtiene comparación entre presupuesto y gastos por categoría
    """
    try:
        # Obtener gastos por categoría del usuario
        gastos_por_cat = mi_gestor.obtener_gastos_por_categoria(user_id)
        
        # Obtener presupuesto total del usuario
        presupuesto_total = mi_gestor.obtener_presupuesto_usuario(user_id)
        
        # Calcular presupuesto sugerido por categoría (distribución proporcional)
        total_gastado = sum(gastos_por_cat.values())
        
        presupuesto_por_categoria = {}
        if total_gastado > 0:
            for cat, gasto in gastos_por_cat.items():
                proporcion = gasto / total_gastado
                presupuesto_por_categoria[cat] = presupuesto_total * proporcion
        
        return {
            "categorias": list(gastos_por_cat.keys()),
            "gastos_reales": list(gastos_por_cat.values()),
            "presupuesto_sugerido": list(presupuesto_por_categoria.values())
        }
    except Exception as e:
        logging.error(f"Error en comparación de presupuesto: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener comparación")

@app.get("/gastos/diarios")
def obtener_gastos_diarios(user_id: int = Depends(obtener_usuario_actual)):
    """
    Obtiene el total de gastos agrupados por día
    """
    try:
        gastos_diarios = mi_gestor.obtener_gastos_por_dia(user_id)
        return {
            "fechas": list(gastos_diarios.keys()),
            "totales": list(gastos_diarios.values())
        }
    except Exception as e:
        logging.error(f"Error al obtener gastos diarios: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener gastos diarios")
        
@app.get("/gastos/reporte/pdf")
def generar_reporte_pdf(user_id: int = Depends(obtener_usuario_actual)):
    """Genera un reporte ejecutivo en PDF para el usuario"""
    filename = f"reporte_ejecutivo_{user_id}.pdf"
    
    # 1. Obtener datos
    gastos = mi_gestor.obtener_todos_los_gastos(user_id)
    resumen = mi_gestor.obtener_resumen(user_id) 
    usuario = mi_gestor.obtener_usuario_por_id(user_id)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 2. Configurar el documento
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = [] 
    styles = getSampleStyleSheet()
    
    # Título
    story.append(Paragraph(f"Reporte Ejecutivo de Gastos - FinanzasPro", styles['Title']))
    story.append(Paragraph(f"Usuario: {usuario['nombre']} | Fecha: {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Tabla de Resumen
    data_resumen = [
        ["Concepto", "Valor"],
        ["Total Gastado", f"${resumen['total_general']:,.2f}"],
        ["Presupuesto Mensual", f"${resumen['presupuesto_limite']:,.2f}"],
        ["Saldo Disponible", f"${resumen['saldo_disponible']:,.2f}"],
        ["Nivel de Alerta", resumen['nivel_alerta'].upper()]
    ]
    t_resumen = Table(data_resumen, colWidths=[200, 100])
    t_resumen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(Paragraph("Resumen Financiero", styles['Heading2']))
    story.append(t_resumen)
    story.append(Spacer(1, 20))
    
    # Tabla de Gastos Detallada
    story.append(Paragraph("Desglose de Gastos", styles['Heading2']))
    data_gastos = [["Fecha", "Categoría", "Descripción", "Monto"]]
    for g in gastos[:20]: 
        data_gastos.append([g['fecha'], g['categoria'], g['descripcion'], f"${g['monto']:.2f}"])
    
    t_gastos = Table(data_gastos, colWidths=[80, 100, 200, 80])
    t_gastos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 9)
    ]))
    story.append(t_gastos)
    
    # 3. Construir PDF
    doc.build(story)
    
    return FileResponse(filename, filename=filename, media_type='application/pdf')

# Montamos la carpeta static al final para evitar conflictos con las rutas de la API
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
