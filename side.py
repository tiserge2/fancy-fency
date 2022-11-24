import os
from threading import Timer

def show_size():
    Timer(1, show_size).start()
    size = os.get_terminal_size()
    print("columns:", size.columns)
    print("lines:", size.lines, "\n")

