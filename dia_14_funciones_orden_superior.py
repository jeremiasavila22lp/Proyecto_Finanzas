"""
===========================================
DÍA 14: FUNCIONES DE ORDEN SUPERIOR
===========================================

Las funciones de orden superior son funciones que pueden:
1. Recibir otras funciones como argumentos
2. Retornar funciones como resultado
3. O ambas

Son fundamentales en programación funcional y hacen el código más flexible y reutilizable.
"""

print("=" * 60)
print("DÍA 14: FUNCIONES DE ORDEN SUPERIOR EN PYTHON")
print("=" * 60)

# ===========================================
# 1. CONCEPTOS BÁSICOS
# ===========================================

print("\n" + "=" * 60)
print("1. CONCEPTOS BÁSICOS")
print("=" * 60)

# En Python, las funciones son objetos de primera clase
# Esto significa que pueden ser:
# - Asignadas a variables
# - Pasadas como argumentos
# - Retornadas desde otras funciones

def saludar():
    return "¡Hola!"

# Asignar función a una variable
mi_funcion = saludar
print(f"\nFunción asignada a variable: {mi_funcion()}")

# Las funciones pueden almacenarse en estructuras de datos
funciones = [saludar, len, str.upper]
print(f"Funciones en lista: {funciones}")


# ===========================================
# 2. MAP() - Aplicar función a cada elemento
# ===========================================

print("\n" + "=" * 60)
print("2. MAP() - Transformar elementos de una secuencia")
print("=" * 60)

print("\n--- ¿Qué hace map()? ---")
print("Aplica una función a cada elemento de un iterable")
print("Sintaxis: map(función, iterable)")

# Ejemplo 1: Elevar al cuadrado
numeros = [1, 2, 3, 4, 5]

def cuadrado(x):
    return x ** 2

resultado_map = map(cuadrado, numeros)
print(f"\nNúmeros originales: {numeros}")
print(f"Al cuadrado con map(): {list(resultado_map)}")

# Ejemplo 2: Con lambda
numeros = [1, 2, 3, 4, 5]
cubos = list(map(lambda x: x ** 3, numeros))
print(f"\nAl cubo con lambda: {cubos}")

# Ejemplo 3: Convertir temperaturas
celsius = [0, 10, 20, 30, 40]
fahrenheit = list(map(lambda c: (c * 9/5) + 32, celsius))
print(f"\nCelsius: {celsius}")
print(f"Fahrenheit: {fahrenheit}")

# Ejemplo 4: Map con múltiples iterables
numeros1 = [1, 2, 3, 4]
numeros2 = [10, 20, 30, 40]
suma = list(map(lambda x, y: x + y, numeros1, numeros2))
print(f"\nSuma de dos listas: {suma}")

# Ejemplo 5: Procesar strings
nombres = ["juan", "maría", "pedro"]
nombres_capitalizados = list(map(str.capitalize, nombres))
print(f"\nNombres capitalizados: {nombres_capitalizados}")


# ===========================================
# 3. FILTER() - Filtrar elementos
# ===========================================

print("\n" + "=" * 60)
print("3. FILTER() - Filtrar elementos según condición")
print("=" * 60)

print("\n--- ¿Qué hace filter()? ---")
print("Filtra elementos que cumplen una condición (retorna True)")
print("Sintaxis: filter(función_booleana, iterable)")

# Ejemplo 1: Números pares
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def es_par(x):
    return x % 2 == 0

pares = list(filter(es_par, numeros))
print(f"\nNúmeros: {numeros}")
print(f"Solo pares: {pares}")

# Ejemplo 2: Con lambda - números mayores a 5
mayores_5 = list(filter(lambda x: x > 5, numeros))
print(f"Mayores a 5: {mayores_5}")

# Ejemplo 3: Filtrar strings
palabras = ["python", "es", "genial", "y", "poderoso"]
palabras_largas = list(filter(lambda p: len(p) > 3, palabras))
print(f"\nPalabras: {palabras}")
print(f"Palabras largas (>3 letras): {palabras_largas}")

# Ejemplo 4: Filtrar diccionarios
estudiantes = [
    {"nombre": "Ana", "edad": 20, "nota": 85},
    {"nombre": "Luis", "edad": 22, "nota": 92},
    {"nombre": "María", "edad": 19, "nota": 78},
    {"nombre": "Carlos", "edad": 21, "nota": 88}
]

aprobados = list(filter(lambda e: e["nota"] >= 80, estudiantes))
print(f"\nEstudiantes aprobados (nota >= 80):")
for est in aprobados:
    print(f"  {est['nombre']}: {est['nota']}")

