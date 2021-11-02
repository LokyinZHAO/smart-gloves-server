import pickle
import socket
from SmartGlovesProject.music_info import MusicInfo

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 9999))
    music_info = s.recv(4096)
    music_info = pickle.loads(music_info)
    print(music_info)
