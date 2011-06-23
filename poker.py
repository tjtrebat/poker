__author__ = 'Tom'

import sys
import uuid
import socket
import pickle
from threading import Thread
from tkinter import *
from tkinter.ttk import *
from cards import *

class PokerGUI(Thread):
    def __init__(self, root):
        Thread.__init__(self)
        self.root = root
        self.canvas = Canvas(self.root, width=800, height=500)
        self.bet = Scale(self.root, from_=0, to=500)
        self.btn_bet = Button(self.root, text='Bet', state=DISABLED)
        self.add_widgets()
        self.cards = self.get_cards()
        self.player_cards = {}
        self.player_chips = {}
        self.face_down_image = PhotoImage(file="cards/b1fv.gif")
        self.player_id = str(uuid.uuid4())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.new_game()
        self.start()

    def add_widgets(self):
        self.root.title("Poker")
        self.root.geometry("800x560")
        self.root.resizable(0, 0)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.canvas.pack(fill='both', expand='yes')
        self.bet.pack()
        self.btn_bet.pack()

    def get_cards(self):
        cards = {}
        deck = Deck()
        for card in deck:
            cards[hash(card)] = PhotoImage(file=card.get_image())
        return cards

    def connect(self):
        HOST = socket.gethostname()    # The remote host
        PORT = 50007              # The same port as used by the server
        try:
            self.server.connect((HOST, PORT))
        except:
            sys.exit("Connection refused by remote host.")
        self.send_data(bytes(self.player_id, "UTF-8"))

    def get_data(self, num_bytes):
        try:
            data = self.server.recv(num_bytes)
        except:
            sys.exit("Connection refused by remote host.")
        return data
            
    def send_data(self, data):
        try:
            self.server.send(data)
        except:
            sys.exit("Connection refused by remote host.")

    def new_game(self):
        player_position = 1
        data = self.get_data(8000)
        player_data = pickle.loads(data)
        for id, cards in player_data:
            self.player_cards[id] = []
            self.player_chips[id] = None
            if id == self.player_id:
                position = self.get_position(0)
                offset = (-75, 0,)
                images = [self.cards[hash(card)] for card in cards]
            else:
                position = self.get_position(player_position)
                offset = (-10, -10,)
                images = [self.face_down_image,] * 2
                player_position += 1
            self.player_cards[id].append(self.canvas.create_image(position, image=images[0]))
            self.player_cards[id].append(self.canvas.create_image(list(map(lambda x, y: x + y, position, offset)),
                                                                  image=images[1]))

    def get_position(self, position):
        positions = ((435, 450), (50, 450), (50, 250), (50, 60), (400, 60), (750, 60), (750, 250), (750, 450),)
        return positions[position]
            
    def run(self):
        while True:
            data = self.get_data(1024)
            data = pickle.loads(data)
            if data[0] == "quit":
                for card in self.player_cards[data[1]]:
                    self.canvas.delete(card)
            elif data[0] == "chips":
                self.player_chips[data[2]] = data[1]

    def quit(self):
        self.send_data(bytes("quit", "UTF-8"))
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    gui = PokerGUI(root)
    root.mainloop()