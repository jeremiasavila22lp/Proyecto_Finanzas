def extracted_function(nums):
    nums -= 1   

"""
EJERCICIOS PRÁCTICOS DE PYTHON
================================
Practica los conceptos aprendidos con estos ejercicios
"""


print("=" * 70)
print("EJERCICIOS PRÁCTICOS - PYTHON")
print("=" * 70)

# ============================================================================
# EJERCICIOS DE BUCLES
# ============================================================================

print("\n" + "=" * 70)
print("EJERCICIOS DE BUCLES")
print("=" * 70)

print("\n--- Ejercicio 1: Tabla de multiplicar ---")
print("Crea la tabla de multiplicar del 7 (del 1 al 10)")
print("\nSolución:")
numero = 7
for i in range(1, 11):
    print(f"  {numero} x {i} = {numero * i}")

print("\n--- Ejercicio 2: Suma acumulativa ---")
print("Suma los números del 1 al 100")
print("\nSolución:")
suma = 0
for i in range(1, 101):
    suma += i
print(f"  La suma de 1 a 100 es: {suma}")

print("\n--- Ejercicio 3: Contar vocales ---")
print("Cuenta las vocales en una frase")
texto = "Python es un lenguaje de programacion"
print(f"Texto: '{texto}'")
print("\nSolución:")
vocales = "aeiouAEIOU"
contador = 0
for letra in texto:
    if letra in vocales:
        contador += 1
print(f"  Número de vocales: {contador}")

print("\n--- Ejercicio 4: Números primos ---")
print("Encuentra números primos del 1 al 20")
print("\nSolución:")
primos = []
for num in range(2, 21):
    es_primo = True
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            es_primo = False
            break
    if es_primo:
        primos.append(num)
print(f"  Números primos: {primos}")

print("\n--- Ejercicio 5: Patrón de asteriscos ---")
print("Crea un triángulo de asteriscos")
print("\nSolución:")
filas = 5
for i in range(1, filas + 1):
    print("  " + "*" * i)


# ============================================================================
# EJERCICIOS DE FUNCIONES
# ============================================================================

print("\n\n" + "=" * 70)
print("EJERCICIOS DE FUNCIONES")
print("=" * 70)

print("\n--- Ejercicio 6: Calculadora básica ---")
print("Crea funciones para operaciones matemáticas")
print("\nSolución:")

def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b

def multiplicar(a, b):
    return a * b

def dividir(a, b):
    if b == 0:
        return "Error: División por cero"
    return a / b

print(f"  10 + 5 = {sumar(10, 5)}")
print(f"  10 - 5 = {restar(10, 5)}")
print(f"  10 * 5 = {multiplicar(10, 5)}")
print(f"  10 / 5 = {dividir(10, 5)}")

print("\n--- Ejercicio 7: Palíndromo ---")
print("Verifica si una palabra es palíndromo")
print("\nSolución:")

def es_palindromo(palabra):
    palabra = palabra.lower().replace(" ", "")
    return palabra == palabra[::-1]

palabras = ["radar", "python", "anilina", "reconocer"]
for palabra in palabras:
    resultado = "SÍ" if es_palindromo(palabra) else "NO"
    print(f"  '{palabra}' es palíndromo: {resultado}")

print("\n--- Ejercicio 8: Fibonacci ---")
print("Genera la secuencia de Fibonacci")
print("\nSolución:")

def fibonacci(n):
    secuencia = []
    a, b = 0, 1
    for _ in range(n):
        secuencia.append(a)
        a, b = b, a + b
    return secuencia

print(f"  Primeros 10 números: {fibonacci(10)}")

print("\n--- Ejercicio 9: Contar palabras ---")
print("Cuenta palabras en un texto")
print("\nSolución:")

def contar_palabras(texto):
    palabras = texto.split()
    return {
        "total_palabras": len(palabras),
        "total_caracteres": len(texto),
        "palabra_mas_larga": max(palabras, key=len) if palabras else ""
    }

texto = "Python es un lenguaje de programacion muy versatil"
resultado = contar_palabras(texto)
print(f"  Texto: '{texto}'")
print(f"  Total palabras: {resultado['total_palabras']}")
print(f"  Total caracteres: {resultado['total_caracteres']}")
print(f"  Palabra más larga: {resultado['palabra_mas_larga']}")

print("\n--- Ejercicio 10: Validador de contraseña ---")
print("Valida si una contraseña es segura")
print("\nSolución:")

