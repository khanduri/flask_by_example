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
    q,
)
from models import Result
from rq.job import Job
from worker import conn
from flask import jsonify


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def process():
    try:
        url = request.form['url']
        job = q.enqueue_call(
            func=count_and_save_words,
            args=(url,),
            result_ttl=5000
        )
        print(job.get_id())
    except Exception as e:
        msg = "URL missing"
        return render_template('index.html', errors=[msg])
    return render_template('index.html')


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        result = Result.query.filter_by(id=job.result).first()
        results = sorted(
            result.result_no_stop_words.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:30]

        return jsonify(results), 200
    return "Nay!", 202


def count_and_save_words(url):
    resp = requests.get(url)
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
    try:
        result = Result(
            url=url,
            result_all=raw_word_count,
            result_no_stop_words=no_stop_words_count
        )
        db.session.add(result)
        db.session.commit()
        return result.id
    except Exception as e:
        print e
        errors.append("Unable to add item to database.")
        return {"error": errors}


@app.route('/<name>')
def hello_name(name):
    return "Hello %s" % name


