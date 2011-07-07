__author__ = 'Tom'

import sys
import socket
import pickle
import datetime

class Data:
    def __init__(self, data):
        self.data = data
        self.timestamp = datetime.datetime.now()

class Connection:
    def __init__(self, host, port):
        self.host, self.port = host, port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        try:
            self.conn.connect((self.host, self.port))
        except socket.error:
            sys.exit("Remote host hung up unexpectedly.")

    def send_data(self, data):
        try:
            self.conn.sendall(pickle.dumps(Data(data)))
        except socket.error:
            sys.exit("Remote host hung up unexpectedly.")

    def close(self):
        self.conn.close()