import cv2
import mediapipe as mp
import math

# Inicializar mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Lista de índices de los puntos deseados para cada dedo
dedos_indices = {
    'indice': [5, 6, 8],   # base, medio, punta
    'medio': [9, 10, 12],
    'anular': [13, 14, 16],
    'menique': [17, 18, 20]
}

def calcular_angulo(p1, p2, p3):
    """
    Calcular el ángulo en grados entre tres puntos.
    p1, p2, p3: (x, y) tuples
    """
    a = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    b = math.sqrt((p3[0] - p2[0])**2 + (p3[1] - p2[1])**2)
    c = math.sqrt((p3[0] - p1[0])**2 + (p3[1] - p1[1])**2)
    
    if a == 0 or b == 0:
        return 0
    
    cos_angle = (a**2 + b**2 - c**2) / (2 * a * b)
    # Asegurarse de que el valor está en el rango [-1, 1] para evitar errores numéricos
    cos_angle = min(1, max(-1, cos_angle))
    angulo_radianes = math.acos(cos_angle)
    angulo_grados = math.degrees(angulo_radianes)
    return angulo_grados

# Abrir la cámara
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("No se puede recibir frame (fin de transmisión?). Saliendo ...")
            break

        # Convertir la imagen de BGR a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Procesar la imagen y detectar las manos
        results = hands.process(frame_rgb)

        # Dibujar las anotaciones de las manos
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                altura, ancho, _ = frame.shape
                flexiones = []
                for dedo, indices in dedos_indices.items():
                    puntos = [hand_landmarks.landmark[idx] for idx in indices]
                    coordenadas = [(int(punto.x * ancho), int(punto.y * altura)) for punto in puntos]
                    angulo = calcular_angulo(*coordenadas)
                    # Ajustar el ángulo al rango 0-180
                    angulo = 180 - angulo  # Invertir el ángulo para que 180 sea extendido y 0 sea flexionado
                    angulo = min(max(angulo, 0), 180)  # Asegurarse de que el ángulo esté entre 0 y 180
                    flexiones.append(int(angulo))  # Convertir a entero para resultados discretos

                    for punto in coordenadas:
                        cv2.circle(frame, punto, 5, (0, 255, 0), -1)

                print(flexiones)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Mostrar la imagen
        cv2.imshow('MediaPipe Hands', frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
