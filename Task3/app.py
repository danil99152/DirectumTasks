import cv2
from tensorflow import keras
import numpy as np
from flask import Flask

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

model = keras.models.load_model('C:/Users/danil99152/Downloads/model2.h5')


@app.route('/<path:file>')
def upload_page(file):
    doc = cv2.imread(file)
    print(type(doc))
    height, width, channels = doc.shape
    doc = cv2.resize(doc, (256, 256)) / 255.
    print(type(doc))
    pred = model.predict(np.expand_dims(doc, axis=0))
    doc_type = "main"
    if pred >= 0.5:
        doc_type = "other"
    return {
        "source": {
            "width": width,
            "height": height,
            "type": doc_type
        }
    }


if __name__ == '__main__':
    app.run()
