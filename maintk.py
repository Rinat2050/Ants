from tkinter import Tk, Canvas
from math import cos, sin, pi


HEX_FIELD_X0 = 150
HEX_FIELD_Y0 = 150
# HEX_WIDTH = 100
# HEX_HEIGHT = int(HEX_WIDTH * (3 ** 0.5 / 2))
HEX_LENGTH = 50

window = Tk()
window.title('ANTS')
window.geometry('500x500')


class Place(Canvas):
    def __init__(self, root):
        super().__init__(root, width=500, height=500)
        self.grid(row=0, column=0)

class Hex():
    def __init__(self, i, j, place):
        self.i = i
        self.j = j
        self.x = self.index_to_coord()[0]
        self.y = self.index_to_coord()[1]
        self.place = place
        self.place.create_polygon(self.count_coord(self.x, self.y), fill="#80CBC4", outline="#004D40")
    @staticmethod
    def count_coord(center_x, center_y):
        coordinates = []
        for i in range(6):
            vertex_x = int(center_x + HEX_LENGTH * cos(i * 2 * pi / 6))
            vertex_y = int(center_y + HEX_LENGTH * sin(i * 2 * pi / 6))
            coordinates.append(vertex_x)
            coordinates.append(vertex_y)
        return coordinates


    def index_to_coord(self):
        x = int(HEX_FIELD_X0 + self.i * HEX_LENGTH * cos(self.j * 2 * pi / 6))
        y = int(HEX_FIELD_Y0 + self.j * HEX_LENGTH * sin(self.j * 2 * pi / 6))
        return x, y


a = Place(window)

a.create_line(0, 0, 200, 50)

b = Hex(1, 1, a)
c = Hex(1, 2, a)
d = Hex(1, 3, a)
e = Hex(1, 4, a)
f = Hex(1, 5, a)
g = Hex(1, 6, a)

print(b.count_coord(100, 100))

window.mainloop()
