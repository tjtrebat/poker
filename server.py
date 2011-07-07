__author__ = 'Tom'

import pickle
import threading
import socketserver

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        data = pickle.loads(data)
        pickle.dump(data, open("data.p", "wb"))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class Server:
    def __init__(self, HOST, PORT):
        self.server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
        self.run()

    def run(self):
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()
        print("Server loop running in thread:", server_thread.getName())

    def get_request(self):
        return self.server.get_request()

  