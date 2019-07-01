import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from genres import Genres
import random
import time
import csv

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
SONGS_CACHE_FILE_PATH = os.path.join(DATA_DIR, "songs.csv")
SPOTIFY_ACCESS_TOKEN = os.environ.get('SPOTIFY_ACCESS_TOKEN')
SPOTIFY_FEATURES_TO_SAVE = ['danceability', 'acousticness', 'valence', 'tempo', 'energy', 'time_signature', 'mode', 'loudness', 'key']
WATSON_IAM_API_KEY = os.environ.get('WATSON_IAM_API_KEY')

genres = Genres.IDS
sp = spotipy.Spotify(auth=SPOTIFY_ACCESS_TOKEN)
sp.trace = False

args = {
    'min_instrumentalness': 0.5,
    'limit': 100,
}

songs = {}
for i in range(0, len(genres)):
    args['seed_genres'] = genres[i: min(i+5, len(genres))]

    while True:
        results = sp.recommendations(**args)

        new_songs = {track['id']: {'spotify_song_id': track['id']} for track in results['tracks'] if not track['id'] in songs}
        if len(new_songs) == 0:
            break
        features_results = sp.audio_features(new_songs.keys())
        
        for feature in features_results:
            for key in SPOTIFY_FEATURES_TO_SAVE:
                new_songs[feature['id']][key] = feature.get(key)
        songs.update(new_songs)

songs = [song for _, song in songs.items()]
for i in range(0, len(songs)):
    songs[i]['id'] = i

keys = songs[0].keys()
with open(SONGS_CACHE_FILE_PATH, "w") as file:
    dict_writter = csv.DictWriter(file, keys)
    dict_writter.writeheader()
    dict_writter.writerows(songs) 