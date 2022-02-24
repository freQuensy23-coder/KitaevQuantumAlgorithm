import numpy as np
from matplotlib import pyplot as plt
from utils import i, rand_vec, randbin, polar_to_cart, draw_sphere


class Qubit:
    def __init__(self, **kwargs):
        a_real, a_complex, b_real, b_complex = rand_vec(dim=4)
        if 'a' in kwargs.keys():
            self._alpha: complex = kwargs.get('a')
            self._beta: complex = kwargs.get('b')
        else:
            self._alpha: complex = complex(a_real, a_complex)
            self._beta: complex = complex(b_real, b_complex)
        self.measured: bool = False
        self.state = None

    def measure(self):
        self.measured = True
        self.state = randbin(abs(self._alpha) ** 2)
        return self.state

    def apply_gate(self, gate):
        if self.measured:
            raise QubitMeasured("This qubit is measured and you can't apply operator to it")
        self._matrix = gate.dot(self._matrix)

    def plot(self) -> plt.figure:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x, y, z = polar_to_cart(phi=self._phi, teta=self._teta)
        ax.quiver([0], [0], [0], [x], [y], [z], color=["red"])
        ax.set_xlim([-1, 1])  # TODO Придумать куда это деть
        ax.set_ylim([-1, 1])
        ax.set_zlim([-1, 1])

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        draw_sphere(ax, 1)
        ax.scatter(x, y, z, c="red")
        return fig

    @property
    def _teta(self) -> float:
        return 2 * np.arccos(abs(self._alpha))

    @property
    def _phi(self) -> float:
        return np.arctan2(self._beta.imag, self._beta.real) - self._gamma

    @property
    def _gamma(self):
        return np.arctan2(self._alpha.imag, self._alpha.real)

    @property
    def _matrix(self):
        return np.array([self._alpha, self._beta])

    @_matrix.setter
    def _matrix(self, matrix: np.array):
        self._alpha, self._beta = matrix


class QubitMeasured(Exception): pass
