from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, Float
db = SQLAlchemy()

class SurveyResult(db.Model):
    __tablename__ = 'survey_result'
    id = Column(Integer, primary_key=True)
    text_id = Column(Text)
    spotify_id = Column(Text)
    anger = Column(Float)
    fear = Column(Float)
    sadness = Column(Float)
    joy = Column(Float)
    analytical = Column(Float)
    confident = Column(Float)
    tentative = Column(Float)
    daceability = Column(Float)
    acousticness = Column(Float) 
    valence = Column(Float)
    tempo = Column(Float)
    energy = Column(Float)
    time_signature = Column(Float)
    mode = Column(Float)
    loudness = Column(Float)
    key = Column(Float)
    
def FromWatsonAndSpotify(text_id, emotionsSet, spotifySongId, songFeatures):
    emotions = {}
    for emotion in emotionsSet.emotions:
        emotions[emotion['name']] = emotion['score']
    return SurveyResult(
        text_id = text_id,
        spotify_id = spotifySongId,
        anger = emotions.get('anger'),
        fear = emotions.get('fear'),
        sadness = emotions.get('sadness'),
        joy = emotions.get('joy'),
        analytical = emotions.get('analytical'),
        confident = emotions.get('confident'),
        tentative = emotions.get('tentative'),
        daceability = songFeatures.get('daceability'),
        acousticness = songFeatures.get('acousticness'),
        valence = songFeatures.get('valence'),
        tempo = songFeatures.get('tempo'),
        energy = songFeatures.get('energy'),
        time_signature = songFeatures.get('time_signature'),
        mode = songFeatures.get('mode'),
        loudness = songFeatures.get('loudness'),
        key = songFeatures.get('key'))