import glob
import traceback

from obs import ObsClient
from obs import PutObjectHeader
from SmartGlovesProject_Server.Data_Prepare.credential import obs_Access_Key_Id, obs_Secret_Access_Key, obs_endpoint

import multiprocessing
import os

import time

from SmartGlovesProject_Server.Data_Prepare.audio_to_spectrogram import Audio2Spectrogram


# 子进程要执行的代码
def run_proc(item):
    mp3_dir = "./resources/mp3/" + item + "/"
    obs_client = ObsClient(access_key_id=obs_Access_Key_Id,
                           secret_access_key=obs_Secret_Access_Key,
                           server=obs_endpoint)
    src_dir = mp3_dir
    log_dir = "./resources/" + item + ".log"
    put_prefix = item
    files = glob.glob(src_dir + "*.mp3", recursive=True)
    spec = Audio2Spectrogram()
    cnt = 0
    log_file = open(log_dir, 'w')
    for file in files:
        track_id = file.split("/")[-1]
        dest_wav = src_dir + track_id.replace("mp3", "wav")
        dest_jpg = src_dir + track_id.replace("mp3", "jpg")
        spec.audio_to_wav(src=file, dest=dest_wav)
        spec.wav_to_spectrogram(src=dest_wav, dest=dest_jpg)
        try:
            wav_headers = PutObjectHeader()
            wav_headers.contentType = 'audio/wav'
            jpg_headers = PutObjectHeader()
            jpg_headers.contentType = 'image/jpeg'

            wav_resp = obs_client.putFile(
                'wav-data',
                objectKey=put_prefix + '/' + track_id.split('.')[0] + ".wav",
                file_path=dest_wav,
                metadata={'mood': put_prefix},
                headers=wav_headers
            )
            if wav_resp.status < 300:
                pass
            else:
                log_file.write(track_id.split('.')[0] + ":" + wav_resp.errorCode + "--" + wav_resp.errorMessage + '\n')

            jpg_resp = obs_client.putFile(
                'spec-data',
                objectKey=put_prefix + track_id.split('.')[0] + ".jpg",
                file_path=dest_jpg,
                metadata={'mood': put_prefix},
                headers=jpg_headers
            )
            if jpg_resp.status < 300:
                pass
            else:
                log_file.write(track_id.split('.')[0] + ":" + jpg_resp.errorCode + " " + jpg_resp.errorMessage + '\n')
        except:
            log_file.write("==========EXCEPTION============\n")
            log_file.write("except-track id:" + track_id + '\n')
            log_file.write(traceback.format_exc() + '\n')
            log_file.write("==========EXCEPTION============\n")
        os.remove(dest_wav)
        os.remove(dest_jpg)
        cnt += 1
    log_file.close()
    return cnt


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)
    batch_log_file = open("./resources/batch.log", 'w')
    total_time = time.time()
    results = [pool.apply_async(run_proc, ("Happy",)),
               pool.apply_async(run_proc, ("Sad",)),
               pool.apply_async(run_proc, ("Angry",)),
               pool.apply_async(run_proc, ("Relaxed",))
               ]
    pool.close()
    pool.join()
    total_time = time.time() - total_time
    total_item = 0
    for res in results:
        total_item += res.get()
    batch_log_file.write(f"Processing finished\n")
    batch_log_file.write(f"Total number of items processed: {total_item}\n")
    batch_log_file.write(f"Total time:  {total_time // 3600}H {(total_time % 3600) // 60}M {int(total_time % 60)}S\n")
