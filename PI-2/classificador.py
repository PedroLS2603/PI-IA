import tensorflow as tf
from tensorflow import keras
import requests
from PIL import Image
from io import BytesIO

def normalizar(image):
    image = tf.cast(image/255. ,tf.float32)
    print(image.shape)
    image = tf.image.resize(image, (64,64))
    print(image.shape)
    image = tf.reshape(image, (64,64,3))

    return image
def predict_url(url):

    request = requests.get(url)

    img_bytes = BytesIO(request.content)

    image = Image.open(fp=img_bytes)
    image = image.convert('RGB')
    arr_image = keras.utils.img_to_array(image)

    # image = normalizar(arr_image)
    print(image.shape)

    model = keras.saving.load_model("classificador/satellite_image_classificator.h5")


    predict = model.predict([image])

    return predict

# def predict_file(image=None):
