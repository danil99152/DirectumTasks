from pytesseract import Output

try:
    from PIL import Image
except ImportError:
    import Image

import pytesseract
from flask import Flask

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\danil99152\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

UPLOAD_FOLDER = 'images/'

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def get_tokens(file):
    img = Image.open(file)
    data = pytesseract.image_to_data(img, output_type=Output.DICT)
    tokens = []
    token = {"text": [], "position": [], "offset": []}
    position = {"left": [], "top": [], "width": [], "height": []}
    offset = 0
    for i in range(len(data['level'])):
        position["left"] = data['left'][i]
        position["top"] = data['top'][i]
        position["width"] = data['width'][i]
        position["height"] = data['height'][i]
        token["position"] = position.copy()
        token["text"] = data['text'][i]
        token["offset"] = offset
        offset += len(data['text'][i])
        new_token = token.copy()
        tokens.append(new_token)
    return tokens


def ocr_core(file):
    io = Image.open(file)
    text = pytesseract.image_to_string(io, lang='rus+eng')
    return text


@app.route('/<path:file>')
def upload_page(file):
    if file.rsplit('.', 1)[1].lower() == "tif":
        filename = file.rsplit('/', 1)[-1].lower()
        tiffile = UPLOAD_FOLDER + filename.replace(filename.rsplit('.', 1)[1].lower(), 'jpg')
        try:
            im = Image.open(file)
            im.thumbnail(im.size)
            im.save(tiffile, "JPEG", quality=100)
        except Exception as e:
            print(e)
        file = tiffile

    extracted_text = ocr_core(file)
    tokens = get_tokens(file)

    return {
        "text": extracted_text,
        "tokens": tokens,
        "source": {
            "width": Image.open(file).size[0],
            "height": Image.open(file).size[1]
        }
    }


if __name__ == '__main__':
    app.run()
