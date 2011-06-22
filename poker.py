__author__ = 'Tom'

import uuid
import socket
import pickle
from cards import *
from tkinter import *
from tkinter.ttk import *
from threading import Thread

class PokerGUI(Thread):
    def __init__(self, root):
        Thread.__init__(self)
        self.root = root
        self.root.title("Poker")
        self.root.geometry("800x560")
        self.root.resizable(0, 0)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.canvas = Canvas(self.root, width=800, height=500)
        self.canvas.pack(fill='both', expand='yes')
        self.face_down_image = PhotoImage(file="cards/b1fv.gif")
        self.player_id = str(uuid.uuid4())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cards = {}
        for card in Deck():
            self.cards[str(card)] = PhotoImage(file=card.get_image())
        self.player_cards = {}
        self.bet = Scale(self.root, from_=0, to=500)
        self.bet.pack()
        self.btn_bet = Button(self.root, text='Bet', state=DISABLED)
        self.btn_bet.pack()
        self.start()

    def get_position(self, position):
        positions = ((435, 450), (50, 450), (50, 250), (50, 60), (400, 60), (750, 60), (750, 250), (750, 450),)
        return positions[position]

    def new_game(self):
        player_position = 1
        player_data = pickle.loads(self.server.recv(8000))
        for id, cards in player_data:
            self.player_cards[id] = []
            if id == self.player_id:
                position = self.get_position(0)
                offset = (-75, 0,)
                images = [self.cards[str(card)] for card in cards]
            else:
                position = self.get_position(player_position)
                offset = (-10, -10,)
                images = [self.face_down_image,] * 2
                player_position += 1
            self.player_cards[id].append(self.canvas.create_image(position, image=images[0]))
            self.player_cards[id].append(self.canvas.create_image(list(map(lambda x, y: x + y, position, offset)),
                                                                  image=images[1]))
        while True:
            pass
            #data = self.server.recv(1024).decode("UTF-8")
            #data = pickle.loads(data)
            #if data[0] == "quit":
            #    pass

    def run(self):
        HOST = socket.gethostname()    # The remote host
        PORT = 50007              # The same port as used by the server
        self.server.connect((HOST, PORT))
        self.server.send(bytes(self.player_id, "UTF-8"))
        self.new_game()

    def quit(self):
        self.server.send(bytes("quit", "UTF-8"))
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    gui = PokerGUI(root)
    root.mainloop()