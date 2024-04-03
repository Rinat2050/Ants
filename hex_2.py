from tkinter import *
from math import cos, sin, pi

# region
ROUND = 4
WIDTH_WINDOW = 900
HEIGHT_WINDOW = 900
HEX_LENGTH = 50  # длина стороны
DELAY = 0  # задержка прорисовки
PRECISION = 1  # точность координат центров и вершин гексов
x0 = WIDTH_WINDOW // 2
y0 = HEIGHT_WINDOW // 2
distance_between_centers = 2 * (HEX_LENGTH * (3 ** 0.5) / 2)


# endregion

class Hex:
    dict_of_hex = {}

    def __init__(self, center_xy: tuple, color):
        self.center_xy = center_xy
        self.i = 999
        self.j = 999
        self.color = color
        self.list_vertex = self.center_to_six_vertex()
        self.paint_hex()
        self.paint_text_coord()
        Hex.dict_of_hex[self.center_xy] = self

    def center_to_six_vertex(self):
        """Преобразует центр в список 6-ти вершин"""
        result = []
        for i in range(6):
            angle_radians = i * 2 * pi / 6
            vertex_x = my_round(self.center_xy[0] + HEX_LENGTH * cos(angle_radians))
            vertex_y = my_round(self.center_xy[1] + HEX_LENGTH * sin(angle_radians))
            result.append((vertex_x, vertex_y))
        return result

    def paint_hex(self):
        """Рисует гекс"""
        window.after(DELAY)
        window.update()
        canvas.create_polygon(self.list_vertex, fill=self.color, outline='white')

    def paint_text_coord(self):
        """Рисует текст"""
        window.after(DELAY)
        window.update()
        canvas.create_text(self.center_xy[0], self.center_xy[1] + 20,
                           text=self.center_xy,
                           fill="white")


def my_round(x, base=PRECISION):
    # return base * round(float(x) / base)  # Это если точность нужно увеличивать до кратного 3, 5, 10
    return int(round(x, PRECISION))
    # return int(x)


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


def paint_index(hex, i, j):
    canvas.create_text(hex.center_xy[0], hex.center_xy[1],
                       text=(i, j),
                       fill="red", font='bold 18')


def create_frame_hex():
    # Первый гекс
    Hex((x0, y0), 'grey')

    # Остальные круги
    for round_hex in range(1, ROUND):
        list_center = []
        # Создание ветвей каркаса
        for branch in range(6):
            distance_between_centers = 2 * (HEX_LENGTH * (3 ** 0.5) / 2) * round_hex
            radians = (branch * 2 * pi / 6) + pi / 6
            vertex_x = my_round(x0 + distance_between_centers * cos(radians))
            vertex_y = my_round(y0 + distance_between_centers * sin(radians))
            Hex((vertex_x, vertex_y), 'green')
            list_center.append((vertex_x, vertex_y))
        # Заполение промежутков
        for ver in range(len(list_center)):
            x1, y1 = list_center[ver % len(list_center)]
            x2, y2 = list_center[(ver + 1) % len(list_center)]
            list_mediate_ver = calculating_intermediate_vertices((x1, y1), (x2, y2), round_hex)
            for v in list_mediate_ver:
                Hex(v, 'green')


def create_index():
    # Создаём индексы
    sorted_dict = dict(sorted(Hex.dict_of_hex.items()))
    iter_dict = iter(sorted_dict.keys())
    x_current = next(iter_dict)[0]
    i = - ROUND + 1
    j = 0
    j0 = 0

    for coord_xy, hex in sorted_dict.items():
        paint_index(hex, i, j - j0)
        hex.i, hex.j = i, j - j0
        x_next = next(iter_dict, '999')[0]  # последовательность заканчивается чудом
        j += 1
        if x_next != x_current:  # идём по столбам
            i += 1
            x_current = x_next
            j = 0
            if i <= 0:  # если столбы начали укорачиваться - оставляем j
                j0 += 1

def list_environment(hex):
    """Поиск координат окружающих гексов (возможно не существующих)"""
    result = []
    x = hex.i
    y = hex.j
    print(hex)
    print(x, y)
    list_search_environment = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]
    for i in range(len(list_search_environment)):
        x_new, y_new = x + list_search_environment[i][0], y + list_search_environment[i][1]
        result.append((x_new, y_new))
    print('гексы рядом: ', result)
    return result



if __name__ == '__main__':
    # region
    window = Tk()
    window.geometry(str(WIDTH_WINDOW) + "x" + str(HEIGHT_WINDOW) + "+1000+0")
    canvas = Canvas(window, width=WIDTH_WINDOW, height=HEIGHT_WINDOW, bg="#53acfd")
    canvas.pack(expand=YES, fill=BOTH)
    canvas.background = "red"
    # endregion

    create_frame_hex()
    create_index()
    print(list_environment(Hex.dict_of_hex[(225, 492)]))


    window.mainloop()
