from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from rq import Queue
from worker import conn


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
q = Queue(connection=conn)


import views


if __name__ == '__main__':
    app.run()
