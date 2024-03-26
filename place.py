from tkinter import Canvas
from calculate import index_to_coord, compare_distance
import constants
from shape import Shape, Ant, Berry, Hex, Web, Spider
from interface import TakeButton, DropButton, Timer
import random


class Place(Canvas):
    ants = []
    hexes_dict = {}
    invisible_hexes_dict = {}
    berries = []
    btn_list = []
    cobwebs = []
    spiders = []

    def __init__(self, root):
        super().__init__(
            root,
            width=constants.WIDTH_WINDOW,
            height=constants.HEIGHT_WINDOW,
        )
        self.place(x=0, y=0, anchor='nw')
        self.create_hexes()
        self.create_anthill()

        self.ants = [
            Ant((6, 5), self, 'Василий'),
            Ant((7, 6), self, 'Игорь'),
            Ant((5, 5), self, 'Коля'),
        ]

        self.bind('<Button-3>', self.activate)
        self.do_invisible_hexes_start()
        self.create_cobwebs(constants.NUMBER_OF_COBWEBS)
        self.create_spiders(constants.NUMBER_OF_SPIDERS)
        self.create_berries(constants.NUMBER_OF_BERRIES)
        self.create_timer(constants.TIME)

    def activate(self, event):
        print('================================')
        self.select_obj(event)
        # print(self.list_of_hexes_nearby(6, 6))

    def select_obj(self, event):
        x, y = event.x, event.y
        for ant in self.ants:
            shift = ant.cell_size / 2
            if ant.selected or ant.stuck or abs(ant.x - x) > shift or abs(ant.y - y) > shift:
                ant.deselect()
                self.itemconfig(ant.obj, image=ant.get_image())
                continue
            ant.select()
            self.itemconfig(ant.obj, image=ant.get_image())
            print(ant.name, 'выбран')
            # self.bind('<Button-1>', ant.move_obj) было/работает
            self.bind('<Button-1>', lambda event, arg=ant: self.ant_direction(event, arg))
            if not ant.carries:
                for berry in self.berries:
                    if berry.has_matching_indexes_with(ant) and not berry.taken:
                        self.btn_list.append(TakeButton(self, "Взять", ant.x, ant.y))
                        break
                hexes_indexes_nearby = self.list_of_hexes_indexes_nearby(ant)
                for ant_friend in self.ants:
                    if (ant_friend.i, ant_friend.j) in hexes_indexes_nearby and ant_friend.stuck:
                        print("Друг в беде!", ant_friend.name, ant_friend.i, ant_friend.j)
            else:
                if self.hexes_dict.get((ant.i, ant.j)).is_anthill:
                    self.btn_list.append(DropButton(self, 'Бросить', ant.x, ant.y))
                    print(ant.name, 'дома с ягодкой')
            break

    def ant_direction(self, event, ant):
        # Не работает как надо. Деректива должна автоматом: сходить или снять паутину рядом
        print(self.hexes_dict[ant.i, ant.j].enemy)
        if not self.hexes_dict[ant.i, ant.j].enemy:  # enemy не работает. Паутина становится врагом после появления :(
            ant.move_obj(event)

    def create_hexes(self):
        center = index_to_coord((6, 6))
        for i in range(12):
            for j in range(12):
                if compare_distance(index_to_coord((i, j)), center, '<=', 300):
                    self.hexes_dict[(i, j)] = Hex((i, j), self)

    def create_anthill(self):
        for index in ((6, 6), (6, 5), (5, 5), (5, 6), (6, 7), (7, 5), (7, 6)):
            self.itemconfig(self.hexes_dict.get(index).obj, fill=constants.BROWN)
            self.hexes_dict.get(index).is_anthill = True

    def do_invisible_hexes_start(self):
        center_hex = self.hexes_dict.get((6, 6))
        for index, hex in self.hexes_dict.items():
            if compare_distance((hex.x, hex.y), (center_hex.x, center_hex.y), '>=', constants.HEX_LENGTH * 4):
                hex.visible = False
                self.itemconfig(hex.obj, fill=constants.GREY)
                self.invisible_hexes_dict[index] = hex  # Пополняем invisible_hexes_dict невидимыми гексами

    def list_of_hexes_indexes_nearby(self, shape: Shape) -> list[tuple[int, int]]:
        x, y = shape.x, shape.y
        hexes_nearby = [index for index, hex in self.hexes_dict.items()
                        if compare_distance((hex.x, hex.y), (x, y), '<', constants.HEX_LENGTH * 2)]
        return hexes_nearby

    def create_berries(self, quantity: int) -> None:
        '''
        Fill up self.berries with random Berry objects
        returns: None
        '''
        hexes_indexes_of_berry = [indexes for indexes, hex in self.hexes_dict.items()
                                  if not hex.is_anthill and not hex.enemy]

        berries_names = random.sample(constants.BERRIES_NAMES, quantity)
        indexes_of_berry_hex = random.sample(hexes_indexes_of_berry, quantity)

        self.berries = [Berry(index, self, name)
                        for index, name in
                        list(zip(indexes_of_berry_hex, berries_names))]

        for berry in self.berries:
            if self.hexes_dict[(berry.i, berry.j)].visible:
                berry.show()

    def ant_takes_berry(self):
        ant = next(filter(lambda ant: ant.selected, self.ants), None)
        if ant is None:
            return  # TODO custom error raise
        ant.deselect()
        self.itemconfig(ant.obj, image=ant.get_image())

        for berry in self.berries:
            if berry.has_matching_indexes_with(ant) and not ant.carries:
                selected_berry = berry
                break

        ant.carries = selected_berry
        selected_berry.take()
        self.itemconfig(selected_berry.obj, image=selected_berry.get_image())
        print(ant.name, 'загружен', selected_berry.name)

    def ant_drops_berry(self):
        ant = next(filter(lambda ant: ant.selected, self.ants), None)
        if ant is None:
            return  # TODO custom error raise
        ant.selected = False
        selected_berry = ant.carries
        ant.carries = None
        selected_berry.throw()
        self.itemconfig(ant.obj, image=ant.get_image())
        self.itemconfig(selected_berry.obj, image=selected_berry.get_image())
        print(ant.name, 'разгружен', selected_berry.name)

    def create_cobwebs(self, number):
        for i in range(number):
            web = Web((5+i, 3), self)
            self.cobwebs.append(web)
            self.hexes_dict[web.i, web.j].enemy = web

    def create_spiders(self, number):
        for i in range(number):
            spider = Spider((5+i, 2), self)
            self.spiders.append(spider)
            self.hexes_dict[spider.i, spider.j].enemy = spider

    def create_timer(self, time):
        self.timer = Timer(self, time, 360, 20)
        # self.timer.start()
