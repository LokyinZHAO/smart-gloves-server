import socket
import pickle

proxy_addr = "localhost"
proxy_port = 6456

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((proxy_addr, proxy_port))

    t = "TRRRULH128F92CDB2E.wav"
    s.send(bytes(t, encoding='utf8'))

    # file = open("TRRIJNE12903CBE8F9.wav", 'rb')
    # p = pickle.dumps(file)
    # s.send(p)

    resp = str(s.recv(1024))
    print(resp)
