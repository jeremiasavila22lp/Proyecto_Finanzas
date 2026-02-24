import sys
import os
import logging
from config_visual import *

def obtener_ruta_db(nombre_archivo):
    """ Obtiene la ruta de la base de datos al lado del ejecutable o script """
    if getattr(sys, 'frozen', False):
        # Si es un ejecutable (.exe), usamos la ruta donde está el .exe
        return os.path.join(os.path.dirname(sys.executable), nombre_archivo)
    # Si es un script .py, está en la misma carpeta del script
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre_archivo)

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.info("---- INICIO DE LA APLICACION ----")

try:
    # Forzar que los prints aparezcan inmediatamente (Python 3.7+)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

print("=" * 50, flush=True)
print("INICIANDO GESTOR DE FINANZAS PRO", flush=True)
print("=" * 50, flush=True)

# Inicializar ventana como None globalmente
ventana = None
ventana_login = None


# --- CONFIGURACIÓN DE ENTORNO ---
# 1. Asegurar que podemos importar módulos locales (gestor_db)
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

# 2. Configurar variables de entorno para TCL/TK (Solución error "init.tcl not found")
if sys.platform == 'win32':
    # Rutas posibles donde podría estar la carpeta 'tcl'
    search_paths = [
        os.path.join(sys.prefix, 'tcl'),
        os.path.join(sys.base_prefix, 'tcl'),
        r"C:\Users\avila\AppData\Local\Programs\Python\Python313\tcl",
    ]
    
    tcl_configured = False
    for base_tcl in search_paths:
        if os.path.exists(base_tcl):
            tcl_lib_path = os.path.join(base_tcl, 'tcl8.6') 
            tk_lib_path = os.path.join(base_tcl, 'tk8.6')
            
            if os.path.exists(tcl_lib_path) and os.path.exists(tk_lib_path):
                os.environ['TCL_LIBRARY'] = tcl_lib_path
                os.environ['TK_LIBRARY'] = tk_lib_path
                print(f"[OK] Configuracion TCL/TK exitosa desde: {base_tcl}")
                tcl_configured = True
                break
                
    if not tcl_configured:
        print("[!] Advertencia: No se encontraron las carpetas TCL/TK automaticamente.")
        print(f"Buscado en: {search_paths}")

# --- IMPORTACIONES ---
print("[DEBUG] Importando tkinter...")
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
print("[DEBUG] Importando gestor_db...")
from gestor_db import GestorConPresupuesto, crear_grafico_gastos_por_mes
print("[DEBUG] Importando matplotlib...")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from tkinter import filedialog
from datetime import datetime, timedelta
print("[DEBUG] Importaciones completadas.") 


# --- INSTANCIA GLOBAL DEL GESTOR ---
print("[DEBUG] Creando instancia del gestor...")
db_path = obtener_ruta_db("FinanzasPro.db")
print(f"[DEBUG] Ruta de la base de datos: {db_path}")
mi_gestor = GestorConPresupuesto(db_path)
print("[DEBUG] Gestor creado exitosamente.")


# --- 2. FUNCIONES DE LA INTERFAZ ---

def filtrar_por_tiempo(opcion, fecha_manual_inicio=None, fecha_manual_fin=None):
    """
    Calcula las fechas de inicio y fin basándose en una opción rápida (Hoy, Semana, Mes, Año)
    o usa las fechas manuales si se elige 'Personalizado'.
    """
    hoy = datetime.now()
    fecha_hoy_str = hoy.strftime('%Y-%m-%d')
    
    if opcion == "Hoy":
        return fecha_hoy_str, fecha_hoy_str

    elif opcion == "Semana" or opcion == "Esta Semana":
        # Restamos los días necesarios para llegar al lunes de esta semana (weekday 0)
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        # Retornamos (inicio, fin) en formato texto
        return inicio_semana.strftime('%Y-%m-%d'), fecha_hoy_str
        
    elif opcion == "Mes" or opcion == "Este Mes":
        # Reemplazamos el día por 1 para obtener el inicio de mes
        inicio_mes = hoy.replace(day=1)
        return inicio_mes.strftime('%Y-%m-%d'), fecha_hoy_str

    elif opcion == "Año" or opcion == "Este Año":
        # Inicio del año actual (1 de Enero)
        inicio_anio = hoy.replace(day=1, month=1)
        return inicio_anio.strftime('%Y-%m-%d'), fecha_hoy_str
        
    elif opcion == "Personalizado":
        # Retornamos tal cual lo que escribió el usuario
        return fecha_manual_inicio, fecha_manual_fin
        
    return None, None

def actualizar_visualizacion_presupuesto():
    """Actualiza todos los elementos visuales del presupuesto"""
    total_gastado = mi_gestor.obtener_total()
    saldo_disponible = mi_gestor.consulta_saldo_disponible()
    porcentaje = mi_gestor.obtener_porcentaje_usado()
    nivel = mi_gestor.obtener_nivel_alerta()
    
    # Actualizar etiquetas de texto
    etiqueta_gastado.config(text=f"Gastado: ${total_gastado:.2f}")
    etiqueta_disponible.config(text=f"Disponible: ${saldo_disponible:.2f}")
    etiqueta_presupuesto.config(text=f"Presupuesto Total: ${mi_gestor.limite:.2f}")
    etiqueta_porcentaje.config(text=f"{porcentaje:.1f}%")
    
    # Actualizar barra de progreso
    barra_progreso['value'] = porcentaje
    
    # Cambiar colores según el nivel de alerta
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
    
    # Aplicar estilos
    style.configure("Presupuesto.Horizontal.TProgressbar", 
                   troughcolor='#E0E0E0',
                   background=color_barra)
    etiqueta_estado_presupuesto.config(text=mensaje_estado, fg=color_texto)
    etiqueta_porcentaje.config(fg=color_texto)



