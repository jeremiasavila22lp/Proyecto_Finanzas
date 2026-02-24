# 📚 DOCUMENTACIÓN COMPLETA - CONTROL DE PRESUPUESTO
## Sistema de Gestión de Finanzas Personales con Tkinter

---

## 🎯 RESUMEN DE IMPLEMENTACIONES

He implementado **7 funcionalidades principales** para mejorar tu control de presupuesto:

1. ✅ **Visualización del Presupuesto en Tiempo Real**
2. ✅ **Configuración Dinámica del Presupuesto**
3. ✅ **Sistema de Alertas con Colores Dinámicos**
4. ✅ **Categorías Predefinidas con Combobox**
5. ✅ **Ventana de Estadísticas por Categoría**
6. ✅ **Historial Mejorado con Tabla (Treeview)**
7. ✅ **Persistencia del Presupuesto en Base de Datos**

---

## 📋 EXPLICACIÓN DETALLADA DE CADA IMPLEMENTACIÓN

### 1️⃣ **VISUALIZACIÓN DEL PRESUPUESTO EN TIEMPO REAL**

#### ¿Qué hace?
Muestra una sección visual en la parte superior de la aplicación con:
- Presupuesto total configurado
- Monto gastado hasta el momento
- Saldo disponible
- Barra de progreso visual
- Porcentaje de presupuesto usado

#### ¿Cómo lo implementé?

**En `PruebaDeTkinter.py` (líneas 265-305):**

```python
# Creé un frame especial para el presupuesto con fondo blanco
frame_presupuesto = tk.Frame(frame_app, bg="white", relief=tk.RAISED, bd=2)
frame_presupuesto.pack(fill=tk.X, pady=(0, 20))

# Etiquetas que muestran la información
etiqueta_presupuesto = tk.Label(...)  # Muestra el presupuesto total
etiqueta_gastado = tk.Label(...)      # Muestra cuánto has gastado
etiqueta_disponible = tk.Label(...)   # Muestra cuánto te queda

# Barra de progreso visual
barra_progreso = ttk.Progressbar(frame_barra, length=400, mode='determinate',
                                style="Presupuesto.Horizontal.TProgressbar")
```

**Función clave: `actualizar_visualizacion_presupuesto()` (líneas 30-63):**

Esta función se ejecuta cada vez que:
- Inicias la aplicación
- Guardas un nuevo gasto
- Modificas el presupuesto

```python
def actualizar_visualizacion_presupuesto():
    # 1. Obtiene los datos del gestor de base de datos
    total_gastado = mi_gestor.obtener_total()
    saldo_disponible = mi_gestor.consulta_saldo_disponible()
    porcentaje = mi_gestor.obtener_porcentaje_usado()
    nivel = mi_gestor.obtener_nivel_alerta()
    
    # 2. Actualiza las etiquetas de texto
    etiqueta_gastado.config(text=f"Gastado: ${total_gastado:.2f}")
    etiqueta_disponible.config(text=f"Disponible: ${saldo_disponible:.2f}")
    
    # 3. Actualiza la barra de progreso
    barra_progreso['value'] = porcentaje  # De 0 a 100
    
    # 4. Cambia los colores según el nivel de alerta (explicado más abajo)
```

---

### 2️⃣ **CONFIGURACIÓN DINÁMICA DEL PRESUPUESTO**

#### ¿Qué hace?
Permite cambiar el presupuesto desde la interfaz sin tener que modificar el código.

#### ¿Cómo lo implementé?

**Botón en la interfaz (línea 303):**
```python
tk.Button(frame_presupuesto, text="⚙ Modificar Presupuesto", 
         command=modificar_presupuesto, ...)
```

