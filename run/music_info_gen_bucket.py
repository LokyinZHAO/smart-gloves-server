import multiprocessing
import os
import glob
import time
import traceback

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


def upload_to_bucket(queue: multiprocessing.Queue, producer: int):
    obs_client = ObsClient(access_key_id=obs_Access_Key_Id,
                           secret_access_key=obs_Secret_Access_Key,
                           server=obs_endpoint)
    src_dir = str(queue.get())
    log_file = open('./log/upload.log', 'w')
    eof_get = 0
    total_time = 0
    cnt = 0
    while True:
        if src_dir == 'EOF':
            eof_get += 1
            if eof_get == producer:
                break
            src_dir = queue.get()
            continue
        obj_name = src_dir.split('/')[-1]
        try:
            start_time = time.time()
            resp = obs_client.putFile('info-data', objectKey=obj_name, file_path=src_dir)
            end_time = time.time()
            total_time += end_time - start_time
            if resp.status < 300:
                cnt += 1
                os.remove(src_dir)
                log_file.write(f'uploaded {cnt} :' + src_dir + '\n')
                log_file.flush()
            else:
                log_file.write(f'fail  :' + src_dir + '\n')
                log_file.flush()
        except:
            log_file.write(f'============exception==========\n')
            log_file.write(src_dir + '\n')
            log_file.write(traceback.format_exc() + '\n')
            log_file.write('================================\n')
            log_file.flush()
        src_dir = queue.get()
    log_file.close()
    return total_time, cnt


def download_from_bucket(queue: multiprocessing.Queue, consumer: int):
    files = glob.glob('./resources/mp3/*/' + '*.mp3', recursive=True)
    obs_client = ObsClient(access_key_id=obs_Access_Key_Id,
                           secret_access_key=obs_Secret_Access_Key,
                           server=obs_endpoint)
    log_file = open('./log/download.log', 'w')
    total_time = 0
    cnt = 0
    for i in files:
        mood = i.split('/')[-2]
        wav_name = i.split('/')[-1].replace('.mp3', '.wav')
        dest = i.replace('.mp3', '.wav')
        try:
            start_time = time.time()
            resp = obs_client.getObject('wav-data',
                                        objectKey=mood + '/' + wav_name,
                                        downloadPath=dest
                                        )
            end_time = time.time()
            total_time += end_time - start_time
            if resp.status < 300:
                cnt += 1
                queue.put(dest, block=True, timeout=None)
                log_file.write(f'downloaded {cnt} :' + dest + '\n')
                log_file.flush()
            else:
                log_file.write(f"fail  :" + mood + '/' + wav_name + '\n')
                log_file.flush()
        except:
            log_file.write(f'============exception==========\n')
            log_file.write(i + '\n')
            log_file.write(traceback.format_exc() + '\n')
            log_file.write('================================\n')
            log_file.flush()
    for i in range(consumer):
        queue.put('EOF')
    log_file.close()
    return total_time, cnt


def music_info_gen_batch(src_queue: multiprocessing.Queue, dest_queue: multiprocessing.Queue, process_id: int):
    src_dir = src_queue.get()
    log_file = open('./log/process' + str(process_id) + '.log', 'w')
    pred = Predictor("./resources/Resnet_SGD_valscore_60.pt")
    time_consume = 0
    item_cnt = 0
    while src_dir != 'EOF':
        try:
            start_time = time.time()
            music = process(src_dir, pred=pred)
            end_time = time.time()
            time_consume += end_time - start_time
            dump_file = open(src_dir.replace('.wav', '.dump'), 'wb')
            pickle.dump(music, dump_file)
            dump_file.close()
            dest_queue.put(src_dir.replace('.wav', '.dump'))
            os.remove(src_dir)
            item_cnt += 1
            log_file.write(f'{item_cnt}: {src_dir} processed\n')
            log_file.flush()
            src_dir = src_queue.get()
        except:
            log_file.write('============exception===========\n')
            log_file.write(src_dir+'\n')
            log_file.write(traceback.format_exc() + '\n')
            log_file.write('================================\n')
            log_file.flush()
    dest_queue.put('EOF')
    log_file.close()
    return time_consume, item_cnt


if __name__ == '__main__':
    """
    @version 2.1
    """
    manager = multiprocessing.Manager()
    wav_queue = manager.Queue(maxsize=4)
    info_queue = manager.Queue(maxsize=4)
    pool = multiprocessing.Pool(processes=6)
    results = [
        pool.apply_async(download_from_bucket, (wav_queue, 4,)),
        pool.apply_async(music_info_gen_batch, (wav_queue, info_queue, 1,)),
        pool.apply_async(music_info_gen_batch, (wav_queue, info_queue, 2,)),
        pool.apply_async(music_info_gen_batch, (wav_queue, info_queue, 3,)),
        pool.apply_async(music_info_gen_batch, (wav_queue, info_queue, 4,)),
        pool.apply_async(upload_to_bucket, (info_queue, 4,))
    ]
    pool.close()
    pool.join()
    batch_log_file = open("./log/batch.log", 'w')
    p_time = 0
    p_cnt = 0
    for i in results[1:5]:
        p_time += i.get()[0]
        p_cnt += i.get()[1]
    p_time /= 4
    d_time = results[0].get()[0]
    d_cnt = results[0].get()[1]
    u_time = results[5].get()[0]
    u_cnt = results[5].get()[1]

    batch_log_file.write(f'download time: {int(d_time // 3600)}H {int((d_time % 3600) // 60)}M {int(d_time % 60)}S\n')
    batch_log_file.write(f'download items: {d_cnt}\n')
    batch_log_file.write(f'download time per item: {d_time / d_cnt}\n')
    batch_log_file.write(f'process time: {int(p_time // 3600)}H {int((p_time % 3600) // 60)}M {int(p_time % 60)}S\n')
    batch_log_file.write(f'process items: {p_cnt}\n')
    batch_log_file.write(f'process time per item: {p_time / p_cnt}\n')
    batch_log_file.write(f'upload time: {int(u_time // 3600)}H {int((u_time % 3600) // 60)}M {int(u_time % 60)}S\n')
    batch_log_file.write(f'upload items: {u_cnt}\n')
    batch_log_file.write(f'upload time per item: {u_time / u_cnt}\n')
    if p_cnt == d_cnt and u_cnt == p_cnt:
        batch_log_file.write('item count matches\n')
    else:
        batch_log_file.write('item count does not match\n')
    batch_log_file.close()

# if __name__ == '__main__':
#     wav_queue = multiprocessing.Queue(maxsize=0)
#     dump_queue = multiprocessing.Queue(maxsize=0)
#     d_time, d_cnt = download_from_bucket(wav_queue, 2)
#     g1_time, g1_cnt = music_info_gen_batch(wav_queue, dump_queue, 1)
#     g2_time, g2_cnt = music_info_gen_batch(wav_queue, dump_queue, 2)
#     u_time, u_cnt = upload_to_bucket(dump_queue, 2)
#     g_time = g1_time + g2_time
#     g_time /= 2
#     g_cnt = g1_cnt + g2_cnt
#     print(f'total download time:{d_time}')
#     print(f'total download items:{d_cnt}')
#     print(f'download time per item: {d_time / d_cnt}')
#     print("")
#     print(f'total process time:{g_time}')
#     print(f'total process items:{g_cnt}')
#     print(f'process time per item: {g_time / g_cnt}')
#     print("")
#     print(f'total upload time:{u_time}')
#     print(f'total upload items:{u_cnt}')
#     print(f'upload time per item: {u_time / u_cnt}')
