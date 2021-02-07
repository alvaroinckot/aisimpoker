from model.base import Session, engine, Base
from model.predictor import Predictor

from flask import Flask, request, jsonify

from celery import Celery
from celery.result import allow_join_result

import traceback
import time
import tempfile
import os
import zipfile
import pickle


from ml.dsl.hands import read_all_tournaments
from ml.dsl.parser import interpret

from ml.engine.multi_column_label_encoder import MultiColumnLabelEncoder

import pandas as pd

from sklearn import tree
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_absolute_error

from xgboost import XGBClassifier

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

LOGS_DIR = "./logs"
PROCESSED_LOGS_FILE_NAME_FORMAT = LOGS_DIR + "/summary_{}_{}.csv"
TRAINNED_MODEL_FILE_NAME_FORMAT = LOGS_DIR + "/{}_{}.dat"


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
def fit_model(id, street):
    worker_session = Session()

    print("received id to fit: " + id + " for the street " + street)
    X = pd.read_csv(PROCESSED_LOGS_FILE_NAME_FORMAT.format(street, id))
    X = MultiColumnLabelEncoder(
        columns=["action", "street", "position", "position_category"]).fit_transform(X)

    y = X['action']
    del X['action']
    del X['street']

    X = X.to_numpy()
    y = y.to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.3, random_state=42, stratify=y)

    classifier = XGBClassifier()
    classifier = classifier.fit(X_train, y_train)

    pickle.dump(classifier, open(
        TRAINNED_MODEL_FILE_NAME_FORMAT.format(street, id), "wb"))

    predicted = classifier.predict(X_test)
    score = classifier.score(X_test, y_test)

    predictor = worker_session.query(
        Predictor).filter(Predictor.id == id).first()

    if(street == 'pre_flop'):
        predictor.pre_flop_success_rate = score

    if(street == 'flop'):
        predictor.flop_success_rate = score

    if(street == 'turn'):
        predictor.turn_success_rate = score

    if(street == 'river'):
        predictor.river_success_rate = score

    predictor.status = 'finished'

    worker_session.commit()


@celery.task
def process_single_log_file(tournament_log):
    print("started to process a new file")
    tournament = interpret(tournament_log.replace(u'\ufeff', ''))
    return [tournament.pre_flop_actions, tournament.flop_actions, tournament.turn_actions, tournament.river_actions]


@celery.task
def process_log_files(id):
    worker_session = Session()
    print("received prossing :" + id)

    dir = LOGS_DIR + "/" + id
    os.mkdir(dir)

    with zipfile.ZipFile(LOGS_DIR + "/" + id + ".zip", 'r') as zip_ref:
        zip_ref.extractall(dir)

    predictor = worker_session.query(Predictor).filter(
        Predictor.id == id).first()

    predictor.total_files = len(os.listdir(dir))

    worker_session.commit()

    tasks, pre_flop_actions, flop_actions, turn_actions, river_actions = [], [], [], [], []

    for tournament_log in read_all_tournaments(dir):  # enumerable
        tasks = tasks + \
            [celery.send_task('wsgi.process_single_log_file', kwargs={
                              "tournament_log": tournament_log})]

    for task in tasks:
        try:
            with allow_join_result():
                tournament = task.get()
                pre_flop_actions = pre_flop_actions + tournament[0]
                flop_actions = flop_actions + tournament[1]
                turn_actions = turn_actions + tournament[2]
                river_actions = river_actions + tournament[3]
        except:
            predictor.failed_files = predictor.failed_files + 1
            traceback.print_exc()
        finally:
            predictor.finished_files = predictor.finished_files + 1
            worker_session.commit()

    predictor.status = 'training_model'
    worker_session.commit()

    pd.DataFrame(pre_flop_actions).fillna(0).to_csv(
        PROCESSED_LOGS_FILE_NAME_FORMAT.format("pre_flop", id), index=None, header=True)

    pd.DataFrame(flop_actions).fillna(0).to_csv(
        PROCESSED_LOGS_FILE_NAME_FORMAT.format("flop", id), index=None, header=True)

    pd.DataFrame(turn_actions).fillna(0).to_csv(
        PROCESSED_LOGS_FILE_NAME_FORMAT.format("turn", id), index=None, header=True)

    pd.DataFrame(river_actions).fillna(0).to_csv(
        PROCESSED_LOGS_FILE_NAME_FORMAT.format("river", id), index=None, header=True)

    streets = ['pre_flop', 'flop', 'turn', 'river']
    for street in streets:
        celery.send_task('wsgi.fit_model', kwargs={
                         "id": str(predictor.id), "street": street})


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
        Predictor.id == request.get_json()["id"]).first()
    p_dict = p.__dict__
    del p_dict['_sa_instance_state']
    return jsonify(p_dict)


@app.route('/eval', methods=['POST'])
def eval():
    return '/eval'


if __name__ == '__main__':
    app.run(debug=True)
