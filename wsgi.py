import traceback
from model.base import Session, engine, Base
from model.predictor import Predictor
from flask import Flask, request, jsonify
import time
from celery import Celery
import tempfile
import os
import zipfile
from ml.dsl.hands import read_all_tournaments
from ml.dsl.parser import interpret
from xgboost import XGBClassifier
import pandas as pd
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
    worker_session = Session()
    print("received " + id)

    dir = LOGS_DIR + "/" + id
    os.mkdir(dir)

    with zipfile.ZipFile(LOGS_DIR + "/" + id + ".zip", 'r') as zip_ref:
        zip_ref.extractall(dir)

    # fetch predictor from db
    # update predictor with file count
    predictor = worker_session.query(Predictor).filter(
        Predictor.id == id).first()

    predictor.total_files = len(os.listdir(dir))

    worker_session.commit()

    pre_flop_actions = []
    flop_actions = []
    turn_actions = []
    river_actions = []

    for tournament_log in read_all_tournaments(dir):  # enumerable
        try:
            tournament = interpret(tournament_log.replace(u'\ufeff', ''))
            pre_flop_actions = pre_flop_actions + tournament.pre_flop_actions
            flop_actions = flop_actions + tournament.flop_actions
            turn_actions = turn_actions + tournament.turn_actions
            river_actions = river_actions + tournament.river_actions
        except:
            predictor.failed_files = predictor.failed_files + 1
            print("error")
            traceback.print_exc()
        finally:
            predictor.finished_files = predictor.finished_files + 1
            worker_session.commit()

    predictor.status = 'training_model'
    worker_session.commit()

    # train
    # set predictor status as finished
    # fit model and save in the predictor class
    # set predictor status as finished

    # Base.metadata.create_all(engine)
    # session = Session()
    # session.add(Job())
    # session.commit()
    worker_session.close()


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

    return {"id": str(predictor.id)}


@app.route('/model', methods=['POST'])
def model():
    p = session.query(Predictor).filter(
        Predictor.id == request.args.get("id")).first()
    p_dict = p.__dict__
    del p_dict['_sa_instance_state']
    return jsonify(p_dict)


@ app.route('/eval', methods=['POST'])
def eval():
    return '/eval'


if __name__ == '__main__':
    app.run(debug=True)
