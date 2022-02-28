"""experiment algorithms"""
import numpy as np
from numpy import pi

from flux_bias import FluxBiasController
from qubit import Qubit
from utils import h, i, rotate_gate, default_mu, adamar_gate


class Algorith:
    def __init__(self, field_range: tuple, mu=default_mu, n=1001, measurements_iterations=1):
        f_min, f_max = field_range
        self.f_min, self.f_max = f_min, f_max
        self.n = n
        self.iters = measurements_iterations
        self.m = mu / h
        self.field_manger = FluxBiasController(field_range=(f_min, f_max))

    def time(self) -> float:
        """Calculate optimum measurements time"""
        def t(n: int) -> float:
            """Return time ensures that the n peak falls at the beginning of the interval [f_min, f_max]"""
            if n < 0 and t:
                raise ValueError("n should be positive integer")
            return pi * (1 + 2 * n) / self.m / self.f_max

        def peak(n, t) -> float:
            """Calculate position (F = ...) of n peak of cos^2 ( m * F * T)"""
            return 2 * pi * (n + 1) / self.m / t

        for n in range(10 ** 9):
            if peak(n-1, t(n)) > self.f_min:
                return t(n - 1) # TODO Действия в случае если n = 0

    def do_measurements(self) -> dict:
        measurements = []
        for k in range(self.n):
            q = Qubit(a=1 + 0 * i, b=0 + 0 * i)
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
                self.f_max = (self.f_max + self.f_min) / 2
            else:
                self.f_min = (self.f_max + self.f_min) / 2

        return self.f_min, self.f_max
