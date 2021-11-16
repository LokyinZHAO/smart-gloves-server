import os

import pandas as pd
import time
import sys

from SmartGlovesProject_Server.Data_Prepare.audio_to_spectrogram import Audio2Spectrogram

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: [mood]")
    df_train = pd.read_csv("./resources/train.csv")

    au_2_wav_spec = Audio2Spectrogram()
    item = sys.argv[1]

    start_time = time.time()
    mp3_dir = "./resources/mp3/" + item + "/"
    wav_dest_dir = "./resources/wav/" + item + "/"
    if not os.path.exists(wav_dest_dir):
        os.mkdir(wav_dest_dir)
    spec_dest_dir = "./resources/spectrogram/" + item + "/"
    if not os.path.exists(spec_dest_dir):
        os.mkdir(spec_dest_dir)
    cnt = au_2_wav_spec.batch_processing(src_dir=mp3_dir, wav_dest_dir=wav_dest_dir, spec_dest_dir=spec_dest_dir)
    end_time = time.time()
    print(f"processing: wav to mel spectrogram")
    print(f"item num: {cnt}")
    print(f"time consumed: {(end_time-start_time)//3600}H {((end_time-start_time)%3600)//60}M {(end_time-start_time)%60}S")
