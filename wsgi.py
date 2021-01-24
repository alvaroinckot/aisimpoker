from model.base import Session, engine, Base
from model.predictor import Predictor
from flask import Flask, request
import time
from celery import Celery
import tempfile
import os
import zipfile
app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

LOGS_DIR = "./logs"


def make_celery(app):
    celery = Celery(
        'wsgi',
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)

Base.metadata.create_all(engine)

session = Session()


@celery.task
def process_log_files(id):
    os.mkdir(LOGS_DIR + "/" + id)
    with zipfile.ZipFile(LOGS_DIR + "/" + id + ".zip", 'r') as zip_ref:
        zip_ref.extractall(LOGS_DIR + "/" + id)
    # Base.metadata.create_all(engine)
    # session = Session()
    # session.add(Job())
    # session.commit()
    # session.close()


@app.route('/upload', methods=['POST'])
def upload():

    file = request.files.get("file")
    if(file == None):
        return 'file cannot be empty'

    predictor = Predictor()
    session.add(predictor)
    session.commit()

    file.save(LOGS_DIR + "/" + str(predictor.id) + ".zip")

    celery.send_task('wsgi.process_log_files',
                     kwargs={"id": str(predictor.id)})

    return LOGS_DIR + "/" + str(predictor.id) + ".zip"


@ app.route('/model', methods=['POST'])
def model():
    return '/model'


@ app.route('/eval', methods=['POST'])
def eval():
    return '/eval'


if __name__ == '__main__':
    app.run(debug=True)
