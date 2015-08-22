from app import db
import json


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    raw_result_all = db.Column(db.String())
    raw_result_no_stop_words = db.Column(db.String())

    _result_all = None
    _result_no_stop_words = None

    @property
    def result_all(self):
        if self.raw_result_all:
            self._result_all = json.loads(self.raw_result_all)
        return self._result_all

    @result_all.setter
    def result_all(self, data):
        self._result_all = data
        self.raw_result_all = json.dumps(self._result_all)

    @property
    def result_all(self):
        if self.raw_result_all:
            self._result_all = json.loads(self.raw_result_all)
        return self._result_all

    @result_all.setter
    def result_all(self, data):
        self._result_all = data
        self.raw_result_all = json.dumps(self._result_all)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id: %s; url: %s>' % (self.id, self.url)
