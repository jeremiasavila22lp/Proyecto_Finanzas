"""
TUTORIAL COMPLETO DE PYTHON
===========================
Temas:
1. Bucles de 10 días
2. Funciones del 11_día
3. Módulos de 12 días
4. Comprensión de listas de 13 días
"""

# ============================================================================
# 1. BUCLES DE 10 DÍAS
# ============================================================================
print("=" * 80)
print("1. BUCLES - Estructuras de repetición")
print("=" * 80)

# --- BUCLE FOR ---
print("\n--- BUCLE FOR ---")
print("Uso: Cuando sabes cuántas veces quieres repetir algo\n")

# Ejemplo 1: Iterar sobre una lista
print("Ejemplo 1: Iterar sobre frutas")
frutas = ["manzana", "banana", "naranja", "uva"]
for fruta in frutas:
    print(f"  Me gusta la {fruta}")

# Ejemplo 2: Usar range() para números
print("\nEjemplo 2: Contar del 1 al 5")
for i in range(1, 6):
    print(f"  Número: {i}")

# Ejemplo 3: Iterar con índice usando enumerate()
print("\nEjemplo 3: Lista con índices")
colores = ["rojo", "verde", "azul"]
for indice, color in enumerate(colores, start=1):
    print(f"  Color #{indice}: {color}")

# Ejemplo 4: Iterar sobre un diccionario
print("\nEjemplo 4: Diccionario de estudiantes")
estudiantes = {"Juan": 85, "María": 92, "Pedro": 78}
for nombre, nota in estudiantes.items():
    print(f"  {nombre} obtuvo {nota} puntos")

# Ejemplo 5: Bucle anidado (tablas de multiplicar)
print("\nEjemplo 5: Tabla de multiplicar del 2 y 3")
for numero in [2, 3]:
    print(f"\n  Tabla del {numero}:")
    for i in range(1, 6):
        print(f"    {numero} x {i} = {numero * i}")

# --- BUCLE WHILE ---
print("\n\n--- BUCLE WHILE ---")
print("Uso: Cuando no sabes cuántas veces repetir, pero tienes una condición\n")

# Ejemplo 1: Contador simple
print("Ejemplo 1: Contar hasta 5")
contador = 1
while contador <= 5:
    print(f"  Contador: {contador}")
    contador += 1

# Ejemplo 2: Validación de entrada
print("\nEjemplo 2: Simulación de validación de contraseña")
intentos = 0
max_intentos = 3
password_correcta = "python123"
password_ingresada = ""

# Simulamos intentos fallidos y luego exitoso
intentos_simulados = ["abc", "123", "python123"]
while intentos < max_intentos and password_ingresada != password_correcta:
    password_ingresada = intentos_simulados[intentos]
    intentos += 1
    if password_ingresada == password_correcta:
        print(f"  ¡Contraseña correcta en intento {intentos}!")
    else:
        print(f"  Intento {intentos}: Contraseña incorrecta")

# Ejemplo 3: Acumulador
print("\nEjemplo 3: Sumar números hasta llegar a 20")
suma = 0
numero = 1
while suma < 20:
    suma += numero
    print(f"  Sumando {numero}, total: {suma}")
    numero += 1

# --- BREAK y CONTINUE ---
print("\n\n--- BREAK y CONTINUE ---")

# Ejemplo con BREAK
print("Ejemplo con BREAK: Buscar un número específico")
numeros = [1, 3, 5, 7, 9, 11, 13]
buscar = 7
for num in numeros:
    if num == buscar:
        print(f"  ¡Encontrado! El número {buscar} está en la lista")
        break
    print(f"  Revisando: {num}")

# Ejemplo con CONTINUE
print("\nEjemplo con CONTINUE: Saltar números pares")
for num in range(1, 11):
    if num % 2 == 0:
        continue  # Salta los números pares
    print(f"  Número impar: {num}")


# ============================================================================
# 2. FUNCIONES DEL 11_DÍA
# ============================================================================
print("\n\n" + "=" * 80)
print("2. FUNCIONES - Bloques de código reutilizables")
print("=" * 80)

# --- FUNCIONES BÁSICAS ---
print("\n--- FUNCIONES BÁSICAS ---\n")

# Ejemplo 1: Función simple sin parámetros
def saludar():
    """Función que imprime un saludo"""
    print("  ¡Hola, bienvenido a Python!")

print("Ejemplo 1: Función sin parámetros")
saludar()

# Ejemplo 2: Función con parámetros
def saludar_persona(nombre):
    """Función que saluda a una persona específica"""
    print(f"  ¡Hola, {nombre}! ¿Cómo estás?")

print("\nEjemplo 2: Función con parámetros")
saludar_persona("Carlos")
saludar_persona("Ana")

