import tkinter as tk
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =========================
# CONFIG
# =========================
fs = 44100
block_size = 1024
running = False


# =========================
# EFECTO DE VOZ MEJORADO
# =========================
def efecto_anonymous(audio):
    # Distorsión suave
    audio = np.tanh(audio * 2)

    # Modulación ligera (más limpia)
    t = np.arange(len(audio)) / fs
    modulador = 0.8 + 0.2 * np.sin(2 * np.pi * 15 * t)

    return audio * modulador


# =========================
# CALLBACK AUDIO
# =========================
def callback(indata, outdata, frames, time, status):
    global ultima_muestra

    if status:
        print(status)

    audio = indata[:, 0]
    ultima_muestra = audio.copy()

    audio_mod = efecto_anonymous(audio)
    audio_mod = np.clip(audio_mod, -1, 1)

    outdata[:, 0] = audio_mod


# =========================
# CONTROL
# =========================
def iniciar():
    global stream, running
    if not running:
        stream = sd.Stream(
            samplerate=fs,
            blocksize=block_size,
            channels=1,
            callback=callback
        )
        stream.start()
        running = True


def detener():
    global running
    if running:
        stream.stop()
        stream.close()
        running = False


# =========================
# VISUALIZADOR DJ
# =========================
def actualizar_espectro():
    if running and ultima_muestra is not None:

        fft = np.abs(np.fft.rfft(ultima_muestra))
        fft = fft[:100]  # menos barras (más limpio)

        ax.clear()

        # Crear colores tipo gradiente DJ
        colors = plt.cm.plasma(np.linspace(0, 1, len(fft)))

        ax.bar(range(len(fft)), fft, color=colors)

        # Estilo oscuro
        ax.set_facecolor("#121212")
        fig.patch.set_facecolor("#121212")

        ax.set_xticks([])
        ax.set_yticks([])

        ax.set_title("Visualizador de Audio", color="white")

        # Quitar bordes
        for spine in ax.spines.values():
            spine.set_visible(False)

        canvas.draw()

    root.after(50, actualizar_espectro)


# =========================
# INTERFAZ
# =========================
root = tk.Tk()
root.title("Voice Changer DJ")
root.geometry("700x500")
root.configure(bg="#1e1e1e")

frame = tk.Frame(root, bg="#2c2c2c", padx=20, pady=20)
frame.pack(fill="both", expand=True)

titulo = tk.Label(
    frame,
    text="Voice Changer DJ",
    font=("Segoe UI", 16, "bold"),
    bg="#2c2c2c",
    fg="white"
)
titulo.pack(pady=10)


# =========================
# BOTONES
# =========================
btn_iniciar = tk.Button(
    frame,
    text="▶ Iniciar",
    command=iniciar,
    bg="#1abc9c",
    fg="white",
    width=20
)
btn_iniciar.pack(pady=5)

btn_detener = tk.Button(
    frame,
    text="⏹ Detener",
    command=detener,
    bg="#e74c3c",
    fg="white",
    width=20
)
btn_detener.pack(pady=5)


# =========================
# GRÁFICA
# =========================
fig, ax = plt.subplots()
fig.patch.set_facecolor("#121212")

canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

ultima_muestra = None


# =========================
# LOOP UI
# =========================
actualizar_espectro()
root.mainloop()