# IMPORTANTE: INSTALAR LAS LIBRERÍAS NECESARIAS
# pip install opencv-python mediapipe

# =========================
# IMPORTACIONES
# =========================

import cv2
import mediapipe as mp
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# =========================
# CONFIGURACIÓN DEL MODELO
# =========================

# Asegúrate de tener este archivo en la misma carpeta
MODEL_PATH = "examples/hand_landmarker.task"

# Configuración base del modelo
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)

# Opciones del detector
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2
)

# Crear detector
detector = vision.HandLandmarker.create_from_options(options)


# =========================
# CONEXIONES DE LA MANO
# =========================

# Cada par representa una línea entre puntos
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),        # pulgar
    (0,5),(5,6),(6,7),(7,8),        # índice
    (5,9),(9,10),(10,11),(11,12),   # medio
    (9,13),(13,14),(14,15),(15,16), # anular
    (13,17),(17,18),(18,19),(19,20),# meñique
    (0,17)                          # base de la mano
]


# =========================
# INICIAR CÁMARA
# =========================

cap = cv2.VideoCapture(0)


# =========================
# LOOP PRINCIPAL
# =========================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Efecto espejo
    frame = cv2.flip(frame, 1)

    # Convertir a RGB (MediaPipe usa RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convertir a formato MediaPipe
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    # =========================
    # DETECCIÓN DE MANOS
    # =========================

    result = detector.detect(mp_image)

    # =========================
    # DIBUJAR RESULTADOS
    # =========================

    if result.hand_landmarks:

        for hand_landmarks in result.hand_landmarks:

            h, w, _ = frame.shape

            # Convertimos landmarks a coordenadas de pantalla
            puntos = []
            for landmark in hand_landmarks:
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                puntos.append((x, y))

            # =========================
            # DIBUJAR CONEXIONES
            # =========================
            for conexion in HAND_CONNECTIONS:
                x1, y1 = puntos[conexion[0]]
                x2, y2 = puntos[conexion[1]]

                cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

            # =========================
            # DIBUJAR PUNTOS
            # =========================
            for x, y in puntos:
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            # =========================
            # RESALTAR DEDO ÍNDICE
            # =========================
            x, y = puntos[8]
            cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)


    # =========================
    # MOSTRAR VIDEO
    # =========================

    cv2.imshow("Hand Tracking (Python 3.13)", frame)

    # Salir con tecla ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break


# =========================
# LIMPIEZA
# =========================

cap.release()
cv2.destroyAllWindows()