# Ejemplo 3: Función con retorno
def sumar(a, b):
    """Suma dos números y retorna el resultado"""
    return a + b

print("\nEjemplo 3: Función con retorno")
resultado = sumar(5, 3)
print(f"  5 + 3 = {resultado}")

# Ejemplo 4: Función con múltiples parámetros y valores por defecto
def crear_perfil(nombre, edad, ciudad="Desconocida"):
    """Crea un perfil de usuario"""
    return {
        "nombre": nombre,
        "edad": edad,
        "ciudad": ciudad
    }

print("\nEjemplo 4: Parámetros con valores por defecto")
perfil1 = crear_perfil("Laura", 25, "Madrid")
perfil2 = crear_perfil("Miguel", 30)  # Usa el valor por defecto
print(f"  Perfil 1: {perfil1}")
print(f"  Perfil 2: {perfil2}")

# --- FUNCIONES AVANZADAS ---
print("\n\n--- FUNCIONES AVANZADAS ---\n")

# Ejemplo 5: Función con *args (argumentos variables)
def sumar_todos(*numeros):
    """Suma cualquier cantidad de números"""
    total = sum(numeros)
    return total

print("Ejemplo 5: *args - Argumentos variables")
print(f"  Suma de 1, 2, 3: {sumar_todos(1, 2, 3)}")
print(f"  Suma de 10, 20, 30, 40: {sumar_todos(10, 20, 30, 40)}")

# Ejemplo 6: Función con **kwargs (argumentos con nombre)
def mostrar_info(**datos):
    """Muestra información de forma flexible"""
    print("  Información recibida:")
    for clave, valor in datos.items():
        print(f"    {clave}: {valor}")

print("\nEjemplo 6: **kwargs - Argumentos con nombre")
mostrar_info(nombre="Pedro", edad=28, profesion="Ingeniero")

# Ejemplo 7: Función lambda (anónima)
print("\nEjemplo 7: Funciones lambda")
cuadrado = lambda x: x ** 2
print(f"  Cuadrado de 5: {cuadrado(5)}")

# Lambda con múltiples parámetros
multiplicar = lambda x, y: x * y
print(f"  3 × 4 = {multiplicar(3, 4)}")

# Ejemplo 8: Funciones como argumentos (callbacks)
def aplicar_operacion(numeros, operacion):
    """Aplica una operación a cada número"""
    return [operacion(num) for num in numeros]

print("\nEjemplo 8: Funciones como argumentos")
nums = [1, 2, 3, 4, 5]
cuadrados = aplicar_operacion(nums, lambda x: x ** 2)
print(f"  Números: {nums}")
print(f"  Cuadrados: {cuadrados}")

# Ejemplo 9: Decoradores básicos
def mi_decorador(func):
    """Decorador que añade funcionalidad extra"""
    def wrapper():
        print("  --- Antes de la función ---")
        func()
        print("  --- Después de la función ---")
    return wrapper

@mi_decorador
def decir_hola():
    print("  ¡Hola desde la función decorada!")

print("\nEjemplo 9: Decoradores")
decir_hola()

# Ejemplo 10: Función recursiva
def factorial(n):
    """Calcula el factorial de un número"""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print("\nEjemplo 10: Recursión")
print(f"  Factorial de 5: {factorial(5)}")
print(f"  5! = 5 × 4 × 3 × 2 × 1 = {factorial(5)}")


# ============================================================================
# 3. MÓDULOS DE 12 DÍAS
# ============================================================================
print("\n\n" + "=" * 80)
print("3. MÓDULOS - Organización y reutilización de código")
print("=" * 80)

# --- IMPORTAR MÓDULOS ESTÁNDAR ---
print("\n--- MÓDULOS ESTÁNDAR DE PYTHON ---\n")

# Ejemplo 1: Módulo math
import math

print("Ejemplo 1: Módulo math (matemáticas)")
print(f"  Pi: {math.pi}")
print(f"  Raíz cuadrada de 16: {math.sqrt(16)}")
print(f"  Seno de 90°: {math.sin(math.radians(90))}")
print(f"  Redondear hacia arriba 3.2: {math.ceil(3.2)}")

# Ejemplo 2: Módulo random
import random

print("\nEjemplo 2: Módulo random (números aleatorios)")
print(f"  Número aleatorio entre 1 y 10: {random.randint(1, 10)}")
print(f"  Elemento aleatorio de lista: {random.choice(['rojo', 'verde', 'azul'])}")
lista_numeros = [1, 2, 3, 4, 5]
random.shuffle(lista_numeros)
print(f"  Lista mezclada: {lista_numeros}")

# Ejemplo 3: Módulo datetime
from datetime import datetime, timedelta

