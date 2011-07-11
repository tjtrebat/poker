__author__ = 'Tom'

import sys
import socket
import asyncore

class PokerHandler(asyncore.dispatcher_with_send):
    def __init__(self, file_name, *args):
        self.file_name = file_name
        super(PokerHandler, self).__init__(*args)

    def handle_read(self):
        try:
            data = self.recv(1024).decode("UTF-8")
            handle = open(self.file_name, "a")
        except (socket.error, IOError):
            sys.exit("Error reading data from client.")
        print(data)
        handle.write(data + "\n")

    @classmethod
    def load_data(cls, line):
        line = line.split()
        line = [w.decode("UTF-8") for w in line]
        return line

class PokerServer(asyncore.dispatcher):
    def __init__(self, host, port, file_name):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.file_name = file_name
        asyncore.loop()

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print('Incoming connection from %s' % repr(addr))
            self.handler = PokerHandler(self.file_name, sock)

    def get_data(self):
        return self.handler.data