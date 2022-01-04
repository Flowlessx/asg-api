from kivymd.toast import toast
from modules.DB_Connection import DB_Connection
import socket


class Socket_Server:
    def __init__(self, host, port):

        # constructor
        self._host = host    # Listen to all addresses with None
        self._port = port   # 'STAR' on telephone keypad :)

    def socket_server_listener(self):

        # Socket for accepting communication
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind((self._host, self._port))  # Binding to ifaces, port

        server.listen()  # Listening

        while True:
            # Communication socket and address to communicate with clients
            commSocket, address = server.accept()
            print(f"Connection from {address}")
            message = commSocket.recv(1024).decode('utf-8')
            print(f"Message received: {message}")
            commSocket.send(f"Server says: Message received!".encode('utf-8'))
            commSocket.close()
            print(f"Connection with {address} ended!")
