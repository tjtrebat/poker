__author__ = 'Tom'

import pickle
import socketserver
from connection import *
from cards import *

class PokerPlayer(Hand):
    def __init__(self, host, port):
        super(PokerPlayer, self).__init__()
        self.chips = 50
        self.last_bet = 0
        self.has_raised = False
        self.conn = Connection(host, port)

    """
    def is_playing(self):
        return self in self.poker.players

    def run(self):
        while True:
            if self.is_playing():
                data = self.conn.get_data(1024)
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
    """

class PokerHandler(socketserver.BaseRequestHandler):
    pass

class Poker:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.players = []
        self.max_players = 1
        self.in_game = False
        self.player_turn = 0
        self.current_bet = 2
        self.pot = 0
        self.round = 1
        self.server = None
        self.start_lobby()
        self.new_game()

    def start_lobby(self):
        HOST, PORT = "localhost", 50007
        self.server = socketserver.TCPServer((HOST, PORT), PokerHandler)
        while len(self.players) < self.max_players:
            conn, address = self.server.get_request()
            print('Connected by', address)
            data = pickle.loads(conn.recv(1024))
            self.players.append(PokerPlayer(data.data[0], int(data.data[1])))

    def new_game(self):
        for i in range(2):
            for player in self.players:
                player.add(self.deck.pop())
        for i in range(len(self.players)):
            players = self.players[i:len(self.players)] + self.players[0:i]
            players = [{"cards": player.cards, "chips": player.chips} for player in players]
            self.players[i].conn.send_data(players)
        #self.bet(1)
        #self.players[self.player_turn].has_raised = True
        #self.bet(2)
        #self.turn()

    def bet(self, bet):
        self.pot += bet
        player = self.players[self.player_turn]
        player.chips -= bet
        player.last_bet = bet
        self.player_turn = self.get_next_turn()
        if bet:
            for p in self.players:
                p.conn.send_data({"player_id": player.id, "chips": player.chips, "pot": self.pot})

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
            data = {"cards": [self.deck.pop() for i in range(num_cards)]}
            for player in self.players:
                player.last_bet = 0
                player.conn.send_data(data)
            self.current_bet = 0
        self.round += 1

    def turn(self):
        bet = self.current_bet
        player = self.players[self.player_turn]
        if bet > player.last_bet:
            bet -= player.last_bet
        player.conn.send_data({"bet": bet})

    def quit(self, player):
        self.players.remove(player)
        player.conn.close()
        for p in self.players:
            p.conn.send_data({"exit": player.id})

    def get_next_turn(self):
        return (self.player_turn + 1) % len(self.players)

if __name__ == "__main__":
    poker = Poker()