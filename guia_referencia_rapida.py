# ============================================================================
# GUÍA DE REFERENCIA RÁPIDA - PYTHON
# ============================================================================

"""
Esta es una guía de referencia rápida con ejemplos concisos de:
1. Bucles
2. Funciones
3. Módulos
4. Comprensión de listas
"""

# ============================================================================
# 1. BUCLES - CHEAT SHEET
# ============================================================================

print("=" * 70)
print("1. BUCLES - GUÍA RÁPIDA")
print("=" * 70)

# FOR LOOP
print("\n[FOR LOOP]")
for i in range(5):
    print(f"  Iteración {i}")

# FOR con lista
frutas = ["manzana", "banana", "naranja"]
for fruta in frutas:
    print(f"  {fruta}")

# FOR con enumerate (índice + valor)
for idx, fruta in enumerate(frutas, 1):
    print(f"  {idx}. {fruta}")

# WHILE LOOP
print("\n[WHILE LOOP]")
contador = 0
while contador < 3:
    print(f"  Contador: {contador}")
    contador += 1

# BREAK y CONTINUE
print("\n[BREAK y CONTINUE]")
for i in range(10):
    if i == 3:
        continue  # Salta el 3
    if i == 5:
        break  # Termina en 5
    print(f"  {i}")


# ============================================================================
# 2. FUNCIONES - CHEAT SHEET
# ============================================================================

print("\n" + "=" * 70)
print("2. FUNCIONES - GUÍA RÁPIDA")
print("=" * 70)

# Función básica
def saludar(nombre):
    return f"Hola, {nombre}"

print(f"\n[FUNCIÓN BÁSICA]\n  {saludar('Ana')}")

# Función con valor por defecto
def crear_usuario(nombre, rol="usuario"):
    return {"nombre": nombre, "rol": rol}

print(f"\n[VALOR POR DEFECTO]\n  {crear_usuario('Pedro')}")

# Función con *args
def sumar(*numeros):
    return sum(numeros)

print(f"\n[*ARGS]\n  Suma: {sumar(1, 2, 3, 4, 5)}")

# Función con **kwargs
def mostrar_datos(**datos):
    return datos

print(f"\n[**KWARGS]\n  {mostrar_datos(nombre='Juan', edad=25)}")

# Lambda
cuadrado = lambda x: x ** 2
print(f"\n[LAMBDA]\n  Cuadrado de 7: {cuadrado(7)}")

# Decorador
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        print("  [Antes]")
        resultado = func(*args, **kwargs)
        print("  [Después]")
        return resultado
    return wrapper

@mi_decorador
def decir_hola():
    print("  ¡Hola!")

print("\n[DECORADOR]")
decir_hola()


# ============================================================================
# 3. MÓDULOS - CHEAT SHEET
# ============================================================================

print("\n" + "=" * 70)
print("3. MÓDULOS - GUÍA RÁPIDA")
print("=" * 70)

# Módulo math
import math
print(f"\n[MATH]\n  Pi: {math.pi:.2f}")
print(f"  Raíz de 16: {math.sqrt(16)}")

# Módulo random
import random
print(f"\n[RANDOM]\n  Número aleatorio: {random.randint(1, 100)}")
print(f"  Elección: {random.choice(['A', 'B', 'C'])}")

# Módulo datetime
from datetime import datetime
ahora = datetime.now()
print(f"\n[DATETIME]\n  Ahora: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")

# Módulo json
import json
datos = {"nombre": "Python", "version": 3.9}
print(f"\n[JSON]\n  {json.dumps(datos, indent=2)}")

# Módulo os
import os
print(f"\n[OS]\n  Directorio: {os.getcwd()}")


# ============================================================================
# 4. COMPRENSIÓN DE LISTAS - CHEAT SHEET
# ============================================================================

print("\n" + "=" * 70)
print("4. COMPRENSIÓN DE LISTAS - GUÍA RÁPIDA")
print("=" * 70)

# List comprehension básica
cuadrados = [x**2 for x in range(5)]
print(f"\n[BÁSICA]\n  Cuadrados: {cuadrados}")

# Con condición (filtro)
pares = [x for x in range(10) if x % 2 == 0]
print(f"\n[CON FILTRO]\n  Pares: {pares}")

# Con if-else
clasificacion = ["par" if x % 2 == 0 else "impar" for x in range(5)]
print(f"\n[IF-ELSE]\n  {clasificacion}")

