import socket

class client():
    def __init__(self):
        # get the ip of the computer from the connected network
        self.ip = self.get_ip()
        self.port = 55555
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = "INIT"
        self.game_status = ""
        self.response = ""

    def get_ip(self):
        # if we cannot connect to the network raise an exception
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            address = sock.getsockname()
            sock.close()
            return address[0]
        except Exception as e:
            return "Issue connecting"

    # connect to another computer on the network while the ip and port 
    def connect(self, server_address):
        try:
            self.client_sock.connect(server_address)
            self.status = "CONNECTED"
        except socket.error as e:
            self.status = "FAILED"
            print(e)

    # send data to another computer once we established a successful connection
    def send(self, data):
        try:
            self.client_sock.send(str.encode(data))
            self.status = "SENT"
        except socket.error as e:
            self.status = "FAILED"
            print(e)

    # disconnect from a computer
    def disconnect(self):
        try:
            self.client_sock.close()
            self.status = "INIT"
        except socket.error as e:
            self.status = "FAILED"
            print(e)
        