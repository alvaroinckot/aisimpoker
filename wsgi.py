from model.base import Session, engine, Base
from model.job import Job
from flask import Flask, request
app = Flask(__name__)

Base.metadata.create_all(engine)

session = Session()


@app.route('/upload', methods=['POST'])
def upload():
    session.add(Job())
    session.commit()
    session.close()
    return '/upload'


@app.route('/model', methods=['POST'])
def model():
    return '/model'


@app.route('/eval', methods=['POST'])
def eval():
    return '/eval'
