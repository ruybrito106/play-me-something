import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from genres import Genres
import random
import time

class SongResolver:
    def __init__(self, accessToken, emotions=None):
        self.emotions = emotions

        token = accessToken
        if "=" in token:
            _, token = token.split("=", 1)

        self.sp = spotipy.Spotify(auth=token)
        self.sp.trace=False
    
    def resolve(self):
        # watson results = (emotional_tons ++ language_tons)
        # emotional_tons = [anger, fear, sadness, joy]
        # language_tons = [analytical, confident, tentative]
        # 0.5 <= score <= 1.0
        #
        # spotify
        # https://developer.spotify.com/documentation/web-api/reference/browse/get-recommendations/
        #
        # v0: adhoc mapping
        # anger = low valence, low tempo
        # fear = low valence, high tempo, high energy
        # sadness = low valence, low energy
        # joy = high valence

        emotion_keys = self.emotions.get_names()

        args = {
            'seed_artists': ['2VZNmg4vCnew4Pavo8zDdW', '0YC192cP3KPCRWx8zr8MfZ', '1nIUhcKHnK6iyumRyoV68C', '71jzN72g8qWMCMkWC5p1Z0', '3PhL2Vdao2v8SS8AptuhAr'],
            'target_acousticness': 0.9,
            'target_instrumentalness': 0.9,
            'limit': 1,
        }
        
        # divino implementar aq
        if 'joy' in emotion_keys:
            args['min_valence'] = 0.5
        elif 'anger' in emotion_keys:
            args['max_valence'] = 0.7
            args['max_tempo'] = 0.7
        elif 'fear' in emotion_keys:
            args['max_valence'] = 0.7
            args['min_tempo'] = 0.5
            args['min_energy'] = 0.5
        elif 'sadness' in emotion_keys:
            args['max_valence'] = 0.7
            args['max_energy'] = 0.7

        results = self.sp.recommendations(**args)
        track_id = ""

        if len(results['tracks']) > 0:
            track_id = results['tracks'][0]['id']

        return {
            "track": track_id,
        }

    def set_data(self):
        genres = Genres.IDS

        args = {
            'min_instrumentalness': 0.5,
            'limit': 100,
        }

        songs = {}
        while len(songs) < 1000:
            random.shuffle(genres)
            args['seed_genres'] = genres[:5]
            results = self.sp.recommendations(**args)

            for result in results['tracks']:
                songs[result['id']] = ''
            
            time.sleep(1)
        
        pd.DataFrame({'ID': songs.keys()}).to_csv('data/songs.csv')

