import librosa
from SmartGlovesProject_Server.Data_Prepare.audio_to_spectrogram import wav_to_spectrogram
from SmartGlovesProject_Server.beat_tracker import get_beats
from SmartGlovesProject_Server.mood_predictor import Predictor
from SmartGlovesProject_Server.short_time_fourier_trans import fourier_trans
from SmartGlovesProject_Server.spectral_centroid_tracer import trace_spec_cent
from music_info import MusicInfo


def process(src_path: str):
    """Process the given music file，return MusicInfo
    @param src_path:the file to process, .wav expected
    @return: Music Info
    """
    # predict mood
    pred = Predictor("./resources/Resnet_SGD_valscore_60.pt")
    spec_file = src_path.replace(".wav", ".jpg")
    wav_to_spectrogram(src=src_path, dest=spec_file)
    mood_dict = pred.predict(spec_file, k=4)

    # get music sampling
    y, sr = librosa.load(src_path)
    # get beat time
    beat_time = get_beats(y, sr)
    # get stft
    fourier_trans_y_db = fourier_trans(y, sr)
    # get spectral centroid
    spec_cent = trace_spec_cent(y, sr)

    # generate Music Info
    music_info = MusicInfo()
    music_info.__setattr__("name", src_path.split('/')[-1].replace(".wav", ""))
    music_info.__setattr__("mood", mood_dict)
    music_info.__setattr__("beat frame", beat_time)
    music_info.__setattr__("fourier trans db", fourier_trans_y_db)
    music_info.__setattr__("spectrogram centroid", spec_cent)

    return music_info


if __name__ == '__main__':
    '''
    @version 3.1
    '''
    music = process("./resources/wav/Angry/TRRRULH128F92CDB2E.wav")
    print(music)
