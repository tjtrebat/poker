__author__ = 'Tom'

import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_image(self):
        try:
            rank = int(self.rank)
        except ValueError:
            rank = self.rank[0].lower()
        return 'cards/{}.gif'.format(self.suit[0].lower() + str(rank))

    def __hash__(self):
        return hash(self.rank) ^ hash(self.suit)

    def __str__(self):
        return '{} of {}s'.format(self.rank, self.suit)

class Deck:
    def __init__(self, count=1):
        self.count = count
        self.cards = self.get_cards()

    def pop(self):
        return self.cards.pop()
    
    def shuffle(self):
        random.shuffle(self.cards)

    def get_cards(self):
        cards = []
        for i in range(self.count):
            for rank in list(range(2, 11)) + ['Jack', 'Queen', 'King', 'Ace']:
                for suit in ('Spade', 'Heart', 'Diamond', 'Club'):
                    cards.append(Card(str(rank), suit))
        return cards

    def __getitem__(self, item):
        return self.cards[item]

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return ','.join([str(card) for card in self.cards])

class Hand(object):
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def __str__(self):
        return ','.join([str(card) for card in self.cards])