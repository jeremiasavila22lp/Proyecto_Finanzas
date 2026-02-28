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
        self.conexion = None
        self.es_postgresql = finanzas_bd.startswith("postgres://") or finanzas_bd.startswith("postgresql://")
        
        self.p = "%s" if self.es_postgresql else "?"
        self.serial_type = "SERIAL PRIMARY KEY" if self.es_postgresql else "INTEGER PRIMARY KEY AUTOINCREMENT"
        self.default_date = "CURRENT_TIMESTAMP" if self.es_postgresql else "CURRENT_TIMESTAMP"
        
        self._conectar()
        self._inicializar_tablas()

    def _conectar(self):
        """Establece o recupera la conexión a la base de datos"""
        with self.lock:
            try:
                if self.es_postgresql:
                    if self.conexion is None or self.conexion.closed != 0:
                        self.conexion = psycopg2.connect(self.archivo_bd)
                        print("[OK] Conexión PostgreSQL (Neon) restablecida.")
                else:
                    if self.conexion is None:
                        self.conexion = sqlite3.connect(self.archivo_bd, check_same_thread=False)
                        self.conexion.row_factory = sqlite3.Row
                        print("[OK] Conexión SQLite establecida.")
            except Exception as e:
                logging.error(f"Error de conexión: {e}")
                raise e

    def _get_cursor(self):
        """Retorna un cursor fresco y asegura que la conexión esté viva"""
        self._conectar()
        if self.es_postgresql:
            # En Postgres, si hubo un error previo, hay que hacer rollback para limpiar el estado
            try:
                self.conexion.rollback()
            except:
                pass
            return self.conexion.cursor(cursor_factory=RealDictCursor)
        return self.conexion.cursor()

    def _inicializar_tablas(self):
        with self.lock:
            cur = self._get_cursor()
            try:
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS usuarios (
                        id {self.serial_type},
                        nombre TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        codigo_acceso TEXT UNIQUE,
                        fecha_creacion TEXT DEFAULT {self.default_date},
                        presupuesto REAL DEFAULT 5000.0
                    )
                """)
                cur.execute(f"""
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
                # 2. MIGRACIÓN: Asegurar que existe la columna 'codigo_acceso'
                try:
                    cur.execute("ALTER TABLE usuarios ADD COLUMN codigo_acceso TEXT")
                    self.conexion.commit()
                    print("[MIGRACIÓN] Columna 'codigo_acceso' añadida correctamente.")
                except:
                    # Si ya existe, no hará nada
                    pass

                # 3. MIGRACIÓN: Generar PIN para usuarios que no lo tengan
                cur.execute("SELECT id FROM usuarios WHERE codigo_acceso IS NULL")
                usuarios_sin_pin = cur.fetchall()
                if usuarios_sin_pin:
                    import random
                    print(f"[MIGRACIÓN] Generando PIN para {len(usuarios_sin_pin)} usuarios...")
                    for u in usuarios_sin_pin:
                        u_id = u['id'] if self.es_postgresql else u[0]
                        nuevo_pin = "".join([str(random.randint(0, 9)) for _ in range(6)])
                        cur.execute(f"UPDATE usuarios SET codigo_acceso = {self.p} WHERE id = {self.p}", (nuevo_pin, u_id))
                        self.conexion.commit()

                self.conexion.commit()
            finally:
                cur.close()

    def registrar_usuario(self, nombre, email, password):
        with self.lock:
            cur = self._get_cursor()
            try:
                import random
                codigo = "".join([str(random.randint(0, 9)) for _ in range(6)])
                password_hash = pwd_context.hash(password)
                
                cur.execute(f"INSERT INTO usuarios (nombre, email, password_hash, codigo_acceso) VALUES ({self.p}, {self.p}, {self.p}, {self.p}) RETURNING id" if self.es_postgresql else f"INSERT INTO usuarios (nombre, email, password_hash, codigo_acceso) VALUES (?, ?, ?, ?)", 
                            (nombre, email, password_hash, codigo))
                
                user_id = cur.fetchone()['id'] if self.es_postgresql else cur.lastrowid
                self.conexion.commit()
                return (True, user_id)
            except (sqlite3.IntegrityError, psycopg2.IntegrityError):
                self.conexion.rollback()
                return (False, "El email ya está registrado")
            except Exception as e:
                self.conexion.rollback()
                return (False, str(e))
            finally:
                cur.close()

    def verificar_login(self, email, password):
        with self.lock:
            cur = self._get_cursor()
            try:
                cur.execute(f"SELECT * FROM usuarios WHERE email = {self.p}", (email,))
                usuario = cur.fetchone()
                if not usuario: return (False, "Usuario no encontrado")
                
                usuario_dict = dict(usuario)
                if pwd_context.verify(password, usuario_dict['password_hash']):
                    del usuario_dict['password_hash']
                    return (True, usuario_dict)
                return (False, "Contraseña incorrecta")
            except Exception as e:
                return (False, str(e))
            finally:
                cur.close()

    def obtener_usuario_por_id(self, user_id):
        with self.lock:
            cur = self._get_cursor()
            try:
                cur.execute(f"SELECT id, nombre, email, presupuesto, codigo_acceso FROM usuarios WHERE id = {self.p}", (user_id,))
                res = cur.fetchone()
                return dict(res) if res else None
            finally:
                cur.close()

    def obtener_usuario_por_codigo(self, codigo):
        with self.lock:
            cur = self._get_cursor()
            try:
                cur.execute(f"SELECT id FROM usuarios WHERE codigo_acceso = {self.p}", (str(codigo),))
                res = cur.fetchone()
                if res:
                    return res['id'] if self.es_postgresql else res[0]
                return None
            finally:
                cur.close()

    def obtener_presupuesto_usuario(self, user_id):
        with self.lock:
            cur = self._get_cursor()
            try:
                cur.execute(f"SELECT presupuesto FROM usuarios WHERE id = {self.p}", (user_id,))
                res = cur.fetchone()
                if not res: return 5000.0
                return float(res['presupuesto'] if self.es_postgresql else res[0])
            finally:
                cur.close()

    def actualizar_presupuesto_usuario(self, user_id, nuevo_limite):
        with self.lock:
            cur = self._get_cursor()
            try:
                cur.execute(f"UPDATE usuarios SET presupuesto = {self.p} WHERE id = {self.p}", (float(nuevo_limite), user_id))
                self.conexion.commit()
                return True
            except:
                self.conexion.rollback()
                return False
            finally:
                cur.close()

    def agregar_gasto(self, monto, categoria, descripcion, usuario_id):
        with self.lock:
            cur = self._get_cursor()
            try:
                cur.execute(f"""
                    INSERT INTO gastos (monto, categoria, descripcion, usuario_id, fecha) 
                    VALUES ({self.p}, {self.p}, {self.p}, {self.p}, CURRENT_DATE)
                """, (monto, categoria, descripcion, usuario_id))
                self.conexion.commit()
                return True
            except Exception as e:
                self.conexion.rollback()
                logging.error(f"Error al agregar gasto: {e}")
                return False
            finally:
                cur.close()

    def obtener_todos_los_gastos(self, usuario_id):
        with self.lock:
            cur = self._get_cursor()
            try:
                cur.execute(f"SELECT * FROM gastos WHERE usuario_id = {self.p} ORDER BY fecha DESC", (usuario_id,))
                return [dict(f) for f in cur.fetchall()]
            finally:
                cur.close()

    def eliminar_gasto(self, id_gasto, usuario_id):
        with self.lock:
            cur = self._get_cursor()
            try:
                cur.execute(f"DELETE FROM gastos WHERE id = {self.p} AND usuario_id = {self.p}", (id_gasto, usuario_id))
                self.conexion.commit()
                return cur.rowcount > 0
            except:
                self.conexion.rollback()
                return False
            finally:
                cur.close()

    def obtener_total_gastado(self, usuario_id):
        with self.lock:
            cur = self._get_cursor()
            try:
                cur.execute(f"SELECT SUM(monto) AS total FROM gastos WHERE usuario_id = {self.p}", (usuario_id,))
                res = cur.fetchone()
                if not res: return 0.0
                val = res['total'] if self.es_postgresql else res[0]
                return float(val) if val else 0.0
            finally:
                cur.close()

    def obtener_gastos_por_categoria(self, usuario_id):
        with self.lock:
            cur = self._get_cursor()
            try:
                cur.execute(f"SELECT categoria, SUM(monto) AS total FROM gastos WHERE usuario_id = {self.p} GROUP BY categoria", (usuario_id,))
                resultados = cur.fetchall()
                return {f['categoria'] if self.es_postgresql else f[0]: float(f['total'] if self.es_postgresql else f[1]) for f in resultados}
            finally:
                cur.close()

    def obtener_gastos_por_dia(self, usuario_id):
        with self.lock:
            cur = self._get_cursor()
            try:
                cur.execute(f"SELECT fecha, SUM(monto) AS total FROM gastos WHERE usuario_id = {self.p} GROUP BY fecha ORDER BY fecha ASC", (usuario_id,))
                resultados = cur.fetchall()
                return {f['fecha'] if self.es_postgresql else f[0]: float(f['total'] if self.es_postgresql else f[1]) for f in resultados}
            finally:
                cur.close()

    def obtener_resumen(self, usuario_id):
        # Este método llama a otros que ya tienen lock, pero por seguridad lo envolvemos también
        with self.lock:
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