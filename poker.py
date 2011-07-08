__author__ = 'Tom'

import pickle
import datetime
from client import *
from server import *
from cards import *

class PokerPlayer(Hand):
    def __init__(self, id, host, port):
        super(PokerPlayer, self).__init__()
        self.id = id
        self.chips = 50
        self.last_bet = 0
        self.has_raised = False
        self.conn = Client(host, port)

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
        self.last_updated = None
        self.server = PokerServer("localhost", 50007)
        #self.run_lobby()
        #self.new_game()
        #self.players[0].conn.send({"timestamp": datetime.datetime.now()})
        #self.server.server.serve_forever() #self.start()

    def run_lobby(self):
        while len(self.players) < self.max_players:
            conn, address = self.server.get_request()
            print('Connected by', address)
            data = pickle.loads(conn.recv(1024))
            self.players.append(PokerPlayer(data["id"], data["host"], data["port"]))

    def new_game(self):
        for i in range(2):
            for player in self.players:
                player.add(self.deck.pop())
        for i in range(len(self.players)):
            players = self.players[i:len(self.players)] + self.players[0:i]
            player_data = [{"id": p.id} for p in players]
            player_data[0].update({"cards": players[0].cards})
            self.players[i].conn.send({"players": player_data, "timestamp": datetime.datetime.now()})
        #self.bet(1)
        #self.players[self.player_turn].has_raised = True
        #self.bet(2)
        #self.turn()

    def run(self):
        pass
        """
        while True:
            try:
                data = pickle.load(open("data.p", "rb"))
            except (IOError, EOFError):
                pass
            else:
                if self.last_updated is None or self.last_updated < data["timestamp"]:
                    print(data)
                    self.last_updated = data["timestamp"]
            self.event.wait(1)
        """


    """
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
    """

if __name__ == "__main__":
    poker = Poker()