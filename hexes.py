from math import cos, sin, pi
import constants


class Hexes:
    def __init__(self, rounds, anthill_round, canvas):
        self.canvas = canvas
        self.rounds = rounds
        self.anthill_round = anthill_round
        self.x0 = constants.WIDTH_WINDOW // 2
        self.y0 = constants.HEIGHT_WINDOW // 2
        self.create_frame_hex()
        self.create_index()
        self.hexes_dict = Hex.hexes_indexes

    def create_frame_hex(self):
        # Первый гекс
        Hex((self.x0, self.y0), self.canvas)
        # Остальные круги
        for round_hex in range(1, constants.ROUNDS):
            list_center = []
            # Создание ветвей каркаса
            for branch in range(6):
                distance_between_centers = 2 * (constants.HEX_LENGTH * (3 ** 0.5) / 2) * round_hex
                radians = (branch * 2 * pi / 6) + pi / 6
                vertex_x = round(self.x0 + distance_between_centers * cos(radians))
                vertex_y = round(self.y0 + distance_between_centers * sin(radians))
                Hex((vertex_x, vertex_y), self.canvas)
                list_center.append((vertex_x, vertex_y))
            # Заполнение промежутков
            for ver in range(len(list_center)):
                x1, y1 = list_center[ver % len(list_center)]
                x2, y2 = list_center[(ver + 1) % len(list_center)]
                list_mediate_ver = Hexes.calculating_intermediate_vertices((x1, y1), (x2, y2), round_hex)
                for v in list_mediate_ver:
                    Hex(v, self.canvas)

    def create_index(self):
        # Создаём индексы
        sorted_dict = dict(sorted(Hex.hexes_coords.items()))
        iter_dict = iter(sorted_dict.keys())
        x_current = next(iter_dict)[0]
        i = - constants.ROUNDS + 1
        j = 0
        j0 = 0

        for coord_xy, hex_elem in sorted_dict.items():
            hex_elem.i, hex_elem.j = i, j - j0
            if constants.SHOW_INDEX:
                hex_elem.paint_index()
            if constants.SHOW_COORD:
                hex_elem.paint_text_coord()  # если надо подписать координаты
            self.fill_hexes_indexes(hex_elem)
            x_next = next(iter_dict, '999')[0]  # последовательность заканчивается чудом
            j += 1
            if x_next != x_current:  # идём по столбам
                i += 1
                x_current = x_next
                j = 0
                if i <= 0:  # если столбы начали укорачиваться - оставляем j
                    j0 += 1

    @staticmethod
    def fill_hexes_indexes(hexagon):
        """Наполняет словарь индекс-гекс"""
        Hex.hexes_indexes[(hexagon.i, hexagon.j)] = hexagon

    @staticmethod
    def calculating_intermediate_vertices(coord_1, coord_2, count_med_ver) -> list:
        """Вычисляет координаты промежуточных вершин"""
        result = []
        x1, y1 = coord_1
        x2, y2 = coord_2
        for part in range(1, count_med_ver):
            lam = part / (count_med_ver - part)
            x, y = (round((x1 + x2 * lam) / (1 + lam)), round((y1 + y2 * lam) / (1 + lam)))
            result.append((x, y))
        return result

    @staticmethod
    def find_neighbors(hexagon) -> list[tuple]:
        """Поиск координат окружающих гексов"""
        neighbors = []
        i = hexagon.i
        j = hexagon.j
        base_neighbors = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]
        for index in range(len(base_neighbors)):
            i_new, j_new = i + base_neighbors[index][0], j + base_neighbors[index][1]
            if (i_new, j_new) in Hex.hexes_indexes.keys():
                neighbors.append((i_new, j_new))
        return neighbors

    def find_neighbors_round(self, hexagon, circle=0) -> set[tuple]:
        """Поиск координат окружающих колец гексов"""
        neighbors = set()
        neighbors.add((hexagon.i, hexagon.j))
        new_neighbors = set()
        new_neighbors.add((hexagon.i, hexagon.j))
        for i in range(circle):
            for neighbor in neighbors:
                new_neighbors.update(set(self.find_neighbors(self.hexes_dict[neighbor])))
            neighbors = new_neighbors.copy()
            new_neighbors = set()
        return neighbors


class Hex:
    hexes_coords = {}
    hexes_indexes = {}

    def __init__(self, center_xy: tuple, canvas):
        self.canvas = canvas
        self.x, self.y = center_xy
        self.i = 999
        self.j = 999
        self.list_vertex = self.center_to_six_vertex()
        self.obj = self.paint()
        Hex.hexes_coords[(self.x, self.y)] = self
        self.visible = False
        self.is_anthill = False
        self.load = None
        self.ant = []

    def make_visible(self):
        self.visible = True
        self.canvas.itemconfig(self.obj, fill=constants.GREEN)

    def make_invisible(self):
        self.visible = False
        self.canvas.itemconfig(self.obj, fill=constants.GREY)

    def center_to_six_vertex(self):
        """Преобразует центр в список шести вершин"""
        result = []
        for i in range(6):
            angle_radians = i * 2 * pi / 6
            vertex_x = round(self.x + constants.HEX_LENGTH * cos(angle_radians), 1)
            vertex_y = round(self.y + constants.HEX_LENGTH * sin(angle_radians), 1)
            result.append((vertex_x, vertex_y))
        return result

    def click_is_inside(self, x, y):
        """Узнаёт, где был клик"""
        flag = True
        for point in range(6):
            next_point = (point + 1) % 6
            x1, y1 = self.list_vertex[point][0], self.list_vertex[point][1]
            x2, y2 = self.list_vertex[next_point][0], self.list_vertex[next_point][1]
            # Произведение векторов https://stackoverflow.com/questions/3838319
            #       /how-can-i-check-if-a-point-is-below-a-line-or-not
            s = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
            if s < 0:
                flag = False
        return flag

    def paint(self):
        """Рисует гекс"""
        return self.canvas.create_polygon(self.list_vertex, fill=constants.GREY, outline="#004D40")

    def paint_text_coord(self):
        """Подписывает координаты прямо на гексах"""
        self.canvas.create_text(self.x, self.y - 20,
                                text=(self.x, self.y),
                                fill="white")

    def paint_index(self):
        """Подписывает индексы прямо на гексах"""
        self.canvas.create_text(self.x, self.y + 20,
                                text=(self.i, ':', self.j),
                                fill="blue")
