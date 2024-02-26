from tkinter import Tk, Canvas, Label
from calculate import index_to_coord
from constants import *
from PIL import ImageTk, Image
import os

class Ant(Canvas):
    def __init__(self, i, j, root):
        super().__init__(root, width=30, height=30, bd=0, highlightthickness=0)
        self.i = i
        self.j = j
        self.x = HEX_FIELD_X0 + index_to_coord(i, j)[0]
        self.y = HEX_FIELD_Y0 + index_to_coord(i, j)[1]
        self.radius = 18
        self.image = Image.open("image/ant.png").resize((50, 50))
        self.ant_image = ImageTk.PhotoImage(self.image)
        self.panel = Label(root, image = self.ant_image, text = "Ant")
        self.panel.place(x=self.x, y=self.y, anchor='center', )
        self.bind('<B1-Motion>', self.move)
        self.lbl = Label(root, text=(self.i, self.j))
        self.lbl.place(x=self.x, y=self.y+5, anchor='n')

    def move(self, event):
        pass
