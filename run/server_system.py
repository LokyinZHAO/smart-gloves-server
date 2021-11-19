import pickle
import socket
import sys
import traceback

from obs import ObsClient
from obs import PutObjectHeader

import librosa
import numpy as np
from SmartGlovesProject_Server.Data_Prepare.audio_to_spectrogram import wav_to_spectrogram
from SmartGlovesProject_Server.beat_tracker import get_beats
from SmartGlovesProject_Server.mood_predictor import Predictor
from SmartGlovesProject_Server.short_time_fourier_trans import fourier_trans
from SmartGlovesProject_Server.spectral_centroid_tracer import trace_spec_cent
from SmartGlovesProject_Server.framer import to_frames
from SmartGlovesProject_Server.Data_Prepare.credential import obs_Access_Key_Id, obs_Secret_Access_Key, obs_endpoint
from music_info import MusicInfo
import SmartGlovesProject_Server.Util.frame_selector as frame_selector

proxy_addr = "localhost"
proxy_port = 6456

server_addr = "0.0.0.0"
server_port = 7435

pred = Predictor("./resources/Resnet_SGD_valscore_60.pt")

wav_file_dir = "./resources/wav/Angry/"

obs_client = ObsClient(access_key_id=obs_Access_Key_Id,
                       secret_access_key=obs_Secret_Access_Key,
                       server=obs_endpoint)


def process(src_path: str):
    """Process the given music file，return MusicInfo
    Arguments:
        src_path:the file to process, .wav expected
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

    return music_info


def callback(transferredAmount, totalAmount, totalSeconds):
    # 获取上传平均速率(KB/S)
    print(transferredAmount * 1.0 / totalSeconds / 1024)
    # 获取上传进度百分比
    print(transferredAmount * 100.0 / totalAmount)


def upload_to_bucket(pack_file_dir, pack_name):
    try:
        headers = PutObjectHeader()
        headers.contentType = 'text/plain'
        resp = obs_client.putFile(bucketName="info-data",
                                  objectKey=pack_name,
                                  file_path=pack_file_dir,
                                  # progressCallback=callback,
                                  headers=headers
                                  )
        if resp.status < 300:
            print('requestId:', resp.requestId)
            print('etag:', resp.body.etag)
            print('versionId:', resp.body.versionId)
            print('storageClass:', resp.body.storageClass)
            return True
        else:
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
            return False
    except:
        print(traceback.format_exc())
        return False


if __name__ == '__main__':
    '''
    @version 2.3
    '''
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((proxy_addr, proxy_port))
    proxy_socket.listen(1)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_addr, server_port))
    server_socket.listen(1)

    print("start listening")

    while True:
        request_conn, request_addr = proxy_socket.accept()
        print("new request connection: " + request_addr[0])
        request = request_conn.recv(1024).decode("utf8")
        while request == '':
            request = request_conn.recv(1024).decode("utf8")
            print('get empty body')
        wav_file_dir = ''
        if request == 'uploaded':
            # 直接从文件中找
            wav_file_dir = open('./resources/upload_music.pkl', 'rb')
            pkl_object = pickle.load(wav_file_dir)
            pkl_object.tofile('./resources/upload_music.wav')
            wav_file_dir = './resources/upload_music.wav'
        else:
            # 音乐名
            wav_file_dir = "resources/wav/Angry/" + request + '.wav'
        # request_conn.send(bytes("200 OK", encoding='utf8'))
        print("get request: " + request + " from " + request_addr[0])
        music = process(wav_file_dir)
        # 序列化成文件
        dump_file_path = "./test_resources/music_info.dumps"
        dump_file = open(dump_file_path, 'wb')
        pickle.dump(music, dump_file)
        dump_file.close()
        # 将序列化文件上传到桶
        print("data ready: " + dump_file_path)
        dump_name = "music_info.dumps"
        resp = upload_to_bucket(dump_file_path, dump_name)
        if resp:
            print("dumps uploaded to bucket: " + dump_name)
            print("start listening")
            client_conn, client_addr = server_socket.accept()
            print("new connection: " + client_addr[0])
            client_conn.send(bytes("music_info.dumps", encoding='utf8'))
            print("pack target sent to " + client_addr[0])
            client_conn.close()
        request_conn.close()