# Ejemplo 5: Filtrar valores None
datos = [1, None, 3, None, 5, 0, 7, None]
sin_none = list(filter(lambda x: x is not None, datos))
print(f"\nDatos con None: {datos}")
print(f"Sin None: {sin_none}")


# ===========================================
# 4. REDUCE() - Reducir a un solo valor
# ===========================================

print("\n" + "=" * 60)
print("4. REDUCE() - Reducir secuencia a un valor único")
print("=" * 60)

from functools import reduce

print("\n--- ¿Qué hace reduce()? ---")
print("Aplica una función acumulativa a los elementos")
print("Reduce la secuencia a un solo valor")
print("Sintaxis: reduce(función, iterable, [inicial])")

# Ejemplo 1: Suma de todos los elementos
numeros = [1, 2, 3, 4, 5]

def sumar(acumulador, elemento):
    print(f"  Acumulador: {acumulador}, Elemento: {elemento}, Resultado: {acumulador + elemento}")
    return acumulador + elemento

print(f"\nNúmeros: {numeros}")
print("Proceso de suma:")
total = reduce(sumar, numeros)
print(f"Total: {total}")

# Ejemplo 2: Producto con lambda
numeros = [1, 2, 3, 4, 5]
producto = reduce(lambda x, y: x * y, numeros)
print(f"\nProducto de {numeros}: {producto}")

# Ejemplo 3: Encontrar el máximo
numeros = [45, 23, 89, 12, 67, 34]
maximo = reduce(lambda x, y: x if x > y else y, numeros)
print(f"\nMáximo de {numeros}: {maximo}")

# Ejemplo 4: Concatenar strings
palabras = ["Python", "es", "increíble"]
frase = reduce(lambda x, y: x + " " + y, palabras)
print(f"\nPalabras: {palabras}")
print(f"Frase: {frase}")

# Ejemplo 5: Con valor inicial
numeros = [1, 2, 3, 4, 5]
suma_con_inicial = reduce(lambda x, y: x + y, numeros, 100)
print(f"\nSuma de {numeros} con inicial 100: {suma_con_inicial}")


# ===========================================
# 5. FUNCIONES QUE RETORNAN FUNCIONES
# ===========================================

print("\n" + "=" * 60)
print("5. FUNCIONES QUE RETORNAN FUNCIONES")
print("=" * 60)

print("\n--- Closures y Factory Functions ---")

# Ejemplo 1: Función que crea multiplicadores
def crear_multiplicador(n):
    """Retorna una función que multiplica por n"""
    def multiplicar(x):
        return x * n
    return multiplicar

multiplicar_por_2 = crear_multiplicador(2)
multiplicar_por_5 = crear_multiplicador(5)

print(f"\n5 × 2 = {multiplicar_por_2(5)}")
print(f"5 × 5 = {multiplicar_por_5(5)}")

# Ejemplo 2: Función que crea saludadores
def crear_saludador(saludo):
    def saludar(nombre):
        return f"{saludo}, {nombre}!"
    return saludar

saludar_formal = crear_saludador("Buenos días")
saludar_informal = crear_saludador("Hola")

print(f"\n{saludar_formal('Sr. García')}")
print(f"{saludar_informal('amigo')}")

# Ejemplo 3: Función con estado (contador)
def crear_contador():
    contador = 0
    
    def incrementar():
        nonlocal contador
        contador += 1
        return contador
    
    return incrementar

contador1 = crear_contador()
contador2 = crear_contador()

print(f"\nContador 1: {contador1()}")  # 1
print(f"Contador 1: {contador1()}")  # 2
print(f"Contador 2: {contador2()}")  # 1


# ===========================================
# 6. DECORADORES - Funciones que modifican funciones
# ===========================================

print("\n" + "=" * 60)
print("6. DECORADORES - Modificar comportamiento de funciones")
print("=" * 60)

print("\n--- ¿Qué son los decoradores? ---")
print("Funciones que envuelven otras funciones para extender su comportamiento")

# Ejemplo 1: Decorador simple
def mi_decorador(func):
    def envoltura():
        print("  [Antes de ejecutar la función]")
        func()
        print("  [Después de ejecutar la función]")
    return envoltura

@mi_decorador
def decir_hola():
    print("  ¡Hola!")

print("\nEjecutando función decorada:")
decir_hola()

# Ejemplo 2: Decorador con argumentos
def decorador_con_args(func):
    def envoltura(*args, **kwargs):
        print(f"  Argumentos: {args}, {kwargs}")
        resultado = func(*args, **kwargs)
        print(f"  Resultado: {resultado}")
        return resultado
    return envoltura

