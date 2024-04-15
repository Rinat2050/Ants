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
            # Заполение промежутков
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

        for coord_xy, hex in sorted_dict.items():
            hex.i, hex.j = i, j - j0
            hex.paint_index()
            # hex.paint_text_coord()      # если надо подписать координаты
            self.fill_hexes_indexes(hex)
            x_next = next(iter_dict, '999')[0]  # последовательность заканчивается чудом
            j += 1
            if x_next != x_current:  # идём по столбам
                i += 1
                x_current = x_next
                j = 0
                if i <= 0:  # если столбы начали укорачиваться - оставляем j
                    j0 += 1

    def fill_hexes_indexes(self, hex):
        """Наполняет словарь индекс-гекс"""
        Hex.hexes_indexes[(hex.i, hex.j)] = hex

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

    def find_neighbors(self, hex) -> list[tuple]:
        """Поиск координат окружающих гексов"""
        neighbors = []
        i = hex.i
        j = hex.j
        base_neighbors = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]
        for index in range(len(base_neighbors)):
            i_new, j_new = i + base_neighbors[index][0], j + base_neighbors[index][1]
            if (i_new, j_new) in Hex.hexes_indexes.keys():
                neighbors.append((i_new, j_new))
        return neighbors

    def find_neighbors_round(self, hex, round=3) -> set[tuple]:
        """Поиск координат окружающих колец гексов"""
        neighbors = set()
        neighbors.update(set(self.find_neighbors(hex)))
        new_neighbors = neighbors.copy()
        for i in range(round):
            for neighbor in neighbors:
                new_neighbors.update(set(self.find_neighbors(self.hexes_dict[neighbor])))

        return new_neighbors


class Hex:
    hexes_coords = {}
    hexes_indexes = {}

    def __init__(self, center_xy: tuple, canvas):
        self.canvas = canvas
        self.x, self.y = center_xy
        self.i = 999
        self.j = 999
        self.list_vertex = self.center_to_six_vertex()
        self.obj = self.paint_hex()
        Hex.hexes_coords[(self.x, self.y)] = self
        self.visible = True
        self.is_anthill = False
        self.enemy = None
        self.load = None

    def center_to_six_vertex(self):
        """Преобразует центр в список 6-ти вершин"""
        result = []
        for i in range(6):
            angle_radians = i * 2 * pi / 6
            vertex_x = round(self.x + constants.HEX_LENGTH * cos(angle_radians), 1)
            vertex_y = round(self.y + constants.HEX_LENGTH * sin(angle_radians), 1)
            result.append((vertex_x, vertex_y))
        return result

    def paint_hex(self):
        """Рисует гекс"""
        return self.canvas.create_polygon(self.list_vertex, fill=constants.GREEN, outline="#004D40")

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
