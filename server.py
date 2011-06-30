__author__ = 'Tom'

import socketserver
from cards import *

class PokerPlayer(Hand):
    def __init__(self, id, request):
        super(PokerPlayer, self).__init__()
        self.id = id
        self.request = request

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

class PokerServer(socketserver.BaseRequestHandler):
    poker = Poker()

    def handle(self):
        data = self.request.recv(1024).decode("UTF-8").strip().split()
        if data[0] == "add" and self.poker.in_lobby:
            self.poker.players.append(PokerPlayer(data[1], self.request))
            self.request.send(bytes("hello!", "UTF-8"))
            if len(self.poker.players) > 7:
                self.poker.in_lobby = False

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.TCPServer((HOST, PORT), PokerServer)
    server.serve_forever()