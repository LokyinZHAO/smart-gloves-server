import multiprocessing
import os

import time
import sys

from SmartGlovesProject_Server.Data_Prepare.audio_to_spectrogram import Audio2Spectrogram


# 子进程要执行的代码
def run_proc(item):
    if len(sys.argv) != 2:
        print("usage: [mood]")

    au_2_wav_spec = Audio2Spectrogram()

    start_time = time.time()
    mp3_dir = "./resources/mp3/" + item + "/"
    wav_dest_dir = "./resources/wav/" + item + "/"
    if not os.path.exists(wav_dest_dir):
        os.mkdir(wav_dest_dir)
    spec_dest_dir = "./resources/spectrogram/" + item + "/"
    if not os.path.exists(spec_dest_dir):
        os.mkdir(spec_dest_dir)
    cnt = au_2_wav_spec.batch_processing(src_dir=mp3_dir,
                                         wav_dest_dir=wav_dest_dir,
                                         spec_dest_dir=spec_dest_dir,
                                         status=False)
    end_time = time.time()
    delta = end_time - start_time
    ret_dic = {
        "time_consume": delta,
        "items": cnt
    }
    return ret_dic


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)
    results = [pool.apply_async(run_proc, ("Happy",)), pool.apply_async(run_proc, ("Sad",)),
               pool.apply_async(run_proc, ("Angry",)), pool.apply_async(run_proc, ("Relaxed",))]
    pool.close()
    pool.join()
    total_time = 0
    total_item = 0
    for res in results:
        total_time += res.get()["time_consume"]
        total_time += res.get()["items"]
    print(f"Processing finished")
    print(f"Total number of items processed: {total_item}")
    print(f"Total time: {total_time}")
