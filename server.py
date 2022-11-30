import socket
from threading import Timer, Thread
import json

class server():
    def __init__(self):
        self.has_connection = False
        self.ip = self.get_ip()[0]
        self.port = self.get_ip()[1]
        self.address = (self.ip, self.port)
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connected = ""
        self.client_address = ""
        self.server_state = ""
        self.received_data = ""

    def get_ip(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            address = sock.getsockname()
            sock.close()
            self.has_connection = True
            return address[0], address[1]
        except Exception as e:
            self.has_connection = False
            return "Connection Issue", "Try later"

    def start_server(self):
        Timer(1, self.start_server).start()
        try:
            self.server_sock.bind(self.address)
            self.server_sock.listen(10)
            self.client_connected, self.client_address = self.server_sock.accept()
            data = self.client_connected.recv(2048).decode("utf-8")
            if not data:
                print("====> Disconnected.. ")
            else:
                self.process_data(data)

        except socket.error as e:
            self.started = False

    def send(self, data):
        try:
            self.client_connected.send(str.encode(data))
            self.status = "SENT"
        except socket.error as e:
            self.status = "FAILED"
            print(e)


    def process_data(self, data):
        received_data = json.loads(data)
        self.received_data = received_data

        if received_data['type'] == "INVITE" and received_data['message'] == 'INIT':
            self.server_state = "NEW_INVITE"
        elif received_data['type'] == "INVITE" and received_data['message'] != 'INIT':
            self.server_state = "NEW_RESPONSE"
        elif received_data['type'] == "GAME":
            self.server_state = "GAME"
        elif received_data['type'] == "ALT" and received_data == "PAUSE":
            self.server_state = "PAUSE"
        elif received_data['type'] == "ALT" and received_data == "QUIT":
            self.server_state = "QUIT"
        elif received_data['type'] == "ALT" and received_data == "RESUME":
            self.server_state = "RESUME"
            

if __name__ == "__main__":
    server_ = server()
    server_.start_server()