import tkinter as tk
from tkinter import ttk, messagebox
import math

coeficientes_estatica = {
    ("Hielo", "Hielo"): 0.1,
    ("Vidrio", "Vidrio"): 0.9,
    ("Madera", "Cuero"): 0.4,
    ("Madera", "Piedra"): 0.7,
    ("Madera", "Madera"): 0.4,
    ("Acero", "Acero"): 0.74,
    ("Acero", "Hielo"): 0.03,
    ("Acero", "Latón"): 0.5,
    ("Acero", "Teflón"): 0.04,
    ("Teflón", "Teflón"): 0.04,
    ("Caucho", "Cemento (seco)"): 1,
    ("Caucho", "Cemento (húmedo)"): 0.3,
    ("Cobre", "Hierro (fundido)"): 1.1,
    ("Esquí (encerado)", "Nieve (0°C)"): 0.1,
    ("Articulaciones humanas", "Articulaciones humanas"): 0.1,
}

coeficientes_cinetica = {
    ("Hielo", "Hielo"): 0.03,
    ("Vidrio", "Vidrio"): 0.4,
    ("Madera", "Cuero"): 0.3,
    ("Madera", "Piedra"): 0.3,
    ("Madera", "Madera"): 0.3,
    ("Acero", "Acero"): 0.57,
    ("Acero", "Hielo"): 0.02,
    ("Acero", "Latón"): 0.4,
    ("Acero", "Teflón"): 0.04,
    ("Teflón", "Teflón"): 0.04,
    ("Caucho", "Cemento (seco)"): 0.81,
    ("Caucho", "Cemento (húmedo)"): 0.25,
    ("Cobre", "Hierro (fundido)"): 0.32,
    ("Esquí (encerado)", "Nieve (0°C)"): 0.05,
    ("Articulaciones humanas", "Articulaciones humanas"): 0.003,
}

materiales = list(set([mat for par in coeficientes_estatica for mat in par]))

def obtener_compatibles(n1):
    compatibles = []
    for (a, b) in coeficientes_estatica:
        if a == n1 and b not in compatibles:
            compatibles.append(b)
        elif b == n1 and a not in compatibles:
            compatibles.append(a)
    return compatibles

root = tk.Tk()
root.title("¿Está en Reposo?")
root.geometry("400x500")

def actualizar_n2(event):
    n1 = n1_combobox.get()
    compatibles = obtener_compatibles(n1)
    n2_combobox['values'] = compatibles
    n2_combobox.set('')

tk.Label(root, text="Peso (kg):").pack()
peso_entry = tk.Entry(root)
peso_entry.pack()

tk.Label(root, text="Ángulo (°):").pack()
angulo_entry = tk.Entry(root)
angulo_entry.pack()

tk.Label(root, text="Superficie N1:").pack()
n1_combobox = ttk.Combobox(root, values=materiales, state="readonly")
n1_combobox.pack()
n1_combobox.bind("<<ComboboxSelected>>", actualizar_n2)

tk.Label(root, text="Superficie N2:").pack()
n2_combobox = ttk.Combobox(root, state="readonly")
n2_combobox.pack()

tk.Label(root, text="Tipo de fricción:").pack()
friccion_tipo = ttk.Combobox(root, values=["Estática", "Cinética"], state="readonly")
friccion_tipo.set("Estática")
friccion_tipo.pack()

def calcular():
    try:
        masa = float(peso_entry.get())
        angulo = float(angulo_entry.get())
        n1 = n1_combobox.get()
        n2 = n2_combobox.get()
        tipo_friccion = friccion_tipo.get()

        if not (n1 and n2):
            messagebox.showerror("Error", "mira que la transparencia no es una opcion.")
            return

        angulo_rad = math.radians(angulo)
        g = 9.8

        px = masa * g * math.sin(angulo_rad)
        py = masa * g * math.cos(angulo_rad)
        froz = px
        normal = py

        if tipo_friccion == "Estática":
            mu = coeficientes_estatica.get((n1, n2)) or coeficientes_estatica.get((n2, n1))
        else:
            mu = coeficientes_cinetica.get((n1, n2)) or coeficientes_cinetica.get((n2, n1))

        if mu is None:
            messagebox.showerror("Error", "No existe coeficiente para esa combinación.")
            return

        resultado = froz <= mu * normal

        if resultado:
            messagebox.showinfo("RESULTADO", "muy bien caballero, esta en reposo.")
        else:
            messagebox.showinfo("RESULTADO", "NO ESTA EN REPOSOOOOOOO.")

    except ValueError:
        messagebox.showerror("XXXXXXXXX", "SOLO PUEDEN SER NUMEROS >:(")

tk.Button(root, text="Confirmar", command=calcular).pack(pady=20)

root.mainloop()
