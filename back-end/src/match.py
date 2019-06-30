def NaiveMatch(emotionSet):
    emotion_keys = emotionSet.get_names()
    args = {}
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
    return args