**Función `modificar_presupuesto()` (líneas 193-207):**
```python
def modificar_presupuesto():
    # 1. Muestra un diálogo para ingresar el nuevo presupuesto
    nuevo_presupuesto = simpledialog.askfloat(
        "Modificar Presupuesto",
        f"Presupuesto actual: ${mi_gestor.limite:.2f}\n\nIngresa el nuevo presupuesto:",
        minvalue=0.01,  # No permite valores negativos o cero
        initialvalue=mi_gestor.limite  # Muestra el valor actual
    )
    
    # 2. Si el usuario ingresó un valor, lo guarda
    if nuevo_presupuesto:
        mi_gestor.guardar_presupuesto(nuevo_presupuesto)
        actualizar_visualizacion_presupuesto()  # Actualiza la interfaz
        messagebox.showinfo("✓ Actualizado", 
                          f"Presupuesto actualizado a ${nuevo_presupuesto:.2f}")
```

**En `gestor_db.py` - Método `guardar_presupuesto()` (líneas 99-107):**
```python
def guardar_presupuesto(self, nuevo_limite):
    """Guarda el presupuesto en la base de datos"""
    self.limite = float(nuevo_limite)
    
    # INSERT OR REPLACE: Si existe, lo actualiza; si no, lo crea
    self.cursor.execute("""
        INSERT OR REPLACE INTO configuracion (clave, valor) 
        VALUES ('presupuesto', ?)
    """, (self.limite,))
    self.conexion.commit()
```

---

### 3️⃣ **SISTEMA DE ALERTAS CON COLORES DINÁMICOS**

#### ¿Qué hace?
Cambia automáticamente los colores de la interfaz según qué tan cerca estés de tu límite:
- 🟢 **Verde** (0-79%): "Presupuesto bajo control"
- 🟠 **Naranja** (80-99%): "Cuidado, te acercas al límite"
- 🔴 **Rojo** (100%+): "¡Has superado tu presupuesto!"

#### ¿Cómo lo implementé?

**En `gestor_db.py` - Método `obtener_nivel_alerta()` (líneas 130-141):**
```python
def obtener_nivel_alerta(self):
    """Retorna el nivel de alerta basado en el porcentaje usado"""
    porcentaje = self.obtener_porcentaje_usado()
    
    if porcentaje < 80:
        return 'seguro'      # Verde
    elif porcentaje < 100:
        return 'advertencia' # Naranja
    else:
        return 'peligro'     # Rojo
```

**En `PruebaDeTkinter.py` - Dentro de `actualizar_visualizacion_presupuesto()` (líneas 42-62):**
```python
# Obtiene el nivel de alerta
nivel = mi_gestor.obtener_nivel_alerta()

# Define colores y mensajes según el nivel
if nivel == 'seguro':
    color_barra = '#4CAF50'  # Verde
    color_texto = '#2E7D32'
    mensaje_estado = "✓ Presupuesto bajo control"
elif nivel == 'advertencia':
    color_barra = '#FF9800'  # Naranja
    color_texto = '#E65100'
    mensaje_estado = "⚠ Cuidado, te acercas al límite"
else:  # peligro
    color_barra = '#F44336'  # Rojo
    color_texto = '#C62828'
    mensaje_estado = "🚨 ¡Has superado tu presupuesto!"

# Aplica los colores a la barra de progreso
style.configure("Presupuesto.Horizontal.TProgressbar", 
               background=color_barra)

# Aplica los colores al texto
etiqueta_estado_presupuesto.config(text=mensaje_estado, fg=color_texto)
etiqueta_porcentaje.config(fg=color_texto)
```

**Alerta antes de guardar un gasto que exceda el límite (líneas 82-93):**
```python
# Verifica si el nuevo gasto excederá el presupuesto
if total_actual + monto_float > mi_gestor.limite:
    # Muestra un diálogo de confirmación
    respuesta = messagebox.askyesno(
        "⚠ Advertencia de Presupuesto",
        f"Este gasto de ${monto_float:.2f} hará que superes tu presupuesto.\n\n"
        f"Total actual: ${total_actual:.2f}\n"
        f"Nuevo total: ${total_actual + monto_float:.2f}\n"
        f"Presupuesto: ${mi_gestor.limite:.2f}\n\n"
        "¿Deseas continuar de todas formas?"
    )
    if not respuesta:  # Si el usuario dice "No", cancela el guardado
        return
```