@decorador_con_args
def sumar(a, b):
    return a + b

print("\nFunción con argumentos:")
sumar(5, 3)

# Ejemplo 3: Decorador para medir tiempo
import time

def medir_tiempo(func):
    def envoltura(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"  Tiempo de ejecución: {fin - inicio:.6f} segundos")
        return resultado
    return envoltura

@medir_tiempo
def proceso_lento():
    time.sleep(0.1)
    return "Proceso completado"

print("\nMidiendo tiempo:")
proceso_lento()


# ===========================================
# 7. SORTED() con key - Ordenamiento personalizado
# ===========================================

print("\n" + "=" * 60)
print("7. SORTED() con KEY - Ordenamiento personalizado")
print("=" * 60)

# Ejemplo 1: Ordenar por longitud
palabras = ["python", "es", "un", "lenguaje", "genial"]
ordenadas = sorted(palabras, key=len)
print(f"\nPalabras: {palabras}")
print(f"Ordenadas por longitud: {ordenadas}")

# Ejemplo 2: Ordenar por última letra
ordenadas_ultima = sorted(palabras, key=lambda p: p[-1])
print(f"Ordenadas por última letra: {ordenadas_ultima}")

# Ejemplo 3: Ordenar diccionarios
estudiantes = [
    {"nombre": "Ana", "nota": 85},
    {"nombre": "Luis", "nota": 92},
    {"nombre": "María", "nota": 78},
    {"nombre": "Carlos", "nota": 88}
]

por_nota = sorted(estudiantes, key=lambda e: e["nota"], reverse=True)
print(f"\nEstudiantes ordenados por nota:")
for est in por_nota:
    print(f"  {est['nombre']}: {est['nota']}")

# Ejemplo 4: Ordenar tuplas
puntos = [(3, 4), (1, 2), (5, 1), (2, 3)]
por_x = sorted(puntos, key=lambda p: p[0])
por_y = sorted(puntos, key=lambda p: p[1])
print(f"\nPuntos: {puntos}")
print(f"Ordenados por X: {por_x}")
print(f"Ordenados por Y: {por_y}")


# ===========================================
# 8. ANY() y ALL() - Evaluación de condiciones
# ===========================================

print("\n" + "=" * 60)
print("8. ANY() y ALL() - Evaluación de condiciones")
print("=" * 60)

print("\n--- ANY() ---")
print("Retorna True si AL MENOS UN elemento es True")

numeros = [1, 3, 5, 7, 8, 9]
hay_par = any(n % 2 == 0 for n in numeros)
print(f"\nNúmeros: {numeros}")
print(f"¿Hay algún par?: {hay_par}")

print("\n--- ALL() ---")
print("Retorna True si TODOS los elementos son True")

numeros = [2, 4, 6, 8, 10]
todos_pares = all(n % 2 == 0 for n in numeros)
print(f"\nNúmeros: {numeros}")
print(f"¿Todos son pares?: {todos_pares}")

# Ejemplo combinado
edades = [18, 21, 25, 30, 17]
print(f"\nEdades: {edades}")
print(f"¿Algún menor de edad?: {any(e < 18 for e in edades)}")
print(f"¿Todos mayores de edad?: {all(e >= 18 for e in edades)}")


# ===========================================
# 9. ZIP() - Combinar iterables
# ===========================================

print("\n" + "=" * 60)
print("9. ZIP() - Combinar múltiples iterables")
print("=" * 60)

nombres = ["Ana", "Luis", "María"]
edades = [20, 22, 19]
ciudades = ["Madrid", "Barcelona", "Valencia"]

combinado = list(zip(nombres, edades, ciudades))
print(f"\nNombres: {nombres}")
print(f"Edades: {edades}")
print(f"Ciudades: {ciudades}")
print(f"\nCombinado con zip():")
for nombre, edad, ciudad in zip(nombres, edades, ciudades):
    print(f"  {nombre}, {edad} años, de {ciudad}")

# Crear diccionario con zip
claves = ["nombre", "edad", "ciudad"]
valores = ["Pedro", 25, "Sevilla"]
persona = dict(zip(claves, valores))
print(f"\nDiccionario creado: {persona}")


# ===========================================
# 10. EJEMPLO PRÁCTICO COMPLETO
# ===========================================

print("\n" + "=" * 60)
print("10. EJEMPLO PRÁCTICO COMPLETO")
print("=" * 60)

print("\n--- Sistema de procesamiento de ventas ---")

