__author__ = 'Tom'

import sys
import uuid
import socket
import pickle
from threading import Thread
from tkinter import *
from tkinter.ttk import *
from cards import *

class Player:
    def __init__(self, root, id):
        self.id = id
        self.canvas = Canvas(root, width=145, height=115)
        self.cards = []
        self.chips = None
        self.num_chips = 0

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
        self.btn_bet = Button(self.player_frame, text='Bet', state=DISABLED)
        self.add_widgets()
        self.cards = self.get_cards()
        self.player = Player(self.canvas, str(uuid.uuid4()))
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
        self.bet.pack()
        self.lbl_bet.pack(side='left')
        self.btn_bet.pack(side='right')

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
            sys.exit("Remote host hung up unexpectedly.")
        self.send_data(bytes(self.player.id, "UTF-8"))

    def get_data(self, num_bytes):
        try:
            data = self.server.recv(num_bytes)
        except:
            sys.exit("Remote host hung up unexpectedly.")
        return data
            
    def send_data(self, data):
        try:
            self.server.send(data)
        except:
            sys.exit("Remote host hung up unexpectedly.")

    def new_game(self):
        player_position = 1
        data = self.get_data(8000)
        player_data = pickle.loads(data)
        for id, cards, chips in player_data:
            self.players.append(Player(self.canvas, id, cards, num_chips=chips))





            if id == self.player.id:
                position = self.get_position(0)
                offset = (-75, 0,)
                images = [self.cards[hash(card)] for card in cards]
            else:
                position = self.get_position(player_position)
                offset = (-10, -10,)
                images = [self.face_down_image,] * 2
                player_position += 1
            self.player_cards[id].append(self.canvas.create_image(position, image=images[0]))
            self.player_cards[id].append(self.canvas.create_image(self.get_position_offset(position, offset),
                                                                  image=images[1]))
            self.player_chips[id] = self.canvas.create_text(self.get_position_offset(position, (-25, 65,)), text=chips)
            self.num_player_chips[id] = int(chips)
            self.bet.config(to=int(chips))

    def get_position(self, position):
        positions = ((435, 450), (50, 450), (50, 250), (50, 60), (400, 60), (750, 60), (750, 250), (750, 450),)
        return positions[position]

    def get_position_offset(self, position, offset):
        return list(map(lambda x, y: x + y, position, offset))
            
    def run(self):
        while True:
            data = self.get_data(1024)
            if not data: break
            data = pickle.loads(data)
            if data[0] == "quit":
                for card in self.player_cards[data[1]]:
                    self.canvas.delete(card)
            elif data[0] == "chips":
                self.canvas.itemconfig(self.player_chips[self.player_id], text=data[1])
                self.num_player_chips[self.player_id] = int(data[1])
                self.bet.config(to=int(data[1]))
            elif data[0] == "turn":
                self.btn_bet.config(state=ACTIVE)
            print(data)

    def scale_bet(self, bet):
        self.lbl_bet.config(text=int(float(bet)))

    def quit(self):
        self.send_data(bytes("quit", "UTF-8"))
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    gui = PokerGUI(root)
    root.mainloop()