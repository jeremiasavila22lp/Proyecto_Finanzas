# 📚 Tutorial Completo de Python

## Resumen de Temas

Este tutorial cubre 4 temas fundamentales de Python con más de 40 ejemplos prácticos:

1. **Bucles de 10 días** - Estructuras de repetición
2. **Funciones del 11_día** - Bloques de código reutilizables
3. **Módulos de 12 días** - Organización y reutilización de código
4. **Comprensión de listas de 13 días** - Sintaxis concisa y elegante

---

## 1. 🔄 BUCLES

### Bucle FOR
**Uso:** Cuando sabes cuántas veces quieres repetir algo

```python
# Iterar sobre una lista
frutas = ["manzana", "banana", "naranja"]
for fruta in frutas:
    print(f"Me gusta la {fruta}")

# Usar range() para números
for i in range(1, 6):
    print(f"Número: {i}")

# Con enumerate() para obtener índice
for indice, fruta in enumerate(frutas, start=1):
    print(f"{indice}. {fruta}") 
```

### Bucle WHILE
**Uso:** Cuando no sabes cuántas veces repetir, pero tienes una condición

```python
contador = 1
while contador <= 5:
    print(f"Contador: {contador}")
    contador += 1
```

### BREAK y CONTINUE

```python
# BREAK - Termina el bucle
for num in [1, 3, 5, 7, 9]:
    if num == 7:
        break
    print(num)  # Imprime: 1, 3, 5

# CONTINUE - Salta a la siguiente iteración
for num in range(1, 6):
    if num % 2 == 0:
        continue
    print(num)  # Imprime: 1, 3, 5
```

---

## 2. ⚙️ FUNCIONES

### Funciones Básicas

```python
# Función simple
def saludar(nombre):
    return f"¡Hola, {nombre}!"

# Función con valores por defecto
def crear_perfil(nombre, edad, ciudad="Desconocida"):
    return {"nombre": nombre, "edad": edad, "ciudad": ciudad}

perfil = crear_perfil("Ana", 25)  # ciudad será "Desconocida"
```

### Funciones Avanzadas

```python
# *args - Argumentos variables
def sumar_todos(*numeros):
    return sum(numeros)

sumar_todos(1, 2, 3)      # 6
sumar_todos(10, 20, 30, 40)  # 100

# **kwargs - Argumentos con nombre
def mostrar_info(**datos):
    for clave, valor in datos.items():
        print(f"{clave}: {valor}")

mostrar_info(nombre="Pedro", edad=28, profesion="Ingeniero")
```

### Funciones Lambda

```python
# Lambda simple
cuadrado = lambda x: x ** 2
cuadrado(5)  # 25

# Lambda con múltiples parámetros
multiplicar = lambda x, y: x * y
multiplicar(3, 4)  # 12
```

### Decoradores

```python
def mi_decorador(func):
    def wrapper():
        print("Antes de la función")
        func()
        print("Después de la función")
    return wrapper

@mi_decorador
def decir_hola():
    print("¡Hola!")

decir_hola()
# Salida:
# Antes de la función
# ¡Hola!
# Después de la función
```

### Recursión

```python
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

factorial(5)  # 120 (5 × 4 × 3 × 2 × 1)
```

---

## 3. 📦 MÓDULOS

### Módulos Estándar Más Usados

#### math - Operaciones matemáticas
```python
import math

math.pi           # 3.141592653589793
math.sqrt(16)     # 4.0
math.ceil(3.2)    # 4
math.floor(3.8)   # 3
```

#### random - Números aleatorios
```python
import random

random.randint(1, 10)              # Número entre 1 y 10
random.choice(['A', 'B', 'C'])     # Elemento aleatorio
random.shuffle(lista)              # Mezcla la lista
```

#### datetime - Fechas y horas
```python
from datetime import datetime, timedelta

ahora = datetime.now()
print(ahora.strftime('%Y-%m-%d %H:%M:%S'))

mañana = ahora + timedelta(days=1)
```

#### json - Trabajar con JSON
```python
import json

datos = {"nombre": "Python", "version": 3.9}
json_string = json.dumps(datos, indent=2)
datos_recuperados = json.loads(json_string)
```

#### os - Sistema operativo
```python
import os

os.getcwd()           # Directorio actual
os.listdir('.')       # Lista archivos
os.path.exists(ruta)  # Verifica si existe
```

### Formas de Importar

```python
# Forma 1: Importar módulo completo
import math
math.sqrt(25)

# Forma 2: Importar función específica
from math import sqrt
sqrt(25)

# Forma 3: Importar con alias
import datetime as dt
dt.datetime.now()

# Forma 4: Importar todo (NO RECOMENDADO)
from math import *
```

### Crear Tu Propio Módulo

**Archivo: mi_modulo.py**
```python
def saludar(nombre):
    return f"Hola, {nombre}"

PI = 3.14159

class Calculadora:
    def sumar(self, a, b):
        return a + b
```

**Uso:**
```python
import mi_modulo

print(mi_modulo.saludar("Ana"))
print(mi_modulo.PI)
calc = mi_modulo.Calculadora()
print(calc.sumar(5, 3))
```

---

