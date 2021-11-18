import pickle

from SmartGlovesProject_Server.mood_predictor import Predictor
from music_info import MusicInfo
import SmartGlovesProject_Server
import socket

if __name__ == '__main__':
    '''
    @version 1.3
    '''
    pred = Predictor(trained_weights_path=SmartGlovesProject_Server.trained_weight_file)
    # mp3_music_file = "./test_resources/audio/LightYourStory.mp3"
    wav_music_file = "./test_resources/audio/LightYourStory.wav"
    spec_file = "./test_resources/spectrogram/Light&YourStory.jpg"
    # spec_transformer.audio_to_wav(mp3_music_file, wav_music_file)
    spec_transformer.wav_to_spectrogram(wav_music_file, spec_file)
    mood, prob = pred.predict(spec_file, k=4)
    beats_time, strength, strength_mean = beats_tracker.get_beats(music_src=wav_music_file,
                                                                  offset=30,
                                                                  duration=30)
    short_time_fourier_transer = STFTer()
    fourier_trans_y_db, time_per_frame = STFTer.fourier_trans(src_file=wav_music_file,
                                                              offset=30,
                                                              duration=30)
    music_info = MusicInfo()
    music_info.__setattr__("name", wav_music_file)
    music_info.__setattr__("mood", mood)
    music_info.__setattr__("prob", prob)
    music_info.__setattr__("beats", beats_time)
    music_info.__setattr__("strength", strength)
    music_info.__setattr__("mean", strength_mean)
    music_info.__setattr__("fourier_trans_y_db_frames", fourier_trans_y_db)
    music_info.__setattr__("time_per_frame", time_per_frame)
    print("Music info generated")
    print(music_info)
    serialized_music_info = pickle.dumps(music_info)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9998))
    server_socket.listen(5)
    print("start listening")
    while True:
        sock, addr = server_socket.accept()
        print(f"new connection:{addr}")
        sock.send(serialized_music_info)
        print(f"music info sent")
        sock.close()
