from flask import (
    Flask,
    render_template,
    request,
)
from flask.ext.sqlalchemy import SQLAlchemy
import os
import requests


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():

    errors = []
    if request.method == "POST":
        try:
            url = request.form['url']
            resp = requests.get(url)
            print(resp.text)
        except:
            msg = """
            Unable to get URL(%s). Please make sure it's valid and try again.
            """ % url

            errors.append(msg)

    return render_template('index.html')


@app.route('/<name>')
def hello_name(name):
    return "Hello %s" % name


if __name__ == '__main__':
    app.run()
