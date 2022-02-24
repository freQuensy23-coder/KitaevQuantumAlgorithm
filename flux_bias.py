import numpy as np
from numpy import pi

from utils import h, i, rotate_gate, default_mu
from random import uniform


class FluxBiasController:
    """This class knows real field value and can apply it to qbits"""
    def __init__(self, mu=default_mu, field=None, field_range: tuple = None):
        if field is None and field_range is None:
            raise ValueError("Flux Controller needs field value or field range.")
        if field_range is not None:
            f_min, f_max = field_range
        if field != 0:
            self.field = field or uniform(f_min, f_max)
        else:
            self.field = 0
        self.m = mu / h
        self.total_time = 0

    def apply_field(self, qubit, time=None):
        self.total_time += time
        phi = self.m * self.field * time
        qubit.apply_gate(rotate_gate(phi=phi))
        return locals()