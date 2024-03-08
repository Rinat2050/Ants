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
    hex_list = []
    ant_list = []

    def __init__(self, root):
        super().__init__(
            root,
            width=constants.WIDTH_WINDOW,
            height=constants.HEIGHT_WINDOW,
        )
        self.place(x=0, y=0, anchor='nw')
        self.create_hex()

        self.ant1 = Ant(6, 11, self)
        self.ant2 = Ant(6, 1, self)
        self.ant_list.append(self.ant1)
        self.ant_list.append(self.ant2)
        self.bind('<Button-3>', self.select_obj)

    def select_obj(self, evemt):
        x = evemt.x
        y = evemt.y

        for ant in self.ant_list:
            shift = ant.cell_size / 2
            if (ant.selected is False) and (ant.x - shift <= x <= ant.x + shift) and (ant.y - shift <= y <= ant.y + shift):
                ant.selected = True
                self.bind('<Button-1>', ant.move_obj)
                print('selected True?')
            else:
                ant.selected = False
                print('selected False')
                    # self.canvas.create_oval(x-1, y-1,x+1, y+1, fill='black') - показывает точками где тыкаем

    def create_hex(self):
        for i in range(12):
            for j in range(12):
                if (index_to_coord(i - 6, j)[0]) ** 2 + (index_to_coord(i, j - 6)[1]) ** 2 <= 350 ** 2:
                    b = Hex(i, j, self)
                    self.hex_list.append(b)



place_hex = Place(window)

window.mainloop()
