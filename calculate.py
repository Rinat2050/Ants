import constants
from typing import Tuple


def index_to_coord(i: int, j: int) -> Tuple[int, int]:
    """
    Converts hexagonal grid indices to Cartesian coordinates.

    Parameters:
        i (int): Index along the horizontal axis.
        j (int): Index along the vertical axis.

    Returns:
        tuple: A tuple containing the Cartesian coordinates (x, y)
               corresponding to the input indices.

    Notes:
        - The hexagonal grid is assumed to have a regular layout,
          with hexagons arranged in a staggered pattern.
        - i represents the column index, while j represents the row index.
        - The function calculates the coordinates based on the indices
          and the constants defined in the 'constants' module.

    Example:
        Assuming constants.HEX_LENGTH = 10 and constants.HEX_h = 8:

        index_to_coord(0, 0) returns (0, 0)
        index_to_coord(1, 0) returns (15.0, 4)
        index_to_coord(0, 1) returns (0, 16)
    """
    if i % 2 == 0:
        column_y = 0
    else:
        column_y = constants.HEX_h
    x = i * constants.HEX_LENGTH * 1.5
    y = j * 2 * constants.HEX_h + column_y
    return x, y
