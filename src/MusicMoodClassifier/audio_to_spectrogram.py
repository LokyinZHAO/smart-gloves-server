from pydub import AudioSegment
import librosa
import librosa.display
import matplotlib.pyplot as plt
import pylab
import numpy as np


class Audio2Spectrogram:
    """
    Convert the sound signal of music into a spectrogram
    """

    def __init__(self):
        pass

    @staticmethod
    def audio_to_wav(src, dest):
        """Convert the mp3 audio file into wav format.

        Args:
            src: the source file to be converted, mp3 format expected.
            dest: the target wav file to be created.

        Returns:None

        """
        audio = AudioSegment.from_mp3(src)
        audio.export(dest, format='wav')

    @staticmethod
    def wav_to_spectrogram(src, dest):
        """Convert wav audio to spectrogram file

        Args:
            src:the source file to be converted, wav format expected.
            dest:the target spectrogram to be created, in jpg format.

        Returns: None

        """
        y, sr = librosa.load(src)
        S = librosa.feature.melspectrogram(y=y, sr=sr)

        x_pixels = 384
        y_pixels = 128
        plt.figure(figsize=(x_pixels / 100, y_pixels / 100))
        plt.axis('off')
        # add an axes
        plt.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])

        librosa.display.specshow(librosa.power_to_db(S, ref=np.max), y_axis='mel', x_axis='time')

        plt.savefig(dest, bbox_inches=None, pad_inches=0, dpi=100)
        plt.close()
        plt.show()
