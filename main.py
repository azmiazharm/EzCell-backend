
from flask import Flask, request
from keras.preprocessing import image
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import time

model = tf.keras.models.load_model('./model/malaria-90.h5')

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Helloo</h1>'


@app.route('/process', methods=['POST'])
def infer_image():
    if 'file' not in request.files:
        return "Image missing"

    file = request.files.get('file')
    if not file:
        return "File not found"

    img = resize_img(file.read())

    result = predict(img)
    return result

def resize_img(img):
    img = Image.open(io.BytesIO(img))
    img = img.resize((118, 118))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return np.vstack([img])

def predict(img):
    a = getTime()   
    print(a)
    classes = model.predict(img, batch_size=10)

    print(getTime())
    print(classes)
    print(classes[0])

    
    if classes[0]>0:
        return {
            "result" : "uninfected",
            "process" : str(round(getTime() - a, 2)) + " s"
            }
    else:
        return {
            "result" : "infected",
            "process" : str(round(getTime() - a, 2)) + " s"
            }

def getTime():
    return time.time()


if(__name__ == "__main__"):
    app.run(debug=True)