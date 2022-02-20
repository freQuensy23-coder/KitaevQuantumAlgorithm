import numpy as np

from utils import h, i, rotate_gate
from random import uniform


class FluxBiasController:
    def __init__(self, f_min, f_max, mu=927 * 10 ** (-26), field=None):
        self.field = field or uniform(f_min, f_max)
        self.mu = mu
        self.f_min = f_min
        self.f_max = f_max

    def apply_field(self, qubit, time=None):
        time = time or self.time()
        phi = self.mu / h * self.field * time
        qubit.apply_gate(rotate_gate(phi=phi))
        return locals()

    def time(self):
        return 2 * np.pi * h / (self.f_max - self.f_min) / self.mu
