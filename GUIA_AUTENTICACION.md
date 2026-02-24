# 🔐 Sistema de Autenticación - FinanzasPro

## 📋 Resumen de Implementación

Se ha implementado exitosamente un sistema completo de autenticación de usuarios con registro y login para tu aplicación FinanzasPro.

## ✅ Cambios Realizados

### 1. **Base de Datos (gestor_db.py)**

#### Tabla de Usuarios

```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
)
```

#### Modificación en Tabla de Gastos

- Se agregó la columna `usuario_id INTEGER` con clave foránea a la tabla usuarios
- Cada gasto ahora está asociado a un usuario específico

#### Métodos Nuevos

- `registrar_usuario(nombre, email, password)` - Crea un nuevo usuario
- `verificar_login(email, password)` - Valida credenciales
- `obtener_usuario_por_id(user_id)` - Obtiene datos del usuario

**Seguridad**: Las contraseñas se almacenan encriptadas con SHA-256

---

### 2. **API (api_corregido.py)**

#### Nuevos Endpoints

**POST /auth/registro**

```json
{
  "nombre": "Juan Pérez",
  "email": "juan@email.com",
  "password": "mipassword"
}
```

Respuesta: `{ "mensaje": "...", "token": "...", "usuario": {...} }`

**POST /auth/login**

```json
{
  "email": "juan@email.com",
  "password": "mipassword"
}
```

Respuesta: `{ "mensaje": "...", "token": "...", "usuario": {...} }`

**POST /auth/logout**

- Cierra la sesión del usuario
- Requiere token en header: `Authorization: Bearer {token}`

#### Endpoints Protegidos

Ahora **TODOS** los endpoints de gastos requieren autenticación:

- `POST /gastos` - Crear gasto
- `GET /gastos` - Listar gastos
- `DELETE /gastos/{id}` - Eliminar gasto
- `PUT /gastos/{id}` - Actualizar gasto
- `GET /gastos/resumen` - Obtener resumen

**Cada endpoint verifica el token y asocia las operaciones con el usuario autenticado.**

---

### 3. **Frontend**

#### Nuevo Archivo: `login.html`

- **Diseño Premium**: Gradientes violetas, animaciones suaves
- **Dos Formularios**:
  - Iniciar Sesión
  - Registrarse
- **Validación**: Contraseña mínimo 6 caracteres, email válido
- **Estados Visuales**: Loading spinner, mensajes de error/éxito
- **Auto-redirect**: Si ya hay sesión activa, redirige a la app

#### Modificaciones en `index.html`

- Encabezado con nombre del usuario: "Bienvenido, Juan 👋"
- Botón "Cerrar Sesión" (rojo, esquina superior derecha)
- Se eliminó el container duplicado

#### Modificaciones en `script.js`

**Nuevas Funciones**:

```javascript
obtenerToken()          // Obtiene token de localStorage
obtenerUsuario()        // Obtiene datos del usuario
getAuthHeaders()        // Genera headers con token
cerrarSesion()          // Limpia sesión y redirige
```

**Protección**:

- Al cargar, verifica si hay token
- Sin token → Redirige a `/static/login.html`
- Con token → Muestra nombre del usuario y carga datos

**Todas las peticiones fetch ahora incluyen**:

```javascript
headers: getAuthHeaders()
// Genera: { 'Content-Type': 'application/json', 'Authorization': 'Bearer {token}' }
```

---

## 🚀 Cómo Usar

### 1. **Iniciar el Servidor**

```bash
.\iniciar_web.bat
```

El servidor corre en: <http://127.0.0.1:8000>

### 2. **Acceder a la Aplicación**

- Ir a: <http://127.0.0.1:8000>
- Automáticamente te redirige a `/static/login.html`

### 3. **Registrar un Nuevo Usuario**

1. Click en pestaña "Registrarse"
2. Llenar: Nombre, Email, Contraseña (min. 6 caracteres)
3. Click "Crear Cuenta"
4. Automáticamente se loguea y redirige a la app principal

### 4. **Iniciar Sesión**

1. Pestaña "Iniciar Sesión"
2. Email y Contraseña
3. Click "Iniciar Sesión"
4. Redirige a la app principal

### 5. **Usar la Aplicación**

- Verás tu nombre en la parte superior: "Bienvenido, [Tu Nombre] 👋"
- Todos tus gastos están asociados a tu usuario
- Solo ves TUS gastos, no los de otros usuarios

### 6. **Cerrar Sesión**

