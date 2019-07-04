import math

import pandas as pd

from joblib import load

from sklearn.preprocessing import MinMaxScaler

class SongsMatcher:
    ALL_COLS = ['danceability', 'acousticness', 'valence', 'tempo', 'energy', 'time_signature', 'mode', 'loudness', 'key']
    COLS = ['danceability', 'acousticness', 'valence', 'tempo', 'energy', 'time_signature', 'loudness']
    EMOTIONS = ['anger', 'fear', 'sadness', 'joy', 'analytical', 'confident', 'tentative']

    def __init__(self, path):
        self.data = pd.read_csv(path, sep=',')
        self.scaler = MinMaxScaler()
        
        self.data[self.ALL_COLS] = self.scaler.fit_transform(self.data[self.ALL_COLS])
        self.clf = load('../model/linear_regression.joblib')

    @staticmethod
    def distance(row, attrs):
        cols = SongsMatcher.COLS
        return math.sqrt(sum([pow(attrs[index] - row[cols[index]], 2) for index in range(len(cols))]))

    def find_closest_to_emotions(self, emotionsSet):
        es = {}
        for e in emotionsSet.emotions:
            es[e['name']] = e['score']
        
        attrs = self.clf.predict([[es[x] if x in es else 0.0 for x in self.EMOTIONS]])
        attrs = self.scaler.transform(attrs)
        attrs = list(attrs[0])

        spotify_attrs = attrs[0:6] + [attrs[7]]
        
        best = (None, 10000.0)
        for _, row in self.data.iterrows():
            d = self.distance(row, spotify_attrs)
            if best[0] is None or d < best[1]:
                best = (row['spotify_song_id'], d)
                # print ([row[x] for x in self.COLS])

        # print (map(lambda x : round(x, 3), spotify_attrs))
        return best[0]