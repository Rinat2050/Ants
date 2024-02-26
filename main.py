from tkinter import Tk, Canvas
from ant import Ant
from hex import Hex
from calculate import index_to_coord
import constants


window = Tk()
window.title('ANTS')
window.geometry('{w}x{h}+1100+0'.format(
    w=constants.WIDTH_WINDOW,
    h=constants.HEIGHT_WINDOW),
)


class Place(Canvas):
    def __init__(self, root):
        super().__init__(
            root,
            width=constants.WIDTH_WINDOW,
            height=constants.HEIGHT_WINDOW,
        )
        self.place(x=0, y=0, anchor='nw')


place_hex = Place(window)

for i in range(12):
    for j in range(12):
        x = index_to_coord(i - 6, j)[0]
        y = index_to_coord(i, j - 6)[1]
        if (x**2 + y**2) <= 350**2:
            b = Hex(i, j, place_hex)

ant = Ant(6, 11, window)


window.mainloop()
