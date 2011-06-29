__author__ = 'Tom'

import sys
import uuid
import socket
import pickle
from threading import Thread
from tkinter import *
from tkinter.ttk import *
from cards import *

class PlayerCanvas:
    def __init__(self, root, id):
        self.id = id
        self.canvas = Canvas(root, width=145, height=115)
        self.cards = []
        self.chips = None
        self.chip_total = 0

    def __str__(self):
        return self.id

class PokerGUI(Thread):
    def __init__(self, root):
        Thread.__init__(self)
        self.root = root
        self.canvas = Canvas(self.root, width=800, height=520)
        self.player_frame = Frame(self.root)
        self.bet = Scale(self.player_frame, from_=0, command=self.scale_bet)
        self.lbl_bet = Label(self.player_frame, text=0)
        self.btn_bet = Button(self.player_frame, text='Bet', command=self.place_bet, state=DISABLED)
        self.btn_fold = Button(self.player_frame, text='Fold', state=DISABLED)
        self.add_widgets()
        self.cards = self.get_cards()
        self.player = PlayerCanvas(self.canvas, str(uuid.uuid4()))
        self.players = [self.player,]
        self.face_down_image = PhotoImage(file="cards/b1fv.gif")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.new_game()
        self.start()

    def add_widgets(self):
        self.root.title("Poker")
        self.root.geometry("800x580")
        self.root.resizable(0, 0)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.canvas.pack(fill='both', expand='yes')
        self.player_frame.pack()
        self.bet.grid(row=0, column=0)
        self.lbl_bet.grid(row=0, column=1)
        self.btn_bet.grid(row=1, column=0)
        self.btn_fold.grid(row=1, column=1)

    def get_cards(self):
        cards = {}
        deck = Deck()
        for card in deck:
            cards[hash(card)] = PhotoImage(file=card.get_image())
        return cards

    def new_game(self):
        data = self.get_data(8000)
        player_data = pickle.loads(data)
        for id, cards, chips in player_data:
            if id == self.player.id:
                player = self.player
                images = [self.cards[hash(card)] for card in cards]
                self.bet.config(to=int(chips))
            else:
                player = PlayerCanvas(self.canvas, id)
                images = [self.face_down_image,] * 2
                self.players.append(player)
            for i, image in enumerate(images):
                player.cards.append(player.canvas.create_image(5 + 70 * i, 50, image=image, anchor=W))
            player.chip_total = int(chips)
            player.chips = player.canvas.create_text(75, 110, text="Chips: %d" % player.chip_total)
        for i, player in enumerate(self.players):
            self.canvas.create_window(self.get_position(i), window=player.canvas)

    def place_bet(self):
        self.btn_bet.config(state=DISABLED)
        self.btn_fold.config(state=DISABLED)
        self.lbl_bet.config(text=0)
        self.send_data(("bet", int(self.bet.get()),))
        self.bet.set(0)

    def get_position(self, position):
        positions = ((400, 470), (75, 450), (75, 250), (75, 60), (400, 60), (725, 60), (725, 250), (725, 450),)
        return positions[position]

    def get_player(self, id):
        for player in self.players:
            if id == player.id:
                return player

    def scale_bet(self, bet):
        self.lbl_bet.config(text=int(float(bet)))

    def quit(self):
        self.send_data(("quit",))
        self.root.destroy()

    def run(self):
        while True:
            data = self.get_data(1024)
            if not data: break
            data = pickle.loads(data)
            if data[0] == "quit":
                player = self.get_player(data[1])
                player.canvas.delete(ALL)
                self.players.remove(player)
            elif data[0] == "chips":
                player = self.get_player(data[1])
                player.chip_total = int(data[2])
                player.canvas.itemconfig(player.chips, text="Chips: %d" % player.chip_total)
                if player == self.player:
                    self.bet.config(to=int(player.chip_total))
            elif data[0] == "turn":
                self.btn_bet.config(state=ACTIVE)
                self.btn_fold.config(state=ACTIVE)
                self.bet.config(from_=data[1])
                self.lbl_bet.config(text=data[1])
            print(data)

    def connect(self):
        HOST = socket.gethostname()    # The remote host
        PORT = 50007              # The same port as used by the server
        try:
            self.server.connect((HOST, PORT))
            self.server.send(bytes(self.player.id, "UTF-8"))
        except:
            sys.exit("Remote host hung up unexpectedly.")

    def get_data(self, num_bytes):
        try:
            data = self.server.recv(num_bytes)
        except:
            sys.exit("Remote host hung up unexpectedly.")
        return data

    def send_data(self, data):
        try:
            self.server.send(pickle.dumps(data))
        except:
            sys.exit("Remote host hung up unexpectedly.")

if __name__ == "__main__":
    root = Tk()
    gui = PokerGUI(root)
    root.mainloop()