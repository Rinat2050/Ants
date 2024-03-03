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
    ants_list = []
    def __init__(self, root):
        super().__init__(
            root,
            width=constants.WIDTH_WINDOW,
            height=constants.HEIGHT_WINDOW,
        )
        self.place(x=0, y=0, anchor='nw')
        self.create_hex()
        self.ant = Ant(6, 11, self)

    def create_hex(self):
        for i in range(12):
            for j in range(12):
                if (index_to_coord(i - 6, j)[0]) ** 2 + (index_to_coord(i, j - 6)[1]) ** 2 <= 350 ** 2:
                    b = Hex(i, j, self)
                    self.ants_list.append(b)



place_hex = Place(window)
# print(place_hex.ants_list)
# print(place_hex.ant.x, place_hex.ant.y)
# place_hex.ant.x = 300
# print(place_hex.ant.x, place_hex.ant.y)
window.mainloop()


