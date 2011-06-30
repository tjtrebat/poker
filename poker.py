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
        self.id = str(uuid.uuid4())
        self.root = root
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.start()

    def connect(self):
        HOST, PORT = "localhost", 9999
        self.socket.connect((HOST, PORT))
        self.socket.send(bytes("add {}".format(self.id), "UTF-8"))

    def run(self):
        while True:
            data = self.socket.recv(1024).decode("UTF-8")
            if not data: break
            print(data)

if __name__ == "__main__":
    root = Tk()
    gui = PokerGUI(root)
    root.mainloop()