__author__ = 'Tom'

import sys
import pickle
import socket

class Client:
    def __init__(self, host, port):
        self.host, self.port = host, port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.conn.setblocking(0)

    def connect(self):
        try:
            self.conn.connect((self.host, self.port))
        except socket.error:
            sys.exit("Remote host hung up unexpectedly.")

    def send(self, data):
        try:
            self.conn.sendall(pickle.dumps(data))
        except socket.error:
            sys.exit("Remote host hung up unexpectedly.")

    def close(self):
        self.conn.close()