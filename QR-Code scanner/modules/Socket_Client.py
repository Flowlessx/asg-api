from kivymd.toast import toast
from DB_Connection import DB
import socket


class Socket_Client:
    def __init__(self, host, port):

        # constructor
        self._host = host    # Listen to all addresses with None
        self._port = port   # 'STAR' on telephone keypad :)

    def create_socket_app_client(self):

        socket_app_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        socket_app_client.connect((self._host, self._port))

        socket.send("Hello!!!".encode('utf-8'))
        print(socket.recv(1024))
