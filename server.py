__author__ = 'Tom'

import socket
import pickle
from cards import *
from threading import Thread

class PokerPlayer(Hand, Thread):
    def __init__(self, poker, id, conn):
        Thread.__init__(self)
        super(PokerPlayer, self).__init__()
        self.poker = poker
        self.id = id
        self.conn = conn
        self.start()

    def is_playing(self):
        return (self in self.poker.players)

    def quit(self):
        self.poker.players.remove(self)
        self.conn.close()

    def run(self):
        while True:
            if self.is_playing():
                data = self.conn.recv(1024).decode("UTF-8")
                if data == "quit":
                    self.quit()

class Poker(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.deck = Deck(count=2)
        self.deck.shuffle()
        self.players = []
        self.start()

    def run(self):
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = 50007              # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        while len(self.players) < 8:
            conn, address = s.accept()
            print('Connected by', address)
            data = conn.recv(1024).decode("UTF-8")
            if not data: break
            self.players.append(PokerPlayer(self, data, conn))
        self.new_game()

    def new_game(self):
        for i in range(2):
            for player in self.players:
                card = self.deck.pop()
                player.add(card)
                player.conn.send(pickle.dumps(card))

    def __str__(self):
        s = ""
        for i, player in enumerate(self.players):
            s += "Player %d: %s\n" % (i + 1, str(player))
        return s

if __name__ == "__main__":
    poker = Poker()