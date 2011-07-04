__author__ = 'Tom'

import sys
import socket
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
        self.has_raised = False
        self.event = Event()
        self.start()

    def is_playing(self):
        return self in self.poker.players

    def run(self):
        while True:
            if self.is_playing():
                data = self.conn.recv(1024)
                if not data: break
                data = pickle.loads(data)
                if data[0] == "quit":
                    self.poker.quit(self)
                elif data[0] == "bet":
                    bet = int(data[1])
                    if bet > self.poker.current_bet:
                        self.poker.raise_bet(bet)
                        self.has_raised = True
                    else:
                        if self.poker.players[self.poker.get_next_turn()].has_raised:
                            self.poker.next_round()
                    self.poker.bet(bet)
                    if self.poker.round < 5:
                        self.poker.turn()

    def send_data(self, data):
        self.event.wait(1)
        try:
            self.conn.send(pickle.dumps(data))
        except socket.error:
            sys.exit("Remote host hung up unexpectedly.")

class Poker(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.deck = Deck()
        self.deck.shuffle()
        self.players = []
        self.in_game = False
        self.player_turn = 0
        self.current_bet = 2
        self.pot = 0
        self.round = 1
        self.start()

    def new_game(self):
        for i in range(2):
            for player in self.players:
                player.add(self.deck.pop())
        player_data = [(player.id, player.cards, player.chips,) for player in self.players]
        for player in self.players:
            player.send_data(player_data)
        self.bet(1)
        self.players[self.player_turn].has_raised = True
        self.bet(2)
        self.turn()

    def bet(self, bet):
        self.pot += bet
        player = self.players[self.player_turn]
        player.chips -= bet
        player.last_bet = bet
        self.player_turn = self.get_next_turn()
        if bet:
            for p in self.players:
                p.send_data(("chips", player.id, player.chips,))
                p.send_data(("pot", self.pot,))

    def raise_bet(self, bet):
        self.current_bet = bet
        for p in self.players:
            p.has_raised = False

    def next_round(self):
        if self.round < 4:
            if self.round > 1:
                num_cards = 1
            else:
                num_cards = 3
            data = ("round", [self.deck.pop() for i in range(num_cards)],)
            for player in self.players:
                player.last_bet = 0
                player.send_data(data)
            self.current_bet = 0
        self.round += 1

    def turn(self):
        bet = self.current_bet
        player = self.players[self.player_turn]
        if bet > player.last_bet:
            bet -= player.last_bet
        player.send_data(("turn", bet,))

    def quit(self, player):
        self.players.remove(player)
        if self.in_game:
            for p in self.players:
                p.send_data(("quit", player.id,))
        player.conn.close()

    def get_next_turn(self):
        return (self.player_turn + 1) % len(self.players)

    def run(self):
        HOST, PORT = socket.gethostname(), 50007
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        while len(self.players) < 8:
            conn, address = s.accept()
            print('Connected by', address)
            data = conn.recv(1024).decode("UTF-8")
            if not data: break
            self.players.append(PokerPlayer(self, data, conn))
        self.in_game = True
        self.new_game()

    def __str__(self):
        s = ""
        for i, player in enumerate(self.players):
            s += "Player {}: {}\n".format(i + 1, str(player))
        return s

if __name__ == "__main__":
    poker = Poker()