def guardar_gasto():
    """Captura los datos y los guarda en la base de datos"""
    monto = entrada_monto.get()
    categoria = combo_categoria.get()
    descripcion = entrada_descripcion.get()
    
    if not monto or not categoria:
        messagebox.showwarning("Campos vacíos", "Por favor, completa el monto y la categoría")
        return


    try:
        monto_float = float(monto)
        if monto_float <= 0:
            messagebox.showerror("Error", "El monto debe ser mayor a cero")
            return
        
        # Verificar si excederá el presupuesto
        total_actual = mi_gestor.obtener_total()
        forzar = False

        if total_actual + monto_float > mi_gestor.limite:
            respuesta = messagebox.askyesno(
                "⚠ Advertencia de Presupuesto",
                f"Este gasto de ${monto_float:.2f} hará que superes tu presupuesto.\n\n"
                f"Total actual: ${total_actual:.2f}\n"
                f"Nuevo total: ${total_actual + monto_float:.2f}\n"
                f"Presupuesto: ${mi_gestor.limite:.2f}\n\n"
                "¿Deseas continuar de todas formas?"
            )
            if not respuesta:
                return
            forzar = True
        
        # Guardar el gasto
        desc_final = descripcion if descripcion else "Sin descripción"
        if mi_gestor.agregar_gasto(monto_float, categoria, desc_final, forzar=forzar):
            messagebox.showinfo("✓ Éxito", f"Gasto de ${monto_float:.2f} guardado en {categoria}")
            
            # Actualizar lista de categorías con la nueva (si existe)
            cats_db = [c.capitalize() for c in mi_gestor.obtener_categorias_unicas()]
            # Unir con las comunes para no perder las predefinidas
            todas_cats = sorted(list(set(CATEGORIAS_COMUNES + cats_db)))
            combo_categoria['values'] = todas_cats
            
            limpiar_campos()

            actualizar_visualizacion_presupuesto()

        else:
            messagebox.showwarning("Atención", "El gasto no se guardó.")
        

    except ValueError:
        messagebox.showerror("Error", "El monto debe ser un número válido")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el gasto: {str(e)}")


def cerrar_mes_actual():
    """Archiva el mes actual y reinicia los gastos usando el gestor"""
    respuesta = messagebox.askyesno("Confirmar Cierre de Mes", 
        "¿Estás seguro? Esto guardará el resumen en el historial y ELIMINARÁ todos los gastos actuales para empezar de cero.")
    
    if respuesta:
        exito, total = mi_gestor.cerrar_mes()
        if exito:
            # Actualizar la interfaz principal
            actualizar_visualizacion_presupuesto()
            messagebox.showinfo("✓ Mes Cerrado", 
                f"El mes se archivó con un total de ${total:,.2f}.\nLos gastos han sido reiniciados.")
        else:
            messagebox.showerror("Error", "No se pudo cerrar el mes. Revisa la base de datos.")

def ver_historial_cierres():
    """Muestra una ventana con el resumen de los meses archivados"""
    ventana_resumen = tk.Toplevel(ventana)
    ventana_resumen.title("📜 Historial de Cierres Mensuales")
    ventana_resumen.geometry("600x400")
    ventana_resumen.configure(bg=COLOR_FONDO)
    
    tk.Label(ventana_resumen, text="Resumen de Meses Archivados", 
             font=("Arial", 16, "bold"), bg=COLOR_FONDO, fg=COLOR_ACCENTO).pack(pady=20)
    
    # Tabla para mostrar los cierres
    columnas = ("Fecha", "Total Gastado", "Presupuesto", "Estado")
    tabla_cierres = ttk.Treeview(ventana_resumen, columns=columnas, show="headings", height=10)
    
    tabla_cierres.heading("Fecha", text="📅 Fecha")
    tabla_cierres.heading("Total Gastado", text="💰 Gastado")
    tabla_cierres.heading("Presupuesto", text="🎯 Presupuesto")
    tabla_cierres.heading("Estado", text="📊 Estado")
    
    tabla_cierres.column("Fecha", width=150, anchor="center")
    tabla_cierres.column("Total Gastado", width=120, anchor="center")
    tabla_cierres.column("Presupuesto", width=120, anchor="center")
    tabla_cierres.column("Estado", width=150, anchor="center")
    
    tabla_cierres.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
    
    # Cargar los datos
    datos = mi_gestor.obtener_historial_cierres()
    for fila in datos:
        # Extraemos por nombre de clave (JSON style)
        valores = (
            fila['fecha_cierre'],
            f"${float(fila['total_gastado']):,.2f}",
            f"${float(fila['presupuesto_fijado']):,.2f}",
            fila['estado']
        )
        
        tag = 'excedido' if "Excedido" in fila['estado'] else 'normal'
        tabla_cierres.insert("", tk.END, values=valores, tags=(tag,))

    tabla_cierres.tag_configure('excedido', foreground="#ff5252")
    
    tk.Button(ventana_resumen, text="Cerrar", command=ventana_resumen.destroy, 
              bg="#555555", fg="white", font=("Arial", 10)).pack(pady=10)

def mostrar_grafico_historial():
    try:
        datos = mi_gestor.obtener_gastos_por_mes()
        fig = crear_grafico_gastos_por_mes(datos)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el gráfico:\n{e}")
        return
    # Crear una ventana emergente para el gráfico
    win = tk.Toplevel()
    win.title("Historial de cierres – Gastos por mes")
    win.geometry("900x500")
    win.configure(bg="#f5f5f5")   # fondo neutro
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    # Botón para cerrar
    ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=10)

    def fade_in(alpha=0.0):
        if alpha < 1.0:
            alpha += 0.05
            win.attributes('-alpha', alpha)
            win.after(20, lambda: fade_in(alpha))
    fade_in()   


