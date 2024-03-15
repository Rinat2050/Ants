from tkinter import Canvas
from calculate import index_to_coord
import constants
from shape import Ant, Berry, Hex
from interface import UserButton


class Place(Canvas):
    ant_list = []
    hex_dict = {}
    berry_list = []

    def __init__(self, root):
        super().__init__(
            root,
            width=constants.WIDTH_WINDOW,
            height=constants.HEIGHT_WINDOW,
        )
        self.place(x=0, y=0, anchor='nw')
        self.create_hex()
        self.create_anthill()

        self.ant1 = Ant(6, 5, self, 'Василий')
        self.ant2 = Ant(7, 6, self, 'Игорь')
        self.ant_list.append(self.ant1)
        self.ant_list.append(self.ant2)
        self.berry1 = Berry(6, 4, self)
        self.berry_list.append(self.berry1)
        self.bind('<Button-3>', self.activate)
        self.do_invisible_hex_start()
        self.bnt_take = UserButton(self, "Взять")

    def activate(self, event):
        self.select_obj(event)

        #
        #         button.plase


    def select_obj(self, evemt):
        x = evemt.x
        y = evemt.y
        for ant in self.ant_list:
            shift = ant.cell_size / 2
            if not ant.selected and abs(ant.x - x) <= shift and abs(ant.y - y) <= shift:
                print(ant.name, 'выбран')
                ant.selected = True
                self.bind('<Button-1>', ant.move_obj)
                self.itemconfig(ant.obj, image=ant.img_selected_True)
                for berry in self.berry_list:
                    if berry.i == ant.i and berry.j == ant.j:
                        self.bnt_take.visible()
            else:
                ant.selected = False
                # print(ant.name, 'selected False')
                # self.canvas.create_oval(x-1, y-1,x+1, y+1, fill='black') - показывает точками где тыкаем

    def create_hex(self):
        for i in range(12):
            for j in range(12):
                if (index_to_coord(i - 6, j)[0]) ** 2 + (index_to_coord(i, j - 6)[1]) ** 2 <= 300 ** 2:
                    b = Hex(i, j, self)
                    self.hex_dict[(i, j)] = b

    def create_anthill(self):
        for hex_index in self.hex_dict.keys():
            if hex_index in ((6, 6), (6, 5), (5, 5), (5, 6), (6, 7), (7, 5), (7, 6)):
                self.itemconfig(self.hex_dict.get(hex_index).obj, fill=constants.BROWN)

    def do_invisible_hex_start(self):
        x = self.hex_dict.get((6, 6)).x
        y = self.hex_dict.get((6, 6)).y
        for hex_val in self.hex_dict.values():
            if (hex_val.x - x) ** 2 + (hex_val.y - y) ** 2 >= (constants.HEX_LENGTH * 4) ** 2:
                self.itemconfig(hex_val.obj, fill=constants.GREY)
                hex_val.visible = False

    def ant_take(self):
        for selected_ant in self.ant_list:
            if selected_ant.selected is True:
                selected_ant.loading == True
                print(selected_ant.name, 'загружен')