print("\nEjemplo 3: Módulo datetime (fechas y horas)")
ahora = datetime.now()
print(f"  Fecha y hora actual: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  Solo fecha: {ahora.strftime('%d/%m/%Y')}")
manana = ahora + timedelta(days=1)
print(f"  Mañana será: {manana.strftime('%d/%m/%Y')}")

# Ejemplo 4: Módulo os
import os

print("\nEjemplo 4: Módulo os (sistema operativo)")
print(f"  Directorio actual: {os.getcwd()}")
print(f"  Sistema operativo: {os.name}")

# Ejemplo 5: Módulo json
import json

print("\nEjemplo 5: Módulo json (trabajar con JSON)")
datos = {
    "nombre": "Python",
    "version": 3.9,
    "caracteristicas": ["simple", "potente", "versátil"]
}
json_string = json.dumps(datos, indent=2)
print("  Datos en formato JSON:")
print(f"{json_string}")

# --- DIFERENTES FORMAS DE IMPORTAR ---
print("\n\n--- FORMAS DE IMPORTAR MÓDULOS ---\n")

# Forma 1: import modulo
print("Forma 1: import math")
print(f"  math.sqrt(25) = {math.sqrt(25)}")

# Forma 2: from modulo import funcion
from math import pow
print("\nForma 2: from math import pow")
print(f"  pow(2, 3) = {pow(2, 3)}")

# Forma 3: import modulo as alias
import datetime as dt
print("\nForma 3: import datetime as dt")
print(f"  dt.datetime.now() = {dt.datetime.now().strftime('%H:%M:%S')}")

# Forma 4: from modulo import *
print("\nForma 4: from math import * (importa todo)")
print("  [!] No recomendado en produccion, puede causar conflictos")

# --- CREAR TU PROPIO MÓDULO ---
print("\n\n--- CREAR TU PROPIO MÓDULO ---\n")
print("Para crear un módulo:")
print("  1. Crea un archivo .py (ejemplo: mi_modulo.py)")
print("  2. Define funciones, clases o variables")
print("  3. Importa con: import mi_modulo")
print("\nEjemplo de contenido de mi_modulo.py:")
print("""
  # mi_modulo.py
  def saludar(nombre):
      return f"Hola, {nombre}"
  
  PI = 3.14159
  
  class Calculadora:
      def sumar(self, a, b):
          return a + b
""")
print("\nUso:")
print("""
  import mi_modulo
  print(mi_modulo.saludar("Ana"))
  print(mi_modulo.PI)
  calc = mi_modulo.Calculadora()
  print(calc.sumar(5, 3))
""")


# ============================================================================
# 4. COMPRENSIÓN DE LISTAS DE 13 DÍAS
# ============================================================================
print("\n\n" + "=" * 80)
print("4. COMPRENSIÓN DE LISTAS - Sintaxis concisa y elegante")
print("=" * 80)

# --- LIST COMPREHENSION BÁSICA ---
print("\n--- COMPRENSIÓN DE LISTAS BÁSICA ---\n")

# Ejemplo 1: Crear lista de cuadrados
print("Ejemplo 1: Lista de cuadrados")
# Forma tradicional
cuadrados_tradicional = []
for i in range(1, 6):
    cuadrados_tradicional.append(i ** 2)
print(f"  Forma tradicional: {cuadrados_tradicional}")

# Con list comprehension
cuadrados_comprehension = [i ** 2 for i in range(1, 6)]
print(f"  List comprehension: {cuadrados_comprehension}")

# Ejemplo 2: Transformar strings
print("\nEjemplo 2: Convertir a mayúsculas")
nombres = ["ana", "juan", "pedro", "maría"]
nombres_mayus = [nombre.upper() for nombre in nombres]
print(f"  Original: {nombres}")
print(f"  Mayúsculas: {nombres_mayus}")

# Ejemplo 3: Extraer longitudes
print("\nEjemplo 3: Longitud de palabras")
palabras = ["python", "es", "genial"]
longitudes = [len(palabra) for palabra in palabras]
print(f"  Palabras: {palabras}")
print(f"  Longitudes: {longitudes}")

# --- LIST COMPREHENSION CON CONDICIONES ---
print("\n\n--- COMPRENSIÓN DE LISTAS CON CONDICIONES ---\n")

# Ejemplo 4: Filtrar números pares
print("Ejemplo 4: Filtrar números pares")
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
pares = [num for num in numeros if num % 2 == 0]
print(f"  Números: {numeros}")
print(f"  Pares: {pares}")

# Ejemplo 5: Filtrar y transformar
print("\nEjemplo 5: Cuadrados de números impares")
cuadrados_impares = [num ** 2 for num in range(1, 11) if num % 2 != 0]
print(f"  Cuadrados de impares (1-10): {cuadrados_impares}")

