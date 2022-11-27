import socket
from threading import Timer, Thread
import ipaddress

class server():
    def __init__(self):
        self.ip = self.get_ip()
        self.port = 55555
        self.address = (self.ip, self.port)
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connected = ""
        self.client_address = ""
        # self.search_online_player()
        # self.start_server()

    def get_ip(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        address = sock.getsockname()
        netmask = ipaddress.IPv4Network(address[0]).netmask
        print(netmask)
        sock.close()
        return address[0]

    def start_server(self):
        Timer(1, self.start_server).start()
        try:
            self.server_sock.bind(self.address)
            self.server_sock.listen(1)
            print(f"Server listening on: {self.ip}:{self.port}")
            self.client_connected, self.client_address = self.server_sock.accept()
            print("Connected to", self.client_address)
            data = self.client_connected.recv(2048).decode("utf-8")
            if not data:
                print("====> Disconnected.. ")
            else:
                print("====> Reading data.. ")
                self.process_data(data)
        except socket.error as e:
            str(e)

    def search_online_player(self):
        value_to_send = f"my addess is: {self.ip}/{self.port}"
        dest = ('<broadcast>', 10100)
        sock_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print("Searching for online player...")
        sock_broadcast.sendto(value_to_send, dest)
        while 1:
            (buf,address) = sock_broadcast.recvfrom(10100)

            if not len(buf):
                break
            print(f"received from {address}:{buf}")

    def process_data(self, data):
        print("Data: ", data)

serv = server()