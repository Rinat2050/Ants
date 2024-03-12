from tkinter import Canvas
from ant import Ant
from hex import Hex
from calculate import index_to_coord
import constants


class Place(Canvas):
    hex_list = []
    ant_list = []
    hex_dict = {}

    def __init__(self, root):
        super().__init__(
            root,
            width=constants.WIDTH_WINDOW,
            height=constants.HEIGHT_WINDOW,
        )
        self.place(x=0, y=0, anchor='nw')
        self.create_hex()
        self.create_anthill()

        self.ant1 = Ant(5, 5, self, 'Василий')
        self.ant2 = Ant(7, 6, self, 'Игорь')
        self.ant_list.append(self.ant1)
        self.ant_list.append(self.ant2)
        self.bind('<Button-3>', self.select_obj)
        self.do_invisible_hex_start()

    def select_obj(self, evemt):
        x = evemt.x
        y = evemt.y
        for ant in self.ant_list:
            shift = ant.cell_size / 2
            if (ant.selected is False) and (ant.x - shift <= x <= ant.x + shift) and (
                    ant.y - shift <= y <= ant.y + shift):
                ant.selected = True
                self.bind('<Button-1>', ant.move_obj)
                print(ant.name, 'выбран')
                self.itemconfig(ant.obj, image=ant.img_selected_True)
            else:
                ant.selected = False
                # print(ant.name, 'selected False')
                # self.canvas.create_oval(x-1, y-1,x+1, y+1, fill='black') - показывает точками где тыкаем

    def create_hex(self):
        for i in range(12):
            for j in range(12):
                if (index_to_coord(i - 6, j)[0]) ** 2 + (index_to_coord(i, j - 6)[1]) ** 2 <= 300 ** 2:
                    b = Hex(i, j, self)
                    self.hex_list.append(b)
                    self.hex_dict[(i, j)] = b

    def create_anthill(self):
        for elem_hex in self.hex_list:
            if [elem_hex.i, elem_hex.j] in ([6, 6], [6, 5], [5, 5], [5, 6], [6, 7], [7, 5], [7, 6]):
                self.itemconfig(elem_hex.obj, fill=constants.BROWN)

    def do_invisible_hex_start(self):
        x = self.hex_dict[(6, 6)].x
        y = self.hex_dict[(6, 6)].y
        for elem in self.hex_list:
            if (elem.x - x) ** 2 + (elem.y - y) ** 2 >= (constants.HEX_LENGTH * 4) ** 2:
                self.itemconfig(elem.obj, fill=constants.GREY)
                elem.visible = False
