class MusicInfo:
    """
    Information of Music,Generally contains the following attributes:
        name: music_name
        mood: music mood
        prob: probability of each mood
        beats: beats time
        strength: music beat intensity, normalized to [0, 1]
        mean: average beat intensity

    """

    def __init__(self):
        """store music information for serialization
        """

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __str__(self):
        to_str = "=======================\n"
        for atrr in self.__dict__:
            to_str += f'{atrr.__str__()} : {self.__dict__[atrr]}\n'
        to_str += "=======================\n"
        return to_str
