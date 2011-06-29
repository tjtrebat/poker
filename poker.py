__author__ = 'Tom'

import uuid
import socket
from threading import Thread
from tkinter import *
from tkinter.ttk import *
from cards import *

class PokerGUI(Thread):
    def __init__(self, root):
        Thread.__init__(self)
        self.root = root
        self.player_id = str(uuid.uuid4())
        self.start()

    def run(self):
        HOST, PORT = "localhost", 9999
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.send(bytes("add {}".format(self.player_id), "UTF-8"))

if __name__ == "__main__":
    root = Tk()
    gui = PokerGUI(root)
    root.mainloop()