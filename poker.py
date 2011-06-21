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
        positions = ((50, 450), (50, 250), (50, 60), (400, 60), (750, 60), (750, 250), (750, 450),)
        return positions[position]

    def new_game(self):
        data = self.server.recv(1024)
        players = pickle.loads(data)
        self.player_cards = {player: [] for player in players}
        players.remove(self.player_id)
        data = self.server.recv(1024)
        cards = pickle.loads(data)
        self.player_cards[self.player_id].append(self.canvas.create_image((435, 450), image=self.cards[str(cards[0])]))
        self.player_cards[self.player_id].append(self.canvas.create_image((355, 450), image=self.cards[str(cards[1])]))
        for i, player in enumerate(players):
            self.player_cards[player].append(self.canvas.create_image(self.get_position(i), image=self.face_down_image))
            self.player_cards[player].append(self.canvas.create_image(list(map(lambda x, y: x + y, self.get_position(i), (-10, -10))),
                                                                          image=self.face_down_image))

    def run(self):
        HOST = socket.gethostname()    # The remote host
        PORT = 50007              # The same port as used by the server
        self.server.connect((HOST, PORT))
        self.server.send(bytes(self.player_id, "UTF-8"))
        self.new_game()
        data = self.server.recv(1024).decode("UTF-8")
        if data == "bet":
            self.btn_bet.config(state=ACTIVE)
        elif data == "quit":
            id = self.server.recv(1024).decode("UTF-8")


    def quit(self):
        self.server.send(bytes("quit", "UTF-8"))
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    gui = PokerGUI(root)
    root.mainloop()