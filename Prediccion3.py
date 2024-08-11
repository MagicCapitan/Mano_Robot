import cv2
import mediapipe as mp

# Inicializar la captura de video
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se puede abrir la cámara.")
    exit()

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

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

    # Mostrar el frame con las anotaciones de MediaPipe
    cv2.imshow("Video", frame)
    
    # Salir del bucle si se presiona la tecla 'Esc'
    if cv2.waitKey(1) & 0xFF == 27:
        break

    # Imprimir los puntos de referencia de la mano
    if puntos_mano:
        print(puntos_mano)
    
# Liberar la captura de video y cerrar las ventanas
#cap.release()  # Libera el objeto de captura de video
#cv2.destroyAllWindows()  # Cierra todas las ventanas abiertas por OpenCV
