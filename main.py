from copy import copy

import numpy as np
from matplotlib import pyplot as plt

import algorithms
from flux_bias import FluxBiasController
from algorithms import Kitaev
from qubit import Qubit
from utils import adamar_gate, i, rotate_gate

f_min = 10 ** (-9)
f_max = 10 * 10 ** (-9)
N = 1000


def measure(field_manager):
    data = []
    for k in range(N):
        q = Qubit(a=1 + 0 * i, b=0 + 0 * i)
        q.apply_gate(adamar_gate)
        field_manager.apply_field(q, time=algorithm.time())
        q.apply_gate(adamar_gate)
        data.append(q.measure())
    data = np.bincount(data)
    if len(data) == 1:
        return {0: data[0], 1: 0}
    return {0: data[0], 1: data[1]}


if __name__ == "__main__":
    algorithm = Kitaev(field_range=(f_min, f_max))
    field = FluxBiasController(field_range=(f_min, f_max))
    data = (measure(field))
    print(data[0]/(data[0] + data[1]))
    print(data)
    print((field.field - f_min) / f_max * 100)
