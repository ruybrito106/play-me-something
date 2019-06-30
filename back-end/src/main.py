from ibm_watson import ToneAnalyzerV3, ApiException
import json
import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from emotions import EmotionSet
from song import SongResolver, SongFeaturesResolver
from survey_result import db, SurveyResult, FromWatsonAndSpotify

app = Flask(__name__)
CORS(app)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class Emotions(Resource):
    def __init__(self):
        self.tone_analyzer = ToneAnalyzerV3(
            version='2017-09-21',
            iam_apikey='X1D_Di5vyhWuafHHF-QnCaRgT0pLUP4PQaCNgy1PiE6m',
            url='https://gateway.watsonplatform.net/tone-analyzer/api'
        )

    def post(self, accessToken):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("text")
            args = parser.parse_args()
            print(args)

            response = self.tone_analyzer.tone(tone_input=args["text"])
            
            emotion_set = EmotionSet(response.get_result())
            resolver = SongResolver(accessToken, emotion_set)

            return resolver.resolve(), 200 
        except ApiException as ex:
            print ("Method failed with status code " + str(ex.code) + ": " + ex.message)
            return "Bad request", 400

class Survey(Resource):
    def __init__(self):
        self.tone_analyzer = ToneAnalyzerV3(
            version='2017-09-21',
            iam_apikey='X1D_Di5vyhWuafHHF-QnCaRgT0pLUP4PQaCNgy1PiE6m',
            url='https://gateway.watsonplatform.net/tone-analyzer/api'
        )
        self.db = db

    def post(self, accessToken):
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        parser.add_argument("spotify_song_id")
        args = parser.parse_args()

        response = self.tone_analyzer.tone(tone_input=args["text"])
        emotion_set = EmotionSet(response.get_result())

        song_features_resolver = SongFeaturesResolver(args["spotify_song_id"], accessToken)
        song_features = song_features_resolver.resolve()

        survey_result = FromWatsonAndSpotify(args['text'], emotion_set, args['spotify_song_id'], song_features)

        self.db.session.add(survey_result)
        self.db.session.commit()

        return None, 200

        


api.add_resource(Emotions, "/analyze/<string:accessToken>")
api.add_resource(Survey, "/survey/<string:accessToken>")
app.run(debug=True)