from tkinter import Canvas
from calculate import index_to_coord
import constants
from shape import Ant, Berry, Hex, Web, Spider
from interface import TakeButton, DropButton, Timer
import random

class Place(Canvas):
    ants_list = []
    hexes_dict = {}
    invisible_hexes_dict = {}
    berries_list = []
    btn_list = []
    cobwebs_list = []
    spiders_list = []


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
        self.ant3 = Ant(5, 5, self, 'Коля')
        self.ants_list.append(self.ant1)
        self.ants_list.append(self.ant2)
        self.ants_list.append(self.ant3)

        self.bind('<Button-3>', self.activate)
        self.do_invisible_hexes_start()
        self.create_cobwebs(constants.NUMBER_OF_COBWEBS)
        self.create_spiders(constants.NUMBER_OF_SPIDERS)
        self.create_berries(constants.NUMBER_OF_BERRIES)
        self.create_timer(constants.TIME)


    def activate(self, event):
        print('================================')
        self.select_obj(event)
        # print(self.search_hex_nearby(6, 6))


    def select_obj(self, evemt):
        x = evemt.x
        y = evemt.y
        for ant in self.ants_list:
            shift = ant.cell_size / 2
            if not ant.selected \
                    and not ant.stuck \
                    and abs(ant.x - x) <= shift and abs(ant.y - y) <= shift:
                print(ant.name, 'выбран')
                ant.selected = True
                self.bind('<Button-1>', ant.move_obj)
                #self.bind('<Button-1>', self.ant_direction)
                self.itemconfig(ant.obj, image=ant.photo_selected_True)
                if not ant.loading:
                    for berry in self.berries_list:
                        if berry.i == ant.i and berry.j == ant.j and not berry.taken:
                            btn_take = TakeButton(self, "Взять", ant.x, ant.y)
                            self.btn_list.append(btn_take)
                            break
                    for ant_friend in self.ants_list:
                        if (ant_friend.i, ant_friend.j) in self.search_hex_nearby(ant.i, ant.j) and ant_friend.stuck:
                            print("Друг в беде!", ant_friend.name, ant_friend.i, ant_friend.j)

                elif ant.loading:
                    if self.hexes_dict.get((ant.i, ant.j)).is_anthill:
                        btn_drop = DropButton(self, 'Бросить', ant.x, ant.y)
                        self.btn_list.append(btn_drop)
                        print(ant.name, 'дома с ягодкой')
                break

            else:
                ant.selected = False
                self.itemconfig(ant.obj, image=ant.photo_selected_False)

    def ant_direction(self, event):     # не работает. Деректива должна автоматом: сходить или снять паутину
        self.ant.move_obj(event)

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

    def search_hex_nearby(self, i, j) -> list[object]:
        list_hex_nearby = []
        x = self.hexes_dict.get((i, j)).x
        y = self.hexes_dict.get((i, j)).y
        for indexes, hex_object in self.hexes_dict.items():
            if (hex_object.x - x) ** 2 + (hex_object.y - y) ** 2 <= (constants.HEX_LENGTH * 2) ** 2:
                # list_hex_nearby.append(hex_object)
                list_hex_nearby.append(indexes)
        return list_hex_nearby

    def create_berries(self, number):
        #invisible_hexes_indexes = [indexes for indexes in self.invisible_hexes_dict]
        hexes_indexes_of_berry = []
        for indexes, hex_object in self.hexes_dict.items():
            if not hex_object.is_anthill and not hex_object.enemy:
                hexes_indexes_of_berry.append(indexes)

        berries_name_list = ['смородина', 'малина', 'клубника', 'земляника', 'брусника', 'рябина', 'клюква', 'ирга',
                             'калина', 'шиповник', 'голубика', 'ежевика', 'черешня', 'черника', 'бузина',
                             'вишня', 'черешня', 'жимолость', 'кизил', 'черёмуха']

        for _ in range(number):
            indexes = random.choice(hexes_indexes_of_berry)
            index_i = indexes[0]
            index_j = indexes[1]
            hexes_indexes_of_berry.remove(indexes)

            berry_name = random.choice(berries_name_list)
            berries_name_list.remove(berry_name)

            value = Berry(index_i, index_j, self, berry_name)
            self.berries_list.append(value)
            # value.do_visible_berry()  # показать все ягоды
        for hex_under_berry in self.berries_list:
            if self.hexes_dict[(hex_under_berry.i, hex_under_berry.j)].visible:
                hex_under_berry.do_visible_berry()

    def ant_takes_berry(self):
        for selected_ant in self.ants_list:
            if selected_ant.selected is True:
                self.itemconfig(selected_ant.obj, image=selected_ant.photo_selected_False)
                for berry in self.berries_list:
                    if (selected_ant.i, selected_ant.j) == (berry.i, berry.j) and not selected_ant.loading:
                        selected_berry = berry
                        break

                selected_ant.loading = selected_berry
                selected_berry.taken = True
                self.itemconfig(selected_berry.obj, image=selected_berry.photo_selected_True)
                print(selected_ant.name, 'загружен', selected_berry.name)
                selected_ant.selected = False

    def ant_drops_berry(self):
        for selected_ant in self.ants_list:
            if selected_ant.selected is True:
                self.itemconfig(selected_ant.obj, image=selected_ant.photo_selected_False)
                selected_berry = selected_ant.loading
                selected_ant.loading = None
                selected_berry.taken = False
                self.itemconfig(selected_berry.obj, image=selected_berry.photo_selected_False)
                print(selected_ant.name, 'разгружен', selected_berry.name)
                selected_ant.selected = False

    def create_cobwebs(self, number):
        for i in range(number):
            web = Web(5+i, 3, self)
            self.cobwebs_list.append(web)
            self.hexes_dict[web.i, web.j].enemy = web

    def create_spiders(self, number):
        for i in range(number):
            spider = Spider(5+i, 2, self)
            self.spiders_list.append(spider)
            print(spider.i, spider.j)
            self.hexes_dict[spider.i, spider.j].enemy = spider

    def create_timer(self, time):
        self.timer = Timer(self, time, 360, 20)
        #self.timer.start()