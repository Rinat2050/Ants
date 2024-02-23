from tkinter import Tk, Canvas, Label
from math import cos, sin, pi


HEX_FIELD_X0 = 100
HEX_FIELD_Y0 = 100
HEX_LENGTH = 40
HEX_h = 0.5 * HEX_LENGTH * 3**0.5
HEIGHT_WINDOW = 990
WIDTH_WINDOW = 800


window = Tk()
window.title('ANTS')
window.geometry(str(WIDTH_WINDOW) + 'x' + str(HEIGHT_WINDOW) + '+1100+0')


class Place(Canvas):
    def __init__(self, root):
        super().__init__(root, width=WIDTH_WINDOW, height=HEIGHT_WINDOW)
        self.grid(row=0, column=0)

class Hex():
    def __init__(self, i, j, place_hex):
        self.i = i
        self.j = j
        self.x = self.index_to_coord()[0]
        self.y = self.index_to_coord()[1]
        self.place_hex = place_hex
        self.place_hex.create_polygon(self.count_coord(self.x, self.y), fill="#80CBC4", outline="#004D40")
        self.lbl = Label(self.place_hex, text=(i, j))
        self.lbl.place(x=HEX_FIELD_X0 + self.x , y=HEX_FIELD_Y0+self.y, anchor='center')
    @staticmethod
    def count_coord(center_x, center_y):
        coordinates = []
        for i in range(6):
            vertex_x = HEX_FIELD_X0 + int(center_x + HEX_LENGTH * cos(i * 2 * pi / 6))
            vertex_y = HEX_FIELD_Y0 + int(center_y + HEX_LENGTH * sin(i * 2 * pi / 6))
            coordinates.append(vertex_x)
            coordinates.append(vertex_y)
        return coordinates


    def index_to_coord(self):
        if self.i % 2 == 0:
            column_y = 0
        else:
            column_y = HEX_h
        x = i * HEX_LENGTH*1.5
        y = j * 2 * HEX_h + column_y
        # x = int(HEX_FIELD_X0 + self.i * HEX_LENGTH * cos(self.j * 2 * pi / 6))
        # y = int(HEX_FIELD_Y0 + self.j * HEX_LENGTH * sin(self.j * 2 * pi / 6))
        return x, y

def index_to_coord(i, j):
    if i % 2 == 0:
        column_y = 0
    else:
        column_y = HEX_h
    x = i * HEX_LENGTH*1.5
    y = j * 2 * HEX_h + column_y
    # x = int(HEX_FIELD_X0 + self.i * HEX_LENGTH * cos(self.j * 2 * pi / 6))
    # y = int(HEX_FIELD_Y0 + self.j * HEX_LENGTH * sin(self.j * 2 * pi / 6))
    return x, y

place_hex = Place(window)

for i in range(12):
    for j in range(12):
        if (index_to_coord(i - 6, j)[0])**2 + (index_to_coord(i, j - 6)[1])**2 <= 350**2:
            b = Hex(i, j, place_hex)


print(b.count_coord(100, 100))

window.mainloop()