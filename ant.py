from tkinter import Tk, Canvas, Label
from calculate import index_to_coord
from constants import *

class Ant:
    def __init__(self, i, j, place_hex):
        self.i = i
        self.j = j
        self.x = HEX_FIELD_X0 + index_to_coord(i, j)[0]
        self.y = HEX_FIELD_Y0 + index_to_coord(i, j)[1]
        self.place_hex = place_hex
        self.radius = 18
        self.place_hex.create_oval(self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius, outline='red', width=3)
