
import socket
from _thread import *
import sys

port=5555
server=socket.gethostbyname(socket.gethostname())
ADDR=(server,port)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.bind(ADDR)
except socket.error as e:
    str(e)

s.listen(2)


print("...................the server is waiting for connection................")

def threaded_client(conn):
    conn.send(str.encode("connected"))
    r =""
    while True:
        try:
            data = conn.recv(2048)
            r=data.decode("utf-8")

            if not data:
                print(".....................disconnected......................")
                break
            else:
                print("-----------------connected-------------------------")
                print("received:",r)
                print("sendind:",r)

            conn.sendall(str.encode(r))

        except:
            break
         
    print("the connectiom is lost")
    conn.close


while True:
    conn,addr= s.accept()
    print("connect to" ,addr)

    start_new_thread(threaded_client,(conn,))


