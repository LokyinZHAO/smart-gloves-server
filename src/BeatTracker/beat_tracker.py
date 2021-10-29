import librosa.beat


class BeatTracker:
    """
    Detect the beats of the music
    Delegate librosa.beat
    """

    def __init__(self):
        pass

    @staticmethod
    def get_beats(music_src):
        """Get the beats information of a track

        @param music_src: music source file path
        @return: estimated beat event locations in time units
        """
        y, sr = librosa.load(music_src)
        tempo, track_beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
        return track_beats

