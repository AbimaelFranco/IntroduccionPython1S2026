# Importamos la librería tkinter y le damos el alias "tk"
import tkinter as tk

# Importamos una herramienta para mostrar mensajes emergentes
from tkinter import messagebox


# =========================
# VENTANA PRINCIPAL
# =========================

# Creamos la ventana principal de la aplicación
root = tk.Tk()

# Le ponemos un título a la ventana
root.title("Demo GUI - Curso Python")

# Definimos el tamaño de la ventana (ancho x alto)
root.geometry("400x300")

# Cambiamos el color de fondo
root.configure(bg="#2c3e50")  # color oscuro


# =========================
# ESTILOS (FUENTES)
# =========================

# Definimos estilos de texto para reutilizarlos
FONT_TITLE = ("Segoe UI", 16, "bold")   # título grande
FONT_LABEL = ("Segoe UI", 10)           # texto normal
FONT_BUTTON = ("Segoe UI", 10, "bold")  # texto del botón


# =========================
# FUNCIÓN PRINCIPAL
# =========================

def saludar():
    """
    Esta función se ejecuta cuando el usuario presiona el botón.
    """

    # Obtenemos el texto que el usuario escribió en el input
    nombre = entry_nombre.get()

    # Verificamos si el texto está vacío
    # strip() elimina espacios en blanco
    if nombre.strip() == "":
        
        # Mostramos una advertencia si no escribió nada
        messagebox.showwarning("Aviso", "Por favor ingresa tu nombre")

    else:
        # Si sí escribió algo, mostramos el saludo
        label_resultado.config(
            text=f"Hola, {nombre} 👋",  # texto dinámico
            fg="#2ecc71"              # color verde
        )


# =========================
# CONTENEDOR (FRAME)
# =========================

# Creamos un contenedor dentro de la ventana
frame = tk.Frame(
    root,
    bg="#34495e",  # color del fondo
    padx=20,       # espacio interno horizontal
    pady=20        # espacio interno vertical
)

# Lo colocamos en la ventana
frame.pack(expand=True)


# =========================
# TÍTULO
# =========================

titulo = tk.Label(
    frame,
    text="Bienvenido",
    font=FONT_TITLE,
    bg="#34495e",
    fg="white"
)

# Lo colocamos con espacio abajo
titulo.pack(pady=(0, 15))


# =========================
# TEXTO DESCRIPTIVO
# =========================

label_nombre = tk.Label(
    frame,
    text="Ingresa tu nombre:",
    font=FONT_LABEL,
    bg="#34495e",
    fg="white"
)

# anchor="w" alinea a la izquierda
label_nombre.pack(anchor="w")


# =========================
# INPUT (CAJA DE TEXTO)
# =========================

entry_nombre = tk.Entry(
    frame,
    font=FONT_LABEL,
    width=30
)

entry_nombre.pack(pady=5)


# =========================
# BOTÓN
# =========================

boton = tk.Button(
    frame,
    text="Saludar",
    font=FONT_BUTTON,
    bg="#1abc9c",              # color normal
    fg="white",
    activebackground="#16a085",  # color al hacer clic
    activeforeground="white",
    command=saludar,           # función que se ejecuta
    relief="flat",             # estilo sin bordes
    padx=10,
    pady=5
)

boton.pack(pady=10)


# =========================
# RESULTADO
# =========================

label_resultado = tk.Label(
    frame,
    text="",  # empieza vacío
    font=FONT_LABEL,
    bg="#34495e",
    fg="white"
)

label_resultado.pack(pady=10)


# =========================
# EJECUCIÓN
# =========================

# Inicia el programa y mantiene la ventana abierta
root.mainloop()