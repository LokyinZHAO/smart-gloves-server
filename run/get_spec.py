import os

import pandas as pd

from SmartGlovesProject_Server.Data_Prepare.spotify_utils import get_all_songs_from_df
from SmartGlovesProject_Server.Data_Prepare.audio_to_spectrogram import Audio2Spectrogram

if __name__ == '__main__':
    df_train = pd.read_csv("./resources/train.csv")
    mood = ["Angry", "Happy", "Relaxed", "Sad"]

    for item in mood:
        sub_df = df_train[df_train.mood_cat == item].reset_index(drop=True)
        dest_dir = "./resources/mp3/" + item + "/"
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)
        get_all_songs_from_df(sub_df, dest_dir=dest_dir)

    au_2_wav_spec = Audio2Spectrogram()
    for item in mood:
        mp3_dir = "./resources/mp3/" + item + "/"
        wav_dest_dir = "./resources/wav/" + item + "/"
        if not os.path.exists(wav_dest_dir):
            os.mkdir(wav_dest_dir)
        spec_dest_dir = "./resources/spectrogram/" + item + "/"
        if not os.path.exists(spec_dest_dir):
            os.mkdir(spec_dest_dir)
        au_2_wav_spec.batch_processing(src_dir=mp3_dir, wav_dest_dir=wav_dest_dir, spec_dest_dir=spec_dest_dir,
                                       status=True)
