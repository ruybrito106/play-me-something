from ibm_watson import ToneAnalyzerV3, ApiException
import json

from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from emotions import EmotionSet
from song import SongResolver

app = Flask(__name__)
CORS(app)

api = Api(app)

class Emotions(Resource):
    def __init__(self):
        self.tone_analyzer = ToneAnalyzerV3(
            version='2017-09-21',
            iam_apikey='{{API_KEY}}',
            url='https://gateway.watsonplatform.net/tone-analyzer/api'
        )

    def post(self, accessToken):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("text")
            args = parser.parse_args()

            response = self.tone_analyzer.tone(tone_input=args["text"])
            
            emotion_set = EmotionSet(response.get_result())
            resolver = SongResolver(emotion_set)

            return resolver.resolve(), 200 
        except ApiException as ex:
            print ("Method failed with status code " + str(ex.code) + ": " + ex.message)
            return "Bad request", 400

api.add_resource(Emotions, "/analyze/<string:accessToken>")
app.run(debug=True)