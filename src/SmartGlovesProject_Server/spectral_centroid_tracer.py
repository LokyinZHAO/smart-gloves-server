import librosa
import numpy
from sklearn.preprocessing import minmax_scale


def trace_spec_cent(y, sr=22050):
    """get the centroid of spectrogram

    Argument:
        - y: y of wav load
        - sr: sampling rate
    Return:
        the centroid of spectrogram, by frame
    """
    spectral_centroids = librosa.feature.spectral_centroid(y, sr=sr, center=False)[0]
    spec_cent_min_max = minmax_scale(spectral_centroids, feature_range=(-1, 1))
    return spec_cent_min_max
