import cv2
import mediapipe as mp
import os
import numpy as np
from keras_preprocessing.image import load_img, img_to_array
from keras.models import load_model

modelo = 'C:/Users/PC/Documents/Tadeo/Poryecyo de capacidad/Manos/Modelo.h5'
cnn = load_model(modelo)

direccion = 'C:/Users/PC/Documents/Tadeo/Poryecyo de capacidad/Manos/Fotos/Validacion'
dire_img = os.listdir(direccion)
print("Nombres: ", dire_img)

# Leemos la camara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se puede abrir la cámara.")
    exit()

# Creamos un objeto que va almacenar la detección y el seguimiento de las manos
clase_manos = mp.solutions.hands
manos = clase_manos.Hands()

# Método para dibujar las manos
dibujo = mp.solutions.drawing_utils

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se puede leer el frame.")
        break

    color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    copia = frame.copy()
    resultado = manos.process(color)
    posiciones = []

    if resultado.multi_hand_landmarks:
        for mano in resultado.multi_hand_landmarks:
            for id, lm in enumerate(mano.landmark):
                alto, ancho, c = frame.shape
                corx, cory = int(lm.x * ancho), int(lm.y * alto)
                posiciones.append([id, corx, cory])
                dibujo.draw_landmarks(frame, mano, clase_manos.HAND_CONNECTIONS)
            
            if len(posiciones) != 0:
                pto_i1 = posiciones[3]
                pto_i2 = posiciones[17]
                pto_i3 = posiciones[10]
                pto_i4 = posiciones[0]
                pto_i5 = posiciones[9]
                
                x1 = max(pto_i5[1] - 80, 0)
                y1 = max(pto_i5[2] - 80, 0)
                x2 = min(pto_i5[1] + 80, frame.shape[1])
                y2 = min(pto_i5[2] + 80, frame.shape[0])
                
                dedos_reg = copia[y1:y2, x1:x2]
                dedos_reg = cv2.resize(dedos_reg, (200, 200), interpolation=cv2.INTER_CUBIC)
                x = img_to_array(dedos_reg) / 255.0
                x = np.expand_dims(x, axis=0)
                
                vector = cnn.predict(x)
                resultado = vector[0]
                respuesta = np.argmax(resultado)
                
                if respuesta == 1:
                    print(vector, resultado)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    cv2.putText(frame, '{}'.format(dire_img[0]), (x1, y1 - 5), 1, 1.3, (0, 255, 0), 1, cv2.LINE_AA)
                elif respuesta == 0:
                    print(vector, resultado)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(frame, '{}'.format(dire_img[1]), (x1, y1 - 5), 1, 1.3, (0, 0, 255), 1, cv2.LINE_AA)

    cv2.imshow("Video", frame)
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
