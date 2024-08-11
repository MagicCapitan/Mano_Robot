import cv2
import mediapipe as mp
import numpy as np

# Inicializar la captura de video
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se puede abrir la cámara.")
    exit()

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Función para calcular la distancia entre dos puntos
def distancia(punto1, punto2):
    return np.linalg.norm(np.array(punto1) - np.array(punto2))

# Lista para almacenar las longitudes máximas de los dedos
longitud_maxima = [0, 0, 0, 0, 0]  # Una entrada por dedo (pulgar, índice, medio, anular, meñique)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se puede leer el frame.")
        break

    # Convertir el frame a RGB para MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    puntos_mano = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Obtener los puntos de referencia de la mano
            h, w, _ = frame.shape
            for lm in hand_landmarks.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                puntos_mano.append((x, y))
            
            # Calcular las longitudes de los dedos
            if puntos_mano:
                # Puntos de referencia de los dedos
                indices_dedos = [
                    (0, 5), (0, 9), (0, 13), (0, 17), # Muñeca a las puntas de los dedos
                    (5, 6, 7, 8), # Pulgar
                    (9, 10, 11, 12), # Índice
                    (13, 14, 15, 16), # Medio
                    (17, 18, 19, 20)  # Anular y meñique
                ]
                
                longitudes_dedos = []
                for indice in indices_dedos[4:]:
                    longitud = sum(distancia(puntos_mano[indice[i]], puntos_mano[indice[i + 1]]) for i in range(len(indice) - 1))
                    longitudes_dedos.append(longitud)
                
                # Calcular el tamaño de la mano (muñeca a la punta del dedo medio)
                tamano_mano = distancia(puntos_mano[0], puntos_mano[9])
                
                # Normalizar las longitudes de los dedos
                longitudes_normalizadas = [longitud / tamano_mano for longitud in longitudes_dedos]
                
                # Actualizar las longitudes máximas si se detecta una mano completamente extendida
                if all(l > m for l, m in zip(longitudes_normalizadas, longitud_maxima)):
                    longitud_maxima = longitudes_normalizadas
                    print("Longitudes máximas actualizadas:", longitud_maxima)
                
                # Comparar las longitudes actuales con las máximas
                flexion_actual = [l / m if m != 0 else 0 for l, m in zip(longitudes_normalizadas, longitud_maxima)]
                print("Flexión actual de los dedos:", flexion_actual)

    # Mostrar el frame con las anotaciones de MediaPipe
    cv2.imshow("Video", frame)
    
    # Salir del bucle si se presiona la tecla 'Esc'
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Liberar la captura de video y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
