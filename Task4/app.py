import spacy as spacy
from flask import Flask

nlp = spacy.load("en_core_web_sm")

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
            fact['tokens'].append(new_tokens)
        new_fact = fact.copy()
        fact['tokens'] = []
        facts.append(new_fact)
    return facts


@app.route('/<seq>')
def upload_page(seq):
    doc = nlp(seq)
    facts = get_facts(doc)

    return {
        "facts": facts
    }


if __name__ == '__main__':
    app.run()
