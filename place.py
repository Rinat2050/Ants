from tkinter import Canvas
from calculate import index_to_coord
import constants
from shape import Ant, Berry, Hex
from interface import TakeButton, DropButton
import random

class Place(Canvas):
    ants_list = []
    hexes_dict = {}
    invisible_hexes_dict = {}
    berries_dict = {}
    btn_list = []

    def __init__(self, root):
        super().__init__(
            root,
            width=constants.WIDTH_WINDOW,
            height=constants.HEIGHT_WINDOW,
        )
        self.place(x=0, y=0, anchor='nw')
        self.create_hexes()
        self.create_anthill()

        self.ant1 = Ant(6, 5, self, 'Василий')
        self.ant2 = Ant(7, 6, self, 'Игорь')
        self.ants_list.append(self.ant1)
        self.ants_list.append(self.ant2)


        # self.berry1 = Berry(6, 4, self, 'Малинка')
        # self.berries_dict[(6, 4)] = self.berry1

        self.bind('<Button-3>', self.activate)
        self.do_invisible_hexes_start()

        self.create_berries(constants.NUMBER_OF_BERRIES)

    def activate(self, event):
        self.select_obj(event)

    def select_obj(self, evemt):
        x = evemt.x
        y = evemt.y
        for ant in self.ants_list:
            shift = ant.cell_size / 2
            if not ant.selected and abs(ant.x - x) <= shift and abs(ant.y - y) <= shift:
                print(ant.name, 'выбран')
                ant.selected = True
                self.bind('<Button-1>', ant.move_obj)
                self.itemconfig(ant.obj, image=ant.photo_selected_True)
                for berry in self.berries_dict.values():
                    if berry.i == ant.i and berry.j == ant.j and not berry.taken:

                        if not berry.visible:
                            berry.do_visible_berry()

                        btn_take = TakeButton(self, "Взять", 200, 800)
                        self.btn_list.append(btn_take)


                if ant.loading and self.hexes_dict.get((ant.i, ant.j)).is_anthill:
                    btn_drop = DropButton(self, 'Бросить', 300, 800)
                    self.btn_list.append(btn_drop)
                    print(ant.name, 'дома с ягодкой')

            else:
                ant.selected = False

    def create_hexes(self):
        for i in range(12):
            for j in range(12):
                if (index_to_coord(i - 6, j)[0]) ** 2 + (index_to_coord(i, j - 6)[1]) ** 2 <= 300 ** 2:
                    b = Hex(i, j, self)
                    self.hexes_dict[(i, j)] = b

    def create_anthill(self):
        for hex_index in self.hexes_dict.keys():
            if hex_index in ((6, 6), (6, 5), (5, 5), (5, 6), (6, 7), (7, 5), (7, 6)):
                self.itemconfig(self.hexes_dict.get(hex_index).obj, fill=constants.BROWN)
                self.hexes_dict.get(hex_index).is_anthill = True

    def do_invisible_hexes_start(self):
        x = self.hexes_dict.get((6, 6)).x
        y = self.hexes_dict.get((6, 6)).y
        for indexes, hex_object in self.hexes_dict.items():
            if (hex_object.x - x) ** 2 + (hex_object.y - y) ** 2 >= (constants.HEX_LENGTH * 4) ** 2:
                self.itemconfig(hex_object.obj, fill=constants.GREY)
                hex_object.visible = False
                self.invisible_hexes_dict[indexes] = hex_object # Пополняем invisible_hexes_dict невидимыми гексами

    def create_berries(self, number):
        invisible_hexes_indexes = [indexes for indexes in self.invisible_hexes_dict]
        berries_name_list = ['смородина', 'малина', 'клубника', 'земляника', 'брусника', 'рябина', 'клюква', 'ирга',
                             'калина', 'шиповник']

        for _ in range(number):
            indexes = random.choice(invisible_hexes_indexes)
            index_i = indexes[0]
            index_j = indexes[1]
            invisible_hexes_indexes.remove(indexes)

            berry_name = random.choice(berries_name_list)
            berries_name_list.remove(berry_name)

            value = Berry(index_i, index_j, self, berry_name)
            self.berries_dict[indexes] = value


    def ant_takes_berry(self):
        for selected_ant in self.ants_list:
            if selected_ant.selected is True:
                self.itemconfig(selected_ant.obj, image=selected_ant.photo_selected_False)
                selected_berry = self.berries_dict[(selected_ant.i, selected_ant.j)]
                selected_ant.loading = selected_berry
                selected_berry.taken = True
                self.itemconfig(selected_berry.obj, image=selected_berry.photo_selected_True)
                print(selected_ant.name, 'загружен', selected_berry.name)

    def ant_drops_berry(self):
        for selected_ant in self.ants_list:
            if selected_ant.selected is True:
                self.itemconfig(selected_ant.obj, image=selected_ant.photo_selected_False)
                selected_berry = self.berries_dict[(selected_ant.i, selected_ant.j)]
                selected_ant.loading = None
                selected_berry.taken = False
                self.itemconfig(selected_berry.obj, image=selected_berry.photo_selected_False)
                print(selected_ant.name, 'разгружен', selected_berry.name)
