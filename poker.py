__author__ = 'Tom'

import uuid
import socket
import pickle
from server import *
from tkinter import *
from tkinter.ttk import *

class PokerGUI(Thread):
    def __init__(self, root):
        Thread.__init__(self)
        self.root = root
        self.root.title("Poker")
        self.root.geometry("800x550")
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.canvas = Canvas(self.root, width=800, height=500)
        self.canvas.pack(fill='both', expand='yes')
        self.face_down_image = PhotoImage(file="cards/b1fv.gif")
        self.player_id = uuid.uuid4()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cards = {}
        for card in Deck():
            self.cards[card] = PhotoImage(file=card.get_image())
        self.connect_to_server()

    """
    def new_game(self):
        for i in range(2):
            for player in self.poker.players:
                self.poker.deal_card(player)
                position = player.get_position()
                if i > 0:
                    if not player.position:
                        position = (position[0] - 75, position[1])
                    else:
                        position = (position[0] - 10, position[1] - 10)
                if not player.position:
                    image = self.cards[player.cards[-1]]
                else:
                    image = self.face_down_image
                self.images[player].append(self.canvas.create_image(position, image=image))
                #self.canvas.itemconfig(self.images[player][-1], image=self.cards[player.cards[-1]])
        #self.bet = Scale(self.root, from_=0, to=)


    def get_position(self, position):
        positions = ((435, 450), (50, 450), (50, 250), (50, 60), (400, 60), (750, 60), (750, 250), (750, 450),)
        return positions[position]
    """
    
    def connect_to_server(self):
        HOST = socket.gethostname()    # The remote host
        PORT = 50007              # The same port as used by the server
        self.server.connect((HOST, PORT))
        self.server.send(bytes(str(self.player_id), "UTF-8"))
        while True:
            data = self.server.recv(1024)
            card = pickle.loads(data)
            print(card)

    def quit(self):
        self.server.send(bytes("quit", "UTF-8"))
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    gui = PokerGUI(root)
    root.mainloop()