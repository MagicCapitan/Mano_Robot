import serial as seri
import time
import numpy as np
# Configura el puerto COM (asegúrate de que sea el correcto)
ser = seri.Serial('COM3', 9600)  # Reemplaza 'COM3' con el puerto que esté usando tu Arduino
time.sleep(2)  # Espera para que el Arduino se inicialice

# Arreglo de cuatro elementos que queremos enviar
while True:
    Random1 = int(np.random.rand() * 180)
    Random2 = int(np.random.rand() * 180)
    Random3 = int(np.random.rand() * 180)
    Random4 = int(np.random.rand() * 180)
    
    data = [Random1, Random2, Random3, Random4]

# Enviar los datos como una cadena separada por comas
    data_str = ','.join(map(str, data)) + '\n'
    ser.write(data_str.encode())