# Anidada
matriz = [[i*j for j in range(3)] for i in range(3)]
print(f"\n[ANIDADA - MATRIZ]")
for fila in matriz:
    print(f"  {fila}")

# Dictionary comprehension
cuadrados_dict = {x: x**2 for x in range(5)}
print(f"\n[DICT COMPREHENSION]\n  {cuadrados_dict}")

# Set comprehension
letras = {letra for letra in "python"}
print(f"\n[SET COMPREHENSION]\n  {letras}")


# ============================================================================
# CASOS DE USO COMUNES
# ============================================================================

print("\n" + "=" * 70)
print("CASOS DE USO COMUNES")
print("=" * 70)

# Caso 1: Procesar lista de datos
print("\n[CASO 1: Procesar datos de productos]")
productos = [
    {"nombre": "Laptop", "precio": 1000, "stock": 5},
    {"nombre": "Mouse", "precio": 25, "stock": 50},
    {"nombre": "Teclado", "precio": 75, "stock": 30}
]

# Obtener nombres de productos caros (>50)
caros = [p["nombre"] for p in productos if p["precio"] > 50]
print(f"  Productos caros: {caros}")

# Caso 2: Transformar datos
print("\n[CASO 2: Convertir temperaturas]")
celsius = [0, 10, 20, 30, 40]
fahrenheit = [(c * 9/5) + 32 for c in celsius]
print(f"  Celsius: {celsius}")
print(f"  Fahrenheit: {fahrenheit}")

# Caso 3: Validar datos
print("\n[CASO 3: Validar emails]")
emails = ["user@example.com", "invalid", "admin@site.org"]
validos = [email for email in emails if "@" in email and "." in email]
print(f"  Emails válidos: {validos}")

# Caso 4: Agrupar datos
print("\n[CASO 4: Agrupar por categoría]")
numeros = list(range(1, 11))
agrupados = {
    "pares": [n for n in numeros if n % 2 == 0],
    "impares": [n for n in numeros if n % 2 != 0]
}
print(f"  Pares: {agrupados['pares']}")
print(f"  Impares: {agrupados['impares']}")


# ============================================================================
# COMPARACIÓN: TRADICIONAL vs MODERNO
# ============================================================================

print("\n" + "=" * 70)
print("COMPARACIÓN: CÓDIGO TRADICIONAL vs MODERNO")
print("=" * 70)

print("\n[Ejemplo: Obtener cuadrados de números pares]")

# Forma tradicional
print("\nFORMA TRADICIONAL:")
resultado_tradicional = []
for i in range(10):
    if i % 2 == 0:
        resultado_tradicional.append(i ** 2)
print(f"  {resultado_tradicional}")

# Forma moderna (list comprehension)
print("\nFORMA MODERNA:")
resultado_moderno = [i**2 for i in range(10) if i % 2 == 0]
print(f"  {resultado_moderno}")


# ============================================================================
# TIPS Y MEJORES PRÁCTICAS
# ============================================================================

print("\n" + "=" * 70)
print("TIPS Y MEJORES PRÁCTICAS")
print("=" * 70)

print("""
BUCLES:
  [OK] Usa 'for' cuando sabes el numero de iteraciones
  [OK] Usa 'while' para condiciones dinamicas
  [OK] Evita modificar la lista mientras iteras sobre ella
  [OK] Usa 'enumerate()' cuando necesites el indice

FUNCIONES:
  [OK] Una funcion debe hacer UNA cosa bien
  [OK] Usa nombres descriptivos
  [OK] Documenta con docstrings
  [OK] Evita efectos secundarios inesperados
  [OK] Retorna valores en lugar de modificar variables globales

MODULOS:
  [OK] Importa solo lo que necesitas
  [OK] Usa alias para nombres largos (import numpy as np)
  [OK] Organiza imports: estandar, terceros, propios
  [OK] Evita 'from module import *'

COMPRENSION DE LISTAS:
  [OK] Usala para operaciones simples
  [OK] No sacrifiques legibilidad por brevedad
  [OK] Para logica compleja, usa bucles tradicionales
  [OK] Considera generadores para grandes volumenes de datos
""")

print("\n" + "=" * 70)
print("FIN DE LA GUÍA DE REFERENCIA")
print("=" * 70)
