import os
from threading import Timer

def show_size():
    Timer(1, show_size).start()
    os.system("clear")
    size = os.get_terminal_size()
    print("columns:", size.columns)
    print("lines:", size.lines, "\n")

show_size()