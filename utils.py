import random
from typing import *
import math
import numpy as np

# import TrimLog

dataVar = TypeVar("dataVar", int, float)


class VectorDescriber:
    def __init__(
        self, x_weight: dataVar = 0, y_weight: dataVar = 0, k_weight: dataVar = 0
    ):
        self.x_weight = x_weight
        self.y_weight = y_weight
        self.k_weight = k_weight


class D2Vector:
    def __init__(self, x: dataVar = 0, y: dataVar = 0):
        self.x = x
        self.y = y
        self.position = [self.x, self.y]

        self.distance: float = 0
        self.k: float = 0

    def __str__(self) -> str:
        return "Position({0}, {1}), distance={2}".format(self.x, self.y, self.distance)

    def _k_get(self):
        if self.x == 0:
            return self.y, 0
        r = np.sqrt(np.square(self.x) + np.square(self.y))
        theta = np.degrees(np.arctan(self.y / self.x))
        return r, theta

    def random_init(self, r1: int, r2: int) -> None:
        self.x = random.randint(r1, r2)
        self.y = random.randint(r1, r2)

    def get_dis(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def set_dis(self, dis: dataVar) -> None:
        self.distance = dis


class Subject(D2Vector):
    def __init__(self, name: str, attr: VectorDescriber):
        super().__init__()
        self.name: str = name
        self.attr: VectorDescriber = attr

        if self.attr.x_weight == 0 and self.attr.y_weight == 0:
            raise ValueError("x_weight and y_weight can't be 0 at the same time!")
        elif self.attr.x_weight == 0:
            if self.attr.y_weight < 0:
                theta = 270
            else:
                theta = 90
        elif self.attr.y_weight == 0:
            if self.attr.x_weight < 0:
                theta = 180
            else:
                theta = 0
        else:
            theta = np.degrees(np.arctan(self.attr.y_weight / self.attr.x_weight))
            if self.attr.x_weight < 0:
                theta += 180
            elif self.attr.x_weight > 0 > self.attr.y_weight:
                theta += 360
        r = self.attr.k_weight
        self.x = r * np.cos(np.radians(theta))
        self.y = r * np.sin(np.radians(theta))
        if self.attr.x_weight == 0:
            self.x = 0
        if self.attr.y_weight == 0:
            self.y = 0
        self.position = [self.x, self.y]
        self.theta = theta
        self.r = r

    def __str__(self) -> str:
        return "name={0} Position({1}, {2}), theta={3}, r={4}".format(
            self.name, self.x, self.y, self.theta, self.r
        )

    def upload_data(self, attr: VectorDescriber) -> None:
        self.attr = attr
        if self.attr.x_weight == 0 and self.attr.y_weight == 0:
            raise ValueError("x_weight and y_weight can't be 0 at the same time!")
        elif self.attr.x_weight == 0:
            if self.attr.y_weight < 0:
                theta = 270
            else:
                theta = 90
        elif self.attr.y_weight == 0:
            if self.attr.x_weight < 0:
                theta = 180
            else:
                theta = 0
        else:
            theta = np.degrees(np.arctan(self.attr.y_weight / self.attr.x_weight))
            if self.attr.x_weight < 0:
                theta += 180
            elif self.attr.x_weight > 0 > self.attr.y_weight:
                theta += 360
        r = self.attr.k_weight
        self.x = r * np.cos(np.radians(theta))
        self.y = r * np.sin(np.radians(theta))
        if self.attr.x_weight == 0:
            self.x = 0
        if self.attr.y_weight == 0:
            self.y = 0
        self.position = [self.x, self.y]
        self.theta = theta
        self.r = r


learn_list = TypeVar("learn_list", list[Subject], list[Subject])


# if __name__ == "__main__":
#     s = Subject("Maths", VectorDescriber(0, -1, 10))
#     print(s)
