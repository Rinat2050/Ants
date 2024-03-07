from calculate import index_to_coord
from tkinter import Label
from math import cos, sin, pi
import constants

class Hex:
    def __init__(self, i, j, canvas):

        self.i = i
        self.j = j
        self.x = index_to_coord(self.i, self.j)[0] + constants.HEX_FIELD_X0
        self.y = index_to_coord(self.i, self.j)[1] + constants.HEX_FIELD_Y0

        self.canvas = canvas
        self.canvas.create_polygon(
            self.count_coord(self.x, self.y),
            fill="#80CBC4",
            outline="#004D40",
        )
        self.canvas.create_text(self.x, self.y,
                                text=(self.i, self.j),
                                fill="blue"
        )

    @staticmethod
    def count_coord(center_x, center_y):
        coordinates = []
        for i in range(6):
            vertex_x = int(
                    center_x +
                    constants.HEX_LENGTH * cos(i * 2 * pi / 6)
                )
            vertex_y = int(
                    center_y +
                    constants.HEX_LENGTH * sin(i * 2 * pi / 6)
                )
            coordinates.append(vertex_x)
            coordinates.append(vertex_y)
        return coordinates
