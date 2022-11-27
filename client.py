import socket

class client():
    def __init__(self):
        self.ip = self.get_ip()
        self.port = 55555
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = "INIT"
        print(self.ip)

    def get_ip(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        address = sock.getsockname()
        sock.close()
        return address[0]

    def connect(self, server_address):
        try:
            self.client_sock.connect(server_address)
            self.status = "CONNECTED"
        except socket.error as e:
            self.status = "FAILED"
            print(e)

    def send(self, data):
        try:
            self.client_sock.send(str.encode(data))
            self.status = "SENT"
        except socket.error as e:
            self.status = "FAILED"
            print(e)
        
# cli = client()
# server_address = ("192.168.125.221", 55555)
# connection = cli.connect(server_address)
# print(cli.send("Hello Sergio"))