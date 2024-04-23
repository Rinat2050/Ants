import constants
from typing import Tuple
import math
import operator


def index_to_coord(index: Tuple[int, int]) -> Tuple[int, int]:
    """
    Converts hexagonal grid indices to Cartesian coordinates.

    Parameters:
        index[0] (int): Index along the horizontal axis.
        index[1] (int): Index along the vertical axis.

    Returns:
        tuple: A tuple containing the Cartesian coordinates (x, y)
               corresponding to the input indices.

    Notes:
        - The hexagonal grid is assumed to have a regular layout,
          with hexagons arranged in a staggered pattern.
        - index[0] represents the column index, while index[1] represents the row index.
        - The function calculates the coordinates based on the indices
          and the constants defined in the 'constants' module.

    Example:
        Assuming constants.HEX_LENGTH = 10 and constants.HEX_h = 8:

        index_to_coord((0, 0)) returns (0, 0)
        index_to_coord((1, 0)) returns (15.0, 4)
        index_to_coord((0, 1)) returns (0, 16)
    """
    i, j = index
    column_y = 0 if i % 2 == 0 else constants.HEX_h

    x = i * constants.HEX_LENGTH * 1.5
    y = j * 2 * constants.HEX_h + column_y
    return (x, y)


def compare_distance(dot1: tuple[float, float], dot2: tuple[float, float], operator_str: str, distance: float):
    operators = {
        '<': operator.lt,
        '>': operator.gt,
        '<=': operator.le,
        '>=': operator.ge,
        '==': operator.eq,
        '!=': operator.ne
    }

    # If the arguments are provided as tuples, unpack them
    dist = math.dist(dot1, dot2)

    try:
        return operators[operator_str](dist, distance)
    except KeyError:
        raise ValueError("Invalid comparison operator")


def get_for_list(array, index):
    try:
        return array[index]
    except IndexError:
        return None
