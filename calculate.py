from constants import *
def index_to_coord(i, j):
    if i % 2 == 0:
        column_y = 0
    else:
        column_y = HEX_h
    x = i * HEX_LENGTH*1.5
    y = j * 2 * HEX_h + column_y
    return x, y