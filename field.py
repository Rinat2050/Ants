from tkinter import Canvas
from calculate import index_to_coord, compare_distance
import constants
from shape import Shape, Ant, Berry, Hex, Web, Spider
from interface import TakeButton, DropButton, Timer
import random


class Field(Canvas):
    ants = []
    hexes_dict = {}
    invisible_hexes_dict = {}
    btn_list = []

    def __init__(self, root):
        super().__init__(
            root,
            width=constants.WIDTH_WINDOW,
            height=constants.HEIGHT_WINDOW,
            bg='grey',
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

        self.cobwebs = self.create_random_objects(Web,
                                                  constants.NUMBER_OF_COBWEBS, 'is_anthill')
        self.spiders = self.create_random_objects(Spider,
                                                  constants.NUMBER_OF_SPIDERS, 'is_anthill', 'enemy')
        self.berries = self.create_random_objects(Berry,
                                                  constants.NUMBER_OF_BERRIES, 'is_anthill', 'enemy')
        self.create_timer(constants.TIME)
        self.bind('<Button-3>', self.activate)

    def activate(self, event):
        print('================================')
        self.select_obj(event)
        #  print(self.list_of_hexes_nearby(6, 6))

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
            self.bind('<Button-1>', lambda e, arg=ant: self.ant_direction(e, arg))
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
        # print(self.hexes_dict[ant.i, ant.j].enemy)
        if not self.hexes_dict[ant.i, ant.j].enemy:  # enemy не работает. Паутина становится врагом после появления :(
            ant.move_obj(event)
        print('--не пойду! Там враг!')

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

    def create_random_objects(self, class_name, quantity: int, *invalid_places: tuple) -> list:
        '''
        Fill up random objects
        returns: None
        '''

        hexes_indexes = set([indexes for indexes in self.hexes_dict.keys()])


    def create_random_objects(self, class_object, quantity: int, *invalid_places: tuple) -> None:
        '''
        Fill up random objects
        returns: None
        '''
        hexes_indexes = set()

        for atribute in invalid_places:
            for hex in self.hexes_dict.values():
                if hex.__dict__[atribute]:
                    hexes_indexes.discard((hex.i, hex.j))

        indexes_of_objects_hex = random.sample(list(hexes_indexes), quantity)
        objects = [class_object(index, self)
                   for index in list(indexes_of_objects_hex)]
        for obj in objects:
            if self.hexes_dict[(obj.i, obj.j)].visible:
                obj.show()
        return objects

    def ant_takes_berry(self):
        ant = next(filter(lambda ant: ant.selected, self.ants), None)
        if ant is None:
            return  # TODO custom error raise or pass like argument ant object
        ant.deselect()
        self.itemconfig(ant.obj, image=ant.get_image())

        for berry in self.berries:
            if berry.has_matching_indexes_with(ant) and not ant.carries:
                selected_berry = berry
                break

        ant.carries = selected_berry
        selected_berry.take()
        self.itemconfig(selected_berry.obj, image=selected_berry.get_image())
        print(ant.name, 'взял ягоду')

    def ant_drops_berry(self):
        ant = next(filter(lambda ant: ant.selected, self.ants), None)
        if ant is None:
            return  # TODO custom error raise or pass like argument ant object
        ant.selected = False
        selected_berry = ant.carries
        ant.carries = None
        selected_berry.throw()
        self.itemconfig(ant.obj, image=ant.get_image())
        self.itemconfig(selected_berry.obj, image=selected_berry.get_image())
        print(ant.name, 'бросил ягоду')

    def create_timer(self, time):
        self.timer = Timer(self, time, 360, 20)
