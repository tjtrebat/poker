__author__ = 'Tom'

import sys
import socket
import pickle

class Server:
    def __init__(self, conn=None):
        self.conn = conn or socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        HOST, PORT = socket.gethostname(), 50007
        try:
            self.conn.connect((HOST, PORT))
        except socket.error:
            sys.exit("Remote host hung up unexpectedly.")

    @classmethod
    def get_bytes(cls, data):
        return bytes(data, "UTF-8")

    @classmethod
    def get_pickle(cls, data):
        return pickle.dumps(data)

    def get_data(self, num_bytes):
        try:
            data = self.conn.recv(num_bytes)
        except socket.error:
            sys.exit("Remote host hung up unexpectedly.")
        return self.load_data(data)

    def send_data(self, data):
        try:
            self.conn.send(data)
        except socket.error:
            sys.exit("Remote host hung up unexpectedly.")

    def load_data(self, data):
        try:
            data = pickle.loads(data)
        except EOFError:
            sys.exit("Remote host hung up unexpectedly.")
        return data

    def close(self):
        self.conn.close()