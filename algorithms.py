"""experiment algorithms"""
import numpy as np
from numpy import pi

from flux_bias import FluxBiasController
from qubit import Qubit
from utils import h, i, rotate_gate, default_mu, adamar_gate
from random import uniform


class Algorith:
    def __init__(self, field_range: tuple, mu=default_mu, n=1001, measurements_iterations=1):
        f_min, f_max = field_range
        self.f_min, self.f_max = f_min, f_max
        self.n = n
        self.iters= measurements_iterations
        self.m = mu / h
        self.field_manger = FluxBiasController(field_range=(f_min, f_max))

    def time(self) -> float:
        """Calculate optimum measurements time"""
        # TODO Переписать с использованием функции счетчика числа пиков между f_min и f_max
        def t(n:int):
            if n<0 and n is not isinstance(int):
                raise ValueError("n should be positive integer")
            return pi * (1 + 2 * n) / self.m / self.f_min

        if self.f_min != 0:
            n = 0
            time_limit_counter = 0
            while True:
                time_limit_counter += 1
                if (self.f_min + pi / t(n) / self.m) < self.f_max:  # Next Cos max is lefter than f_max
                    return t(n - 1)
                n += 1
                if time_limit_counter >= 10 ** 5:
                    raise ValueError("Unable to find optimal time")
        if self.f_min == 0:
            return np.pi / self.f_max

    def do_measurements(self) -> dict:
        measurements = []
        for k in range(self.n):
            q = Qubit(a=1 + 0 * i, b=0 + 0 * i)  #
            q.apply_gate(adamar_gate)

            time = self.time()
            self.field_manger.apply_field(q, time=time)

            q.apply_gate(adamar_gate)
            measurements.append(q.measure())

        measurements = np.bincount(measurements)  # Count quantity of |0> and |1> result
        if len(measurements) == 1:
            return {0: measurements[0], 1: 0}
        return {0: measurements[0], 1: measurements[1]}


class Kitaev(Algorith):
    def work(self):
        for k in range(self.iters):
            measurements = self.do_measurements()
            most_popular_state = max(measurements, key=measurements.get)  # | 0 > or | 1 >
            if most_popular_state == 0:
                self.f_max = (self.f_max + self.f_min)/2
            else:
                self.f_min = (self.f_max + self.f_min) / 2

        return self.f_min, self.f_max


