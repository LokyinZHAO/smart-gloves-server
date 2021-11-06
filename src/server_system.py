import pickle

from SmartGlovesProject.predictor import Predictor
from SmartGlovesProject.audio_to_spectrogram import Audio2Spectrogram
from SmartGlovesProject.beat_tracker import BeatTracker
from music_info import MusicInfo
import SmartGlovesProject
import socket

if __name__ == '__main__':
    '''
    @version 1.0 
    '''
    pred = Predictor(trained_weights_path=SmartGlovesProject.trained_weight_file)
    spec_transformer = Audio2Spectrogram()
    beats_tracker = BeatTracker()
    # mp3_music_file = "./test_resources/audio/LightYourStory.mp3"
    wav_music_file = "./test_resources/audio/LightYourStory.wav"
    spec_file = "./test_resources/spectrogram/Light&YourStory.jpg"
    # spec_transformer.audio_to_wav(mp3_music_file, wav_music_file)
    spec_transformer.wav_to_spectrogram(wav_music_file, spec_file)
    mood, prob = pred.predict(spec_file, k=4)
    print(f"mood:{mood}\nprob:{prob}")
    beats_time, strength, strength_mean = beats_tracker.get_beats(wav_music_file)
    music_info = MusicInfo(name=wav_music_file,
                           mood=mood,
                           prob=prob,
                           beats=beats_time,
                           strength=strength,
                           mean=strength_mean)
    serialized_music_info = pickle.dumps(music_info)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 9999))
    server_socket.listen(5)
    print("start listening")
    while True:
        sock, addr = server_socket.accept()
        print(f"new connection:{addr}")
        sock.send(serialized_music_info)
        print(f"music info sent")
        sock.close()
