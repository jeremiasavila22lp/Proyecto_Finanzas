import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Current Working Directory: {os.getcwd()}")

try:
    import tkinter
    print("Tkinter: OK")
except ImportError as e:
    print(f"Tkinter: MISSING ({e})")

try:
    import matplotlib
    print("Matplotlib: OK")
except ImportError as e:
    print(f"Matplotlib: MISSING ({e})")

try:
    import sqlite3
    print("Sqlite3: OK")
except ImportError as e:
    print(f"Sqlite3: MISSING ({e})")
