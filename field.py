from tkinter import Canvas
from calculate import get_for_list
import constants
from shape import Berry, Ant, Spider, Web
from interface import TakeButton, DropButton, HelpButton, UserButton
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

    def activate(self, event):
        """Клик правой клавишей мыши"""
        print('================================')

        for ant in Ant.instances:
            ant.deselect()
        index = self.coord_to_index(event)
        hex_act = self.hexes_dict.get(index, None)
        if hex_act is None:
            print("Нет гекса")
            return None
        if get_for_list(hex_act.ant, 0):
            self.select_obj(hex_act)
        else:
            print("Гекс без муравья")

    def select_obj(self, hex_selected):
        """Действия муравья"""
        ant = get_for_list(hex_selected.ant, 0)
        print(ant.name, "выбран", (hex_selected.i, hex_selected.j))
        if ant.stuck:
            print('Я застакан :(')
            return
        ant.select()
        if ant.carries:
            if hex_selected.is_anthill:
                DropButton(self, 'Положить', hex_selected)
        else:
            if type(hex_selected.load) is Berry:
                TakeButton(self, "Взять", hex_selected)
        for index in self.hexes.find_neighbors(hex_selected):
            friend_hex = self.hexes.hexes_dict[index]
            friend_ant = get_for_list(friend_hex.ant, 0)
            if friend_ant and friend_ant.stuck:
                print("Друг в беде!", friend_ant.name, (friend_ant.i, friend_ant.j))
                HelpButton(self, "Спасти", friend_hex, ant)

    def operate(self, event):
        """Клик левой клавишей мыши"""

        for hex_start in self.hexes_dict.values():
            hex_start_ant = get_for_list(hex_start.ant, 0)
            if hex_start_ant and hex_start_ant.selected:
                hex_start_ant.deselect()
                UserButton.delete_buttons()
                index = self.coord_to_index(event)
                hex_finish = self.hexes_dict.get(index, None)
                if not hex_finish:
                    return
                hex_finish_ant = get_for_list(hex_finish.ant, 0)
                if not hex_finish.is_anthill and hex_finish_ant:
                    return
                if (type(hex_finish.load) in (Spider, Web)) and hex_finish.visible:
                    print('--не пойду! Там враг!')
                    return
                if (hex_finish.i, hex_finish.j) in self.hexes.find_neighbors(hex_start):
                    ant_traveler = hex_start_ant
                    hex_start_ant.move(hex_finish)
                    hex_start.ant.remove(hex_start_ant)
                    hex_finish.ant.append(ant_traveler)
                    break

    @staticmethod
    def ant_takes_berry(hex_with_berry):
        hex_with_berry.ant[0].deselect()
        hex_with_berry.ant[0].carries = hex_with_berry.load
        hex_with_berry.load = None
        hex_with_berry.ant[0].carries.take()
        print(hex_with_berry.ant[0].name, f'взял {hex_with_berry.ant[0].carries.name[:-1]}у')

    @staticmethod
    def ant_drops_berry(hex_taker):
        hex_taker.ant[0].deselect()
        hex_taker.warehouse.append(hex_taker.ant[0].carries)
        hex_taker.warehouse[-1].throw()
        print(hex_taker.ant[0].name, f'положил {hex_taker.ant[0].carries.name[:-1]}у')
        hex_taker.ant[0].carries = None

    @staticmethod
    def ant_help_friend(hex_friend):
        get_for_list(hex_friend.ant, 0).stuck = False
        print(get_for_list(hex_friend.ant, 0).name, 'спасён!')

    def create_anthill(self):
        for index in ((0, 0),):
            self.itemconfig(self.hexes_dict.get(index).obj, fill=constants.BROWN)
            self.hexes_dict.get(index).is_anthill = True
            self.hexes_dict.get(index).warehouse = []

    def do_visible_hexes(self, hex_in_center, circle=0):
        list_of_visible = self.hexes.find_neighbors_round(hex_in_center, circle)
        for index in list_of_visible:
            self.hexes_dict[index].make_visible()

    def create_random_objects(self, class_name, quantity: int, *invalid_places):
        """Fill up random objects. Returns: list"""
        hexes_indexes = set([indexes for indexes in self.hexes_dict.keys()])
        for attribute in invalid_places:
            for hex_elem in self.hexes_dict.values():
                if hex_elem.__dict__[attribute]:
                    hexes_indexes.discard((hex_elem.i, hex_elem.j))
        indexes_of_objects_hex = random.sample(list(hexes_indexes), quantity)
        for hex_elem in self.hexes_dict.values():
            if (hex_elem.i, hex_elem.j) in indexes_of_objects_hex:
                elem = class_name(self, hex_elem)
                hex_elem.load = elem
                if self.hexes_dict[(hex_elem.i, hex_elem.j)].visible:
                    elem.show()

    def create_group_of_ants(self, number):
        for n in range(number):
            self.create_ant((0, 0), constants.ANTS_NAMES[n])

    def create_ant(self, index, name):
        ant = Ant(self, self.hexes_dict[index], name)
        # Field.ants.append(ant)
        self.hexes_dict[index].ant.append(ant)

    def coord_to_index(self, event):
        x, y = event.x, event.y
        for hex_elem in self.hexes_dict.values():
            if hex_elem.click_is_inside(x, y):
                return hex_elem.i, hex_elem.j
        return "Гекс не найден"
