# =========================
# INSTALACIÓN DE LIBRERÍAS
# =========================

# pip install numpy matplotlib

# =========================
# IMPORTACIÓN DE LIBRERÍAS
# =========================

# Tkinter sirve para crear la interfaz gráfica (ventanas, botones, etc.)
import tkinter as tk

# NumPy sirve para hacer cálculos matemáticos de forma rápida
import numpy as np

# Matplotlib sirve para crear gráficas
import matplotlib.pyplot as plt


# =========================
# COLORES (ESTÉTICA)
# =========================

# Definimos colores en variables para reutilizarlos fácilmente
BG_MAIN = "#2c3e50"        # color de fondo principal
BG_PANEL = "#34495e"       # color del panel interno
ACCENT = "#1abc9c"         # color de botones
ACCENT_ACTIVE = "#16a085" # color cuando se presiona el botón
TEXT = "white"             # color del texto


# =========================
# FUNCIÓN GENERAL PARA GRAFICAR EN 3D
# =========================

def graficar_3d(func, titulo):
    """
    Esta función recibe:
    - func: una función matemática (por ejemplo x² + y²)
    - titulo: texto que se mostrará en la gráfica
    
    Su objetivo es generar y mostrar una gráfica 3D.
    """

    # Generamos 100 valores entre -5 y 5 para el eje X
    x = np.linspace(-5, 5, 100)

    # Generamos 100 valores entre -5 y 5 para el eje Y
    y = np.linspace(-5, 5, 100)

    # Convertimos X y Y en una rejilla (tabla de valores)
    # Esto permite evaluar funciones con dos variables
    X, Y = np.meshgrid(x, y)

    # Aplicamos la función matemática a todos los puntos
    # Resultado: matriz de valores Z
    Z = func(X, Y)

    # Creamos una figura (ventana de la gráfica)
    fig = plt.figure()

    # Creamos un sistema de ejes en 3D
    ax = fig.add_subplot(111, projection='3d')

    # Dibujamos la superficie 3D
    # cmap='viridis' aplica colores según el valor de Z
    surf = ax.plot_surface(X, Y, Z, cmap='viridis')

    # Agregamos una barra de color para interpretar los valores
    fig.colorbar(surf)

    # Agregamos un título a la gráfica
    ax.set_title(titulo)

    # Mostramos la gráfica en pantalla
    plt.show()


# =========================
# FUNCIÓN PARA MOSTRAR 4 HEATMAPS
# =========================

def graficar_heatmaps():
    """
    Esta función muestra 4 mapas de calor (heatmaps),
    uno por cada función matemática.
    """

    # Generamos valores para X y Y
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)

    # Creamos la rejilla
    X, Y = np.meshgrid(x, y)

    # Lista de funciones con sus nombres
    funciones = [
        (lambda x, y: x**2 + y**2, "Paraboloide"),
        (lambda x, y: np.sin(x)*np.cos(y), "Seno-Coseno"),
        (lambda x, y: x + y, "Plano"),
        (lambda x, y: np.sin(np.sqrt(x**2 + y**2)), "Onda radial"),
    ]

    # Creamos una figura con 4 subgráficas (2 filas, 2 columnas)
    fig, axs = plt.subplots(2, 2)

    # Recorremos cada espacio de la cuadrícula junto con cada función
    for ax, (func, titulo) in zip(axs.flat, funciones):

        # Calculamos los valores de Z
        Z = func(X, Y)

        # Creamos el mapa de calor
        im = ax.imshow(
            Z,
            cmap='viridis',        # colores
            extent=[-5,5,-5,5],    # escala de los ejes
            origin='lower'         # origen en la esquina inferior
        )

        # Título de cada subgráfica
        ax.set_title(titulo)

        # Barra de color individual
        fig.colorbar(im, ax=ax)

    # Título general de toda la ventana
    plt.suptitle("Mapas de calor de funciones")

    # Mostramos las gráficas
    plt.show()


# =========================
# FUNCIONES QUE SE ACTIVAN CON BOTONES
# =========================

# Cada una de estas funciones llama a la función general
# y le pasa una función matemática diferente

def paraboloide():
    graficar_3d(lambda x, y: x**2 + y**2, "Paraboloide")

def seno_coseno():
    graficar_3d(lambda x, y: np.sin(x) * np.cos(y), "Onda seno-coseno")

def plano():
    graficar_3d(lambda x, y: x + y, "Plano")

def onda_radial():
    graficar_3d(lambda x, y: np.sin(np.sqrt(x**2 + y**2)), "Onda radial")


# =========================
# CREACIÓN DE LA INTERFAZ GRÁFICA
# =========================

# Creamos la ventana principal
root = tk.Tk()

# Título de la ventana
root.title("Graficadora 3D")

# Tamaño de la ventana
root.geometry("420x360")

# Color de fondo
root.configure(bg=BG_MAIN)


# =========================
# CONTENEDOR PRINCIPAL
# =========================

# Creamos un frame (contenedor) dentro de la ventana
frame = tk.Frame(root, bg=BG_PANEL, padx=20, pady=20)

# Lo colocamos en la ventana
frame.pack(expand=True)


# =========================
# TÍTULO DE LA INTERFAZ
# =========================

titulo = tk.Label(
    frame,
    text="Graficadora 3D",
    font=("Segoe UI", 16, "bold"),
    bg=BG_PANEL,
    fg=TEXT
)

titulo.pack(pady=(0, 15))


# =========================
# FUNCIÓN PARA CREAR BOTONES
# =========================

def crear_boton(texto, comando):
    """
    Esta función crea botones reutilizables.
    
    - texto: lo que dice el botón
    - comando: la función que se ejecuta al hacer clic
    """

    return tk.Button(
        frame,
        text=texto,
        command=comando,           # función que se ejecuta
        font=("Segoe UI", 10, "bold"),
        bg=ACCENT,
        fg="white",
        activebackground=ACCENT_ACTIVE,
        relief="flat",
        padx=10,
        pady=8,
        width=25
    )


# =========================
# CREACIÓN DE BOTONES
# =========================

# Cada botón llama a una función distinta

crear_boton("Paraboloide (x² + y²)", paraboloide).pack(pady=5)
crear_boton("Onda seno-coseno", seno_coseno).pack(pady=5)
crear_boton("Plano (x + y)", plano).pack(pady=5)
crear_boton("Onda radial", onda_radial).pack(pady=5)

# Botón adicional para ver los 4 mapas de calor
crear_boton("Ver mapas de calor (4)", graficar_heatmaps).pack(pady=10)


# =========================
# EJECUCIÓN DEL PROGRAMA
# =========================

# Mantiene la ventana abierta y escuchando eventos
root.mainloop()