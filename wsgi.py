from model.base import Session, engine, Base
from model.predictor import Predictor
from flask import Flask, request
import time
from celery import Celery
import tempfile
import os
import zipfile
from ml.dsl.hands import read_all_tournaments
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
    dir = LOGS_DIR + "/" + id
    os.mkdir(dir)

    with zipfile.ZipFile(LOGS_DIR + "/" + id + ".zip", 'r') as zip_ref:
        zip_ref.extractall(dir)

    # fetch predictor from db
    # update predictor with file count

    pre_flop_actions = []
    flop_actions = []
    turn_actions = []
    river_actions = []

    for tournament_log in read_all_tournaments(dir):  # enumerable
        tournament = interpret(tournament_log)
        pre_flop_actions = pre_flop_actions + tournament.pre_flop_actions
        flop_actions = flop_actions + tournament.flop_actions
        turn_actions = turn_actions + tournament.turn_actions
        river_actions = river_actions + tournament.river_actions
        # update predictor total files

    # train
    # set predictor status as finished
    # fit model and save in the predictor class
    # set predictor status as finished

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
    file.save(LOGS_DIR + "/" + str(predictor.id) + ".zip")

    predictor = Predictor()
    session.add(predictor)
    session.commit()

    celery.send_task('wsgi.process_log_files',
                     kwargs={"id": str(predictor.id)})

    return {"id": str(predictor.id)}


@ app.route('/model', methods=['POST'])
def model():
    return '/model'


@ app.route('/eval', methods=['POST'])
def eval():
    return '/eval'


if __name__ == '__main__':
    app.run(debug=True)
