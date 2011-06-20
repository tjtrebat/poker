__author__ = 'Tom'

import socket
import pickle
from cards import *
from threading import Thread

class PlayerThread(Thread):
    def __init__(self, player):
        Thread.__init__(self)
        self.player = player

    def run(self):
        while True:
            data = self.player.conn.recv(1024).decode("UTF-8")
            if data == "quit":
                self.player.poker.players.remove(self.player)

class PokerPlayer(Hand):
    def __init__(self, id, conn, poker):
        super(PokerPlayer, self).__init__()
        self.id = id
        self.conn = conn
        self.poker = poker
        self.thread = PlayerThread(self)
        self.thread.start()

class LobbyThread(Thread):
    def __init__(self, poker):
        Thread.__init__(self)
        self.poker = poker
        self.is_full = False

    def run(self):
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = 50007              # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        while len(self.poker.players) < 8:
            conn, address = s.accept()
            print('Connected by', address)
            data = conn.recv(1024).decode("UTF-8")
            if not data: break
            self.poker.players.append(PokerPlayer(data, conn, self.poker))
        self.is_full = True

class Poker:
    def __init__(self):
        self.deck = Deck(count=2)
        self.deck.shuffle()
        self.players = []
        self.lobby = LobbyThread(self)
        self.lobby.start()
        self.has_started = False


    def deal_card(self, player):
        player.add(self.deck.cards.pop())

    def __str__(self):
        s = ""
        for i, player in enumerate(self.players):
            s += "Player %d: %s\n" % (i + 1, str(player))
        return s

if __name__ == "__main__":
    poker = Poker()