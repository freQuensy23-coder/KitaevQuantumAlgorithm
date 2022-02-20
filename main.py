import numpy as np
from matplotlib import pyplot as plt

from qubit import Qubit
from utils import adamar_gate

if __name__ == "__main__":
    q = Qubit()
    q.plot().show()
    q.apply_gate(adamar_gate)
    q.plot().show()