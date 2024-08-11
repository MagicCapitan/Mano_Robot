#------------------------------- Importamos librerías ---------------------------------
import cv2
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers         #Optimizador con el que vamos a entrenar el modelo
from tensorflow.keras.models import Sequential  #Nos permite hacer redes neuronales secuenciales
from tensorflow.keras.layers import Dropout, Flatten, Dense, Activation
from tensorflow.keras.layers import Conv2D, MaxPooling2D  #Capas para hacer las convoluciones
from tensorflow.keras import backend as K       #Si hay una sesión de Keras, la cerramos para tener todo limpio

K.clear_session()  # Limpiamos todo

datos_entrenamiento = '/content/Entrenamiento'
datos_validacion = '/content/Validacion'

# Parámetros
iteraciones = 20  # Número de iteraciones para ajustar nuestro modelo
altura, longitud = 200, 200 # Tamaño de las imágenes de entrenamiento
batch_size = 1  # Número de imágenes que vamos a enviar
pasos = 829 // batch_size  # Número de veces que se va a procesar la información en cada iteración
pasos_validacion = 829 // batch_size  # Después de cada iteración, validamos lo anterior
filtrosconv1 = 32
filtrosconv2 = 64     # Número de filtros que vamos a aplicar en cada convolución
tam_filtro1 = (3, 3)
tam_filtro2 = (2, 2)   # Tamaños de los filtros 1 y 2
tam_pool = (2, 2)  # Tamaño del filtro en max pooling
clases = 2  # Mano abierta y cerrada (5 dedos y 0 dedos)
lr = 0.0005  # Ajustes de la red neuronal para acercarse a una solución óptima

# Pre-Procesamiento de las imágenes
preprocesamiento_entre = ImageDataGenerator(
    rescale=1./255,   # Pasar los píxeles de 0 a 255 | 0 a 1
    shear_range=0.3, # Generar nuestras imágenes inclinadas para un mejor entrenamiento
    zoom_range=0.3,  # Genera imágenes con zoom para un mejor entrenamiento
    horizontal_flip=True # Invierte las imágenes para mejor entrenamiento
)

preprocesamiento_vali = ImageDataGenerator(
    rescale=1./255
)

imagen_entreno = preprocesamiento_entre.flow_from_directory(
    datos_entrenamiento,       # Va a tomar las fotos que ya almacenamos
    target_size=(altura, longitud),
    batch_size=batch_size,
    class_mode='categorical',  # Clasificación categórica = por clases
)

imagen_validacion = preprocesamiento_vali.flow_from_directory(
    datos_validacion,
    target_size=(altura, longitud),
    batch_size=batch_size,
    class_mode='categorical'
)

# Creamos la red neuronal convolucional (CNN)
cnn = Sequential()  # Red neuronal secuencial
# Agregamos filtros con el fin de volver nuestra imagen muy profunda pero pequeña
cnn.add(Conv2D(filtrosconv1, tam_filtro1, padding='same', input_shape=(altura, longitud, 3), activation='relu')) # Agregamos la primera capa
cnn.add(MaxPooling2D(pool_size=tam_pool)) # Después de la primera capa vamos a tener una capa de max pooling y asignamos el tamaño

cnn.add(Conv2D(filtrosconv2, tam_filtro2, padding='same', activation='relu')) # Agregamos nueva capa
cnn.add(MaxPooling2D(pool_size=tam_pool))

# Ahora vamos a convertir esa imagen profunda a una plana, para tener 1 dimensión con toda la info
cnn.add(Flatten())  # Aplanamos la imagen
cnn.add(Dense(256, activation='relu'))  # Asignamos 256 neuronas
cnn.add(Dropout(0.5)) # Apagamos el 50% de las neuronas en la función anterior para no sobreajustar la red
cnn.add(Dense(clases, activation='softmax'))  # Es nuestra última capa, es la que nos dice la probabilidad de que sea alguna de las clases

# Agregamos parámetros para optimizar el modelo
optimizar = optimizers.Adam(learning_rate=lr)
cnn.compile(loss='categorical_crossentropy', optimizer=optimizar, metrics=['accuracy'])

# Entrenamos nuestra red
cnn.fit(imagen_entreno, steps_per_epoch=pasos, epochs=iteraciones, validation_data=imagen_validacion, validation_steps=pasos_validacion)

# Guardamos el modelo
cnn.save('Modelo.h5')
cnn.save_weights('pesos.h5')
