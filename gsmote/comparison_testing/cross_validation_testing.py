"""Class to compare performance with different classifiers"""
import sys

from imblearn.over_sampling import SMOTE
from sklearn import model_selection

sys.path.append('../../')
# sys.path.append('/content/Modified-Geometric-Smote/')
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeRegressor
from gsmote import EGSmote
from gsmote.oldgsmote import OldGeometricSMOTE
from gsmote.comparison_testing.Evaluator import evaluate,evaluate2
import gsmote.comparison_testing.preprocessing as pp
import pandas as pd

sys.path.append('../../')

#  Directory
path = '../../data/'


def logistic_training():

    kfold = model_selection.StratifiedKFold(n_splits=10, random_state=True)

    scoreings = []

    for train_index, test_index in kfold.split(X,y):
        # print("Train:", train_index, "Validation:", test_index)
        X_t, X_test = X[train_index], X[test_index]
        y_t, y_test = y[train_index], y[test_index]

        GSMOTE = EGSmote()
        X_train, y_train = GSMOTE.fit_resample(X_t, y_t)
        regressor = LogisticRegression(max_iter=120)
        regressor.fit(X_train, y_train)

        # Predicting the Test set results
        y_predict = regressor.predict(X_test)
        y_pred = np.where(y_predict > 0.5, 1, 0)

        scoreings.append(evaluate2(y_test,y_pred))
    scoreings = np.asarray(scoreings)
    fscores = scoreings[:,0]
    gmean = scoreings[:,1]
    auc = scoreings[:,2]

    return ["LR",fscores.mean(),gmean.mean(),auc.mean()]

def gradient_boosting():
    kfold = model_selection.StratifiedKFold(n_splits=10, random_state=True)

    scoreings = []

    for train_index, test_index in kfold.split(X, y):
        # print("Train:", train_index, "Validation:", test_index)
        X_t, X_test = X[train_index], X[test_index]
        y_t, y_test = y[train_index], y[test_index]

        GSMOTE = EGSmote()
        X_train, y_train = GSMOTE.fit_resample(X_t, y_t)
        gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.01, max_depth=3)
        gbc.fit(X_train, y_train)

        # Predicting the Test set results
        y_predict = gbc.predict(X_test)
        y_pred = np.where(y_predict > 0.5, 1, 0)

        scoreings.append(evaluate2(y_test, y_pred))

    scoreings = np.asarray(scoreings)
    fscores = scoreings[:, 0]
    gmean = scoreings[:, 1]
    auc = scoreings[:, 2]

    return ["GBC", fscores.mean(), gmean.mean(), auc.mean()]


# def XGBoost():
#
#     # Fitting X-Gradient boosting
#     gbc = xgb.XGBClassifier(objective="binary:logistic", random_state=42)
#     gbc.fit(X_train, y_train)
#
#     # Predicting the Test set results
#     y_predict = gbc.predict(X_test)
#     y_pred = np.where(y_predict.astype(int) > 0.5, 1, 0)
#
#     return evaluate("XGBoost", y_test, y_pred)


def KNN():

    # Fitting Simple Linear Regression to the Training set

    kfold = model_selection.StratifiedKFold(n_splits=10, random_state=True)

    scoreings = []

    for train_index, test_index in kfold.split(X, y):
        # print("Train:", train_index, "Validation:", test_index)
        X_t, X_test = X[train_index], X[test_index]
        y_t, y_test = y[train_index], y[test_index]

        GSMOTE = EGSmote()
        X_train, y_train = GSMOTE.fit_resample(X_t, y_t)
        classifier = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
        classifier.fit(X_train, y_train)

        # Predicting the Test set results
        y_pred = classifier.predict(X_test)


        scoreings.append(evaluate2(y_test, y_pred))

    scoreings = np.asarray(scoreings)
    fscores = scoreings[:, 0]
    gmean = scoreings[:, 1]
    auc = scoreings[:, 2]

    return ["KNN", fscores.mean(), gmean.mean(), auc.mean()]


def decision_tree():

    kfold = model_selection.StratifiedKFold(n_splits=10, random_state=True)

    scoreings = []

    for train_index, test_index in kfold.split(X, y):
        # print("Train:", train_index, "Validation:", test_index)
        X_t, X_test = X[train_index], X[test_index]
        y_t, y_test = y[train_index], y[test_index]

        GSMOTE = EGSmote()
        X_train, y_train = GSMOTE.fit_resample(X_t, y_t)
        regressor = DecisionTreeRegressor()
        regressor.fit(X_train, y_train)

        # Predicting the Test set results
        y_predict = regressor.predict(X_test)
        y_pred = np.where(y_predict > 0.5, 1, 0)

        scoreings.append(evaluate2(y_test, y_pred))

    scoreings = np.asarray(scoreings)
    fscores = scoreings[:, 0]
    gmean = scoreings[:, 1]
    auc = scoreings[:, 2]

    return ["DT", fscores.mean(), gmean.mean(), auc.mean()]

for filename in os.listdir(path):

    # dataset
    date_file = path+filename.replace('\\', '/')

    # data transformation if necessary.
    X, y = pp.pre_process(date_file)

    X_t, X_test, y_t, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Visualize original data
    # vs(X_t, y_t, "Original data")

    # oversample
    print("---------------------------------------------------------")
    print("Dataset: " + filename)
    print("Oversampling in progress ...")
    # GSMOTE = GSMOTE = EGSmote()
    # X_train, y_train = GSMOTE.fit_resample(X_t, y_t)

    # For SMOTE
    # sm = EGSmote()
    # X_train, y_train = sm.fit_resample(X_t, y_t)


    # visualize oversampled data.
    print("Oversampling completed.")
    print("Plotting oversampled data...")

    # use this line of code to interpret oversampled data.
    # vs(X_train, y_train, "Oversampled ")

    print("Plotting completed")

    performance1 = logistic_training()
    performance2 = gradient_boosting()
    # performance3 = XGBoost()
    performance4 = KNN()
    performance5 = decision_tree()
    # performance7 = GaussianMixture_model()

    labels = ["Classifier", "f_score","g_mean", "auc_value"]

    values = [performance1, performance2, performance4, performance5]
    # values = [performance1]

    scores = pd.DataFrame(values, columns=labels)
    # scores.to_csv("../../output/scores_"+datetime.datetime.now().strftime("%Y-%m-%d__%H_%M_%S")+".csv")
    print(scores)

    # import applications.main as gsom
    # y_test, y_pred = gsom.run()
    # gsom.evaluate(y_test, y_pred)





