import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from genres import Genres
import random
import time
import math

def FindClosestSong(songs, features):
    keys = features.keys()
    best_song = None
    for song in songs:
        distance = 0.0
        for key in keys:
            if key in song:
                distance += (song[key] - features[key]) * (song[key] - features[key])
        # print(features, song, distance)
        if best_song is None or distance < best_distance:
            best_song = song
            best_distance = distance
    return best_song