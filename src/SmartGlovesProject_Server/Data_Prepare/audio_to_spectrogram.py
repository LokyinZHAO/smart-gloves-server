import glob
import os

from tqdm import tqdm
from pydub import AudioSegment
import librosa
import librosa.display
import matplotlib.pyplot as plt
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

    @staticmethod
    def batch_processing(src_dir: str, wav_dest_dir: str, spec_dest_dir: str, status: bool, keep_wav: bool = True):
        """
        Convert all mp3 files in a folder into wav and spectrogram
        @param src_dir: mp3 files dir
        @param wav_dest_dir: wav files dir
        @param spec_dest_dir: spectrogram files dir
        @param status: whether to show the current progress
        @param keep_wav: whether to keep wav file
        @return: total item number
        """
        files = glob.glob(src_dir + "*.mp3", recursive=True)
        spec = Audio2Spectrogram()
        # Check if directory is already created
        if not os.path.exists(wav_dest_dir):
            os.mkdir(wav_dest_dir)
        if not os.path.exists(spec_dest_dir):
            os.mkdir(spec_dest_dir)
        cnt = 0
        if status:
            for file in tqdm(files):
                track_id = file.split("/")[-1]
                dest_wav = wav_dest_dir + track_id.replace("mp3", "wav")
                dest_jpg = spec_dest_dir + track_id.replace("mp3", "jpg")
                spec.audio_to_wav(src=file, dest=dest_wav)
                spec.wav_to_spectrogram(src=dest_wav, dest=dest_jpg)
                if not keep_wav:
                    os.remove(dest_wav)
                cnt += 1
        else:
            for file in files:
                track_id = file.split("/")[-1]
                dest_wav = wav_dest_dir + track_id.replace("mp3", "wav")
                dest_jpg = spec_dest_dir + track_id.replace("mp3", "jpg")
                spec.audio_to_wav(src=file, dest=dest_wav)
                spec.wav_to_spectrogram(src=dest_wav, dest=dest_jpg)
                if not keep_wav:
                    os.remove(dest_wav)
                cnt += 1
        return cnt
