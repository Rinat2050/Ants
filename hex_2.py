from tkinter import *
from math import cos, sin, pi

ROUND = 4
WIDTH_WINDOW = 900
HEIGHT_WINDOW = 900
HEX_LENGTH = 50  # длина стороны
DELAY = 50  # задержка прорисовки
PRECISION = 1  # точность координат центров и вершин гексов
x0 = WIDTH_WINDOW // 2
y0 = HEIGHT_WINDOW // 2
distance_between_centers = 2 * (HEX_LENGTH * (3 ** 0.5) / 2)


class Hex:
    list_of_hex = []

    def __init__(self, center_xy: tuple, color):
        self.center_xy = center_xy
        self.color = color
        self.list_vertex = self.center_to_six_vertex()
        self.paint_hex()
        Hex.list_of_hex.append(self)

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


def my_round(x, base=PRECISION):
    # return base * round(float(x) / base)  # Это если точность нужно увеличивать до кратного 3, 5, 10
    return round(x, PRECISION)


def calculating_intermediate_vertices(coord_1, coord_2, count_med_ver) -> list:
    """Вычисляет координаты промежуточных вершин"""
    result = []
    x1, y1 = coord_1
    x2, y2 = coord_2
    for part in range(1, count_med_ver):
        lam = part / (count_med_ver - part)
        x, y = (x1 + x2 * lam) / (1 + lam), (y1 + y2 * lam) / (1 + lam)
        result.append((x, y))
    return result


window = Tk()
window.geometry(str(WIDTH_WINDOW) + "x" + str(HEIGHT_WINDOW) + "+1000+0")
canvas = Canvas(window, width=WIDTH_WINDOW, height=HEIGHT_WINDOW, bg="#53acfd")
canvas.pack(expand=YES, fill=BOTH)
canvas.background = "red"

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



window.mainloop()
