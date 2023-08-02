"""
Part of pygrbl

Noah Stieler, 2023
"""

from .point import Point
from .exception import CSVLoadException


def load_csv(path: str, dimension: int) -> list:
    """Parses a .csv file and returns a list of positions.
    dimension indicates how many components each position has."""
    out = []
    num_list = []

    with open(path, 'r') as file:
        for line in file:
            line = line.replace('\n', '')
            line_split = line.split(',')
            for item in line_split:
                if item != '':
                    num_list.append(float(item))

    if len(num_list) % dimension != 0:
        raise CSVLoadException

    for i in range(0, len(num_list), dimension):
        if dimension == 2:
            out.append(Point(num_list[i], num_list[i + 1], 0))
        else:
            out.append(Point(num_list[i], num_list[i + 1], num_list[i + 2]))

    return out
