
from sklearn import tree
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
import pandas as pd


class MultiColumnLabelEncoder:
    def __init__(self, columns=None):
        self.columns = columns  # array of column names to encode

    def fit(self, X, y=None):
        return self  # not relevant here

    def transform(self, X):
        '''
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''
        output = X.copy()
        if self.columns is not None:
            for col in self.columns:
                output[col] = preprocessing.LabelEncoder(
                ).fit_transform(output[col])
        else:
            for colname, col in output.iteritems():
                output[colname] = preprocessing.LabelEncoder().fit_transform(col)
        return output

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)


X = pd.read_csv("./compilations/summary_v4.csv")
X = MultiColumnLabelEncoder(columns=["action", "street"]).fit_transform(X)

y = X['action']
del X['action']

X = X.to_numpy()
y = y.to_numpy()


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=.3, random_state=42, stratify=y)


clfa = tree.DecisionTreeClassifier(criterion='entropy')

clfa = clfa.fit(X_train, y_train)

predicted = clfa.predict(X_test)

score = clfa.score(X_test, y_test)

matrix = confusion_matrix(y_test, predicted)

print("\nResultados baseados em Holdout 70/30")
print("Taxa de acerto = %.2f " % score)
print("Matriz de confusao:")
print(matrix)


clfb = tree.DecisionTreeClassifier(criterion='entropy')
folds = 10
result = model_selection.cross_val_score(clfb, X, y, cv=folds)

print("\nResultados baseados em Validacao Cruzada")
print("Qtde folds: %d:" % folds)
print("Taxa de Acerto: %.2f" % result.mean())
print("Desvio padrao: %.2f" % result.std())

# matriz de confusÃ£o da validacao cruzada
Z = model_selection.cross_val_predict(clfb, X, y, cv=folds)
cm = confusion_matrix(y, Z)
print("Matriz de confusao:")
print(cm)
