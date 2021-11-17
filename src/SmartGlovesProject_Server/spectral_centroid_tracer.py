import librosa
from sklearn.preprocessing import minmax_scale


def trace_spec_cent(y, sr=22050):
    """get the centroid of spectrogram

    @param y: y of wav load
    @param sr: sampling rate
    @return: the centroid of spectrogram, by frame
    """
    spectral_centroids = librosa.feature.spectral_centroid(y, sr=sr)[0]
    return minmax_scale(spectral_centroids)
