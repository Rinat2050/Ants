from tkinter import Tk, Canvas, YES, BOTH
from math import cos, sin, pi
import calculate

# region
ROUND = 4
WIDTH_WINDOW = 900
HEIGHT_WINDOW = 900
HEX_LENGTH = 50  # длина стороны
DELAY = 0  # задержка прорисовки
distance_between_centers = 2 * (HEX_LENGTH * (3 ** 0.5) / 2)


# endregion

class Hexes:

    def __init__(self, rounds, anthill_round):
        self.rounds = rounds
        self.anthill_round = anthill_round
        self.x0 = WIDTH_WINDOW // 2
        self.y0 = HEIGHT_WINDOW // 2
        self.create_frame_hex()
        self.create_index()

    def create_frame_hex(self):
        # Первый гекс
        Hex((self.x0, self.y0), 'grey')

        # Остальные круги
        for round_hex in range(1, ROUND):
            list_center = []
            # Создание ветвей каркаса
            for branch in range(6):
                distance_between_centers = 2 * (HEX_LENGTH * (3 ** 0.5) / 2) * round_hex
                radians = (branch * 2 * pi / 6) + pi / 6
                vertex_x = calculate.round_for_painting(self.x0 + distance_between_centers * cos(radians))
                vertex_y = calculate.round_for_painting(self.y0 + distance_between_centers * sin(radians))
                Hex((vertex_x, vertex_y), 'green')
                list_center.append((vertex_x, vertex_y))
            # Заполение промежутков
            for ver in range(len(list_center)):
                x1, y1 = list_center[ver % len(list_center)]
                x2, y2 = list_center[(ver + 1) % len(list_center)]
                list_mediate_ver = Hexes.calculating_intermediate_vertices((x1, y1), (x2, y2), round_hex)
                for v in list_mediate_ver:
                    Hex(v, 'green')

    def create_index(self):
        # Создаём индексы
        sorted_dict = dict(sorted(Hex.hexes_coords.items()))
        iter_dict = iter(sorted_dict.keys())
        x_current = next(iter_dict)[0]
        i = - ROUND + 1
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
        """Поиск координат окружающих гексов (возможно не существующих)"""
        neighbors = []
        x = hex.i
        y = hex.j
        base_neighbors = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]
        for i in range(len(base_neighbors)):
            x_new, y_new = x + base_neighbors[i][0], y + base_neighbors[i][1]
            if (x_new, y_new) in Hex.hexes_indexes.keys():
                neighbors.append((x_new, y_new))
        return neighbors


class Hex:
    hexes_coords = {}
    hexes_indexes = {}

    def __init__(self, center_xy: tuple, color):
        self.center_xy = center_xy
        self.i = 999
        self.j = 999
        self.color = color
        self.list_vertex = self.center_to_six_vertex()
        self.paint_hex()
        self.paint_text_coord()
        Hex.hexes_coords[self.center_xy] = self

    def center_to_six_vertex(self):
        """Преобразует центр в список 6-ти вершин"""
        result = []
        for i in range(6):
            angle_radians = i * 2 * pi / 6
            vertex_x = calculate.round_for_painting(self.center_xy[0] + HEX_LENGTH * cos(angle_radians))
            vertex_y = calculate.round_for_painting(self.center_xy[1] + HEX_LENGTH * sin(angle_radians))
            result.append((vertex_x, vertex_y))
        return result

    def paint_hex(self):
        """Рисует гекс"""
        window.after(DELAY)
        window.update()
        canvas.create_polygon(self.list_vertex, fill=self.color, outline='white')

    def paint_text_coord(self):
        """Подписывает координаты прямо на гексах"""
        window.after(DELAY)
        window.update()
        canvas.create_text(self.center_xy[0], self.center_xy[1] + 20,
                           text=self.center_xy,
                           fill="white")

    def paint_index(self):
        """Подписывает индексы прямо на гексах"""
        canvas.create_text(self.center_xy[0], self.center_xy[1],
                           text=(self.i, self.j),
                           fill="red", font='bold 18')


if __name__ == '__main__':
    # region
    window = Tk()
    window.geometry(str(WIDTH_WINDOW) + "x" + str(HEIGHT_WINDOW) + "+1000+0")
    canvas = Canvas(window, width=WIDTH_WINDOW, height=HEIGHT_WINDOW, bg="#53acfd")
    canvas.pack(expand=YES, fill=BOTH)
    canvas.background = "red"
    # endregion

    hexes = Hexes(ROUND, 1)
    print(Hex.hexes_indexes)
    hex = Hex.hexes_indexes[(-3, 0)]
    print(hexes.find_neighbors(hex))

    window.mainloop()
