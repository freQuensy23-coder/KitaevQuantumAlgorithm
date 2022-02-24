"""experiment algorithms"""
import numpy as np
from numpy import pi

from utils import h, i, rotate_gate, default_mu
from random import uniform


class Kitaev:
    def __init__(self, field_range: tuple, mu=default_mu):
        f_min, f_max = field_range
        self.m = mu / h
        self.f_min, self.f_max = f_min, f_max

    def time(self) -> float:
        """Calculate optimum measurements time"""

        def t(n):
            return pi * (1 + 2 * n) / self.m / self.f_min

        if self.f_min != 0:
            n = 0
            time_limit_counter = 0
            while True:
                time_limit_counter += 1
                if (self.f_min + pi / t(n) / self.m) < self.f_max:  # Next Cos max is lefter then f_max
                    return t(n - 1)
                n += 1
                if time_limit_counter >= 10 ** 5:
                    raise ValueError("Unable to find optimal time")
        if self.f_min == 0:
            return np.pi / self.f_max
