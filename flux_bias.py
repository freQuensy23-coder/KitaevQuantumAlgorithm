import numpy as np
from numpy import pi

from utils import h, i, rotate_gate
from random import uniform


class FluxBiasController:
    def __init__(self, f_min, f_max, mu=927 * 10 ** (-26), field=None):
        self.field = field or uniform(f_min, f_max)
        self.m = mu / h
        self.f_min = f_min
        self.f_max = f_max

    def apply_field(self, qubit, time=None):
        time = time or self.time()
        phi = self.m * self.field * time
        qubit.apply_gate(rotate_gate(phi=phi))
        return locals()

    def time(self):
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
