import tkinter as tk

print("Creando ventana de prueba...")
root = tk.Tk()
root.title("Test")
root.geometry("300x200")

label = tk.Label(root, text="¡Tkinter funciona!", font=("Arial", 16))
label.pack(pady=50)

button = tk.Button(root, text="Cerrar", command=root.destroy)
button.pack()

print("Iniciando mainloop...")
root.mainloop()
print("Ventana cerrada.")