---

### 4️⃣ **CATEGORÍAS PREDEFINIDAS CON COMBOBOX**

#### ¿Qué hace?
En lugar de escribir la categoría manualmente (con riesgo de errores de tipeo), ahora tienes un menú desplegable con categorías comunes.

#### ¿Cómo lo implementé?

**Lista de categorías predefinidas (líneas 15-24):**
```python
CATEGORIAS_COMUNES = [
    "Comida",
    "Transporte", 
    "Entretenimiento",
    "Ropa",
    "Salud",
    "Educación",
    "Servicios",
    "Otros"
]
```

**Combobox en lugar de Entry (líneas 321-325):**
```python
# Antes era: entrada_categoria = ttk.Entry(...)
# Ahora es:
combo_categoria = ttk.Combobox(frame_app, 
                              values=CATEGORIAS_COMUNES,  # Lista de opciones
                              font=("Arial", 12), 
                              state="normal")  # Permite escribir también
```

**Ventajas:**
- ✅ Evita errores de tipeo ("comida" vs "Comida" vs "COMIDA")
- ✅ Más rápido: solo seleccionar en lugar de escribir
- ✅ Puedes seguir escribiendo categorías personalizadas si quieres

---

### 5️⃣ **VENTANA DE ESTADÍSTICAS POR CATEGORÍA**

#### ¿Qué hace?
Muestra cuánto has gastado en cada categoría y qué porcentaje representa del total.

#### ¿Cómo lo implementé?

**En `gestor_db.py` - Método `obtener_gastos_por_categoria()` (líneas 143-150):**
```python
def obtener_gastos_por_categoria(self):
    """Retorna un diccionario con el total gastado por categoría"""
    self.cursor.execute("""
        SELECT categoria, SUM(monto) 
        FROM gastos 
        GROUP BY categoria
    """)
    resultados = self.cursor.fetchall()
    return {cat: monto for cat, monto in resultados}
    # Ejemplo de retorno: {'comida': 1500, 'transporte': 800, ...}
```

**En `PruebaDeTkinter.py` - Función `ver_estadisticas()` (líneas 157-190):**
```python
def ver_estadisticas():
    # 1. Obtiene los gastos agrupados por categoría
    gastos_por_cat = mi_gestor.obtener_gastos_por_categoria()
    
    # 2. Crea una nueva ventana
    ventana_stats = tk.Toplevel(ventana)
    ventana_stats.title("📈 Estadísticas por Categoría")
    
    # 3. Para cada categoría, muestra:
    for categoria, monto in sorted(gastos_por_cat.items(), 
                                   key=lambda x: x[1], reverse=True):
        # Calcula el porcentaje
        porcentaje = (monto / total_general) * 100
        
        # Crea un frame visual para cada categoría
        frame_cat = tk.Frame(frame_scrollable, bg="white", 
                            relief=tk.RAISED, bd=1)
        
        # Muestra: "Comida    $1,500.00 (30.0%)"
        tk.Label(frame_cat, text=categoria.capitalize(), ...)
        tk.Label(frame_cat, text=f"${monto:.2f} ({porcentaje:.1f}%)", ...)
```

**Características:**
- ✅ Ordenado de mayor a menor gasto
- ✅ Muestra monto y porcentaje
- ✅ Scroll si hay muchas categorías

---

### 6️⃣ **HISTORIAL MEJORADO CON TABLA (TREEVIEW)**

#### ¿Qué hace?
Antes el historial se mostraba en un cuadro de texto simple. Ahora usa una tabla profesional con columnas.

#### ¿Cómo lo implementé?