ventas = [
    {"producto": "Laptop", "precio": 1200, "cantidad": 2},
    {"producto": "Mouse", "precio": 25, "cantidad": 5},
    {"producto": "Teclado", "precio": 75, "cantidad": 3},
    {"producto": "Monitor", "precio": 300, "cantidad": 1},
    {"producto": "USB", "precio": 15, "cantidad": 10}
]

print("\nVentas originales:")
for v in ventas:
    print(f"  {v}")

# 1. Calcular total por venta usando map()
totales = list(map(lambda v: v["precio"] * v["cantidad"], ventas))
print(f"\nTotales por venta: {totales}")

# 2. Filtrar ventas mayores a $100
ventas_grandes = list(filter(lambda v: v["precio"] * v["cantidad"] > 100, ventas))
print(f"\nVentas mayores a $100:")
for v in ventas_grandes:
    print(f"  {v['producto']}: ${v['precio'] * v['cantidad']}")

# 3. Calcular total general con reduce()
total_general = reduce(lambda acc, v: acc + (v["precio"] * v["cantidad"]), ventas, 0)
print(f"\nTotal general de ventas: ${total_general}")

# 4. Ordenar por total (sorted con key)
ventas_ordenadas = sorted(ventas, key=lambda v: v["precio"] * v["cantidad"], reverse=True)
print(f"\nVentas ordenadas por total:")
for v in ventas_ordenadas:
    total = v["precio"] * v["cantidad"]
    print(f"  {v['producto']}: ${total}")

# 5. Verificar si hay ventas caras (any/all)
hay_caras = any(v["precio"] > 1000 for v in ventas)
todas_baratas = all(v["precio"] < 2000 for v in ventas)
print(f"\n¿Hay productos caros (>$1000)?: {hay_caras}")
print(f"¿Todos los productos son <$2000?: {todas_baratas}")


# ===========================================
# 11. EJERCICIOS PRÁCTICOS
# ===========================================

print("\n" + "=" * 60)
print("11. EJERCICIOS PARA PRACTICAR")
print("=" * 60)

print("""
EJERCICIO 1: Procesamiento de números
- Crea una lista de números del 1 al 20
- Usa map() para elevar cada uno al cuadrado
- Usa filter() para quedarte solo con los mayores a 100
- Usa reduce() para sumarlos todos

EJERCICIO 2: Procesamiento de texto
- Crea una lista de frases
- Usa map() para convertirlas a mayúsculas
- Usa filter() para quedarte con las que tienen más de 10 caracteres
- Usa sorted() para ordenarlas alfabéticamente

EJERCICIO 3: Análisis de estudiantes
- Crea una lista de diccionarios con estudiantes (nombre, edad, notas)
- Filtra los que tienen promedio >= 70
- Ordénalos por promedio
- Calcula el promedio general de todos

EJERCICIO 4: Crear un decorador
- Crea un decorador que cuente cuántas veces se llama una función
- Aplícalo a varias funciones y verifica que funcione

EJERCICIO 5: Factory function
- Crea una función que genere validadores de rangos
- Por ejemplo: validador_edad = crear_validador(18, 65)
- validador_edad(25) debería retornar True
- validador_edad(70) debería retornar False
""")


# ===========================================
# RESUMEN FINAL
# ===========================================

print("\n" + "=" * 60)
print("RESUMEN - FUNCIONES DE ORDEN SUPERIOR")
print("=" * 60)

print("""
✓ MAP(): Transforma cada elemento aplicando una función
  → map(función, iterable)
  
✓ FILTER(): Filtra elementos según una condición
  → filter(función_booleana, iterable)
  
✓ REDUCE(): Reduce una secuencia a un solo valor
  → reduce(función, iterable, [inicial])
  
✓ SORTED(): Ordena con función personalizada
  → sorted(iterable, key=función)
  
✓ ANY(): True si al menos uno cumple
  → any(condición for item in iterable)
  
✓ ALL(): True si todos cumplen
  → all(condición for item in iterable)
  
✓ ZIP(): Combina múltiples iterables
  → zip(iterable1, iterable2, ...)
  
✓ DECORADORES: Modifican comportamiento de funciones
  → @decorador antes de la función
  
✓ CLOSURES: Funciones que retornan funciones
  → Útiles para crear funciones especializadas

VENTAJAS:
- Código más limpio y expresivo
- Reutilización de lógica
- Programación funcional
- Menos bucles explícitos
- Más declarativo que imperativo
""")

print("\n" + "=" * 60)
print("¡Fin del tutorial de Funciones de Orden Superior!")
print("=" * 60)
