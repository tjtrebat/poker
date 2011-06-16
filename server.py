__author__ = 'Tom'

import socket
from cards import *

class PokerPlayer(Hand):
    def __init__(self, index):
        super(PokerPlayer, self).__init__()
        self.index = index
        self.chips = 500

    def __hash__(self):
        return hash(self.index)

class Poker:
    def __init__(self):
        self.deck = Deck(count=2)
        self.deck.shuffle()
        self.players = []

    def add_player(self, index):
        self.players.append(PokerPlayer(index))

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
        self.start_server()

    def start_server(self):
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = 50007              # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        #print('Connected by', addr)
        while 1:
            data = conn.recv(1024)
            if not data: break
            if data == "add" and len(self.poker.players) < 8:
                self.poker.add_player(len(self.poker.players))
            #conn.send(data)
        conn.close()
