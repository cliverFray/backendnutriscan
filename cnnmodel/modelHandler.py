from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
ruta=r'C:\Users\User\OneDrive - Universidad Peruana de Ciencias\Documents\Procesamiento de imagenes\nutriscan_model.h5'
# Cargar el modelo entrenado

model = tf.keras.models.load_model(r'C:\Users\cfray\Downloads\nutriscan_model.h5')
#model = tf.keras.models.load_model('')

# Cargar una imagen nueva y preprocesarla
img_path = r'C:\Users\cfray\Downloads\nina.jpg'
img = image.load_img(img_path, target_size=IMAGE_SIZE)
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Realizar predicción
predictions = model.predict(img_array)
predicted_class = np.argmax(predictions)

# Mapear la predicción a la clase correspondiente
class_labels = ['DESNUTRIDO', 'NORMAL', 'TUTOR']
print(f'La clase predicha es: {class_labels[predicted_class]}')