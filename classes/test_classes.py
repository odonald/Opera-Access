import socket


class local_ip:
    def __init__(ip):
        ip = print(socket.gethostbyname(socket.gethostname()))
