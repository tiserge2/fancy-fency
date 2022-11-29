import socket
from threading import Timer, Thread
import json
from client import client

class server():
    def __init__(self):
        self.ip = self.get_ip()[0]
        self.port = self.get_ip()[1]
        self.address = (self.ip, self.port)
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connected = ""
        self.client_address = ""
        self.server_state = ""
        self.received_data = ""

    def get_ip(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        address = sock.getsockname()
        sock.close()
        return address[0], address[1]

    def start_server(self):
        Timer(1, self.start_server).start()
        try:
            self.server_sock.bind(self.address)
            self.server_sock.listen(10)
            # print(f"Server listening on: {self.ip}:{self.port}")
            self.client_connected, self.client_address = self.server_sock.accept()
            # print("Connected to", self.client_address)
            data = self.client_connected.recv(2048).decode("utf-8")
            if not data:
                print("====> Disconnected.. ")
                a = 1
            else:
                a = 1
                print("====> Reading data.. ")
                self.process_data(data)
        except socket.error as e:
            str(e)

    def process_data(self, data):
        received_data = json.loads(data)
        print("Data: ", received_data)
        self.received_data = received_data


        if received_data['type'] == "INVITE" and received_data['message'] == 'INIT':
            self.server_state = "NEW_INVITE"
        elif received_data['type'] == "INVITE" and received_data['message'] != 'INIT':
            self.server_state = "NEW_RESPONSE"
        elif received_data['type'] == "GAME":
            print("receiving game data")
            

if __name__ == "__main__":
    server_ = server()
    server_.start_server()