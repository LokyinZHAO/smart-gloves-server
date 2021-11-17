import librosa
import librosa.display
import numpy as np
from matplotlib import pyplot as plt


def fourier_trans(y, sr=22050):
    """ Perform fast Fourier transform on the input music file

    Arguments：
        - y: audio time series
        - sr: Sampling Rate
    Return:
        Fourier transform result. The result of the transformation is a two-dimensional matrix,
        and each element represents the amplitude information (in decibels) at a certain frequency.
    """
    fourier_trans_y = librosa.stft(y, center=False)
    fourier_trans_y_db = librosa.amplitude_to_db(np.abs(fourier_trans_y))
    # debug
    # plt.figure(figsize=(14, 5))
    # librosa.display.specshow(fourier_trans_y_db, sr=sr, x_axis='time', y_axis='hz')
    # plt.colorbar()
    # plt.show()
    # debug
    return fourier_trans_y_db
