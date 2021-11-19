class MusicInfo:
    """
    Information of Music,Generally contains the following attributes:
    Fields:
        name: music_name
        mood: music mood dict. Key is mood among {'angry','happy','sad','relaxed'},
            and the value is the probability of each mood
        color num: color number.{Red, Blue, Yellow, Green} corresponds to 0 to 3
        frames: the result of framing the audio
        time per frame: time per frame, in seconds
        fourier trans db: the fourier trans results, axis 0 is frames, axis 1 is frequency, value is the amplitude
        fourier trans 5: pick 5 representative frequencies on average from the frequencies
        fourier trans 8: pick 8 representative frequencies on average from the frequencies
        beats frame beats frames
        spectrogram centroid: The center of the spectrum represents the "center of mass" of the sound, and is also
            called the first order distance of the spectrum. The smaller the value of the center of the spectrum,
            the more spectrum energy is concentrated in the low frequency range.

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
