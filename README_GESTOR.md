# 💰 Gestor de Finanzas Pro - Guía de Uso

## 🚀 Cómo Ejecutar la Aplicación

### ✅ Método Recomendado (Funciona Correctamente)
**Desde tu editor de código (VS Code, PyCharm, etc.):**
1. Abre el archivo `PruebaDeTkinter.py`
2. Haz clic en el botón **"Run Python File"** (▶️) en la esquina superior derecha
3. La ventana de login aparecerá automáticamente

### ⚠️ Método Alternativo (Desde Terminal)
Si ejecutas desde PowerShell/CMD, la ventana puede quedar oculta:
```bash
python -u PruebaDeTkinter.py
```
**Nota:** Si no ves la ventana, revisa la barra de tareas de Windows.

---

## 🔐 Credenciales de Acceso

Al iniciar la aplicación, verás una ventana de login con fondo oscuro:

- **Usuario:** `admin`
- **Contraseña:** `1234`

---

## 📊 Funcionalidades Principales

### 1️⃣ **Pestaña Resumen**
- Visualiza tu presupuesto total, gastado y disponible
- Barra de progreso con alertas de color:
  - 🟢 **Verde:** Presupuesto bajo control (0-79%)
  - 🟠 **Naranja:** Cuidado, cerca del límite (80-99%)
  - 🔴 **Rojo:** ¡Presupuesto excedido! (100%+)
- Botón para modificar el presupuesto

### 2️⃣ **Pestaña Nuevo Gasto**
- Registra gastos con:
  - Monto
  - Categoría (Comida, Transporte, Entretenimiento, etc.)
  - Descripción opcional
- Validación automática de presupuesto
- Confirmación si vas a exceder el límite

### 3️⃣ **Pestaña Herramientas**
- **Filtros de Fecha:** Filtra gastos por rango de fechas
- **Ver Historial Completo:** Tabla con todos los gastos registrados
  - ✏️ Editar gastos existentes
  - ❌ Eliminar gastos individuales
  - 💣 Borrar todo el historial (con doble confirmación)
- **Ver Gráficos Estadísticos:** Gráfico de pastel con distribución por categoría
- **Exportar a Excel/CSV:** Descarga tus gastos filtrados
- **Limpiar Campos:** Resetea el formulario de registro

---

## 🎨 Características del Diseño

- **Dark Mode:** Interfaz moderna con fondo oscuro
- **Colores Vibrantes:** Paleta de colores profesional
- **Alertas Visuales:** Cambios de color según el estado del presupuesto
- **Gráficos Interactivos:** Visualización de datos con matplotlib

---

## 🗄️ Base de Datos

Los datos se guardan automáticamente en:
```
FinanzasPro.db
```

Esta base de datos SQLite almacena:
- Todos tus gastos (monto, categoría, descripción, fecha)
- Tu presupuesto configurado

---

## 🛠️ Solución de Problemas

### ❌ La ventana no aparece al ejecutar desde terminal
**Solución:** Usa el botón "Run Python File" de tu editor en lugar de la terminal.

### ❌ Error "No module named 'gestor_db'"
**Solución:** Asegúrate de que `gestor_db.py` esté en la misma carpeta que `PruebaDeTkinter.py`.

### ❌ Error con matplotlib
**Solución:** Instala matplotlib:
```bash
pip install matplotlib
```

---

## 📝 Categorías Disponibles

1. Comida
2. Transporte
3. Entretenimiento
4. Ropa
5. Salud
6. Educación
7. Servicios
8. Otros

---

## 💡 Consejos de Uso

1. **Establece un presupuesto realista** desde la pestaña Resumen
2. **Registra tus gastos diariamente** para mejor control
3. **Revisa los gráficos semanalmente** para identificar patrones
4. **Exporta reportes mensuales** para análisis detallado
5. **Usa las alertas de color** como guía para tus decisiones financieras

---

## 🎯 Versión

**Gestor de Finanzas Pro v2.0**
- Sistema de login seguro
- Gestión de presupuesto con alertas
- Gráficos estadísticos
- Exportación a CSV/Excel
- Edición y eliminación de gastos

---

¡Disfruta gestionando tus finanzas! 💰✨