def validar_password(password):
    tiene_mayuscula = any(c.isupper() for c in password)
    tiene_minuscula = any(c.islower() for c in password)
    tiene_numero = any(c.isdigit() for c in password)
    longitud_ok = len(password) >= 8
    
    es_valida = all([tiene_mayuscula, tiene_minuscula, tiene_numero, longitud_ok])
    
    return {
        "valida": es_valida,
        "mayuscula": tiene_mayuscula,
        "minuscula": tiene_minuscula,
        "numero": tiene_numero,
        "longitud": longitud_ok
    }

passwords = ["abc123", "Password123", "PYTHON", "Secure1Pass"]
for pwd in passwords:
    resultado = validar_password(pwd)
    estado = "VÁLIDA" if resultado["valida"] else "INVÁLIDA"
    print(f"  '{pwd}': {estado}")


# ============================================================================
# EJERCICIOS DE MÓDULOS
# ============================================================================

print("\n\n" + "=" * 70)
print("EJERCICIOS DE MÓDULOS")
print("=" * 70)

print("\n--- Ejercicio 11: Cálculos matemáticos ---")
print("Usa el módulo math para cálculos")
print("\nSolución:")

import math

numeros = [4, 9, 16, 25, 36]
print(f"  Números: {numeros}")
print(f"  Raíces cuadradas: {[math.sqrt(n) for n in numeros]}")
print(f"  Área de círculo (r=5): {math.pi * (5 ** 2):.2f}")

print("\n--- Ejercicio 12: Generador de contraseñas ---")
print("Genera contraseñas aleatorias")
print("\nSolución:")

import random
import string

def generar_password(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(longitud))

print("  Contraseñas generadas:")
for i in range(3):
    print(f"    {i+1}. {generar_password()}")

print("\n--- Ejercicio 13: Trabajar con fechas ---")
print("Calcula días entre fechas")
print("\nSolución:")

from datetime import datetime, timedelta

hoy = datetime.now()
cumpleanos = datetime(2025, 12, 25)
diferencia = cumpleanos - hoy

print(f"  Hoy: {hoy.strftime('%d/%m/%Y')}")
print(f"  Navidad: {cumpleanos.strftime('%d/%m/%Y')}")
print(f"  Días hasta Navidad: {diferencia.days}")

print("\n--- Ejercicio 14: Procesar JSON ---")
print("Convierte datos a JSON y viceversa")
print("\nSolución:")

import json

estudiantes = [
    {"nombre": "Ana", "edad": 20, "notas": [85, 90, 88]},
    {"nombre": "Juan", "edad": 22, "notas": [78, 82, 80]},
]

# Convertir a JSON
json_string = json.dumps(estudiantes, indent=2)
print("  Datos en JSON:")
print(json_string)

# Calcular promedio
for estudiante in estudiantes:
    promedio = sum(estudiante["notas"]) / len(estudiante["notas"])
    print(f"  {estudiante['nombre']}: promedio = {promedio:.1f}")


# ============================================================================
# EJERCICIOS DE COMPRENSIÓN DE LISTAS
# ============================================================================

print("\n\n" + "=" * 70)
print("EJERCICIOS DE COMPRENSIÓN DE LISTAS")
print("=" * 70)

print("\n--- Ejercicio 15: Filtrar y transformar ---")
print("Obtén los cuadrados de números impares del 1 al 20")
print("\nSolución:")
cuadrados_impares = [
    val for n in range(1,21)
    if n % 2 != 0
    for val in [n**2]
]
print(f"  {cuadrados_impares}")

print("\n--- Ejercicio 16: Procesar nombres ---")
print("Convierte nombres a formato 'Apellido, Nombre'")
print("\nSolución:")
nombres_completos = ["Juan Perez", "Maria Garcia", "Pedro Lopez"]
formato_apellido = [" ".join(nombre.split()[::-1]) for nombre in nombres_completos]
print(f"  Original: {nombres_completos}")
print(f"  Invertido: {formato_apellido}")

print("\n--- Ejercicio 17: Matriz transpuesta ---")
print("Transpone una matriz 3x3")
print("\nSolución:")
matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
transpuesta = [[matriz[j][i] for j in range(len(matriz))] for i in range(len(matriz[0]))]
print("  Matriz original:")
for fila in matriz:
    print(f"    {fila}")
print("  Matriz transpuesta:")
for fila in transpuesta:
    print(f"    {fila}")

