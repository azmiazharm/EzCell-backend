# Import lib
from flask import Flask, request, jsonify, make_response
from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import time

# Import ML model
malaria_model = tf.keras.models.load_model('./model/malaria-90.h5')

# Define flask app
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>EzCell Backend Service</h1>'


@app.route('/process-malaria', methods=['POST'])
def process_malaria():
    start = time.time()

    if 'file' not in request.files:
        return make_response(jsonify(success=False, message='File not found'), 400)

    file = request.files.get('file')
    if not file:
        return make_response(jsonify(success=False, message='File not found'), 400)

    img = resize_img(file.read())

    result = predict_malaria(img)

    time_taken = '{} s'.format(round(time.time() - start, 2))
    print(time_taken)
    return jsonify(success=True, result=result, process_time=time_taken)

def resize_img(img):
    img = Image.open(io.BytesIO(img))
    img = img.resize((118, 118))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return np.vstack([img])

def predict_malaria(img):
    classes = malaria_model.predict(img, batch_size=10)

    if classes[0]>0:
        return "uninfected"
    else:
        return "infected"

if(__name__ == "__main__"):
    app.run(debug=True, host='0.0.0.0', port=5000)