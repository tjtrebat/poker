__author__ = 'Tom'

import socket
import asyncore

class PokerHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        print(data)
        #if data:
        #    self.send(data)

class PokerServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        asyncore.loop()

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            print('Incoming connection from %s' % repr(addr))
            handler = PokerHandler(sock)