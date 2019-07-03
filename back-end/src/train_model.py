import os
import math

from joblib import dump, load

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeRegressor

from sqlalchemy import create_engine

POSTGRES_URI = os.environ.get('POSTGRES_URI')
db = create_engine(POSTGRES_URI)

def dump_pg_to_csv(path='../data/survey_result.csv'):
    result_set = db.execute("SELECT * FROM survey_result")
    csv = {
        'anger': [],
        'fear': [],
        'sadness': [],
        'joy': [],
        'analytical': [],
        'confident': [],
        'tentative': [],
        'danceability': [],
        'acousticness': [],
        'valence': [],
        'tempo': [],
        'energy': [],
        'time_signature': [],
        'mode': [],
        'loudness': [],
        'key': [],
    }

    for result in result_set:
        csv['anger'].append(result[3] or 0.0)
        csv['fear'].append(result[4] or 0.0)
        csv['sadness'].append(result[5] or 0.0)
        csv['joy'].append(result[6] or 0.0)
        csv['analytical'].append(result[7] or 0.0)
        csv['confident'].append(result[8] or 0.0)
        csv['tentative'].append(result[9] or 0.0)
        csv['danceability'].append(result[10] or 0.0)
        csv['acousticness'].append(result[11] or 0.0)
        csv['valence'].append(result[12] or 0.0)
        csv['tempo'].append(result[13] or 0.0)
        csv['energy'].append(result[14] or 0.0)
        csv['time_signature'].append(result[15] or 0.0)
        csv['mode'].append(result[16] or 0.0)
        csv['loudness'].append(result[17] or 0.0)
        csv['key'].append(result[18] or 0.0)

    pd.DataFrame(csv).to_csv(
        path, 
        sep='\t', 
        header=True,
        columns=['anger', 'fear', 'joy', 'analytical', 'confident', 'tentative', 'danceability', 'acousticness', 'valence', 'tempo', 'energy', 'time_signature', 'mode', 'loudness', 'key']
    )

def scale_data(pred, label):
    scaler = MinMaxScaler()
    scaler.fit(label)
    label = scaler.transform(label)
    
    scaler.fit(pred)
    pred = scaler.transform(pred)

    return pred, label

def evaluate_model(pred, label):
    if len(pred) == 0:
        raise ValueError("Pred cannot be empty")

    errors = list()
    
    sz = len(pred[0])
    for i in range(sz):
        xs, ys = [x[i] for x in pred], [y[i] for y in label]
        errors.append(mean_squared_error(xs, ys))
    
    return map(lambda x : round(x, 3), errors)

def metrics(arr):
    s = sum(arr)
    l = len(arr)  
    mean = s / l

    sq_sum = sum([(x - mean) * (x - mean) for x in arr])
    stdev = math.sqrt(sq_sum / l)

    return (round(mean, 3), round(stdev, 3))

def linear_regression(X_train, y_train, X_test, y_test):
    errors = []
    
    for _ in range(50):
        clf = LinearRegression()
        clf.fit(X_train, y_train)

        dump(clf, '../model/linear_regression.joblib')

        pred = clf.predict(X_test)
        pred, label = scale_data(pd.DataFrame(pred), y_test)
        
        err = evaluate_model(pred, label)
        errors += [err]

    print ([metrics(x) for x in zip(*errors)])

def lasso(X_train, y_train, X_test, y_test):
    errors = []
    
    for _ in range(50):
        clf = Lasso()
        clf.fit(X_train, y_train)

        dump(clf, '../model/lasso.joblib')

        pred = clf.predict(X_test)
        pred, label = scale_data(pd.DataFrame(pred), y_test)
        
        err = evaluate_model(pred, label)
        errors += [err]

    print ([metrics(x) for x in zip(*errors)])

def random_forest(X_train, y_train, X_test, y_test):
    errors = []
    
    for _ in range(50):
        clf = RandomForestRegressor()
        clf.fit(X_train, y_train)

        dump(clf, '../model/random_forest.joblib')

        pred = clf.predict(X_test)
        pred, label = scale_data(pd.DataFrame(pred), y_test)
        
        err = evaluate_model(pred, label)
        errors += [err]

    print ([metrics(x) for x in zip(*errors)])

def extra_trees(X_train, y_train, X_test, y_test):
    errors = []
    
    for _ in range(50):
        clf = ExtraTreesRegressor()
        clf.fit(X_train, y_train)

        dump(clf, '../model/extra_trees.joblib')

        pred = clf.predict(X_test)
        pred, label = scale_data(pd.DataFrame(pred), y_test)
        
        err = evaluate_model(pred, label)
        errors += [err]

    print ([metrics(x) for x in zip(*errors)])

def decision_tree(X_train, y_train, X_test, y_test):
    errors = []
    
    for _ in range(50):
        clf = DecisionTreeRegressor()
        clf.fit(X_train, y_train)

        dump(clf, '../model/decision_tree.joblib')

        pred = clf.predict(X_test)
        pred, label = scale_data(pd.DataFrame(pred), y_test)
        
        err = evaluate_model(pred, label)
        errors += [err]

    print ([metrics(x) for x in zip(*errors)])

def train_model():
    data = pd.read_csv('../data/survey_result.csv', sep='\t', index_col=0)

    X, y = data.iloc[:, :-9], data.iloc[:, 6:]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=200)

    linear_regression(X_train, y_train, X_test, y_test) 
    lasso(X_train, y_train, X_test, y_test)
    random_forest(X_train, y_train, X_test, y_test)
    extra_trees(X_train, y_train, X_test, y_test)
    decision_tree(X_train, y_train, X_test, y_test)

    # danceability => ET
    # accousticness => ET
    # valence => ET
    # tempo => ET
    # energy => ET
    # time_signature => ET
    # mode => RF
    # loudness => ET
    # key => RF

dump_pg_to_csv()
# train_model()
