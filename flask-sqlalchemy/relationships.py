from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy_relationship_example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ExecutionStates(Enum):
    INITIATED = 'INITIATED'
    RUNNED = 'RUNNED'
    VALIDATED = 'VALIDATED'


class TestCase(db.Model):
    test_case_id = db.Column(db.String(100), nullable=False, primary_key=True)
    lookout_id = db.Column(db.String(100), nullable=False)
    app_id = db.Column(db.String(100), nullable=False)
    request = db.relationship('Request', backref='test_case', lazy=True)
    internal_request_execution = db.relationship('InternalRequestExecution', backref='test_case',
                                                 lazy=True)
    test_execution = db.relationship('TestExecution', backref='test_case', lazy=True)

    def __init__(self, app_id=None, lookout_id=None, test_case_id=None):
        self.app_id = app_id
        self.lookout_id = lookout_id
        self.test_case_id = TestCase.generate_id(app_id, lookout_id) if test_case_id is None else test_case_id

    @classmethod
    def generate_id(cls, app_id, lookout_id):
        return app_id + '-' + lookout_id


class Request(db.Model):
    request_id = db.Column(db.String(100), nullable=False, primary_key=True)
    event_id = db.Column(db.String(100), nullable=False)
    lookout_id = db.Column(db.String(100), nullable=False)
    lookout_description = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    date_millis = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body = db.Column(db.Text(), nullable=False)
    http_method = db.Column(db.String(10), nullable=False)
    headers = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    expected_http_status = db.Column(db.Integer, nullable=False)
    expected_response = db.Column(db.Text(), nullable=False)
    app_id = db.Column(db.String(50), nullable=False)
    test_case_id = db.Column(db.String(100), db.ForeignKey('test_case.test_case_id'))
    internal_request_execution = db.relationship('InternalRequestExecution', backref='request', lazy=True)

    def __init__(self, app_id=None, event_id=None, lookout_id=None, lookout_description=None, url=None,
                 date_millis=None,date_time=None,
                 body=None, http_method=None, headers=None, type=None, expected_http_status=None,
                 expected_response=None):
        self.request_id = self._generate_id(app_id, event_id)
        self.app_id = app_id
        self.event_id = event_id
        self.lookout_id = lookout_id
        self.lookout_description = lookout_description
        self.url = url
        self.date_millis = date_millis
        self.date_time = date_time
        self.body = body
        self.http_method = http_method
        self.headers = headers
        self.type = type
        self.expected_http_status = expected_http_status
        self.expected_response = expected_response

    @staticmethod
    def _generate_id(app_id, event_id):
        return app_id + '-' + event_id


class TestExecution(db.Model):
    execution_id = db.Column(db.String(100), nullable=False, primary_key=True)
    test_case_id = db.Column(db.String(100), db.ForeignKey('test_case.test_case_id'), nullable=False, primary_key=True)
    status = db.Column(db.String(50), default=ExecutionStates.INITIATED.value)
    result = db.Column(db.String(100), default="")

    request_executions = db.relationship('RequestExecution', backref='test_execution', lazy=True)
    internal_request_executions = db.relationship('InternalRequestExecution', backref='test_execution', lazy=True)


class RequestExecution(db.Model):
    request_execution_id = db.Column(db.String(100), nullable=False, primary_key=True)

    lookout_description = db.Column(db.String(100), default="")
    url = db.Column(db.String(500), default="")
    body = db.Column(db.Text(), default="")
    http_method = db.Column(db.String(10), default="")
    headers = db.Column(db.Text, default="")
    type = db.Column(db.String(10), default="")
    http_status = db.Column(db.Integer)
    response = db.Column(db.Text(), default="")
    execution_id = db.Column(db.String(100), db.ForeignKey('test_execution.execution_id'), nullable=False)


class InternalRequestExecution(db.Model):
    test_case_id = db.Column(db.String(100), db.ForeignKey('test_case.test_case_id'), nullable=False, primary_key=True)
    execution_id = db.Column(db.String(100), db.ForeignKey('test_execution.execution_id'), nullable=False, primary_key=True)
    request_id = db.Column(db.String(100), db.ForeignKey('request.request_id'), nullable=False, primary_key=True)
    description = db.Column(db.String(100))
    status = db.Column(db.String(50), default=ExecutionStates.INITIATED.value)


if __name__ == '__main__':
    print("Create table")
    db.drop_all()
    db.create_all()
    app_id = "app-test"
    lookout_id = "look123"
    print("Create and save Requests")
    req_1 = Request(app_id=app_id, event_id="ev1", lookout_id=lookout_id, lookout_description="evento 1", url="url1",
                    body="body", http_method="GET", headers="headers", type="E",date_millis=123,
                    expected_http_status=200, expected_response="response")

    req_2 = Request(app_id=app_id, event_id="ev2", lookout_id=lookout_id, lookout_description="evento 2", url="url2",
                    body="body", http_method="GET", headers="headers", type="E",date_millis=123,
                    expected_http_status=400, expected_response="response")

    req_3 = Request(app_id=app_id, event_id="ev3", lookout_id=lookout_id, lookout_description="evento 3", url="url3",
                    body="body", http_method="GET", headers="headers", type="E",date_millis=123,
                    expected_http_status=500, expected_response="response")

    db.session.add(req_1)
    db.session.add(req_2)
    db.session.add(req_3)
    print("Create and save TestCase")
    test_case = TestCase(app_id, lookout_id)
    db.session.add(test_case)
    db.session.commit()