## 4. 📋 COMPRENSIÓN DE LISTAS

### Sintaxis Básica

```python
# Forma tradicional
cuadrados = []
for i in range(5):
    cuadrados.append(i ** 2)

# List comprehension
cuadrados = [i ** 2 for i in range(5)]
# [0, 1, 4, 9, 16]
```

### Con Condiciones

```python
# Filtrar números pares
pares = [num for num in range(10) if num % 2 == 0]
# [0, 2, 4, 6, 8]

# Con if-else
clasificacion = ["par" if num % 2 == 0 else "impar" for num in range(5)]
# ['par', 'impar', 'par', 'impar', 'par']
```

### Comprensión Anidada

```python
# Crear matriz 3x3
matriz = [[i * j for j in range(3)] for i in range(3)]
# [[0, 0, 0], [0, 1, 2], [0, 2, 4]]

# Aplanar lista de listas
lista_anidada = [[1, 2], [3, 4], [5, 6]]
aplanada = [num for sublista in lista_anidada for num in sublista]
# [1, 2, 3, 4, 5, 6]
```

### Dictionary Comprehension

```python
# Crear diccionario de cuadrados
cuadrados_dict = {num: num ** 2 for num in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### Set Comprehension

```python
# Letras únicas de un texto
letras = {letra for letra in "python" if letra != 'o'}
# {'p', 'y', 't', 'h', 'n'}
```

---

## 🎯 CASOS DE USO PRÁCTICOS

### Caso 1: Procesar Datos de Productos

```python
productos = [
    {"nombre": "Laptop", "precio": 1000, "stock": 5},
    {"nombre": "Mouse", "precio": 25, "stock": 50},
    {"nombre": "Teclado", "precio": 75, "stock": 30}
]

# Productos caros (precio > 50)
caros = [p["nombre"] for p in productos if p["precio"] > 50]
# ['Laptop', 'Teclado']
```

### Caso 2: Convertir Temperaturas

```python
celsius = [0, 10, 20, 30, 40]
fahrenheit = [(c * 9/5) + 32 for c in celsius]
# [32.0, 50.0, 68.0, 86.0, 104.0]
```

### Caso 3: Validar Emails

```python
emails = ["user@example.com", "invalid", "admin@site.org"]
validos = [email for email in emails if "@" in email and "." in email]
# ['user@example.com', 'admin@site.org']
```

### Caso 4: Agrupar Datos

```python
numeros = list(range(1, 11))
agrupados = {
    "pares": [n for n in numeros if n % 2 == 0],
    "impares": [n for n in numeros if n % 2 != 0]
}
# {'pares': [2, 4, 6, 8, 10], 'impares': [1, 3, 5, 7, 9]}
```

---

## 💡 MEJORES PRÁCTICAS

### BUCLES
- ✅ Usa `for` cuando sabes el número de iteraciones
- ✅ Usa `while` para condiciones dinámicas
- ✅ Evita modificar la lista mientras iteras sobre ella
- ✅ Usa `enumerate()` cuando necesites el índice

### FUNCIONES
- ✅ Una función debe hacer UNA cosa bien
- ✅ Usa nombres descriptivos
- ✅ Documenta con docstrings
- ✅ Evita efectos secundarios inesperados
- ✅ Retorna valores en lugar de modificar variables globales

### MÓDULOS
- ✅ Importa solo lo que necesitas
- ✅ Usa alias para nombres largos (`import numpy as np`)
- ✅ Organiza imports: estándar, terceros, propios
- ✅ Evita `from module import *`

### COMPRENSIÓN DE LISTAS
- ✅ Úsala para operaciones simples
- ✅ No sacrifiques legibilidad por brevedad
- ✅ Para lógica compleja, usa bucles tradicionales
- ✅ Considera generadores para grandes volúmenes de datos

---

## 📊 COMPARACIÓN: TRADICIONAL vs MODERNO

### Obtener cuadrados de números pares

**Forma Tradicional:**
```python
resultado = []
for i in range(10):
    if i % 2 == 0:
        resultado.append(i ** 2)
```

**Forma Moderna:**
```python
resultado = [i**2 for i in range(10) if i % 2 == 0]
```

Ambos producen: `[0, 4, 16, 36, 64]`

---

## 📁 Archivos Creados

1. **tutorial_python_completo.py** - Tutorial extenso con 40+ ejemplos ejecutables
2. **guia_referencia_rapida.py** - Guía concisa con ejemplos prácticos
3. **RESUMEN.md** - Este documento de referencia visual

---

## 🚀 Cómo Usar Este Tutorial

1. **Ejecuta los archivos Python:**
   ```bash
   py tutorial_python_completo.py
   py guia_referencia_rapida.py
   ```

2. **Lee este resumen** para entender los conceptos rápidamente

3. **Experimenta** modificando los ejemplos

4. **Practica** creando tus propios ejemplos

---

## 📖 Recursos Adicionales

- **Documentación oficial de Python:** https://docs.python.org/es/3/
- **Tutorial interactivo:** https://www.learnpython.org/es/
- **Ejercicios prácticos:** https://www.hackerrank.com/domains/python

---

**¡Feliz aprendizaje! 🎉**
