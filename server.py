__author__ = 'Tom'

import socket
import pickle
from cards import *

class PokerPlayer(Hand):
    def __init__(self):
        super(PokerPlayer, self).__init__()
        self.chips = 500

    #def __hash__(self):
    #    return hash(self.index)

class Poker:
    def __init__(self):
        self.deck = Deck(count=2)
        self.deck.shuffle()
        self.players = []

    def add_player(self):
        self.players.append(PokerPlayer())

    def deal_card(self, player):
        player.add(self.deck.cards.pop())

    def __str__(self):
        s = ""
        for i, player in enumerate(self.players):
            s += "Player %d: %s\n" % (i + 1, str(player))
        return s

class Server:
    def __init__(self):
        self.poker = Poker()
        self.run_server()

    def run_server(self):
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = 50007              # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        while 1:
            conn, addr = s.accept()
            print('Connected by', addr)
            data = conn.recv(1024).decode("UTF-8")
            if not data: break
            if data == "add" and len(self.poker.players) < 8:
                self.poker.add_player()
                conn.send(pickle.dumps(self.poker))
        conn.close()

if __name__ == "__main__":
    server = Server()