**En `PruebaDeTkinter.py` - Función `ver_historial()` (líneas 108-154):**
```python
def ver_historial():
    # 1. Obtiene todos los gastos
    gastos = mi_gestor.obtener_todos_los_gastos()
    
    # 2. Crea un Treeview (tabla)
    columnas = ("ID", "Monto", "Categoría", "Fecha", "Descripción")
    tree = ttk.Treeview(frame_hist, columns=columnas, show="headings")
    
    # 3. Configura cada columna
    tree.heading("ID", text="ID")
    tree.heading("Monto", text="Monto")
    tree.column("ID", width=50, anchor="center")
    tree.column("Monto", width=100, anchor="e")  # Alineado a la derecha
    
    # 4. Inserta cada gasto como una fila
    for gasto in gastos:
        tree.insert("", tk.END, values=(
            gasto[0],  # ID
            f"${gasto[1]:.2f}",  # Monto formateado
            gasto[2].capitalize(),  # Categoría
            gasto[3],  # Fecha
            gasto[4]   # Descripción
        ))
    
    # 5. Agrega scrollbar
    scrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
```

**Ventajas sobre el anterior:**
- ✅ Columnas alineadas y organizadas
- ✅ Más fácil de leer
- ✅ Aspecto más profesional
- ✅ Scrollbar integrada

---

### 7️⃣ **PERSISTENCIA DEL PRESUPUESTO EN BASE DE DATOS**

#### ¿Qué hace?
El presupuesto se guarda en la base de datos, así que cuando cierres y vuelvas a abrir la aplicación, se mantiene el último presupuesto configurado.

#### ¿Cómo lo implementé?

**En `gestor_db.py` - Constructor `__init__()` (líneas 75-98):**

```python
def __init__(self, archivo, limite=5000):
    super().__init__(archivo)
    
    # 1. Crea una tabla de configuración si no existe
    self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracion (
            clave TEXT PRIMARY KEY,
            valor REAL
        )
    """)
    self.conexion.commit()
    
    # 2. Intenta cargar el presupuesto guardado
    self.cursor.execute("SELECT valor FROM configuracion WHERE clave = 'presupuesto'")
    resultado = self.cursor.fetchone()
    
    # 3. Si existe, lo carga; si no, usa el valor por defecto
    if resultado:
        self.limite = resultado[0]  # Carga desde la BD
        print(f"Presupuesto cargado desde BD: ${self.limite}")
    else:
        self.limite = limite  # Usa el valor por defecto
        self.guardar_presupuesto(limite)  # Y lo guarda
        print(f"Nuevo presupuesto establecido: ${self.limite}")
```

**Tabla `configuracion` en la base de datos:**
```
┌──────────────┬────────┐
│    clave     │ valor  │
├──────────────┼────────┤
│ presupuesto  │ 5000.0 │
└──────────────┴────────┘
```

**Flujo completo:**
1. Primera vez: Crea la tabla, guarda el presupuesto inicial (5000)
2. Usuario modifica a 8000: Se actualiza en la BD
3. Usuario cierra la app
4. Usuario abre la app: Carga 8000 desde la BD ✅

---

## 🔧 MÉTODOS AUXILIARES NUEVOS EN `gestor_db.py`

### `obtener_porcentaje_usado()` (líneas 122-128)
```python
def obtener_porcentaje_usado(self):
    """Retorna el porcentaje del presupuesto que se ha usado"""
    gastado = self.obtener_total()
    if self.limite == 0:
        return 0
    porcentaje = (gastado / self.limite) * 100
    return min(100, porcentaje)  # No puede ser más de 100%
```

**Uso:** Para la barra de progreso y las alertas.

---

## 🎨 MEJORAS VISUALES

