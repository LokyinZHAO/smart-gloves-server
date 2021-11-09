import librosa
import librosa.display
import numpy as np
from matplotlib import pyplot as plt


class STFTer:
    """
    Short Time Fourier Transformer
    """

    @staticmethod
    def fourier_trans(src_file, offset=0.0, duration=None, sr=22050):
        """ Perform fast Fourier transform on the input music file

        @param src_file: input file
        @param offset: Sampling start time
        @param duration: Sampling duration
        @param sr: Sampling Rate
        @return: Fourier transform result, and the duration of each frame.
                - The result of the transformation is a two-dimensional matrix,
                and each element represents the amplitude information (in decibels) at a certain frequency.
                - The rows of the two-dimensional array represent frequencies, and the columns represent frame sequences.
                Frame duration represents the time length of each frame (in second)
        """
        y, sr = librosa.load(src_file, sr=sr, offset=offset, duration=duration)
        fourier_trans_y = librosa.stft(y)
        fourier_trans_y_db = librosa.amplitude_to_db(np.abs(fourier_trans_y))
        time_per_frame = duration/fourier_trans_y_db.shape[1]
        # debug
        # plt.figure(figsize=(14, 5))
        # librosa.display.specshow(fourier_trans_y_db, sr=sr, x_axis='time', y_axis='hz')
        # plt.colorbar()
        # plt.show()
        # debug
        return fourier_trans_y_db,time_per_frame
