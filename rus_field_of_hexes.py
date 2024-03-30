import tkinter as tk
import constants
from math import cos, sin, pi, sqrt

window = tk.Tk()
window.title('test')

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_offset = (screen_width - constants.WIDTH_WINDOW)
y_offset = (screen_height - constants.HEIGHT_WINDOW) * 0

window.geometry('{w}x{h}+{x}+{y}'.format(
    w=constants.WIDTH_WINDOW,
    h=constants.HEIGHT_WINDOW,
    x=x_offset,
    y=y_offset,
))

center_x = 400
center_y = 400

canvas = tk.Canvas(window, width=constants.WIDTH_WINDOW, height=constants.HEIGHT_WINDOW)
canvas.place(x=0, y=0, anchor='nw')


def count_coord(center_x, center_y, length=constants.HEX_LENGTH, angle_offset=0):
    coordinates = []
    for i in range(6):
        vertex_x = int(
            center_x +
            length * cos(i * 2 * pi / 6 + angle_offset)
        )
        vertex_y = int(
            center_y +
            length * sin(i * 2 * pi / 6 + angle_offset)
        )
        coordinates.append(vertex_x)
        coordinates.append(vertex_y)
    return coordinates


def paint_hex(center_x, center_y):
    canvas.create_polygon(count_coord(center_x, center_y), fill=constants.GREEN, outline="#004D40")


# for point in count_coord_90()


# hexes = count_coord(center_x, center_y, constants.HEX_h*2, pi / 2)
#
# for index in range(1, len(hexes), 2):
#     paint_hex(hexes[index-1], hexes[index])
#
# hexes2 = count_coord(center_x, center_y, constants.HEX_h*4, pi / 2)
#
# for index in range(1, len(hexes2), 2):
#     paint_hex(hexes2[index-1], hexes2[index])

# paint_hex(center_x, center_y)


def field_of_hexes(round):
    round = round * 2
    for d in range(0, round + 1, 2):
        hexes = count_coord(center_x, center_y, constants.HEX_h * d, pi / 2)
        for index in range(1, len(hexes), 2):
            x1 = hexes[index - 1]
            y1 = hexes[index]

            x2 = hexes[index - 3]
            y2 = hexes[index - 2]

            distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            # if distance-1 > constants.HEX_h*2:
            #     new_x = (x1 + x2)/2
            #     new_y = (y1 + y2)/2
            #     paint_hex(new_x, new_y)
            if distance - 1 > constants.HEX_h * 2 and 0 <= abs(x1 - x2) <= 1:
                for elem in range((d // 2) - 1):
                    new_x = (x1 + x2) / 2
                    new_y = (y1 + y2) / 2 + constants.HEX_h * elem
                    radius = 3
                    canvas.create_oval(new_x - radius, new_y - radius, new_x + radius, new_y + radius, fill='red')

        for index in range(1, len(hexes), 2):
            x = hexes[index - 1]
            y = hexes[index]
            paint_hex(x, y)
            radius = 3
            canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='black')


field_of_hexes(3)



window.mainloop()