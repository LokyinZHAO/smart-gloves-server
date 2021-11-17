import librosa
from SmartGlovesProject_Server.Data_Prepare.audio_to_spectrogram import wav_to_spectrogram
from SmartGlovesProject_Server.beat_tracker import get_beats
from SmartGlovesProject_Server.mood_predictor import Predictor
from SmartGlovesProject_Server.short_time_fourier_trans import fourier_trans
from SmartGlovesProject_Server.spectral_centroid_tracer import trace_spec_cent
from SmartGlovesProject_Server.framer import to_frames
from music_info import MusicInfo
import SmartGlovesProject_Server.Util.frame_selector as frame_selector


def process(src_path: str):
    """Process the given music file，return MusicInfo
    Arguments:
        src_path:the file to process, .wav expected
    Return:
         Music Info
    """
    # predict mood
    pred = Predictor("./resources/Resnet_SGD_valscore_60.pt")
    spec_file = src_path.replace(".wav", ".jpg")
    wav_to_spectrogram(src=src_path, dest=spec_file)
    mood_dict, max_mood = pred.predict(spec_file, k=4)
    color_dict = {
        "angry": 0,
        "sad": 1,
        "happy": 2,
        "relaxed": 3
    }

    color_num = color_dict[max_mood]

    # get music sampling
    y, sr = librosa.load(src_path)
    # get stft
    fourier_trans_y_db = fourier_trans(y, sr)
    fourier_selection_5 = frame_selector.select_frame_5(fourier_trans_y_db)
    fourier_selection_8 = frame_selector.select_frame_8(fourier_trans_y_db)

    # framing
    frames_mean, time_per_frame = to_frames(y, sr=sr)

    # get beat frames
    beat_time = get_beats(y, sr)
    # get spectral centroid
    spec_cent = trace_spec_cent(y, sr)

    # generate Music Info
    music_info = MusicInfo()
    music_info.__setattr__("name", src_path.split('/')[-1].replace(".wav", ""))
    music_info.__setattr__("mood", mood_dict)
    music_info.__setattr__("color num", color_num)
    music_info.__setattr__("fourier trans db", fourier_trans_y_db)
    music_info.__setattr__("fourier trans 5", fourier_selection_5)
    music_info.__setattr__("fourier trans 8", fourier_selection_8)
    music_info.__setattr__("frames", frames_mean)
    music_info.__setattr__("time per frame", time_per_frame)
    music_info.__setattr__("beat frame", beat_time)
    music_info.__setattr__("spectrogram centroid", spec_cent)

    return music_info


if __name__ == '__main__':
    '''
    @version 2.1
    '''
    music = process("./resources/wav/Angry/TRRRULH128F92CDB2E.wav")
    print(music)