- Click en botón rojo "🚪 Cerrar Sesión"
- Te redirige al login
- Token se elimina del navegador

---

## 🔒 Seguridad Implementada

1. **Encriptación de Passwords**: SHA-256 hash
2. **Tokens de Sesión**: UUID únicos por usuario
3. **Verificación en Backend**: Cada endpoint valida el token
4. **Protección Frontend**: Redirige si no hay token
5. **Headers Seguros**: Authorization Bearer token
6. **Email Único**: No se pueden registrar emails duplicados

---

## 📊 Flujo de Autenticación

```
Usuario → login.html → POST /auth/login → Recibe Token
                                               ↓
                        localStorage.setItem('token', token)
                                               ↓
                                    Redirige a index.html
                                               ↓
                               script.js verifica token
                                               ↓
                              Muestra nombre y carga datos
                                               ↓
                  Todas las peticiones incluyen: Authorization: Bearer {token}
                                               ↓
                              Backend verifica token
                                               ↓
                            Retorna datos del usuario
```

---

## 🗄️ Estructura de Base de Datos

### Antes

```
gastos: [id, monto, categoria, descripcion, fecha]
```

### Ahora

```
usuarios: [id, nombre, email, password_hash, fecha_creacion]
gastos:   [id, monto, categoria, descripcion, fecha, usuario_id]
                                                       ↓
                                        FOREIGN KEY → usuarios(id)
```

**Cada gasto está vinculado a un usuario específico mediante `usuario_id`**

---

## 🎨 Interfaz de Usuario

### Login/Registro

- **Fondo**: Gradiente violeta (#667eea → #764ba2)
- **Tarjeta**: Blanca con sombra profunda
- **Animaciones**: Slide-in al cargar, fade-in al cambiar tabs
- **Inputs**: Bordes animados al focus
- **Botones**: Gradiente con hover elevado
- **Estados**: Loading spinner, mensajes coloridos

### App Principal

- **Header**: Flex con nombre y botón logout
- **Personalización**: Muestra "Bienvenido, {nombre} 👋"
- **Botón Logout**: Rojo (#f44336), esquina derecha

---

## 🧪 Pruebas Recomendadas

1. **Registro de Usuario**
   - Crear cuenta con email nuevo ✅
   - Intentar email duplicado (debe fallar) ✅
   - Password corto (debe rechazar) ✅

2. **Login**
   - Credenciales correctas ✅
   - Credenciales incorrectas (debe fallar) ✅
   - Sin llenar campos (validación HTML5) ✅

3. **Gastos**
   - Crear gasto (debe asociarse al usuario) ✅
   - Listar gastos (solo del usuario logueado) ✅
   - Eliminar gasto ✅

4. **Sesión**
   - Cerrar sesión ✅
   - Acceder sin token (debe redirigir a login) ✅
   - Token inválido (debe rechazar) ✅

---

## 📝 Notas Importantes

1. **Tokens en Memoria**: Los tokens se almacenan en un diccionario en memoria.
   - ⚠️ Si reinicias el servidor, se pierden las sesiones activas
   - Para producción, usar Redis o JWT

2. **Base de Datos**: Se crea automáticamente al iniciar
   - Archivo: `FinanzasPro.db`
   - Las migraciones se ejecutan automáticamente

3. **Múltiples Usuarios**: Cada usuario tiene sus propios gastos
   - No hay interferencia entre usuarios
   - Filtro automático por `usuario_id`

4. **Passwords**:
   - Se hashean con SHA-256
   - Nunca se almacenan en texto plano
   - No se pueden recuperar (solo resetear)

---

## 🔄 Próximas Mejoras (Opcional)

1. **JWT Tokens**: Más seguros y stateless
2. **Recuperación de Password**: Endpoint para resetear
3. **Perfil de Usuario**: Página para editar datos
4. **Roles**: Admin, Usuario normal, etc.
5. **OAuth**: Login con Google, Facebook, etc.
6. **Rate Limiting**: Prevenir ataques de fuerza bruta
7. **Tokens de Refresco**: Para sesiones más largas

---

## ✨ ¡Listo para Usar

Tu aplicación ahora tiene:

- ✅ Sistema de registro completo
- ✅ Login seguro con encriptación
- ✅ Sesiones con tokens
- ✅ Interfaz moderna y profesional
- ✅ Protección en todos los endpoints
- ✅ Gastos por usuario

**Cada usuario tiene su propia cuenta y sus propios gastos totalmente separados.**

---

**Creado el**: 2026-02-09
**Versión**: 1.0.0
