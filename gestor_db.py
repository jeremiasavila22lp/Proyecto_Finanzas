import sqlite3
import psycopg2
import logging
from datetime import datetime
from typing import List, Tuple, Dict
from passlib.context import CryptContext
import threading
from psycopg2.extras import RealDictCursor
import os

# Configuración de Passlib para hashing seguro
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

class GestorGastos:
    def __init__(self, finanzas_bd):
        self.lock = threading.RLock()
        self.archivo_bd = finanzas_bd

        if finanzas_bd.startswith("postgres://") or finanzas_bd.startswith("postgresql://"):
            self.es_postgresql = True
            try:
                self.conexion = psycopg2.connect(finanzas_bd)
                self.cursor = self.conexion.cursor(cursor_factory=RealDictCursor) 
                print("[OK] Motor PostgreSQL (Neon) conectado.")
            except Exception as e:
                logging.error(f"Error de conexión a PostgreSQL: {e}")
                raise e
        else:
            self.es_postgresql = False
            self.conexion = sqlite3.connect(finanzas_bd, check_same_thread=False)
            self.conexion.row_factory = sqlite3.Row
            self.cursor = self.conexion.cursor()
            print("[OK] Motor SQLite Local conectado.")
        
        self.p = "%s" if self.es_postgresql else "?"
        self.serial_type = "SERIAL PRIMARY KEY" if self.es_postgresql else "INTEGER PRIMARY KEY AUTOINCREMENT"
        self.default_date = "CURRENT_TIMESTAMP" if self.es_postgresql else "CURRENT_TIMESTAMP"
        
        self._inicializar_tablas()

    def _inicializar_tablas(self):
        """Crea la estructura base si no existe"""
        # Tabla Usuarios
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS usuarios (
                id {self.serial_type},
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                fecha_creacion TEXT DEFAULT {self.default_date},
                presupuesto REAL DEFAULT 5000.0
            )
        """)
        
        # Tabla Gastos
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS gastos (
                id {self.serial_type},
                monto REAL,
                categoria TEXT,
                descripcion TEXT,
                fecha TEXT DEFAULT {self.default_date},
                usuario_id INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)
        self.conexion.commit()

    # ============ MÉTODOS DE USUARIO ============

    def registrar_usuario(self, nombre, email, password):
        try:
            password_hash = pwd_context.hash(password)
            if self.es_postgresql:
                self.cursor.execute(f"INSERT INTO usuarios (nombre, email, password_hash) VALUES (%s, %s, %s) RETURNING id", 
                                    (nombre, email, password_hash))
                user_id = self.cursor.fetchone()['id']
            else:
                self.cursor.execute(f"INSERT INTO usuarios (nombre, email, password_hash) VALUES (?, ?, ?)", 
                                    (nombre, email, password_hash))
                user_id = self.cursor.lastrowid
            self.conexion.commit()
            return (True, user_id)
        except (sqlite3.IntegrityError, psycopg2.IntegrityError):
            return (False, "El email ya está registrado")
        except Exception as e:
            return (False, str(e))

    def verificar_login(self, email, password):
        try:
            self.cursor.execute(f"SELECT * FROM usuarios WHERE email = {self.p}", (email,))
            usuario = self.cursor.fetchone()
            if not usuario: return (False, "Usuario no encontrado")
            
            usuario_dict = dict(usuario)
            if pwd_context.verify(password, usuario_dict['password_hash']):
                # No enviamos el hash al cliente por seguridad
                del usuario_dict['password_hash']
                return (True, usuario_dict)
            return (False, "Contraseña incorrecta")
        except Exception as e:
            return (False, str(e))

    def obtener_usuario_por_id(self, user_id):
        self.cursor.execute(f"SELECT id, nombre, email, presupuesto FROM usuarios WHERE id = {self.p}", (user_id,))
        res = self.cursor.fetchone()
        return dict(res) if res else None

    def obtener_presupuesto_usuario(self, user_id):
        self.cursor.execute(f"SELECT presupuesto FROM usuarios WHERE id = {self.p}", (user_id,))
        res = self.cursor.fetchone()
        if not res: return 5000.0
        return float(res['presupuesto']) if self.es_postgresql else float(res[0])

    def actualizar_presupuesto_usuario(self, user_id, nuevo_limite):
        try:
            self.cursor.execute(f"UPDATE usuarios SET presupuesto = {self.p} WHERE id = {self.p}", (float(nuevo_limite), user_id))
            self.conexion.commit()
            return True
        except: return False

    # ============ MÉTODOS DE GASTOS ============

    def agregar_gasto(self, monto, categoria, descripcion, usuario_id):
        try:
            self.cursor.execute(f"""
                INSERT INTO gastos (monto, categoria, descripcion, usuario_id, fecha) 
                VALUES ({self.p}, {self.p}, {self.p}, {self.p}, CURRENT_DATE)
            """, (monto, categoria, descripcion, usuario_id))
            self.conexion.commit()
            return True
        except Exception as e:
            logging.error(f"Error al agregar gasto: {e}")
            return False

    def obtener_todos_los_gastos(self, usuario_id):
        self.cursor.execute(f"SELECT * FROM gastos WHERE usuario_id = {self.p} ORDER BY fecha DESC", (usuario_id,))
        return [dict(f) for f in self.cursor.fetchall()]

    def eliminar_gasto(self, id_gasto, usuario_id):
        self.cursor.execute(f"DELETE FROM gastos WHERE id = {self.p} AND usuario_id = {self.p}", (id_gasto, usuario_id))
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def obtener_total_gastado(self, usuario_id):
        self.cursor.execute(f"SELECT SUM(monto) AS total FROM gastos WHERE usuario_id = {self.p}", (usuario_id,))
        res = self.cursor.fetchone()
        if not res: return 0.0
        val = res['total'] if self.es_postgresql else res[0]
        return float(val) if val else 0.0

    def obtener_gastos_por_categoria(self, usuario_id):
        self.cursor.execute(f"SELECT categoria, SUM(monto) AS total FROM gastos WHERE usuario_id = {self.p} GROUP BY categoria", (usuario_id,))
        resultados = self.cursor.fetchall()
        return {f['categoria'] if self.es_postgresql else f[0]: float(f['total'] if self.es_postgresql else f[1]) for f in resultados}

    def obtener_gastos_por_dia(self, usuario_id):
        self.cursor.execute(f"SELECT fecha, SUM(monto) AS total FROM gastos WHERE usuario_id = {self.p} GROUP BY fecha ORDER BY fecha ASC", (usuario_id,))
        resultados = self.cursor.fetchall()
        return {f['fecha'] if self.es_postgresql else f[0]: float(f['total'] if self.es_postgresql else f[1]) for f in resultados}

    def obtener_resumen(self, usuario_id):
        total = self.obtener_total_gastado(usuario_id)
        presupuesto = self.obtener_presupuesto_usuario(usuario_id)
        por_cat = self.obtener_gastos_por_categoria(usuario_id)
        
        porcentaje = min(100, (total / presupuesto * 100)) if presupuesto > 0 else 0
        
        return {
            "total_general": total,
            "por_categoria": por_cat,
            "presupuesto_limite": presupuesto,
            "saldo_disponible": max(0, presupuesto - total),
            "porcentaje_usado": porcentaje,
            "nivel_alerta": 'peligro' if porcentaje >= 100 else ('advertencia' if porcentaje >= 80 else 'seguro'),
            "balance_neto": presupuesto - total
        }

# Mantenemos el nombre de la clase para no romper api_corregido.py
class GestorConPresupuesto(GestorGastos):
    def __init__(self, archivo):
        super().__init__(archivo)