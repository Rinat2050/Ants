from tkinter import Canvas
from calculate import index_to_coord
import constants
from shape import Ant, Berry, Hex
from interface import TakeButton, DropButton


class Place(Canvas):
    ant_list = []
    hex_dict = {}
    berry_dict = {}
    btn_list = []

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
        self.berry1 = Berry(6, 4, self, 'Малинка')
        self.berry_dict[(6, 4)] = self.berry1
        self.bind('<Button-3>', self.activate)
        self.do_invisible_hex_start()

    def activate(self, event):
        self.select_obj(event)

    def select_obj(self, evemt):
        x = evemt.x
        y = evemt.y
        for ant in self.ant_list:
            shift = ant.cell_size / 2
            if not ant.selected and abs(ant.x - x) <= shift and abs(ant.y - y) <= shift:
                print(ant.name, 'выбран')
                ant.selected = True
                self.bind('<Button-1>', ant.move_obj)
                self.itemconfig(ant.obj, image=ant.photo_selected_True)
                for berry in self.berry_dict.values():
                    if berry.i == ant.i and berry.j == ant.j and not berry.taken:
                        self.btn_take = TakeButton(self, "Взять", 200, 800)
                        self.btn_list.append(self.btn_take)

                if ant.loading and self.hex_dict.get((ant.i, ant.j)).home:
                    self.btn_drop = DropButton(self, 'Бросить', 300, 800)
                    self.btn_list.append(self.btn_drop)

                    print('Дома?')

            else:
                ant.selected = False

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
                self.hex_dict.get(hex_index).home = True

    def do_invisible_hex_start(self):
        x = self.hex_dict.get((6, 6)).x
        y = self.hex_dict.get((6, 6)).y
        for hex_val in self.hex_dict.values():
            if (hex_val.x - x) ** 2 + (hex_val.y - y) ** 2 >= (constants.HEX_LENGTH * 4) ** 2:
                self.itemconfig(hex_val.obj, fill=constants.GREY)
                hex_val.visible = False

    def ant_takes_berry(self):
        for selected_ant in self.ant_list:
            if selected_ant.selected is True:
                self.itemconfig(selected_ant.obj, image=selected_ant.photo_selected_False)
                selected_berry = self.berry_dict[(selected_ant.i, selected_ant.j)]
                selected_ant.loading = selected_berry
                selected_berry.taken = True
                self.itemconfig(selected_berry.obj, image=selected_berry.photo_selected_True)
                print(selected_ant.name, 'загружен', selected_berry.name)

    def ant_drops_berry(self):
        for selected_ant in self.ant_list:
            if selected_ant.selected is True:
                self.itemconfig(selected_ant.obj, image=selected_ant.photo_selected_False)
                selected_berry = self.berry_dict[(selected_ant.i, selected_ant.j)]
                selected_ant.loading = None
                selected_berry.taken = False
                self.itemconfig(selected_berry.obj, image=selected_berry.photo_selected_False)
                print(selected_ant.name, 'разгружен', selected_berry.name)
