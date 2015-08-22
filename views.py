import requests
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
import operator
import re
import nltk
from flask import (
    render_template,
    request,
)
from app import (
    app,
    db,
)
from models import Result


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def process():
    try:
        url = request.form['url']
        resp = requests.get(url)
    except Exception as e:
        msg = """
        Unable to get URL(%s). Please make sure it's valid and try again.
        """ % url
        return render_template('index.html', errors=[msg])

    if not resp:
        return render_template('index.html')

    errors = []
    # text processing
    raw = BeautifulSoup(resp.text, "html.parser").get_text()
    nltk.data.path.append('./nltk_data/')  # set the path
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)

    # remove punctuation, count raw words
    nonPunct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if nonPunct.match(w)]
    raw_word_count = Counter(raw_words)

    # stop words
    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    no_stop_words_count = Counter(no_stop_words)

    # save the results
    results = sorted(
        no_stop_words_count.items(),
        key=operator.itemgetter(1),
        reverse=True
    )[:30]

    try:
        result = Result(
            url=url,
            result_all=raw_word_count,
            result_no_stop_words=no_stop_words_count
        )
        db.session.add(result)
        db.session.commit()
    except Exception as e:
        print e
        errors.append("Unable to add item to database.")

    return render_template('index.html', errors=errors, results=results)


@app.route('/<name>')
def hello_name(name):
    return "Hello %s" % name


