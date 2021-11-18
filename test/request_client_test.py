import socket

proxy_addr = "localhost"
proxy_port = 6456

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((proxy_addr, proxy_port))
    s.send(bytes("TRRRULH128F92CDB2E.wav", encoding='utf8'))
    resp = str(s.recv(1024))
    print(resp)