### Colores utilizados:
- **Verde** (#4CAF50): Seguro, éxito
- **Naranja** (#FF9800): Advertencia
- **Rojo** (#F44336): Peligro, salir
- **Azul** (#2196F3): Historial
- **Morado** (#673AB7 y #9C27B0): Estadísticas, configuración
- **Blanco** (#FFFFFF): Fondos de secciones
- **Gris claro** (#F5F5F5): Fondo general

### Tipografía:
- **Arial** en diferentes tamaños (8-18px)
- **Bold** para títulos y botones importantes
- **Italic** para mensajes de estado

---

## 📊 ESTRUCTURA DE LA BASE DE DATOS

### Tabla `gastos` (ya existía):
```sql
CREATE TABLE gastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monto REAL,
    categoria TEXT,
    descripcion TEXT
)
```

### Tabla `configuracion` (NUEVA):
```sql
CREATE TABLE configuracion (
    clave TEXT PRIMARY KEY,
    valor REAL
)
```

---

## 🚀 FLUJO DE USO DE LA APLICACIÓN

1. **Al iniciar:**
   - Carga el presupuesto desde la BD
   - Calcula el total gastado
   - Actualiza la visualización (barra, colores, etc.)

2. **Al registrar un gasto:**
   - Valida que el monto sea válido
   - Verifica si excederá el presupuesto → muestra alerta
   - Guarda en la BD
   - Actualiza la visualización

3. **Al modificar el presupuesto:**
   - Muestra diálogo para ingresar nuevo valor
   - Guarda en la BD
   - Actualiza la visualización

4. **Al ver estadísticas:**
   - Consulta gastos agrupados por categoría
   - Calcula porcentajes
   - Muestra en ventana nueva

---

## 💡 CONCEPTOS CLAVE QUE APRENDISTE

### 1. **Tkinter Avanzado:**
- `Toplevel`: Ventanas secundarias
- `Treeview`: Tablas profesionales
- `Combobox`: Menús desplegables
- `Progressbar`: Barras de progreso
- `simpledialog`: Diálogos de entrada

### 2. **SQL:**
- `INSERT OR REPLACE`: Actualiza si existe, crea si no
- `GROUP BY`: Agrupa resultados
- `SUM()`: Suma valores

### 3. **Python:**
- Herencia de clases (`super()`)
- Diccionarios por comprensión
- Formateo de strings con f-strings
- Manejo de excepciones

### 4. **Diseño de Software:**
- Separación de lógica (gestor_db.py) y presentación (PruebaDeTkinter.py)
- Persistencia de datos
- Validación de entrada del usuario
- Feedback visual inmediato

---

## 📝 RESUMEN DE ARCHIVOS MODIFICADOS

### `gestor_db.py`:
- ✅ Agregada tabla `configuracion`
- ✅ Método `guardar_presupuesto()`
- ✅ Método `obtener_porcentaje_usado()`
- ✅ Método `obtener_nivel_alerta()`
- ✅ Método `obtener_gastos_por_categoria()`
- ✅ Constructor mejorado con carga de presupuesto

### `PruebaDeTkinter.py`:
- ✅ Sección visual de presupuesto
- ✅ Función `actualizar_visualizacion_presupuesto()`
- ✅ Función `modificar_presupuesto()`
- ✅ Función `ver_estadisticas()`
- ✅ Historial mejorado con Treeview
- ✅ Combobox de categorías
- ✅ Sistema de alertas con colores dinámicos
- ✅ Validación antes de guardar gastos que excedan el límite

---

## 🎯 PRÓXIMAS FUNCIONALIDADES QUE PODRÍAS AGREGAR

1. **Gráficos con matplotlib:**
   - Gráfico de pastel por categoría
   - Gráfico de línea de gastos por fecha

2. **Filtros de fecha:**
   - Ver gastos del último mes
   - Ver gastos de una semana específica

3. **Editar/Eliminar gastos:**
   - Doble clic en el historial para editar
   - Botón de eliminar

4. **Exportar reportes:**
   - PDF con resumen mensual
   - Excel con todos los gastos

5. **Múltiples presupuestos:**
   - Presupuesto por categoría
   - Presupuesto mensual vs anual

---

¡Espero que esta documentación te ayude a entender cada detalle de la implementación! 🚀
