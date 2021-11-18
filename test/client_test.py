import pickle
import socket
import traceback
from obs import ObsClient
from SmartGlovesProject_Server.Data_Prepare.credential import obs_Access_Key_Id, obs_Secret_Access_Key, obs_endpoint

server_addr = "localhost"
server_port = 7435

obs_client = ObsClient(access_key_id=obs_Access_Key_Id,
                       secret_access_key=obs_Secret_Access_Key,
                       server=obs_endpoint)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((server_addr, server_port))


def get_music_info():
    pack_tar = server_socket.recv(1024).decode("utf-8")
    print("get target " + pack_tar + ", requesting object from bucket")
    try:
        resp = obs_client.getObject(bucketName='info-data',
                                    objectKey=pack_tar,
                                    downloadPath="./test_resources/music_info_download.dumps"
                                    )
        if resp.status < 300:
            print('requestId:', resp.requestId)
            print('url:', resp.body.url)
        else:
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
    except:
        print(traceback.format_exc())
    pack_file = open("./test_resources/music_info_download.dumps", 'rb')
    # 音乐信息反序列化
    music_info = pickle.load(pack_file)
    pack_file.close()
    print(music_info)
    return music_info


if __name__ == '__main__':
    music_info = get_music_info()
