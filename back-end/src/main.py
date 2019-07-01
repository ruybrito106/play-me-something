from ibm_watson import ToneAnalyzerV3, ApiException
import json
import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from emotions import EmotionSet
from song import FindClosestSong
from survey_result import db, SurveyResult, FromWatsonAndSpotify
from cache import FromCsvFilePath
from match import NaiveMatch

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
SONGS_CACHE_FILE_PATH = os.path.join(DATA_DIR, "songs.csv")
TEXTS_CACHE_FILE_PATH = os.path.join(DATA_DIR, "texts.csv")

POSTGRES_URI = os.environ.get('POSTGRES_URI')
WATSON_IAM_APIKEY = os.environ.get('WATSON_IAM_APIKEY')

app = Flask(__name__)
CORS(app)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class Emotions(Resource):
    def __init__(self):
        self.tone_analyzer = ToneAnalyzerV3(
            version='2017-09-21',
            iam_apikey=WATSON_IAM_APIKEY,
            url='https://gateway.watsonplatform.net/tone-analyzer/api'
        )
        self.songs_cache = FromCsvFilePath(SONGS_CACHE_FILE_PATH, idColumn='spotify_song_id')

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("text")
            args = parser.parse_args()

            response = self.tone_analyzer.tone(tone_input=args["text"])
            emotion_set = EmotionSet(response.get_result())
            matched_features = NaiveMatch(emotion_set)
            best_song = FindClosestSong(self.songs_cache.songs_list, matched_features)

            return {"track": best_song['spotify_song_id']}, 200 
        except ApiException as ex:
            print ("Method failed with status code " + str(ex.code) + ": " + ex.message)
            return "Bad request", 400

class Survey(Resource):
    def __init__(self):
        self.tone_analyzer = ToneAnalyzerV3(
            version='2017-09-21',
            iam_apikey=WATSON_IAM_APIKEY,
            url='https://gateway.watsonplatform.net/tone-analyzer/api'
        )
        self.db = db
        self.texts_cache = FromCsvFilePath(TEXTS_CACHE_FILE_PATH)
        self.songs_cache = FromCsvFilePath(SONGS_CACHE_FILE_PATH, idColumn='spotify_song_id')
    
    def get(self):
        random_text = self.texts_cache.get_sample_values()[0]
        random_songs = self.songs_cache.get_sample_values(5)
        random_song_ids = [song['spotify_song_id'] for song in random_songs]
        return {'text_id': random_text['id'], 'text': random_text['text'], 'spotify_song_ids': random_song_ids}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text_id")
        parser.add_argument("spotify_song_id")
        args = parser.parse_args()

        text = self.texts_cache.get_by_id(args["text_id"])['text']
        response = self.tone_analyzer.tone(tone_input=text)
        emotion_set = EmotionSet(response.get_result())

        song_features = self.songs_cache.get_by_id(args['spotify_song_id'])

        survey_result = FromWatsonAndSpotify(args['text_id'], emotion_set, args['spotify_song_id'], song_features)

        self.db.session.add(survey_result)
        self.db.session.commit()

        return '', 200

api.add_resource(Emotions, "/analyze")
api.add_resource(Survey, "/survey")
app.run(debug=True)