print("\n--- Ejercicio 18: Extraer datos ---")
print("Extrae información específica de diccionarios")
print("\nSolución:")
productos = [
    {"nombre": "Laptop", "precio": 1000, "categoria": "Electrónica"},
    {"nombre": "Mesa", "precio": 200, "categoria": "Muebles"},
    {"nombre": "Mouse", "precio": 25, "categoria": "Electrónica"},
    {"nombre": "Silla", "precio": 150, "categoria": "Muebles"}
]

# Nombres de productos electrónicos
electronicos = [p["nombre"] for p in productos if p["categoria"] == "Electrónica"]
print(f"  Productos electrónicos: {electronicos}")

# Precios mayores a 100
caros = {p["nombre"]: p["precio"] for p in productos if p["precio"] > 100}
print(f"  Productos caros: {caros}")

print("\n--- Ejercicio 19: Combinaciones ---")
print("Genera combinaciones de colores y tamaños")
print("\nSolución:")
colores = ["Rojo", "Azul", "Verde"]
tamaños = ["S", "M", "L"]
combinaciones = [f"{color}-{tamaño}" for color in colores for tamaño in tamaños]
print(f"  Combinaciones: {combinaciones}")

print("\n--- Ejercicio 20: Filtro complejo ---")
print("Filtra palabras largas y conviértelas a mayúsculas")
print("\nSolución:")
frase = "Python es un lenguaje de programacion muy versatil y poderoso"
palabras_largas = [palabra.upper() for palabra in frase.split() if len(palabra) > 5]
print(f"  Frase: '{frase}'")
print(f"  Palabras largas (>5 letras): {palabras_largas}")


# ============================================================================
# EJERCICIOS COMBINADOS (DESAFÍO)
# ============================================================================

print("\n\n" + "=" * 70)
print("EJERCICIOS COMBINADOS (DESAFÍO)")
print("=" * 70)

print("\n--- Ejercicio 21: Análisis de texto ---")
print("Analiza un texto completo")
print("\nSolución:")

def analizar_texto(texto):
    palabras = texto.lower().split()
    
    # Frecuencia de palabras
    frecuencia = {}
    for palabra in palabras:
        palabra_limpia = ''.join(c for c in palabra if c.isalnum())
        if palabra_limpia:
            frecuencia[palabra_limpia] = frecuencia.get(palabra_limpia, 0) + 1
    
    # Palabra más común
    palabra_comun = max(frecuencia.items(), key=lambda x: x[1]) if frecuencia else ("", 0)
    
    return {
        "total_palabras": len(palabras),
        "palabras_unicas": len(frecuencia),
        "palabra_mas_comun": palabra_comun[0],
        "frecuencia_max": palabra_comun[1]
    }

texto_ejemplo = "Python es genial. Python es versatil. Python es poderoso."
analisis = analizar_texto(texto_ejemplo)
print(f"  Texto: '{texto_ejemplo}'")
print(f"  Total palabras: {analisis['total_palabras']}")
print(f"  Palabras únicas: {analisis['palabras_unicas']}")
print(f"  Palabra más común: '{analisis['palabra_mas_comun']}' ({analisis['frecuencia_max']} veces)")

print("\n--- Ejercicio 22: Sistema de calificaciones ---")
print("Procesa calificaciones de estudiantes")
print("\nSolución:")

estudiantes_notas = [
    {"nombre": "Ana", "notas": [85, 90, 88, 92]},
    {"nombre": "Juan", "notas": [78, 82, 80, 85]},
    {"nombre": "María", "notas": [95, 98, 92, 96]},
    {"nombre": "Pedro", "notas": [70, 75, 72, 78]}
]

def calcular_estadisticas(estudiantes):
    for estudiante in estudiantes:
        notas = estudiante["notas"]
        promedio = sum(notas) / len(notas)
        nota_max = max(notas)
        nota_min = min(notas)
        
        if promedio >= 90:
            calificacion = "A"
        elif promedio >= 80:
            calificacion = "B"
        elif promedio >= 70:
            calificacion = "C"
        else:
            calificacion = "D"
        
        print(f"  {estudiante['nombre']}:")
        print(f"    Promedio: {promedio:.1f}")
        print(f"    Nota máxima: {nota_max}")
        print(f"    Nota mínima: {nota_min}")
        print(f"    Calificación: {calificacion}")

calcular_estadisticas(estudiantes_notas)

print("\n--- Ejercicio 23: Gestor de inventario ---")
print("Administra inventario de productos")
print("\nSolución:")

inventario = [
    {"id": 1, "nombre": "Laptop", "precio": 1000, "stock": 5},
    {"id": 2, "nombre": "Mouse", "precio": 25, "stock": 50},
    {"id": 3, "nombre": "Teclado", "precio": 75, "stock": 30},
    {"id": 4, "nombre": "Monitor", "precio": 300, "stock": 0}
]

