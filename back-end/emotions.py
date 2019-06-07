class EmotionSet:
    def __init__(self, raw_emotions):
        self.emotions = []

        if 'tones' in raw_emotions['document_tone']:
            for tone in raw_emotions['document_tone']['tones']:
                self.emotions.append({
                    'name': tone['tone_id'],
                    'score': tone['score'],
                })

        print (self.emotions)