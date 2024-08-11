import serial
import time

# Configuración del puerto serial
ser = serial.Serial('COM3', 9600, timeout=1)  # Reemplaza 'COM3' con tu puerto serial

# Función para enviar un arreglo de cuatro números
def enviar_arreglo(arreglo):
    # Convertir el arreglo a una cadena de texto con números separados por comas
    datos = ",".join(map(str, arreglo))
    ser.write((datos + "\n").encode())  # Enviar la cadena de texto como bytes
    print(f"Enviando: {datos}")  # Depuración
    time.sleep(0.1)  # Pausa para asegurar que el dispositivo pueda procesar el dato

# Arreglo de ejemplo
mi_arreglo = [180, 20, 30, 40]

# Enviar el arreglo
enviar_arreglo(mi_arreglo)

# Cerrar el puerto serial
ser.close()
