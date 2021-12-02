import pickle
import socket
import sys
import traceback

server_addr = "0.0.0.0"
server_port = 7435

if __name__ == '__main__':
    '''
    @version 2.3
    '''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_addr, server_port))
    server_socket.listen(3)

    print("start listening")
    dump_name = "music_info.dump"
    print("dumps uploaded to bucket: " + dump_name)
    print("start listening")
    while True:
        client_conn, client_addr = server_socket.accept()
        print("new connection: " + client_addr[0])
        client_conn.send(bytes(dump_name, encoding='utf8'))
        print("pack target sent to " + client_addr[0])
        client_conn.close()
