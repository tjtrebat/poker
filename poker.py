__author__ = 'Tom'

from cards import *
from tkinter import *
from tkinter.ttk import *

class PokerHand(Hand):
    def __init__(self):
        super(PokerHand, self).__init__()

class Poker:
    def __init__(self):
        self.deck = Deck(count=2)
        self.deck.shuffle()
        self.players = []

    def add_player(self):
        self.players.append(PokerHand())

    def deal_card(self, player):
        player.add(self.deck.cards.pop())

    def __str__(self):
        s = ""
        for i, player in enumerate(self.players):
            s += "Player %d: %s\n" % (i + 1, str(player))
        return s

class PokerGUI:
    def __init__(self, root):
        self.root = root
        self.poker = Poker()
        self.poker.add_player()
        self.new_game()
        print(self.poker)

    def new_game(self):
        for i in range(2):
            for player in self.poker.players:
                self.poker.deal_card(player)

if __name__ == "__main__":
    root = Tk()
    PokerGUI(root)
    root.mainloop()