__author__ = 'Tom'

import socketserver
from cards import *

class PokerPlayer(Hand):
    def __init__(self, socket):
        super(PokerPlayer, self).__init__()
        self.socket = socket

class Poker:
    def __init__(self):
        self.deck = Deck(count=2)
        self.deck.shuffle()
        self.players = []
        self.in_lobby = True

    def deal_cards(self):
        for i in range(2):
            for player in self.players:
                card = self.deck.cards.pop()
                player.add(card)

    def __str__(self):
        s = ""
        for i, player in enumerate(self.players):
            s += "Player %d: %s\n" % (i + 1, str(player))
        return s

class PokerServer(socketserver.StreamRequestHandler):
    poker = Poker()

    def handle(self):
        data = self.rfile.readline().decode("UTF-8").strip()
        print(data)
        if data[0] == "add":
            print("Adding Player %d" % data[1])

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.TCPServer((HOST, PORT), PokerServer)
    server.serve_forever()