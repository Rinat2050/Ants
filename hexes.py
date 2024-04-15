from tkinter import Tk, Canvas, YES, BOTH
from math import cos, sin, pi
import calculate
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
                vertex_x = calculate.round_for_painting(self.x0 + distance_between_centers * cos(radians))
                vertex_y = calculate.round_for_painting(self.y0 + distance_between_centers * sin(radians))
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
            self.fill_hexes_indexes(hex)
            x_next = next(iter_dict, '888')[0]  # последовательность заканчивается чудом
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
            x, y = int((x1 + x2 * lam) / (1 + lam)), int((y1 + y2 * lam) / (1 + lam))
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
        # self.paint_text_coord()
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
            vertex_x = calculate.round_for_painting(self.x + constants.HEX_LENGTH * cos(angle_radians))
            vertex_y = calculate.round_for_painting(self.y + constants.HEX_LENGTH * sin(angle_radians))
            result.append((vertex_x, vertex_y))
        return result

    def paint_hex(self):
        """Рисует гекс"""
        # window.after(constants.DELAY)
        # window.update()
        return self.canvas.create_polygon(self.list_vertex, fill=constants.GREEN, outline="#004D40")

    def paint_text_coord(self):
        """Подписывает координаты прямо на гексах"""
        # window.after(constants.DELAY)
        # window.update()
        self.canvas.create_text(self.x, self.y + 20,
                                text=(self.x, self.y),
                                fill="white")

    def paint_index(self):
        """Подписывает индексы прямо на гексах"""
        self.canvas.create_text(self.x, self.y + 20,
                                text=(self.i, ':', self.j),
                                fill="blue")


if __name__ == '__main__':
    # region
    window = Tk()
    window.geometry(str(constants.WIDTH_WINDOW) + "x" + str(constants.HEIGHT_WINDOW) + "+1000+0")
    canvas = Canvas(window, width=constants.WIDTH_WINDOW, height=constants.HEIGHT_WINDOW, bg="#53acfd")
    canvas.pack(expand=YES, fill=BOTH)
    canvas.background = "red"
    # endregion

    hexes = Hexes(constants.ROUNDS, 1)
    print(Hex.hexes_indexes)
    hex = Hex.hexes_indexes[(-3, 0)]
    print(hexes.find_neighbors(hex))

    window.mainloop()
