__author__ = 'Tom'

import pickle
import random
import datetime
import threading
import socketserver
from tkinter import *
from tkinter.ttk import *
from connection import *
from cards import *

class PlayerCanvas:
    def __init__(self, root):
        self.canvas = Canvas(root, width=145, height=115)
        self.cards = []
        self.chips = None
        self.chip_total = 0
        self.position = 0

    def get_position(self):
        positions = ((400, 470), (75, 450), (75, 250), (75, 60), (400, 60), (725, 60), (725, 250), (725, 450),)
        return positions[self.position]

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        data = pickle.loads(data)
        pickle.dump(data, open("data.p", "wb"))
        #print(data.data)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class PlayerGUI:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(self.root, width=800, height=520)
        self.pot = self.canvas.create_text(400, 320, text="Pot: 0")
        self.player_frame = Frame(self.root)
        self.bet = Scale(self.player_frame, from_=0, command=self.scale_bet)
        self.lbl_bet = Label(self.player_frame, text=0)
        self.btn_bet = Button(self.player_frame, text='Bet', command=self.place_bet, state=DISABLED)
        self.btn_fold = Button(self.player_frame, text='Fold', state=DISABLED)
        self.add_widgets()
        self.cards = self.get_cards()
        self.players = []
        self.face_down_image = PhotoImage(file="cards/b1fv.gif")
        self.num_cards = 0
        HOST, PORT = "localhost", random.randint(10000,60000)
        self.start_server(HOST, PORT)
        self.last_updated = None
        self.update_widgets()
        self.conn = Connection(HOST, 50007)
        self.conn.send_data((HOST, PORT,))
        #self.new_game()

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

    def update_widgets(self):
        try:
            data = pickle.load(open("data.p", "rb"))
        except (IOError, EOFError):
            pass
        else:
            print(data)
            if self.last_updated is None:
                print("Ohhh we updating these widgets...")
                #for i, player in enumerate(data):
                #    pass
                
        self.root.after(1000, self.update_widgets)

    def start_server(self, host, port):
        server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()
        print("Server loop running in thread:", server_thread.getName())

    def new_game(self):
        pass
        """
        player_data = self.conn.get_data(4096)
        my_index = [data[0] for data in player_data].index(self.player.id)
        position = 0
        index = my_index
        while position < 8:
            id, cards, chips = player_data[index]
            if id == self.player.id:
                player = self.player
                images = [self.cards[hash(card)] for card in cards]
                self.bet.config(to=int(chips))
            else:
                player = PlayerCanvas(self.canvas, id)
                images = [self.face_down_image,] * 2
                self.players.append(player)                
            for i, image in enumerate(images):
                player.cards.append(player.canvas.create_image(70 * i + 5, 50, image=image, anchor=W))
            player.chip_total = int(chips)
            player.chips = player.canvas.create_text(75, 110, text="Chips: {}".format(player.chip_total))
            player.position = position
            self.canvas.create_window(player.get_position(), window=player.canvas)
            index = (index + 1) % 8
            position += 1
        """

    def place_bet(self):
        self.btn_bet.config(state=DISABLED)
        self.btn_fold.config(state=DISABLED)
        self.conn.send_data({"player_id": self.player.id, "bet": int(self.bet.get())})

    def scale_bet(self, bet):
        self.lbl_bet.config(text=int(float(bet)))

    def quit(self):
        self.conn.send_data({"exit": self.player.id})
        self.root.destroy()

    """
    def run(self):
        while True:
            data = self.conn.get_data(1024)
            if data[0] == "quit":
                player = self.get_player(data[1])
                player.canvas.delete(ALL)
                self.players.remove(player)
            elif data[0] == "chips":
                player = self.get_player(data[1])
                player.chip_total = int(data[2])
                player.canvas.itemconfig(player.chips, text="Chips: {}".format(player.chip_total))
                if player == self.player:
                    self.bet.config(to=int(player.chip_total))
            elif data[0] == "pot":
                self.canvas.itemconfig(self.pot, text="Pot: {}".format(data[1]))
            elif data[0] == "turn":
                min_bet = int(data[1])
                self.btn_bet.config(state=ACTIVE)
                self.btn_fold.config(state=ACTIVE)
                self.bet.config(from_=min_bet)
                self.bet.set(min_bet)
                self.lbl_bet.config(text=data[1])
                self.root.focus_force()
            elif data[0] == "round":
                for card in data[1]:
                    self.canvas.create_image(70 * self.num_cards + 255, 240, image=self.cards[hash(card)])
                    self.num_cards += 1
            print(data)
    """

    def get_cards(self):
        cards = {}
        deck = Deck()
        for card in deck:
            cards[hash(card)] = PhotoImage(file=card.get_image())
        return cards

if __name__ == "__main__":
    root = Tk()
    gui = PlayerGUI(root)
    root.mainloop()