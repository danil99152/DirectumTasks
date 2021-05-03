import spacy as spacy
from pytesseract import Output

try:
    from PIL import Image
except ImportError:
    import Image

import pytesseract
from flask import Flask

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\danil99152\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

nlp = spacy.load("en_core_web_sm")

UPLOAD_FOLDER = 'images/'

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def convert_cat(cat):
    return {
        'ORG': "ORGANIZATION",
        'GPE': "LOCATION",
    }[cat]


def get_facts(doc):
    facts = []
    fact = {"text": [], "tag": [], "tokens": []}
    tokens = {"text": [], "offset": []}
    for ent in doc.ents:
        fact['text'] = ent.text
        try:
            fact['tag'] = convert_cat(ent.label_)
        except KeyError:
            fact['tag'] = ent.label_
        start_char = 0
        for token in ent:
            tokens['text'] = token.text
            tokens['offset'] = ent.start_char + start_char
            start_char = len(token.text) + 1
            new_tokens = tokens.copy()
            fact['tokens'] = new_tokens
        new_fact = fact.copy()
        facts.append(new_fact)
    return facts


def ocr_core(file):
    io = Image.open(file)
    text = pytesseract.image_to_string(io, lang='eng')
    return text


@app.route('/<seq>')
def upload_page(seq):
    print(seq)
    if seq.rsplit('.', 1)[1].lower() == "tif":
        filename = seq.rsplit('/', 1)[-1].lower()
        tiffile = UPLOAD_FOLDER + filename.replace(filename.rsplit('.', 1)[1].lower(), 'jpg')
        try:
            im = Image.open(seq)
            im.thumbnail(im.size)
            im.save(tiffile, "JPEG", quality=100)
        except Exception as e:
            print(e)
        seq = tiffile

        extracted_text = ocr_core(seq)
        doc = nlp(extracted_text)
    else:
        doc = nlp(seq)

    facts = get_facts(doc)
    #
    return {
        "facts": facts
    }


if __name__ == '__main__':
    app.run()
