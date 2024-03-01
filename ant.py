from tkinter import Tk, Canvas, Label
from calculate import index_to_coord
from constants import *
from PIL import ImageTk, Image
import os

class Ant:
    def __init__(self, i, j, canvas):
        self.canvas = canvas
        self.i = i
        self.j = j
        self.x = HEX_FIELD_X0 + index_to_coord(i, j)[0]
        self.y = HEX_FIELD_Y0 + index_to_coord(i, j)[1]
        self.cell_size = ANT_CELL_SIZE
        self.image = Image.open("image/ant.png").resize((self.cell_size, self.cell_size))
        self.ant_img = ImageTk.PhotoImage(self.image)
        self.ant_obj = self.canvas.create_image(self.x, self.y, anchor='center', image=self.ant_img)
        self.canvas.bind('<B1-Motion>', self.move_obj)
        self.canvas.bind('<ButtonRelease-1>', self.button_release)

    def move_obj(self, event):
        new_x = event.x
        new_y = event.y
        # print(new_x, new_y)
        self.canvas.coords(self.ant_obj,
                           new_x,
                           new_y
                           )
        self.search_hex(new_x, new_y)

    def search_hex(self, x, y):
        for hex in self.canvas.ants_list:
            if (x - hex.x)**2 + (y - hex.y)**2 <= HEX_h ** 2:
                #print(hex.i, hex.j)
                # print(hex.x, hex.y)
                self.i = hex.i
                self.j = hex.j
                return hex.x, hex.y

    def button_release(self, event):
        center_x = self.search_hex(event.x, event.y)[0]
        center_y = self.search_hex(event.x, event.y)[1]
        x_move = event.x - center_x
        y_move = event.y - center_y
        self.canvas.move(self.ant_obj, x_move, y_move)
        print(event.x, event.y)
        print(center_x, center_y)
        print(self.i, self.j)