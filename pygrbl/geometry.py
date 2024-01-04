"""
Part of pygrbl

Defines chamber geometries that are used to ensure
all points are always within desired bounds.

Noah Stieler, 2023
"""

import random
from math import pi, sin, cos, sqrt

from .point import Point


class PyGRBLChamber:
    """Not to be instantiated, acts an abstract class."""

    def is_point_valid(self, point: Point) -> bool:
        pass


class ChamberCylinder3D(PyGRBLChamber):

    def __init__(self, radius: float, height: float, padding: float,
                 target_radius: float, target_height: float):
        self.radius: float = radius
        self.height: float = height
        self.padding: float = padding

        self.target_radius: float = target_radius
        self.target_height: float = target_height

    @property
    def true_radius(self) -> float:
        return self.radius - self.padding - self.target_radius

    @property
    def true_height(self) -> float:
        return self.height - self.padding - self.target_height / 2

    def is_point_valid(self, point: Point) -> bool:
        if sqrt(pow(point.x, 2) + pow(point.y, 2)) < self.true_radius and abs(point.z) < self.true_height:
            return True
        else:
            return False


class ChamberCircle2D(PyGRBLChamber):

    def __init__(self, radius: float, padding: float, target_radius: float):
        self.radius: float = radius
        self.padding: float = padding
        self.target_radius: float = target_radius

    @property
    def true_radius(self) -> float:
        return self.radius - self.padding - self.target_radius

    def is_point_valid(self, point: Point) -> bool:
        if point.mag < self.true_radius:
            return True
        else:
            return False

    @staticmethod
    def gen_rand_uniform(num_points: int, radius: float, order='none') -> list:
        """Generates uniformly distributed points within chamber bounds."""
        max_iter = 8000
        min_dist = 0.1  # mm

        li = []
        iter_count = 0

        while len(li) < num_points and iter_count < max_iter:
            iter_count += 1
            angle = random.random() * 2 * pi
            mag = (radius / sqrt(radius)) * sqrt(radius * random.random())
            # sqrt() is need to make distribution uniform
            new_pos = Point(mag * cos(angle), mag * sin(angle))
            skip = False
            for i in range(len(li)):
                dist = new_pos.dist(li[i])
                if dist < min_dist:
                    skip = True
                    break
            if not skip:
                li.append(new_pos)

        if order == 'none':
            return li
        elif order == 'nearest_neighbour':
            li_nn = []
            cur_pos = Point(0, 0)

            while len(li) != 0:
                index = ChamberCircle2D._get_nearest_neighbour(li, cur_pos)
                li_nn.append(li[index])
                cur_pos = li[index]
                del li[index]
            return li_nn

    @staticmethod
    def _get_nearest_neighbour(pos_list: list, pos: Point) -> int:
        """Finds the index of the closest point that has not been visited yet."""
        nn = -1
        best_dist = float('inf')

        for i in range(len(pos_list)):
            dist = pos_list[i].dist(pos)
            if dist <= best_dist:
                nn = i
                best_dist = dist

        return nn