# Productos sin stock
sin_stock = [p["nombre"] for p in inventario if p["stock"] == 0]
print(f"  Productos sin stock: {sin_stock}")

# Valor total del inventario
valor_total = sum(p["precio"] * p["stock"] for p in inventario)
print(f"  Valor total del inventario: ${valor_total}")

# Productos ordenados por precio
ordenados = sorted(inventario, key=lambda x: x["precio"], reverse=True)
print("  Productos ordenados por precio (mayor a menor):")
for p in ordenados:
    print(f"    {p['nombre']}: ${p['precio']}")


print("\n\n" + "=" * 70)
print("¡FELICITACIONES! Has completado todos los ejercicios")
print("=" * 70)
print("\nSigue practicando y experimentando con Python.")
print("La práctica constante es la clave del éxito en programación.")
print("=" * 70)


"""
Funciones de orden superior
"""

def resta_numero(num):
    return num - 1

def orden_funcion(funcion, lista):
    # Aplicamos la función (resta_numero) a cada elemento de la lista uno por uno
    restas = [funcion(x) for x in lista]
    return restas

resultado = orden_funcion(resta_numero, [1, 3, 5, 7, 9])
print(resultado)

def multi_numero(num):
    return num * 2

def orden_funcion_multiplicar(funcion, lista):
    multipli = [funcion(x) for x in lista]
    return multipli

resultados = orden_funcion_multiplicar(multi_numero, [1, 3, 5, 7, 9])
print(resultados)   

def cuadrado(x):
    return x ** 2
def cubo(x):
    return x ** 3
def absoluto(x):
    if x >= 0:
        return x
    else:
        return -(x)

def higher_order_function(type): # Mas simple y facil de leer
   operaciones = {
        "cuadrado": cuadrado,
        "cubo": cubo,
        "absoluto": absoluto
   }
   return operaciones[type]

result = higher_order_function("cuadrado")
print(result(5))
result = higher_order_function("cubo")
print(result(6))
result = higher_order_function("absoluto")
print(result(-7))    

def add_ten():
    ten = 10
    def add(num):
        return num + ten
    return add

closure_result = add_ten()
print("4+10:",closure_result(4))
print("20+10:",closure_result(20))

# decoradores python

def greeting():
    return "Hello, World!"
def uppercase_decorator(function):
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase
    return wrapper
g = uppercase_decorator(greeting)
print("print g:", g())

''' Decoradores '''
def uppercase_decorator(function):
    def wrapper(*args, **kwargs): # <--- Ahora acepta cualquier parámetro
        func_result = function(*args, **kwargs)
        if isinstance(func_result, str): # Si es texto, lo hacemos mayúsculas
            return func_result.upper()
        return func_result
    return wrapper

@uppercase_decorator
def greeting():
    return "Hello, World!"
print("print greeting:", greeting())
def uppercase_decorator(function):
    def wrapper(*args, **kwargs): # <--- Ahora acepta cualquier parámetro
        func_result = function(*args, **kwargs)
        if isinstance(func_result, str): # Si es texto, lo hacemos mayúsculas
            return func_result.upper()
        return func_result
    return wrapper

def split_string_decorator (function):
    def wrapper():
        func = function()
        split_string = func.split()
        return split_string
    return wrapper

@split_string_decorator
@uppercase_decorator
def greeting():
    return "Hello, World!"
print("print greeting:", greeting())

# aceptacion de parametros en funciones decoradoras

def decorador_de_parametros(funciones):
    def aceptacion_de_parametros(param1, param2, param3):
        funciones(param1, param2, param3)
        print("Yo soy {}".format(param3))
    return aceptacion_de_parametros

print("nombre:",("Juan", "Perez", 25))

# ============================================================================
# EXPLICACIÓN: FUNCIONES LAMBDA Y MAP
# ============================================================================

"""
¿Para qué sirve lambda en map()?

La función map(función, iterable) aplica una función a cada elemento de una lista (u otro iterable).
Lambda es una forma de crear esa "función" de manera rápida y sin nombre.

Estructura: lambda argumentos : expresión
"""

numbers = [1, 2, 3, 4, 5, 6, 7, 8 ,9, 10, 11, 12, 13, 14, 15]

# Opción A: Usando una función definida con 'def'
def cuadrado(x):
    return x ** 2

cuadrados_con_def = list(map(cuadrado, numbers))
print(f"Cuadrados (con def): {cuadrados_con_def}")

