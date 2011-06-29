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

    def new_game(self):
        for i in range(2):
            for player in self.players:
                card = self.deck.cards.pop()
                player.add(card)

    def __str__(self):
        s = ""
        for i, player in enumerate(self.players):
            s += "Player %d: %s\n" % (i + 1, str(player))
        return s

class Lobby(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super(Lobby, self).__init__(self, request, client_address, server)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.TCPServer((HOST, PORT), Lobby)
    poker = Poker()
    while len(poker.players) < 2:
        poker.players.append(PokerPlayer(server.get_request())

"""
import sys
import socketserver
import pickle
from threading import *
from cards import *

class PokerPlayer(Hand, Thread):
    def __init__(self, poker, id, conn):
        Thread.__init__(self)
        super(PokerPlayer, self).__init__()
        self.poker = poker
        self.id = id
        self.conn = conn
        self.chips = 50
        self.last_bet = 0
        self.event = Event()
        self.start()

    def is_playing(self):
        return (self in self.poker.players)

    def bet(self, amount):
        self.chips -= amount
        self.last_bet = amount
        for player in self.poker.players:
            player.send_data(("chips", self.id, self.chips,))

    def turn(self):
        self.send_data(("turn", self.poker.min_bet - self.last_bet,))

    def quit(self):
        self.poker.players.remove(self)
        if self.poker.in_game:
            for player in self.poker.players:
                player.send_data(("quit", self.id,))
        self.conn.close()

    def run(self):
        while True:
            if self.is_playing():
                data = self.conn.recv(1024)
                if not data: break
                data = pickle.loads(data)
                if data[0] == "quit":
                    self.quit()
                elif data[0] == "bet":
                    self.poker.min_bet = int(data[1])
                    self.bet(self.poker.min_bet)
                    self.poker.player_turn = self.poker.get_next_player()
                    self.poker.players[self.poker.get_next_player()].turn()

    def send_data(self, data):
        self.event.wait(1)
        try:
            self.conn.send(pickle.dumps(data))
        except:
            sys.exit("Remote host hung up unexpectedly.")

class PokerServer(socketserver.BaseRequestHandler):
    def handle(self):
        pass

class Poker:
    def __init__(self):
        self.deck = Deck(count=2)
        self.deck.shuffle()
        self.players = []
        self.in_game = False
        self.player_turn = 0
        self.min_bet = 2
        self.server = PokerServer()

    def new_game(self):
        for i in range(2):
            for player in self.players:
                player.add(self.deck.cards.pop())
        player_data = [(player.id, player.cards, player.chips,) for player in self.players]
        for player in self.players:
            player.send_data(player_data)

    def get_next_player(self):
        return ((self.player_turn + 1) % len(self.players))

    def handle(self):
        while len(self.players) < 3:
            conn, address = s.accept()
            print('Connected by', address)
            data = conn.recv(1024).decode("UTF-8")
            if not data: break
            self.players.append(PokerPlayer(self, data, conn))
        self.new_game()
        self.in_game = True
        while True:
            self.players[self.player_turn].bet(1)
            self.player_turn = self.get_next_player()
            self.players[self.player_turn].bet(2)
            self.players[self.get_next_player()].turn()
            break

    def __str__(self):
        s = ""
        for i, player in enumerate(self.players):
            s += "Player %d: %s\n" % (i + 1, str(player))
        return s

if __name__ == "__main__":
    poker = Poker()
"""