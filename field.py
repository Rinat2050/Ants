from tkinter import Canvas
from calculate import compare_distance, get_for_list
import constants
from shape import Shape, Berry, Web, Spider, Ant
from interface import TakeButton, DropButton, Timer, GameProgressbar, HelpButton
import random
from hexes import Hexes


class Field(Canvas):
    def __init__(self, root):
        super().__init__(
            root,
            width=constants.WIDTH_WINDOW,
            height=constants.HEIGHT_WINDOW,
            bg='grey',
        )
        self.place(x=0, y=0, anchor='nw')
        self.hexes = Hexes(constants.ROUNDS, 1, self)
        self.hexes_dict = self.hexes.hexes_dict
        self.do_visible_hexes(self.hexes_dict[0, 0], 1)
        self.create_anthill()
        self.create_ant((0, 0), 'Василий')
        self.create_ant((0, 0), 'Игорь')
        self.create_ant((1, 0), 'Коля')
        self.create_random_objects(Web, constants.NUMBER_OF_COBWEBS, 'is_anthill', 'load')
        self.create_random_objects(Spider, constants.NUMBER_OF_SPIDERS, 'is_anthill', 'load')
        self.create_random_objects(Berry, constants.NUMBER_OF_BERRIES, 'is_anthill', 'load')
        self.create_timer(constants.TIME)
        self.create_progressbar(constants.TIME)

    def activate(self, event):
        """Клик правой клавишей мыши"""
        print('================================')
        for hex in self.hexes_dict.values():
            hex.del_buttons()
        for ant in Ant.ants:
            ant.deselect()
        index = self.coord_to_index(event)
        hex = self.hexes_dict.get(index, None)
        if hex is None:
            print("Нет гекса")
            return None
        if get_for_list(hex.ant, 0):
            self.select_obj(hex)
        else:
            print("Гекс без муравья")

    def select_obj(self, hex):
        """Действия муравья"""
        ant = get_for_list(hex.ant, 0)
        print(ant.name, "выбран", (hex.i, hex.j))
        if type(hex.load) is Web or type(hex.load) is Spider:
            print('Я застакан :(')
            return
        ant.select()
        if ant.carries:
            if hex.is_anthill:
                hex.buttons.append(DropButton(self, 'Положить', hex))
        else:
            if type(hex.load) is Berry:
                hex.buttons.append(TakeButton(self, "Взять", hex))
        for index in self.hexes.find_neighbors(hex):
            friend_hex = self.hexes.hexes_dict[index]
            friend_ant = get_for_list(friend_hex.ant, 0)
            if friend_ant and friend_ant.stuck:
                print("Друг в беде!", friend_ant.name, (friend_ant.i, friend_ant.j))
                hex.buttons.append(HelpButton(self, "Спасти", hex))

    def operate(self, event):
        """Клик левой клавишей мыши"""
        for hex_start in self.hexes_dict.values():
            hex_start_ant = get_for_list(hex_start.ant, 0)
            if hex_start_ant and hex_start_ant.selected:
                hex_start_ant.deselect()
                hex_start.del_buttons()
                index = self.coord_to_index(event)
                hex_finish = self.hexes_dict.get(index, None)
                hex_finish_ant = get_for_list(hex_finish.ant, 0)
                if not hex_finish or hex_finish_ant:
                    return
                if (hex_finish.i, hex_finish.j) in self.hexes.find_neighbors(hex_start):
                    ant_traveler = hex_start_ant
                    hex_start_ant.move(hex_finish)
                    hex_start.ant.remove(hex_start_ant)
                    hex_finish.ant.append(ant_traveler)
                    break

    def ant_takes_berry(self, hex):
        hex.ant[0].deselect()
        hex.ant[0].carries = hex.load
        hex.load = None
        hex.ant[0].carries.take()
        print(hex.ant[0].name, 'взял ягоду')

    def ant_drops_berry(self, hex):
        hex.ant[0].deselect()
        hex.warehouse.append(hex.ant[0].carries)
        hex.warehouse[-1].throw()
        hex.ant[0].carries = None
        print(hex.ant[0].name, 'положил ягоду')

    def ant_direction(self, event, ant):
        # Не работает как надо. Деректива должна автоматом: сходить или снять паутину рядом
        # if not self.hexes_dict[ant.i, ant.j].enemy:  # enemy не работает. Паутина становится врагом после появления :(
        #     ant.move_obj(event)
        print('--не пойду! Там враг!')

    def create_anthill(self):
        for index in ((0, 0),):
            self.itemconfig(self.hexes_dict.get(index).obj, fill=constants.BROWN)
            self.hexes_dict.get(index).is_anthill = True
            self.hexes_dict.get(index).create_warehouse()

    def do_visible_hexes(self, hex_in_center, round=0):
        # center_hex = self.hexes_dict.get((0, 0))
        # for index, hex in self.hexes_dict.items():
        #     if compare_distance((hex.x, hex.y), (center_hex.x, center_hex.y), '>=',
        #     constants.HEX_LENGTH * invisible_rounds):
        #         hex.visible = False
        #         self.itemconfig(hex.obj, fill=constants.GREY)
        #         self.invisible_hexes_dict[index] = hex  # Пополняем invisible_hexes_dict невидимыми гексами
        list_of_visible = self.hexes.find_neighbors_round(hex_in_center, round)
        for index in list_of_visible:
            self.hexes_dict[index].visible = True
            self.itemconfig(self.hexes_dict[index].obj, fill=constants.GREEN)

    def list_of_hexes_indexes_nearby(self, shape: Shape) -> list[tuple[int, int]]:
        x, y = shape.x, shape.y
        hexes_nearby = [index for index, hex in self.hexes_dict.items()
                        if compare_distance((hex.x, hex.y), (x, y), '<', constants.HEX_LENGTH * 2)]
        return hexes_nearby

    def create_random_objects(self, class_name, quantity: int, *invalid_places: tuple) -> list:
        '''
        Fill up random objects. Returns: list
        '''
        hexes_indexes = set([indexes for indexes in self.hexes_dict.keys()])
        for atribute in invalid_places:
            for hex in self.hexes_dict.values():
                if hex.__dict__[atribute]:
                    hexes_indexes.discard((hex.i, hex.j))
        indexes_of_objects_hex = random.sample(list(hexes_indexes), quantity)
        for hex in self.hexes_dict.values():
            if (hex.i, hex.j) in indexes_of_objects_hex:
                elem = class_name(self, hex)
                hex.load = elem
                if self.hexes_dict[(hex.i, hex.j)].visible:
                    elem.show()

    def create_ant(self, index, name):
        ant = Ant(self, self.hexes_dict[index], name)
        # Field.ants.append(ant)
        self.hexes_dict[index].ant.append(ant)

    def create_timer(self, time):
        self.timer = Timer(self, time, 999, 70)

    def create_progressbar(self, time):
        self.progressbar = GameProgressbar(self, time, 999, 40)

    def coord_to_index(self, event):
        x, y = event.x, event.y
        for hex in self.hexes_dict.values():
            if compare_distance((hex.x, hex.y), (x, y), '<=', constants.HEX_h):
                return (hex.i, hex.j)
        return ("Гекс не найден")
