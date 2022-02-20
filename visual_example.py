import numpy as np
from matplotlib import pyplot as plt

from flux_bias import FluxBiasController
from qubit import Qubit
from utils import adamar_gate, i, rotate_gate


if __name__ == "__main__":
    q = Qubit(a=1 + 0*i, b=0 + 0*i)
    q.plot().show()
    q.apply_gate(adamar_gate)
    q.plot().show()

    q.apply_gate(rotate_gate(np.pi/6))
    q.plot().show()
    q.apply_gate(adamar_gate)
    q.plot().show()
    print(abs(q._alpha) ** 2)
    print("teta", q._teta * 59,"phi", q._phi*59)
