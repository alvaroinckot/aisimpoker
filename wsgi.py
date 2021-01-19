from flask import Flask, request
app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload():
    return '/upload'


@app.route('/model', methods=['POST'])
def model():
    return '/model'


@app.route('/eval', methods=['POST'])
def eval():
    return '/eval'
