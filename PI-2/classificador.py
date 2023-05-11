import tensorflow as tf
from tensorflow import keras
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
import os

def normalizar(image):
    image = cv2.resize(image, (64,64))
    image = image.reshape((1, 64, 64, 3,))
    image = tf.cast(image/255. ,tf.float32)

    return image

def predict_url(url):

    request = requests.get(url)

    image = Image.open(fp=BytesIO(request.content))
    image = image.convert('RGB')

    arr_image = np.array(image)

    labels = os.listdir(f"{os.getcwd()}/classificador/train")

    image = normalizar(arr_image)

    model = keras.saving.load_model("classificador/satellite_image_classificator.h5")

    probabilidades = model.predict([image])

    predict = tf.math.argmax(probabilidades[0])

    predict = str(tf.gather(labels, predict).numpy()).split("'")[1]

    return predict.upper()

