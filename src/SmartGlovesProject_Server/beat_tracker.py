import librosa.beat
import librosa.display
import numpy as np


class BeatTracker:
    """
    Detect the beats of the music
    Delegate librosa.beat
    """

    def __init__(self):
        pass

    @staticmethod
    def get_beats(music_src, offset=0.0, duration=None, sr=22050):
        """Get the beats information of a track

        @param music_src: music source file path
        @param offset: Sampling start time
        @param duration: Sampling duration
        @param sr: Sampling Rate
        @return: estimated beat event locations in time units, scaled beats strength, mean of strength
        """
        # set sampling rate to 
        y, sr = librosa.load(music_src, offset=offset, duration=duration, sr=sr)
        # convert amplitude to decibels
        # y_db = librosa.amplitude_to_db(abs(y))
        # tempo, track_beats_time = librosa.beat.beat_track(y=y, sr=sr, units="time")
        tempo, track_beats_time = librosa.beat.beat_track(y=y, sr=sr, units='time')
        beats_track = []
        for beat_time in track_beats_time:
            # 对前后0.1s的数据进行平均
            beats_track.append(np.abs(y[int((beat_time - 0.1) * sr):int((beat_time + 0.1) * sr)]).mean())
        beats_track = np.array(beats_track)
        scaled_beats_track = [(i - beats_track.min()) / (beats_track.max() - beats_track.min()) for i in beats_track]
        print(np.mean(scaled_beats_track))
        return track_beats_time, scaled_beats_track, np.mean(scaled_beats_track)
