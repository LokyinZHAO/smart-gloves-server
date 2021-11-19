import multiprocessing
import os
import glob
import time

import librosa

import SmartGlovesProject_Server.mood_predictor
from SmartGlovesProject_Server.Data_Prepare.audio_to_spectrogram import wav_to_spectrogram
from SmartGlovesProject_Server.Data_Prepare.credential import obs_Access_Key_Id, obs_Secret_Access_Key, obs_endpoint
from obs import ObsClient
import pickle

from SmartGlovesProject_Server.Util import frame_selector
from SmartGlovesProject_Server.beat_tracker import get_beats
from SmartGlovesProject_Server.framer import to_frames
from SmartGlovesProject_Server.mood_predictor import Predictor
from SmartGlovesProject_Server.short_time_fourier_trans import fourier_trans
from SmartGlovesProject_Server.spectral_centroid_tracer import trace_spec_cent
from music_info import MusicInfo


def process(src_path: str, pred: SmartGlovesProject_Server.mood_predictor.Predictor):
    """Process the given music file，return MusicInfo
    Arguments:
        @param src_path:the file to process, .wav expected
        @param pred: predictor
    Return:
         Music Info
    """
    # predict mood
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

    os.remove(spec_file)
    return music_info


def upload_to_bucket(file_dir, client: ObsClient):
    obj_name = file_dir.split('/')[-2] + '/' + file_dir.split('/')[-1]
    resp = client.putFile('info-data', objectKey=obj_name, file_path=file_dir)
    if resp.status < 300:
        return True
    else:
        return False


def download_from_bucket(tar: str, obs_client: ObsClient):
    mood = tar.split('/')[-2]
    wav_name = tar.split('/')[-1].replace('.mp3', '.wav')
    resp = obs_client.getObject('wav-data',
                                objectKey=mood + '/' + wav_name,
                                downloadPath=tar.replace('.mp3', '.wav')
                                )
    if resp.status < 300:
        return True
    else:
        return False


def music_info_gen_batch(src_dir: str):
    mood = src_dir.split('/')[-1]
    log_file = open('./resources/' + mood + '.log', 'w')
    obs_client = ObsClient(access_key_id=obs_Access_Key_Id,
                           secret_access_key=obs_Secret_Access_Key,
                           server=obs_endpoint)
    files = glob.glob(src_dir + "/*.mp3", recursive=True)
    pred = Predictor("./resources/Resnet_SGD_valscore_60.pt")
    time_consume = 0
    item_cnt = 0
    for i in files:
        download_ok = download_from_bucket(i, obs_client)
        if download_ok is True:
            start_time = time.time()
            music = process(i.replace('.mp3', '.wav'), pred)
            end_time = time.time()
            time_consume += end_time - start_time
            dump_file = open(i.replace('.mp3', '.dump'), 'wb')
            pickle.dump(music, dump_file)
            dump_file.close()
            upload_ok = upload_to_bucket(i.replace('.wav', '.dump'), obs_client)
            if not upload_ok:
                log_file.write("missing upload:" + i.replace('.mp3', '.dump') + '\n')
            else:
                os.remove(i.replace('.mp3', '.dump'))
                os.remove(i.replace('.mp3', '.wav'))
                item_cnt += 1
        else:
            log_file.write("missing download:" + i + '\n')
            continue
    log_file.close()
    return time_consume, item_cnt


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)
    batch_log_file = open("./resources/batch.log", 'w')
    results = [pool.apply_async(music_info_gen_batch, ("resources/mp3/Angry",)),
               pool.apply_async(music_info_gen_batch, ("resources/mp3/Happy",)),
               pool.apply_async(music_info_gen_batch, ("resources/mp3/Relaxed",)),
               pool.apply_async(music_info_gen_batch, ("resources/mp3/Sad",))
               ]
    pool.close()
    pool.join()
    total_item = 0
    total_time = 0
    for res in results:
        total_item += res.get()[1]
        total_time += res.get()[0]
    total_time /= 4
    batch_log_file.write(f"Processing finished\n")
    batch_log_file.write(f"Total number of items processed: {total_item}\n")
    batch_log_file.write(
        f"Total time:  {int(total_time // 3600)}H {int((total_time % 3600) // 60)}M {int(total_time % 60)}S\n")
    batch_log_file.write("Average time per item: %.2fs\n" % (total_time / total_item))
    batch_log_file.close()
