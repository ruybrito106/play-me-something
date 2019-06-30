class EmotionSet:
    def __init__(self, raw_emotions):
        self.emotions = []
        
        if 'tones' in raw_emotions['document_tone']:
            for tone in raw_emotions['document_tone']['tones']:
                self.emotions.append({
                    'name': str(tone['tone_id']),
                    'score': tone['score'],
                })

    def get_names(self):
        return map((lambda x : x['name']), self.emotions)