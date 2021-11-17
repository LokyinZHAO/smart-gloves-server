import librosa.beat
import librosa.display


def get_beats(y, sr=22050):
    """Get the beats information of a track

    @param y: audio time series
    @param sr: Sampling Rate
    @return: estimated beat event locations in frames units
    """
    tempo, track_beats_time = librosa.beat.beat_track(y=y, sr=sr, units='frames')
    # beats_track = []
    # for beat_time in track_beats_time:
    #     # 对前后0.1s的数据进行平均
    #     beats_track.append(np.abs(y[int((beat_time - 0.1) * sr):int((beat_time + 0.1) * sr)]).mean())
    # beats_track = np.array(beats_track)
    # scaled_beats_track = [(i - beats_track.min()) / (beats_track.max() - beats_track.min()) for i in beats_track]
    # print(np.mean(scaled_beats_track))
    # return track_beats_time, scaled_beats_track, np.mean(scaled_beats_track)
    return track_beats_time
