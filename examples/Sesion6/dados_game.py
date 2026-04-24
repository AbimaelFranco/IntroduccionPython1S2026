import tkinter as tk
import random

# Configuración de la ventana
root = tk.Tk()
root.title("🎲 Juego de Dados")
root.geometry("400x500")
root.configure(bg="#1e1e2f")

# Variables
resultado = tk.StringVar()
resultado.set("Presiona 'Lanzar'")

# Función para simular lanzamiento con animación
def lanzar_dados():
    animar(10)

def animar(contador):
    if contador > 0:
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        resultado.set(f"🎲 {dado1}   🎲 {dado2}")
        root.after(100, animar, contador - 1)
    else:
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        total = dado1 + dado2
        resultado.set(f"🎲 {dado1}   🎲 {dado2}\n\nTotal: {total}")

# Título
titulo = tk.Label(
    root,
    text="Juego de Dados",
    font=("Helvetica", 24, "bold"),
    bg="#1e1e2f",
    fg="#ffffff"
)
titulo.pack(pady=30)

# Área de resultado
label_resultado = tk.Label(
    root,
    textvariable=resultado,
    font=("Helvetica", 28),
    bg="#2b2b3c",
    fg="#00ffcc",
    width=10,
    height=4,
    relief="ridge",
    bd=3
)
label_resultado.pack(pady=40)

# Botón de lanzar
boton = tk.Button(
    root,
    text="🎲 Lanzar Dados",
    font=("Helvetica", 16, "bold"),
    bg="#00c896",
    fg="white",
    activebackground="#00a67d",
    activeforeground="white",
    padx=20,
    pady=10,
    bd=0,
    command=lanzar_dados
)
boton.pack(pady=20)

# Footer
footer = tk.Label(
    root,
    text="Suerte 🍀",
    font=("Helvetica", 10),
    bg="#1e1e2f",
    fg="#888"
)
footer.pack(side="bottom", pady=10)

root.mainloop()