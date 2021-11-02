class MusicInfo:
    def __init__(self, name, mood, prob, beats, strength, mean):
        """store music information for serialization

        @param name: music_name
        @param mood: music mood
        @param prob: probability of each mood
        @param beats: beats time
        @param strength: music beat intensity, normalized to [0, 1]
        @param mean: average beat intensity
        """
        self.music_name = name
        self.mood = mood
        self.prob = prob
        self.beats = beats
        self.strength = strength
        self.mean = mean