def ver_historial():
    """Muestra el historial completo de gastos con diseño Premium y edición completa"""
    ventana_historial = tk.Toplevel(ventana)
    ventana_historial.title("📊 Historial Detallado de Gastos")
    ventana_historial.geometry("1000x700") 
    ventana_historial.configure(bg=COLOR_FONDO)
    
    frame_hist = tk.Frame(ventana_historial, bg=COLOR_FONDO, padx=20, pady=20)
    frame_hist.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # --- NUEVO CODIGO --- Filtro por tiempo

    frame_filtros = tk.Frame(frame_hist, bg=COLOR_FONDO)
    frame_filtros.pack(pady=10)

    tk.Label(frame_filtros, text="Filtrar por tiempo:", bg=COLOR_FONDO, fg=COLOR_ACCENTO).pack(side=tk.LEFT, padx=5)
    
    combo_filtro = ttk.Combobox(frame_filtros, values=["Todos", "Hoy", "Semana", "Mes", "Año", "personalizado"], width=15)
    combo_filtro.pack(side=tk.LEFT, padx=5)

    tk.Label(frame_filtros, text="Categoría:", bg=COLOR_FONDO, fg=COLOR_ACCENTO).pack(side=tk.LEFT, padx=(15,5))
    
    # Obtener categorías únicas para el filtro
    cats_para_filtro = ["Todas"] + sorted([c.capitalize() for c in mi_gestor.obtener_categorias_unicas()])
    combo_cat_filtro = ttk.Combobox(frame_filtros, values=cats_para_filtro, width=15, state="readonly")
    combo_cat_filtro.pack(side=tk.LEFT, padx=5)
    combo_cat_filtro.set("Todas")

    tk.Label(frame_filtros, text="Desde:", bg=COLOR_FONDO, fg="white").pack(side=tk.LEFT, padx=(10,2))
    entry_manual_inicio = tk.Entry(frame_filtros, width=10, bg="#2a2a3d", fg="white")
    entry_manual_inicio.pack(side=tk.LEFT, padx=2)
    entry_manual_inicio.insert(0, datetime.now().strftime('%Y-%m-%d')) 

    tk.Label(frame_filtros, text="Hasta:", bg=COLOR_FONDO, fg="white").pack(side=tk.LEFT, padx=(5,2))
    entry_manual_fin = tk.Entry(frame_filtros, width=10, bg="#2a2a3d", fg="white")
    entry_manual_fin.pack(side=tk.LEFT, padx=2)
    entry_manual_fin.insert(0, datetime.now().strftime('%Y-%m-%d'))


    # Esto va justo debajo de combo_filtro_tiempo.pack(...)
    
    def aplicar_filtro_tiempo(event=None):
        opcion_tiempo = combo_filtro.get()
        categoria_seleccionada = combo_cat_filtro.get()
        
        # 1. Determinar fechas
        if opcion_tiempo == "Todos":
            f_ini, f_fin = None, None
            entry_manual_inicio.delete(0, tk.END)
            entry_manual_fin.delete(0, tk.END)
        else:
            if opcion_tiempo in ["personalizado", "Personalizado"]:
                f_ini = entry_manual_inicio.get()
                f_fin = entry_manual_fin.get()
            else:
                f_ini, f_fin = filtrar_por_tiempo(opcion_tiempo)
                entry_manual_inicio.delete(0, tk.END)
                entry_manual_inicio.insert(0, f_ini)
                entry_manual_fin.delete(0, tk.END)
                entry_manual_fin.insert(0, f_fin)

        # 2. Obtener datos base (por tiempo si existe)
        if f_ini and f_fin:
            datos = mi_gestor.obtener_todos_los_gastos_filtrados(f_ini, f_fin)
        else:
            datos = mi_gestor.obtener_todos_los_gastos()

        # 3. Filtrar por CAPA de categoría si no es "Todas"
        if categoria_seleccionada != "Todas":
            datos = [g for g in datos if str(g['categoria']).lower() == categoria_seleccionada.lower()]

        cargar_datos_en_tabla(datos)

    combo_filtro.bind("<<ComboboxSelected>>", aplicar_filtro_tiempo)
    combo_cat_filtro.bind("<<ComboboxSelected>>", aplicar_filtro_tiempo)
    combo_filtro.current(0)
    
    tk.Label(frame_hist, text=" Historial Completo de Gastos", 
            font=("Arial", 18, "bold"), bg=COLOR_FONDO, fg=COLOR_ACCENTO).pack(pady=(0, 20))
    
    def ordenar_por_monto():
        # Llamamos al nuevo método del gestor
        datos_ordenados = mi_gestor.obtener_gastos_ordenados_por_monto()
        # Refrescamos la tabla con los nuevos datos
        cargar_datos_en_tabla(datos_ordenados)

        ventana_historial.update_idletasks()

    # --- CONFIGURACIÓN DE ESTILO ---
    estilo_tabla = ttk.Style()
    estilo_tabla.theme_use("clam")
    estilo_tabla.configure("Treeview", 
                          background="#2a2a3d", 
                          foreground="white", 
                          fieldbackground="#2a2a3d",
                          rowheight=30,
                          font=("Arial", 10))
    estilo_tabla.map("Treeview", background=[('selected', '#bb86fc')], foreground=[('selected', 'black')])
    estilo_tabla.configure("Treeview.Heading", 
                          background="#3a3a5d", 
                          foreground="white", 
                          font=('Arial', 11, 'bold'))

    tk.Label(frame_hist, text="🔍 Buscar gasto:", bg="#1e1e2e", fg="white").pack(pady=5)

    entrada_busqueda = tk.Entry(frame_hist, bg="#2a2a3d", fg="white", font=("Arial", 10))
    entrada_busqueda.pack(pady=5)

    entrada_busqueda.bind("<KeyRelease>", lambda event: filtro_busqueda())

    tk.Button(frame_filtros, text="➡️ Aplicar", command=aplicar_filtro_tiempo, 
             bg="#3f51b5", fg="white", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=10)

    combo_filtro.bind("<<ComboboxSelected>>", aplicar_filtro_tiempo)
    combo_filtro.current(0)
    
    def filtro_busqueda():
        texto = entrada_busqueda.get()
        for fila in tabla.get_children():
            tabla.delete(fila)

        resultados = mi_gestor.buscar_gastos(texto)

        for i, gasto in enumerate(resultados):
            tag_color = 'par' if i % 2 == 0 else 'impar'
            valores = (
                gasto['id'], 
                f"${float(gasto['monto']):.2f}", 
                gasto['categoria'], 
                gasto['fecha'], 
                gasto['descripcion']
            )
            tabla.insert("", "end", values=valores, tags=(tag_color,)) 
        actualizar_total_visual()
        actualizar_resumen_categorias() # ¡Importante! Actualizar el desglose al buscar
        
    # Etiqueta para el total (Debajo del buscador)
    label_total = tk.Label(frame_hist, text="Total en pantalla: $0.00", font=("Arial", 12, "bold"), bg="#1e1e2e", fg="#4CAF50")
    label_total.pack(pady=(0, 10))

    def actualizar_resumen_categorias():
        # Habilitar para poder borrar e insertar
        label_resumen_cats.config(state=tk.NORMAL)
        label_resumen_cats.delete("1.0", tk.END)
        
        resumen = {}
        LIMITE_CATEGORIA = 5000.00
        suma = 0.0  # ✅ Inicializar suma
        
        for item in tabla.get_children():
            valores = tabla.item(item)["values"]
            monto = float(str(valores[1]).replace('$', '').replace(',', ''))
            categoria = valores[2]
            resumen[categoria] = resumen.get(categoria, 0) + monto
            suma += monto  # ✅ Acumular suma total

        if not resumen:
            label_resumen_cats.insert(tk.END, "Realiza un filtro para ver el desglose", "normal")
        else:
            for cat, total in resumen.items():
                texto = f"{cat}: ${total:,.2f}\n"
                # Elegir color por línea
                tag = "rojo" if total > LIMITE_CATEGORIA else "verde"
                label_resumen_cats.insert(tk.END, texto, tag)

        # Volver a deshabilitar para que el usuario no pueda escribir en él
        label_resumen_cats.config(state=tk.DISABLED)
        
        # CAMBIAR COLOR TAMBIÉN EN EL TOTAL PRINCIPAL
        color_total = "#FF3131" if suma > mi_gestor.limite else "#00FF00"
        
        try:
            label_total.config(text=f"💰 Total en pantalla: ${suma:,.2f}", fg=color_total)
        except NameError:
            pass

    # Creamos un contenedor para que se vea ordenado
    frame_resumen = tk.LabelFrame(ventana_historial, text="📊 Desglose por Categoría", bg="#1e1e2e", fg="white")
    frame_resumen.pack(side=tk.BOTTOM, fill="x", padx=20, pady=5)

    # Etiqueta donde se escribirá el resumen
        # Widget de Texto (reemplaza al Label) para permitir múltiples colores
    label_resumen_cats = tk.Text(frame_resumen, height=6, bg="#1e1e2e", font=("Arial", 10, "bold"), bd=0, highlightthickness=0, cursor="arrow")
    label_resumen_cats.pack(pady=5, fill="x")
    
    # Configuramos los colores (tags)
    label_resumen_cats.tag_configure("rojo", foreground="#FF3131", justify='center')
    label_resumen_cats.tag_configure("verde", foreground="#00FF00", justify='center')
    label_resumen_cats.tag_configure("normal", foreground="white", justify='center')
    label_resumen_cats.config(state=tk.DISABLED) # Deshabilitar escritura manual

    # Creamos la tabla
    columnas = ("ID", "Monto", "Categoría", "Fecha", "Descripción")
    tabla = ttk.Treeview(frame_hist, columns=columnas, show="headings", height=8)
    
    tabla.heading("ID", text="🆔 ID")
    tabla.heading("Monto", text="💰 Monto ($)")
    tabla.heading("Categoría", text="🏷 Categoría")
    tabla.heading("Fecha", text="📅 Fecha")
    tabla.heading("Descripción", text="📝 Descripción")

    tabla.column("ID", width=60, anchor="center")
    tabla.column("Monto", width=120, anchor="center")
    tabla.column("Categoría", width=150, anchor="center")
    tabla.column("Fecha", width=130, anchor="center")
    tabla.column("Descripción", width=300, anchor="w")

    scrollbar = ttk.Scrollbar(frame_hist, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    
    tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    # Colores para el efecto cebra
    tabla.tag_configure('par', background='#2e2e3e', foreground='white')
    tabla.tag_configure('impar', background='#1e1e2e', foreground='white')  
    
    # --- FUNCIONES INTERNAS ---

    def cargar_datos_en_tabla(lista_gastos=None):
        if lista_gastos is None:
            lista_gastos = mi_gestor.obtener_todos_los_gastos()

        for i in tabla.get_children():
            tabla.delete(i)

        for i, fila in enumerate(lista_gastos):
            tag_color = 'par' if i % 2 == 0 else 'impar'
            valores = (
                fila['id'], 
                f"${float(fila['monto']):.2f}", 
                fila['categoria'], 
                fila['fecha'], 
                fila['descripcion']
            )
            
            tabla.insert('', 'end', values=valores, tags=(tag_color,))
        
        actualizar_total_visual() 
        actualizar_resumen_categorias() # ¡Asegurar que el desglose siempre se actualiza!

    def actualizar_total_visual():
        suma = 0.0
        for fila in tabla.get_children():
            valores = tabla.item(fila, 'values')
            try:
                # El valor viene como "$150.00", quitamos el $
                monto_str = str(valores[1]).replace("$", "")
                suma += float(monto_str)
            except ValueError:
                pass
        
        # Si label_total no existiera aún (por orden de declaración), lo manejamos
        try:
            label_total.config(text=f"💰 Total en pantalla: ${suma:.2f}")
        except NameError:
            pass


    def abrir_ventana_editar(valores_fila):
        # valores_fila contiene: (ID, Monto, Categoría, Fecha, Descripción)
        id_gasto = valores_fila[0]
        
        ventana_edit = tk.Toplevel(ventana_historial)
        ventana_edit.title(f"Editando Gasto #{id_gasto}")
        ventana_edit.geometry("350x480")
        ventana_edit.configure(bg="#1e1e2e") 
        ventana_edit.grab_set() 

        # Campos de entrada
        tk.Label(ventana_edit, text="Monto:", bg="#1e1e2e", fg="white").pack(pady=(10,0))
        entry_monto = tk.Entry(ventana_edit)
        entry_monto.insert(0, str(valores_fila[1]).replace("$", "").replace(",", ""))
        entry_monto.pack(pady=5)

        tk.Label(ventana_edit, text="Categoría:", bg="#1e1e2e", fg="white").pack(pady=(10,0))
        entry_cat = tk.Entry(ventana_edit)
        entry_cat.insert(0, valores_fila[2])
        entry_cat.pack(pady=5)

        tk.Label(ventana_edit, text="Descripción:", bg="#1e1e2e", fg="white").pack(pady=(10,0))
        entry_desc = tk.Entry(ventana_edit)
        entry_desc.insert(0, valores_fila[4])
        entry_desc.pack(pady=5)

        tk.Label(ventana_edit, text="Fecha (AAAA-MM-DD):", bg="#1e1e2e", fg="white").pack(pady=(10,0))
        entry_fecha = tk.Entry(ventana_edit)
        entry_fecha.insert(0, valores_fila[3])
        entry_fecha.pack(pady=5)

        def guardar_cambios():
            monto_val = entry_monto.get()
            cat_val = entry_cat.get()
            desc_val = entry_desc.get()
            fecha_val = entry_fecha.get()

            if not monto_val or not cat_val:
                messagebox.showwarning("Campos vacíos", "Por favor, completa el monto y la categoría")
                return

            try:
                float(monto_val)
            except ValueError:
                messagebox.showerror("Error de Dato", "El monto debe ser un número válido.")
                return

            if mi_gestor.actualizar_gasto(id_gasto, monto_val, cat_val, desc_val, fecha_val):
                cargar_datos_en_tabla() 
                actualizar_visualizacion_presupuesto() 
                ventana_edit.destroy()
                messagebox.showinfo("Éxito", "Gasto actualizado")
            else:
                messagebox.showerror("Error", "No se pudo actualizar. Revisa los datos.")

        tk.Button(ventana_edit, text="ACTUALIZAR", command=guardar_cambios, 
                  bg="#bb86fc", fg="black", font=("Arial", 10, "bold")).pack(pady=20)

    def preparar_edicion():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un gasto de la lista para editar.")
            return
            
        item = tabla.item(seleccion[0]) # Usar el primer elemento por seguridad en single-select
        valores_fila = item['values'] 
        abrir_ventana_editar(valores_fila)

    def editar_seleccionado():
        preparar_edicion()

    def confirmar_eliminar_uno():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un gasto.")
            return
            
        item_id = seleccion[0]
        gasto_id = tabla.item(item_id)['values'][0]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar el gasto ID {gasto_id}?"):
            if mi_gestor.eliminar_gasto(gasto_id):
                tabla.delete(item_id)
                actualizar_total_visual() # Actualizar total en la ventana de historial
                actualizar_visualizacion_presupuesto() # Actualizar dashboard
                messagebox.showinfo("Éxito", "Gasto eliminado correctamente")

    def confirmar_limpieza_total():
        if messagebox.askyesno("💣 PELIGRO", "¿Borrar TODO el historial?"):
            if mi_gestor.eliminar_todos_los_gastos():
                cargar_datos_en_tabla()
                actualizar_visualizacion_presupuesto()

    # --- BOTONES DE ACCIÓN ---
    f_acciones = tk.Frame(ventana_historial, bg=COLOR_FONDO)
    f_acciones.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

    tk.Button(f_acciones, text="✏️ EDITAR", command=editar_seleccionado, bg="#FF9800", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side=tk.LEFT, padx=5)
    tk.Button(f_acciones, text="❌ ELIMINAR", command=confirmar_eliminar_uno, bg="#F44336", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side=tk.LEFT, padx=5)
    tk.Button(f_acciones, text="💣 BORRAR TODO", command=confirmar_limpieza_total, bg="#b71c1c", fg="white", font=("Arial", 9, "bold"), padx=15).pack(side=tk.LEFT, padx=20)
    tk.Button(f_acciones, text="Cerrar", command=ventana_historial.destroy, bg="#555555", fg="white", font=("Arial", 10)).pack(side=tk.RIGHT, padx=5)

    tk.Button(f_acciones, text="🔝 ORDENAR $", command=ordenar_por_monto, 
              bg="#673AB7", fg="white", font=("Arial", 10, "bold"), padx=10).pack(side=tk.LEFT, padx=5)

    cargar_datos_en_tabla()

def ver_estadisticas():
    """Muestra estadísticas detalladas por categoría con gráfico de pastel (Histórico Completo)"""
    # 1. Obtener datos de gastos por categoría
    fecha_desde = entry_desde.get()
    fecha_hasta = entry_hasta.get() 

    gastos_por_cat = mi_gestor.obtener_gastos_por_rango(fecha_desde, fecha_hasta)
    if not gastos_por_cat:
        messagebox.showinfo("Sin datos", f"No hay gastos entre {fecha_desde} y {fecha_hasta}")
        return  

    generar_grafico(gastos_por_cat, "📊 Distribución de Gastos (Histórico)")

def ver_estadisticas_filtradas():
    """Muestra estadísticas filtradas por rango de fechas"""
    f_inicio = entry_desde.get()
    f_fin = entry_hasta.get()
    
    # Obtenemos solo los gastos en ese rango
    gastos_por_cat = mi_gestor.obtener_gastos_por_rango(f_inicio, f_fin)
    
    if not gastos_por_cat:
        messagebox.showinfo("Sin datos", f"No hay gastos entre {f_inicio} y {f_fin}")
        return

    generar_grafico(gastos_por_cat, f"📊 Gastos ({f_inicio} a {f_fin})")


def generar_grafico(gastos_por_cat, titulo_ventana):
    """Función auxiliar para generar la ventana y el gráfico"""
    if not gastos_por_cat:
        messagebox.showinfo("Sin datos", "No hay gastos registrados para este periodo")
        return
    
    # 2. Crear ventana de estadísticas
    ventana_stats = tk.Toplevel(ventana)
    ventana_stats.title(titulo_ventana)
    ventana_stats.geometry("700x600")
    ventana_stats.configure(bg=COLOR_FONDO)
    
    # 3. Preparar datos para el gráfico
    categorias = list(gastos_por_cat.keys())
    montos = list(gastos_por_cat.values())

    # 4. Creación del Gráfico de Pastel mejorado (Efecto Dona)
    figura, ax = plt.subplots(figsize=(8, 6), dpi=100)
    figura.patch.set_facecolor(COLOR_FONDO)
    
    # Paleta de colores vibrante y moderna (9 colores para 9 categorías)
    colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F06292', '#AED581', '#FFD54F', '#9B59B6']
    
    # Crea el pastel con hueco central (dona)
    wedges, texts, autotexts = ax.pie(
        montos, 
        labels=categorias, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=colores, 
        shadow=True,
        explode=[0.05] * len(categorias), # Separación elegante
        pctdistance=0.85
    )
    
    # Estilo de los porcentajes
    plt.setp(autotexts, size=10, weight="bold", color="white")
    
    # Añadir el círculo central para convertirlo en dona
    centro_circulo = plt.Circle((0,0), 0.70, fc=COLOR_FONDO)
    figura.gca().add_artist(centro_circulo)

    ax.set_title(titulo_ventana, fontsize=14, fontweight='bold', pad=20, color=COLOR_TEXTO)
    plt.setp(texts, color=COLOR_TEXTO) # Color de etiquetas externas
    ax.legend(wedges, categorias, title="Categorías", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax.axis('equal') 

    figura.tight_layout()

    # 5. Integración del gráfico en Tkinter (Canvas)
    canvas = FigureCanvasTkAgg(figura, master=ventana_stats)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Botón de cierre
    tk.Button(ventana_stats, text="Cerrar", command=ventana_stats.destroy,
              bg="#2196F3", fg="white", font=("Arial", 10), pady=5).pack(pady=10)

def modificar_presupuesto():
    """Permite al usuario cambiar el presupuesto"""
    nuevo_presupuesto = simpledialog.askfloat(
        "Modificar Presupuesto",
        f"Presupuesto actual: ${mi_gestor.limite:.2f}\n\nIngresa el nuevo presupuesto:",
        minvalue=0.01,
        initialvalue=mi_gestor.limite
    )
    
    if nuevo_presupuesto:
        mi_gestor.guardar_presupuesto(nuevo_presupuesto)
        actualizar_visualizacion_presupuesto()
        messagebox.showinfo("✓ Actualizado", 
                          f"Presupuesto actualizado a ${nuevo_presupuesto:.2f}")

def limpiar_campos():
    """Borra el contenido de las cajas de texto"""
    entrada_monto.delete(0, tk.END)
    combo_categoria.set('')
    entrada_descripcion.delete(0, tk.END)
    etiqueta_status.config(text="Esperando nuevo registro...", fg="gray")

def actualizar_preview(event):
    """Muestra qué estás escribiendo en tiempo real"""
    m = entrada_monto.get()
    c = combo_categoria.get()
    if m or c:
        etiqueta_status.config(text=f"Vas a registrar: ${m} en {c}", fg="#0066cc")
    else:
        etiqueta_status.config(text="Esperando datos...", fg="gray")

def exporta_a_excel():
    
    # Abrir diálogo para elegir dónde guardar
    archivo_ruta = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Archivo Excel", "*.xlsx"), ("Archivo CSV", "*.csv")],
        title="Guardar reporte completo"
    )
    
    if not archivo_ruta:
        return  # Usuario canceló
    
    try:
        # Verificar si eligió CSV o Excel
        if archivo_ruta.endswith('.csv'):
            # Exportar solo gastos actuales a CSV (como antes)
            f_inicio = entry_desde.get()
            f_fin = entry_hasta.get()
            gastos = mi_gestor.obtener_todos_los_gastos_filtrados(f_inicio, f_fin)
            
            if not gastos:
                messagebox.showwarning("Sin datos", f"No hay gastos entre {f_inicio} y {f_fin}")
                return
            
            import csv
            with open(archivo_ruta, mode='w', newline='', encoding='utf-8') as file:
                escritor = csv.writer(file)
                escritor.writerow(["ID", "Monto", "Categoría", "Fecha", "Descripción"])
                
                # Convertimos cada diccionario a una lista simple de sus valores
                datos_para_csv = [list(g.values()) for g in gastos]
                escritor.writerows(datos_para_csv)
            
            messagebox.showinfo("✓ Éxito", f"Archivo CSV guardado:\n{archivo_ruta}")
            
        else:
            # Exportar a Excel con múltiples hojas
            if mi_gestor.exportar_a_excel_completo(archivo_ruta):
                messagebox.showinfo("✓ Éxito", 
                    f"Archivo Excel guardado con 2 hojas:\n\n"
                    f"📄 Hoja 1: Gastos del mes actual\n"
                    f"📊 Hoja 2: Historial de cierres\n\n"
                    f"Ubicación: {archivo_ruta}")
                
                # Abrir el archivo automáticamente
                import os
                os.startfile(archivo_ruta)
            else:
                messagebox.showerror("Error", "No se pudo exportar el archivo")
                
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar: {e}")
   

# --- 3. DISEÑO VISUAL ---
# --- 3. DISEÑO VISUAL Y FLUJO PRINCIPAL ---

def iniciar_login():
    """Muestra la ventana de login antes de la app principal"""
    global ventana_login, entry_user, entry_clave
    
    print("[DEBUG] Iniciando ventana de login...")
    ventana_login = tk.Tk()  # Cambiado de Toplevel a Tk para que sea ventana independiente
    ventana_login.title("🔒 Acceso Seguro")
    ventana_login.geometry("300x350")
    ventana_login.configure(bg=COLOR_FONDO)
    ventana_login.resizable(False, False)
    
    # Forzar que la ventana aparezca al frente
    ventana_login.lift()
    ventana_login.attributes('-topmost', True)
    ventana_login.after_idle(ventana_login.attributes, '-topmost', False)
    ventana_login.focus_force()
    
    print("[DEBUG] Ventana de login creada, configurando widgets...")
    
    # Logo o Título
    tk.Label(ventana_login, text="👤", font=("Arial", 50), bg=COLOR_FONDO, fg=COLOR_ACCENTO).pack(pady=(30, 10))
    tk.Label(ventana_login, text="Iniciar Sesión", font=("Arial", 16, "bold"), bg=COLOR_FONDO, fg="white").pack(pady=10)
    
    # Entradas
    frame_campos = tk.Frame(ventana_login, bg=COLOR_FONDO)
    frame_campos.pack(padx=20, pady=10)
    
    tk.Label(frame_campos, text="Usuario:", bg=COLOR_FONDO, fg="white").pack(anchor="w")
    entry_user = ttk.Entry(frame_campos, font=("Arial", 10))
    entry_user.pack(fill=tk.X, pady=(0, 10))
    
    tk.Label(frame_campos, text="Contraseña:", bg=COLOR_FONDO, fg="white").pack(anchor="w")
    entry_clave = ttk.Entry(frame_campos, font=("Arial", 10), show="*")
    entry_clave.pack(fill=tk.X, pady=(0, 20))
    
    # Botón Entrar
    def validar():
        try:
            if entry_user.get() == "admin" and entry_clave.get() == "1234":
                print("[DEBUG] Login exitoso, cerrando ventana de login...")
                ventana_login.destroy()
                crear_ventana_principal()  # Crear la ventana principal después de login exitoso
            else:
                messagebox.showerror("Error", "Credenciales Incorrectas\nIntente: admin / 1234")
        except Exception as e:
            print(f"[ERROR] Error al iniciar aplicación: {str(e)}")
            messagebox.showerror("Error Crítico", f"No se pudo iniciar la aplicación:\n{str(e)}")


    tk.Button(ventana_login, text="ENTRAR", command=validar, 
             bg=COLOR_ACCENTO, fg="black", font=("Arial", 10, "bold"), width=15).pack(pady=10)

    # Manejar cierre de ventana
    ventana_login.protocol("WM_DELETE_WINDOW", lambda: sys.exit())
    
    print("[DEBUG] Iniciando mainloop de login...")
    ventana_login.mainloop()
    print("[DEBUG] Login cerrado.")


def cerrar_sesion():
    if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de cerrar sesión?"):
        ventana.destroy()
        iniciar_login()
        

def crear_ventana_principal():
    """Crea y muestra la ventana principal de la aplicación"""
    global ventana, style, notebook, tab_resumen, tab_registro, tab_herramientas
    global frame_presupuesto, etiqueta_presupuesto, etiqueta_gastado, etiqueta_disponible
    global barra_progreso, etiqueta_porcentaje, etiqueta_estado_presupuesto
    global entrada_monto, combo_categoria, entrada_descripcion, etiqueta_status
    global entry_desde, entry_hasta

    # --- CONFIGURACIÓN VENTANA PRINCIPAL ---
    ventana = tk.Tk()
    ventana.title("💰 Gestor de Finanzas Pro - Panel Principal")
    ventana.geometry("900x700") 
    ventana.configure(bg=COLOR_FONDO)

    # Configurar estilos globales
    style = ttk.Style()
    style.theme_use('clam')
    style.configure(".", background=COLOR_FONDO, foreground=COLOR_TEXTO, fieldbackground=COLOR_TARJETA)
    style.configure("TNotebook", background=COLOR_FONDO, tabposition='n')
    style.configure("TNotebook.Tab", background=COLOR_TARJETA, foreground="white", padding=[15, 5], font=('Arial', 10))
    style.map("TNotebook.Tab", background=[("selected", COLOR_ACCENTO)], foreground=[("selected", "black")])

    # --- ORGANIZACIÓN CON PESTAÑAS (TABS) ---
    notebook = ttk.Notebook(ventana)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Pestaña 1: Resumen (Dashboard)
    tab_resumen = ttk.Frame(notebook)
    notebook.add(tab_resumen, text="📊 Resumen")

    # Pestaña 2: registrar (Nuevo Gasto)
    tab_registro = ttk.Frame(notebook)
    notebook.add(tab_registro, text="📝 Nuevo Gasto")

    # Pestaña 3: Herramientas (Reportes y Filtros)
    tab_herramientas = ttk.Frame(notebook)
    notebook.add(tab_herramientas, text="⚙ Herramientas")


    # === CONTENIDO PESTAÑA RESUMEN ===
    frame_presupuesto = tk.Frame(tab_resumen, bg=COLOR_TARJETA, relief=tk.RAISED, bd=0)
    frame_presupuesto.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    tk.Label(frame_presupuesto, text="Estado Financiero", font=("Arial", 20, "bold"), bg=COLOR_TARJETA, fg=COLOR_TEXTO).pack(pady=20)

    # Círculos o Tarjetas de información
    frame_kpi = tk.Frame(frame_presupuesto, bg=COLOR_TARJETA)
    frame_kpi.pack(pady=20)

    # Función helper para tarjetas
    def crear_tarjeta(parent, titulo, var_label):
        card = tk.Frame(parent, bg="#33334d", padx=20, pady=15)
        card.pack(side=tk.LEFT, padx=15)
        tk.Label(card, text=titulo, font=("Arial", 10), bg="#33334d", fg="#aaaaaa").pack()
        lbl = tk.Label(card, text="$0.00", font=("Arial", 14, "bold"), bg="#33334d", fg="white")
        lbl.pack(pady=5)
        return lbl

    etiqueta_presupuesto = crear_tarjeta(frame_kpi, "Presupuesto Total", None)
    etiqueta_gastado = crear_tarjeta(frame_kpi, "Total Gastado", None)
    etiqueta_disponible = crear_tarjeta(frame_kpi, "Disponible", None)

    # Barra de Progreso Grande
    tk.Label(frame_presupuesto, text="Progreso del Presupuesto", bg=COLOR_TARJETA, fg="#aaaaaa").pack(pady=(40, 5))
    barra_progreso = ttk.Progressbar(frame_presupuesto, length=600, mode='determinate', style="Presupuesto.Horizontal.TProgressbar")
    barra_progreso.pack(ipady=5)

    etiqueta_porcentaje = tk.Label(frame_presupuesto, text="0%", bg=COLOR_TARJETA, fg="white", font=("Arial", 12, "bold"))
    etiqueta_porcentaje.pack(pady=5)

    etiqueta_estado_presupuesto = tk.Label(frame_presupuesto, text="--", font=("Arial", 12), bg=COLOR_TARJETA, fg="#4CAF50")
    etiqueta_estado_presupuesto.pack(pady=10)

    tk.Button(frame_presupuesto, text="Modificar Presupuesto", command=modificar_presupuesto, 
              bg=COLOR_ACCENTO, fg="black", font=("Arial", 10)).pack(pady=20)

    btn_grafico = ttk.Button(frame_presupuesto, text="📊 Ver historial mensual",
                         command=mostrar_grafico_historial)
    btn_grafico.pack(side=tk.LEFT, padx=5, pady=5)

    # === CONTENIDO PESTAÑA REGISTRO ===
    frame_center = tk.Frame(tab_registro, bg=COLOR_FONDO)
    frame_center.place(relx=0.5, rely=0.5, anchor="center") # Centrado en pantalla

    tk.Label(frame_center, text="Registrar Gasto", font=("Arial", 18), bg=COLOR_FONDO, fg="white").pack(pady=20)

    tk.Label(frame_center, text="Monto ($):", bg=COLOR_FONDO, fg="#aaaaaa").pack(anchor="w")
    entrada_monto = ttk.Entry(frame_center, font=("Arial", 14), width=25)
    entrada_monto.pack(pady=5)
    entrada_monto.bind('<KeyRelease>', actualizar_preview)

    tk.Label(frame_center, text="Categoría:", bg=COLOR_FONDO, fg="#aaaaaa").pack(anchor="w", pady=(10,0))
    combo_categoria = ttk.Combobox(frame_center, values=CATEGORIAS_COMUNES, font=("Arial", 12), width=23)
    combo_categoria.pack(pady=5)
    combo_categoria.bind('<<ComboboxSelected>>', actualizar_preview)
    
    # Cargar categorías desde la BD al inicio
    try:
        cats_db = [c.capitalize() for c in mi_gestor.obtener_categorias_unicas()]
        todas_cats = sorted(list(set(CATEGORIAS_COMUNES + cats_db)))
        combo_categoria['values'] = todas_cats
    except Exception as e:
        print(f"Error cargando categorías: {e}")


    tk.Label(frame_center, text="Descripción:", bg=COLOR_FONDO, fg="#aaaaaa").pack(anchor="w", pady=(10,0))
    entrada_descripcion = ttk.Entry(frame_center, font=("Arial", 12), width=25)
    entrada_descripcion.pack(pady=5)

    etiqueta_status = tk.Label(frame_center, text="...", bg=COLOR_FONDO, fg="#666666", font=("Arial", 9, "italic"))
    etiqueta_status.pack(pady=15)

    btn_guardar = tk.Button(frame_center, text=" \U0001F4BE GUARDAR GASTO", command=guardar_gasto, 
                           bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=30, pady=10)
    btn_guardar.pack(pady=10)


    # === CONTENIDO PESTAÑA HERRAMIENTAS ===
    frame_tools = tk.Frame(tab_herramientas, bg=COLOR_FONDO, padx=20, pady=20)
    frame_tools.pack(fill=tk.BOTH, expand=True)

    # Sección Filtros
    frame_f = tk.LabelFrame(frame_tools, text="Filtros de Fecha", bg=COLOR_FONDO, fg="#aaaaaa", padx=15, pady=15)
    frame_f.pack(fill=tk.X, pady=10)

    entry_desde = tk.Entry(frame_f, bg=COLOR_TARJETA, fg="white", width=15)
    entry_desde.pack(side=tk.LEFT, padx=5)
    entry_desde.insert(0, "2025-01-01")

    tk.Label(frame_f, text="a", bg=COLOR_FONDO, fg="white").pack(side=tk.LEFT)

    entry_hasta = tk.Entry(frame_f, bg=COLOR_TARJETA, fg="white", width=15)
    entry_hasta.pack(side=tk.LEFT, padx=5)
    entry_hasta.insert(0, "2025-12-31")

    tk.Button(frame_f, text="Aplicar Filtros", command=ver_estadisticas_filtradas, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=15)

    # Sección Botones Grandes
    frame_btns = tk.Frame(frame_tools, bg=COLOR_FONDO)
    frame_btns.pack(fill=tk.BOTH, expand=True, pady=20)

    def crear_btn_tool(parent, texto, cmd, color, icono="🔹"):
        btn = tk.Button(parent, text=f"{icono}  {texto}", command=cmd, 
                       bg=color, fg="white", font=("Arial", 11), pady=10, anchor="w", padx=20)
        btn.pack(fill=tk.X, pady=5)

    crear_btn_tool(frame_btns, "Ver Historial Completo", ver_historial, "#3f51b5", "📜")
    crear_btn_tool(frame_btns, "Ver Gráficos Estadísticos", ver_estadisticas, "#673AB7", "📈")
    crear_btn_tool(frame_btns, "Exportar Reporte a Excel/CSV", exporta_a_excel, "#009688", "📥")
    crear_btn_tool(frame_btns, "Limpiar Campos de Registro", limpiar_campos, "#FF9800", "🧹")
    crear_btn_tool(frame_btns, "Ver Historial de Cierres", ver_historial_cierres, "#4CAF50", "📊")
    crear_btn_tool(frame_btns, "Cerrar Mes Actual (Archivar)", cerrar_mes_actual, "#d32f2f", "🗓️")

    # Footer
    tk.Label(ventana, text="Gestor de Finanzas Pro v2.0 - Sistema Seguro", 
            font=("Arial", 8), bg=COLOR_FONDO, fg="#444466").pack(side=tk.BOTTOM, pady=5)

    # Botón de Cerrar Sesión
    tk.Button(ventana, text="🔒 Cerrar Sesión", command=cerrar_sesion, 
              bg="#e57373", fg="white", font=("Arial", 9, "bold")).pack(side=tk.BOTTOM, pady=(0, 10))

    # --- INICIALIZACIÓN ---
    # Actualizar la visualización del presupuesto al iniciar
    actualizar_visualizacion_presupuesto()

    # --- INICIAR APLICACIÓN ---
    print("Iniciando Gestor de Finanzas Pro...")
    ventana.mainloop()
    print("Aplicación cerrada.")

# --- LANZAMIENTO ---
print("[DEBUG] Preparando lanzamiento...")
mostrar_login = True  # Sistema de login activado
if mostrar_login:
    iniciar_login()  # Esto levanta el popup y bloquea hasta el login exitoso
else:
    print("[DEBUG] Saltando login, creando ventana principal...")
    crear_ventana_principal()  # Ir directo a la ventana principal

if __name__ == "__main__":
    try:
        # El comando se ejecuta en la terminal, no aquí.
        ventana.mainloop()
    except Exception as e:
        logging.critical("CRASH DETECTADO: ", exc_info=True)
        messagebox.showerror("Error Crítico", f"Ocurrió un error inesperado. Revisa app.log\n\nError: {e}")