# Ejemplo 6: Condición if-else
print("\nEjemplo 6: Clasificar números (par/impar)")
clasificacion = ["par" if num % 2 == 0 else "impar" for num in range(1, 6)]
print(f"  Clasificación de 1-5: {clasificacion}")

# --- LIST COMPREHENSION ANIDADA ---
print("\n\n--- COMPRENSIÓN DE LISTAS ANIDADA ---\n")

# Ejemplo 7: Matriz (lista de listas)
print("Ejemplo 7: Crear matriz 3x3")
matriz = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print("  Matriz:")
for fila in matriz:
    print(f"    {fila}")

# Ejemplo 8: Aplanar lista de listas
print("\nEjemplo 8: Aplanar lista de listas")
lista_anidada = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
aplanada = [num for sublista in lista_anidada for num in sublista]
print(f"  Original: {lista_anidada}")
print(f"  Aplanada: {aplanada}")

# --- OTRAS COMPRENSIONES ---
print("\n\n--- OTRAS COMPRENSIONES (Dict, Set) ---\n")

# Ejemplo 9: Dictionary comprehension
print("Ejemplo 9: Dictionary comprehension")
numeros = [1, 2, 3, 4, 5]
cuadrados_dict = {num: num ** 2 for num in numeros}
print(f"  Diccionario de cuadrados: {cuadrados_dict}")

# Ejemplo 10: Set comprehension
print("\nEjemplo 10: Set comprehension")
texto = "python programming"
letras_unicas = {letra for letra in texto if letra != ' '}
print(f"  Texto: '{texto}'")
print(f"  Letras únicas: {letras_unicas}")

# --- EJEMPLOS PRÁCTICOS AVANZADOS ---
print("\n\n--- EJEMPLOS PRÁCTICOS AVANZADOS ---\n")

# Ejemplo 11: Filtrar y procesar datos
print("Ejemplo 11: Procesar lista de estudiantes")
estudiantes = [
    {"nombre": "Ana", "edad": 20, "nota": 85},
    {"nombre": "Juan", "edad": 22, "nota": 92},
    {"nombre": "Pedro", "edad": 19, "nota": 78},
    {"nombre": "María", "edad": 21, "nota": 88}
]

# Obtener nombres de estudiantes aprobados (nota >= 80)
aprobados = [est["nombre"] for est in estudiantes if est["nota"] >= 80]
print(f"  Estudiantes aprobados: {aprobados}")

# Ejemplo 12: Combinación de listas
print("\nEjemplo 12: Producto cartesiano")
colores = ["rojo", "verde"]
tamaños = ["S", "M", "L"]
combinaciones = [f"{color}-{tamaño}" for color in colores for tamaño in tamaños]
print(f"  Combinaciones: {combinaciones}")

# Ejemplo 13: Procesamiento de strings
print("\nEjemplo 13: Extraer números de texto")
texto_con_numeros = "En 2024 hay 365 días y 12 meses"
numeros_en_texto = [int(palabra) for palabra in texto_con_numeros.split() if palabra.isdigit()]
print(f"  Texto: '{texto_con_numeros}'")
print(f"  Números extraídos: {numeros_en_texto}")


# ============================================================================
# RESUMEN Y COMPARACIONES
# ============================================================================
print("\n\n" + "=" * 80)
print("RESUMEN Y MEJORES PRÁCTICAS")
print("=" * 80)

print("""
1. BUCLES:
   - Usa FOR cuando sabes cuántas iteraciones necesitas
   - Usa WHILE cuando la condición de parada es dinámica
   - BREAK para salir del bucle anticipadamente
   - CONTINUE para saltar a la siguiente iteración

2. FUNCIONES:
   - Define funciones para código que usarás múltiples veces
   - Usa parámetros por defecto para flexibilidad
   - *args para número variable de argumentos posicionales
   - **kwargs para número variable de argumentos con nombre
   - Lambda para funciones simples de una línea

3. MÓDULOS:
   - Organiza código relacionado en archivos separados
   - Importa solo lo que necesitas (from modulo import funcion)
   - Usa alias para nombres largos (import numpy as np)
   - Explora módulos estándar: math, random, datetime, os, json

4. COMPRENSIÓN DE LISTAS:
   - Más concisa y legible que bucles tradicionales
   - Generalmente más rápida
   - Usa con moderación (no sacrifiques legibilidad)
   - También disponible para diccionarios y sets
   
   Sintaxis: [expresion for item in iterable if condicion]
""")

print("\n" + "=" * 80)
print("FIN DEL TUTORIAL")
print("=" * 80)
