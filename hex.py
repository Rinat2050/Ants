from calculate import index_to_coord
from tkinter import Label
from math import cos, sin, pi
import constants


class Hex:
    def __init__(self, i, j, place_hex):
        self.i, self.j = i, j
        self.x, self.y = index_to_coord(self.i, self.j)
        self.place_hex = place_hex
        self.place_hex.create_polygon(
            self.count_coord(self.x, self.y),
            fill="#80CBC4",
            outline="#004D40",
        )
        self.lbl = Label(self.place_hex, text=(self.i, self.j))
        self.lbl.place(
            x=constants.HEX_FIELD_X0 + self.x,
            y=constants.HEX_FIELD_Y0 + self.y,
            anchor='center',
        )

    @staticmethod
    def count_coord(center_x, center_y):
        coordinates = []
        for i in range(6):
            vertex_x = constants.HEX_FIELD_X0 + int(
                    center_x +
                    constants.HEX_LENGTH * cos(i * 2 * pi / 6)
                )
            vertex_y = constants.HEX_FIELD_Y0 + int(
                    center_y +
                    constants.HEX_LENGTH * sin(i * 2 * pi / 6)
                )
            coordinates.append(vertex_x)
            coordinates.append(vertex_y)
        return coordinates
