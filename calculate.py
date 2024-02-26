import constants
    if i % 2 == 0:
        column_y = 0
    else:
        column_y = constants.HEX_h
    x = i * constants.HEX_LENGTH * 1.5
    y = j * 2 * constants.HEX_h + column_y
    return x, y