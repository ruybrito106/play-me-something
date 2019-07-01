import os
import pickle

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

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

def train_model():
    data = pd.read_csv('../data/survey_result.csv', sep='\t', index_col=0)

    X, y = data.iloc[:, :-9], data.iloc[:, 7:]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=200)

    clf = LinearRegression()
    clf.fit(X_train, y_train)

    pickle.dump(clf, open('../model/linear_regression.pkl', 'wb'))

    pred = clf.predict(X_test)
    for i in range(len(y_test)):
        print ('Sample: ', map(lambda x : round(x, 3), list(y_test.iloc[i, :])))
        print ('Pred:   ', map(lambda x : round(x, 3), pred[i]))
        print ()

dump_pg_to_csv()
train_model()
