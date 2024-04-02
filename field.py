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
    # '''
    # cobwebs_list = []
    # spiders_list = []
    # '''

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

# '''
#     def select_obj(self, evemt):
#         x = evemt.x
#         y = evemt.y
#         for ant in self.ants_list:
#             shift = ant.cell_size / 2
#             if not ant.selected \
#                     and not ant.stuck \
#                     and abs(ant.x - x) <= shift and abs(ant.y - y) <= shift:
#                 print(ant.name, 'выбран')
#                 ant.selected = True
#                 # self.bind('<Button-1>', ant.move_obj)          # было/работает
#                 self.bind('<Button-1>', lambda event, arg=ant: self.move_obj(event, arg))
#                 self.itemconfig(ant.obj, image=ant.photo_selected_True)
#                 if not ant.loading:
#                     for berry in self.berries_list:
#                         if berry.i == ant.i and berry.j == ant.j and not berry.taken:
#                             btn_take = TakeButton(self, "Взять", ant.x, ant.y)
#                             self.btn_list.append(btn_take)
#                             break
#                     for ant_friend in self.ants_list:
#                         if (ant_friend.i, ant_friend.j) in self.search_hex_nearby(ant.i, ant.j) and ant_friend.stuck:
#                             print("Друг в беде!", ant_friend.name, ant_friend.i, ant_friend.j)
#                             # self.bind('<Button-1>', self.ant_direction)
#
#                 elif ant.loading:
#                     if self.hexes_dict.get((ant.i, ant.j)).is_anthill:
#                         btn_drop = DropButton(self, 'Положить', ant.x, ant.y)
#                         self.btn_list.append(btn_drop)
#                         print(ant.name, 'дома с ягодкой')
#                 break
# '''

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
# '''
#     def ant_direction(self, event):
#         # Не работает как надо. Деректива должна автоматом: сходить или снять паутину рядом. Надо менять choise_hex
#         #print('--паутина: ', self.hexes_dict[ant.i, ant.j].enemy)
#         print('--не пойду! Там враг!')
#         #ant.move_obj(event)
#         # if not self.hexes_dict[ant.i, ant.j].enemy:  # enemy не работает. Паутина становится врагом после появления
#         #     ant.move_obj(event)
#         # else:
#         #     print('--не пойду! Там враг!', self.hexes_dict[ant.i, ant.j].i, self.hexes_dict[ant.i, ant.j].j)
#
#     def move_obj(self, event, ant):
#         new_x = event.x
#         new_y = event.y
#         if ant.selected:
#             self.choise_hex(ant, new_x, new_y)
#             self.coords(ant.obj, ant.x, ant.y)
#             print(ant.name, 'перемещён')
#             ant.selected = False
#             self.itemconfig(ant.obj, image=ant.photo_selected_False)
#             self.do_visible_hex(ant)       # Открываем невидимый гекс
#             if ant.loading:            # Тащим ягоду
#                 ant.loading.move_berry(ant.x, ant.y - constants.OFFSET_TOP_Y_BERRY, ant)
#             try:
#                 self.btn_list[-1].destroy()
#                 self.btn_list.pop()
#             except:
#                 pass
#
#     def choise_hex(self, ant, x, y):     # изменяет индексы и координаты муравья в свойствах
#         for hex_val in self.hexes_dict.values():
#             if ((x - hex_val.x) ** 2 + (y - hex_val.y) ** 2 <= constants.HEX_h ** 2
#                     and (ant.x - hex_val.x) ** 2 + (ant.y - hex_val.y) ** 2 <= 6 * constants.HEX_h ** 2):
#                 # Позволяет передвигаться ТОЛЬКО на ближайшие хексы
#                 ant.i = hex_val.i
#                 ant.j = hex_val.j
#                 ant.x = hex_val.x
#                 ant.y = hex_val.y
#
#     def do_visible_hex(self, ant):
#         for hex_val in self.hexes_dict.values():
#             if [hex_val.i, hex_val.j] == [ant.i, ant.j] and hex_val.visible is False:
#                 self.itemconfig(hex_val.obj, fill=constants.GREEN)
#                 hex_val.visible = True
#                 print("стал видимым гекс: ", hex_val.i, hex_val.j)
#
#                 for berry in self.berries_list:
#                     if [berry.i, berry.j] == [ant.i, ant.j] and not berry.visible:
#                         berry.do_visible_berry()
#                         print(ant.name, 'нашёл', berry.name)
#                         break
#
#                 for web in self.cobwebs_list:
#                     if [web.i, web.j] == [ant.i, ant.j] and not web.visible:
#                         web.do_visible_web()
#                         print(ant.name, 'нашёл паутину :(', web.id)
#                         ant.stuck = True
#                         break
#
#                 for spider in self.spiders_list:
#                     if [spider.i, spider.j] == [ant.i, ant.j] and not spider.visible:
#                         spider.do_visible_spider()
#                         print(ant.name, 'нашёл паука :(', spider.id)
#                         ant.stuck = True
#                         break
# '''

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
# '''
#         x = self.hexes_dict.get((6, 6)).x
#         y = self.hexes_dict.get((6, 6)).y
#         for indexes, hex_object in self.hexes_dict.items():
#             if (hex_object.x - x) ** 2 + (hex_object.y - y) ** 2 >= (constants.HEX_LENGTH * 4) ** 2:
#                 self.itemconfig(hex_object.obj, fill=constants.GREY)
#                 hex_object.visible = False
#                 self.invisible_hexes_dict[indexes] = hex_object  # Пополняем invisible_hexes_dict невидимыми гексами
#
#     def search_hex_nearby(self, i, j) -> list[object]:
#         list_hex_nearby = []
#         x = self.hexes_dict.get((i, j)).x
#         y = self.hexes_dict.get((i, j)).y
#         for indexes, hex_object in self.hexes_dict.items():
#             if (hex_object.x - x) ** 2 + (hex_object.y - y) ** 2 <= (constants.HEX_LENGTH * 2) ** 2:
#                 # list_hex_nearby.append(hex_object)
#                 list_hex_nearby.append(indexes)
#         return list_hex_nearby
#
#     def create_berries(self, number):
#         # invisible_hexes_indexes = [indexes for indexes in self.invisible_hexes_dict]
#         hexes_indexes_of_berry = []
#         for indexes, hex_object in self.hexes_dict.items():
#             if not hex_object.is_anthill and not hex_object.enemy:
#                 hexes_indexes_of_berry.append(indexes)
#
#         berries_name_list = ['смородина', 'малина', 'клубника', 'земляника', 'брусника', 'рябина', 'клюква', 'ирга',
#                              'калина', 'шиповник', 'голубика', 'ежевика', 'черешня', 'черника', 'бузина',
#                              'вишня', 'черешня', 'жимолость', 'кизил', 'черёмуха']
#
#         for _ in range(number):
#             indexes = random.choice(hexes_indexes_of_berry)
#             index_i = indexes[0]
#             index_j = indexes[1]
#             hexes_indexes_of_berry.remove(indexes)
#
#             berry_name = random.choice(berries_name_list)
#             berries_name_list.remove(berry_name)
#
#             value = Berry(index_i, index_j, self, berry_name)
#             self.berries_list.append(value)
#             # value.do_visible_berry()  # показать все ягоды
#         for hex_under_berry in self.berries_list:
#             if self.hexes_dict[(hex_under_berry.i, hex_under_berry.j)].visible:
#                 hex_under_berry.do_visible_berry()
# '''

    def create_random_objects(self, class_object, quantity: int, *invalid_places: tuple) -> None:
        '''
        Fill up random objects
        returns: None
        '''
        # ('enemy', 'anthil')
        #print(self.hexes_dict[(6, 6)].__dict__)
        hexes_indexes = set()
        for indexes, hex in self.hexes_dict.items():
            hexes_indexes.add(indexes)
        for atribute in invalid_places:
            for hex in self.hexes_dict.values():
                if hex.__dict__[atribute]:
                    hexes_indexes.discard((hex.i, hex.j))
        # hexes_indexes = [indexes for indexes, hex in self.hexes_dict.items()
        #                  if not hex.is_anthill and not hex.enemy]
        # berries_names = random.sample(constants.BERRIES_NAMES, quantity)
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
        print(ant.name, 'загружен', selected_berry.name)

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
        print(ant.name, 'разгружен', selected_berry.name)

    def create_cobwebs(self, number):
        for i in range(number):

            web = Web((5+i, 3), self)
            self.cobwebs.append(web)
# '''
#             web = Web(5 + i, 3, self)
#             self.cobwebs_list.append(web)
# '''
            self.hexes_dict[web.i, web.j].enemy = web

    def create_spiders(self, number):
        for i in range(number):

            spider = Spider((5+i, 2), self)
            self.spiders.append(spider)
# '''
#             spider = Spider(5 + i, 2, self)
#             self.spiders_list.append(spider)
# '''
            self.hexes_dict[spider.i, spider.j].enemy = spider

    def create_timer(self, time):
        self.timer = Timer(self, time, 360, 20)
        # self.timer.start()
