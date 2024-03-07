from tkinter import Canvas, Label
from calculate import index_to_coord
from PIL import ImageTk, Image
import constants
import calculate

class Ant:
    def __init__(self, i, j, canvas):
        self.canvas = canvas
        self.i = i
        self.j = j
        x, y = index_to_coord(i, j)
        self.x = constants.HEX_FIELD_X0 + x
        self.y = constants.HEX_FIELD_Y0 + y
        self.cell_size = constants.ANT_CELL_SIZE
        self.image = Image.open("image/ant.png").resize((self.cell_size, self.cell_size))
        self.ant_img = ImageTk.PhotoImage(self.image)
        self.ant_obj = self.canvas.create_image(self.x, self.y, anchor='center', image=self.ant_img)
        self.canvas.bind('<Button-1>', self.move_obj)

    def move_obj(self, event):
        new_x = event.x
        new_y = event.y
        self.choise_hex(new_x, new_y)
        print(self.i, self.j)
        print(self.x, self.y)
        self.canvas.coords(self.ant_obj, self.x, self.y)

    def choise_hex(self, x, y):
        for hex in self.canvas.hex_list:
            if ((x - hex.x)**2 + (y - hex.y)**2 <= constants.HEX_h ** 2
                    and (self.x - hex.x)**2 + (self.y - hex.y)**2 <= 6*constants.HEX_h ** 2): # Позволяет передвигаться ТОЛЬКО на ближайшие хексы
                self.i = hex.i
                self.j = hex.j
                self.x = hex.x
                self.y = hex.y


