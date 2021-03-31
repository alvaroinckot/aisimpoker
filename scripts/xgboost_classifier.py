from ml.engine.multi_column_label_encoder import MultiColumnLabelEncoder
from sklearn import tree
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from xgboost import XGBClassifier
from sklearn.metrics import mean_absolute_error
import pandas as pd
import os


path = "./compilations/summary_{}_v{}.csv"
version = os.getenv("FILE_COMPILATION_VERSION")
streets = ['pre_flop', 'flop', 'turn', 'river']


def fit():
    print('version ' + version)
    for street in streets:
        print("Street " + street)

        X = pd.read_csv(path.format(street, version))
        X = MultiColumnLabelEncoder(
            columns=["action", "street", "position", "position_category"]).fit_transform(X)

        y = X['action']
        del X['action']
        del X['street']

        X = X.to_numpy()
        y = y.to_numpy()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=.3, random_state=42, stratify=y)

        clfa = XGBClassifier()

        clfa = clfa.fit(X_train, y_train)

        predicted = clfa.predict(X_test)

        score = clfa.score(X_test, y_test)

        matrix = confusion_matrix(y_test, predicted)

        print("\nResultados baseados em Holdout 70/30")
        print("Taxa de acerto = %.4f " % score)
        print("Matriz de confusao:")
        print(matrix)

        clfb = XGBClassifier()
        folds = 10
        result = model_selection.cross_val_score(clfb, X, y, cv=folds)

        print("\nResultados baseados em Validacao Cruzada")
        print("Qtde folds: %d:" % folds)
        print("Taxa de Acerto: %.4f" % result.mean())
        print("Desvio padrao: %.4f" % result.std())

        # matriz de confusÃ£o da validacao cruzada
        Z = model_selection.cross_val_predict(clfb, X, y, cv=folds)
        cm = confusion_matrix(y, Z)
        print("Matriz de confusao:")
        print(cm)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("\n\n")