# Opción B: Usando 'lambda' (Más directo y limpio para una sola línea)
cuadrados_con_lambda = list(map(lambda x: x ** 2, numbers))
print(f"Cuadrados (con lambda): {cuadrados_con_lambda}")

# Otro ejemplo: Convertir nombres a mayúsculas
nombres = ["ana", "juan", "pedro"]
nombres_mayus = list(map(lambda nombre: nombre.capitalize(), nombres))
print(f"Nombres capitalizados: {nombres_mayus}")

cuadrados_par = list(map(lambda x: x * 2, numbers))
print(f"Cuadrados de los números: {cuadrados_par}")

numbers_str = ["1", "2", "3", "4", "5"]
numbers_int = list(map(lambda x: float(x.replace(",", ".")), numbers_str))
print(f"Números convertidos a flotantes: {numbers_int}")

numbers_str = ["1,01", "2,02", "3,03", "4,04", "5,05"]
numbers_int = list(map(lambda x: int(float(x.replace(",", "."))), numbers_str))
print(f"Números convertidos a enteros: {numbers_int}")

nombres = ["ana", "juan", "pedro"]
def mayusculas(nombres):
    return nombres.upper()

nombres_mayus = list(map(mayusculas, nombres))
print(f"Nombres mayúsculas: {nombres_mayus}")

nombres_mayus = list(map(lambda nombre: nombre.upper(), nombres))
print(f"Nombres mayúsculas (con lambda): {nombres_mayus}")

def is_even(numeros): 
    if numeros % 2 == 0:
        return True
    else:
        return False
even_numbers = list(filter(is_even, numeros))
print(f"Números pares: {even_numbers}")

def is_odd(numeros): 
    if numeros % 2 != 0:
        return True
    else:
        return False
odd_numbers = list(filter(is_odd, numeros))
print(f"Números impares: {odd_numbers}")

nombress = ["ana", "juan", "pedro","francisco", "roberto"]
def nombres_cortos(nombress):
    if len(nombress) <= 5:
        return True
    else:
        return False
nombres_cortos = list(filter(nombres_cortos, nombress))
print(f"Nombres cortos: {nombres_cortos}")

numbers_str = ["1", "2", "3", "4", "5"] # reduce
def sumar(x, y):
    return int(x) + int(y)
from functools import reduce
total = reduce(sumar, numbers_str)
print(f"Total: {total}")

# explicacion de en mapa, filtro y reduccion

# map: aplica una funcion a cada elemento de una lista
# filter: filtra los elementos de una lista que cumplen una condicion
# reduce: reduce los elementos de una lista a un solo valor

# diferencia entre funcion de orden superior, cierre y decoradores

# funcion de orden superior: una funcion que recibe como parametro otra funcion o retorna una funcion
# cierre: una funcion que retorna otra funcion y que tiene acceso a las variables de la funcion que la retorna
# decorador: una funcion que recibe como parametro otra funcion y retorna otra funcion que tiene acceso a las variables de la funcion que la retorna

numerosss = [1, 2, 3, 4, 5, 6, 7, 8 ,9, 10, 11, 12, 13, 14, 15]
def square(x):
    return x ** 2 

numbers_squared = list(map(square, numerosss))
print(f"Números al cuadrado: {numbers_squared}")

def par(num):
    if num % 2 == 0:
        return True
    else:
        return False

even_numbers = list(filter(par, numerosss))
print(f"Números pares: {even_numbers}")

numeros_str = ["1", "2", "3", "4", "5"] # reduce
def sumar(x, y):
    return int(x) + int(y)
from functools import reduce
total = reduce(sumar, numeros_str)
print(f"Total: {total}")

countries = ['Estonia', 'Finland', 'Sweden', 'Denmark', 'Norway', 'Iceland']

def llamada_paises(lista):
    def llamada():
        for pais in lista:
            print(pais)
    return llamada

mostrar_paises = llamada_paises(countries)
mostrar_paises()

names = ['Asabeneh', 'Lidiya', 'Ermias', 'Abraham']
def llamada_nombres(nombres):
    nombres = names
    for nombre in nombres:
        print(nombre)

llamada_nombres(names)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def llamada_numeros(numeros):
    numeros = numbers
    for numero in numeros:
        print(numero)

llamada_numeros(numbers)


@uppercase_decorator
def obtener_paises_texto(lista_paises):
    # Retornamos los países como un solo string para que el decorador pueda trabajar
    return ", ".join(lista_paises)
# 3. Probamos
print(obtener_paises_texto(countries))


