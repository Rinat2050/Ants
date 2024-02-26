from tkinter import Tk, Canvas
from ant import Ant
from hex import Hex
from constants import *
from calculate import index_to_coord


window = Tk()
window.title('ANTS')
window.geometry(str(WIDTH_WINDOW) + 'x' + str(HEIGHT_WINDOW) + '+1100+0')


class Place(Canvas):
    def __init__(self, root):
        super().__init__(root, width=WIDTH_WINDOW, height=HEIGHT_WINDOW)
        self.place(x=0, y=0, anchor='nw')



place_hex = Place(window)

for i in range(12):
    for j in range(12):
        if (index_to_coord(i - 6, j)[0])**2 + (index_to_coord(i, j - 6)[1])**2 <= 350**2:
            b = Hex(i, j, place_hex)

ant = Ant(6, 11, window)


window.mainloop()