__author__ = 'Tom'

import random
import pickle
from tkinter import *
from tkinter.ttk import *
from client import *
from server import *
from cards import *

class PlayerCanvas:
    def __init__(self, root, position):
        self.canvas = Canvas(root, width=145, height=115)
        self.cards = []
        self.chips = None
        self.chip_total = 50
        self.position = position

    def get_position(self):
        positions = ((400, 470), (75, 450), (75, 250), (75, 60), (400, 60), (725, 60), (725, 250), (725, 450),)
        return positions[self.position]

class PlayerGUI:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(self.root, width=800, height=520)
        self.pot = self.canvas.create_text(400, 320, text="Pot: 0")
        #self.player_frame = Frame(self.root)
        #self.bet = Scale(self.player_frame, from_=0, command=self.scale_bet)
        #self.lbl_bet = Label(self.player_frame, text=0)
        #self.btn_bet = Button(self.player_frame, text='Bet', command=self.place_bet, state=DISABLED)
        #self.btn_fold = Button(self.player_frame, text='Fold', state=DISABLED)
        self.players = []
        self.face_down_image = PhotoImage(file="cards/b1fv.gif")
        self.cards = self.get_cards()
        self.num_cards = 0
        self.add_widgets()
        self.add_canvas_widgets()
        self.last_updated = None
        HOST, PORT = "localhost", random.randint(10000, 60000)
        self.server = Server(HOST, PORT)
        self.conn = Client("localhost", 50007)
        self.conn.send((HOST, PORT))
        self.update_widgets()

    def add_widgets(self):
        self.root.title("Poker")
        self.root.geometry("800x580")
        self.root.resizable(0, 0)
        #self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.canvas.pack(fill='both', expand='yes')
        #self.player_frame.pack()
        #self.bet.grid(row=0, column=0)
        #self.lbl_bet.grid(row=0, column=1)
        #self.btn_bet.grid(row=1, column=0)
        #self.btn_fold.grid(row=1, column=1)

    def add_canvas_widgets(self):
        for i in range(8):
            player_canvas = PlayerCanvas(self.canvas, i)
            for j in range(2):
                player_canvas.cards.append(player_canvas.canvas.create_image(70 * j + 5, 50,
                                                                             image=self.face_down_image, anchor=W))
            player_canvas.chips = player_canvas.canvas.create_text(75, 110, text="Chips: {}".format(player_canvas.chip_total))
            self.canvas.create_window(player_canvas.get_position(), window=player_canvas.canvas)
            self.players.append(player_canvas)

    def update_widgets(self):
        try:
            data = pickle.load(open("data.p", "rb"))
        except (IOError, EOFError):
            pass
        else:
            if self.last_updated is None or self.last_updated < data["timestamp"]:
                print("Updating widgets...")
                for key, value in data.items():
                    if key == "players":
                        for player in value:
                            player_canvas = self.players[player]
                            if "cards" in data:
                                for card in data["cards"][player]:
                                    print(card)

                self.last_updated = data["timestamp"]
                
        self.root.after(5000, self.update_widgets)

    def get_cards(self):
        cards = {}
        deck = Deck()
        for card in deck:
            cards[hash(card)] = PhotoImage(file=card.get_image())
        return cards

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

    def new_game(self, player_data):
        for i, player in enumerate(player_data):
            images = [self.face_down_image,] * 2
            player_canvas = PlayerCanvas(self.canvas, i)
            if not i:
                images = [self.cards[hash(card)] for card in player["cards"]]
                self.bet.config(to=int(player["chips"]))
            for j, image in enumerate(images):
                player_canvas.cards.append(player_canvas.canvas.create_image(70 * j + 5, 50, image=image, anchor=W))
            player_canvas.chip_total = int(player["chips"])
            player_canvas.chips = player_canvas.canvas.create_text(75, 110, text="Chips: {}".format(player_canvas.chip_total))
            self.canvas.create_window(player_canvas.get_position(), window=player_canvas.canvas)
            self.players.append(player_canvas)

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

if __name__ == "__main__":
    root = Tk()
    gui = PlayerGUI(root)
    root.mainloop()