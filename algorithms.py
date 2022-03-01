"""experiment algorithms"""
import numpy as np
from matplotlib import pyplot as plt
from numpy import pi

from flux_bias import FluxBiasController
from qubit import Qubit
from utils import h, i, rotate_gate, default_mu, adamar_gate, truth_accuracy


class AbstractAlgorithm:
    def __init__(self, field_range: tuple, mu=default_mu, n=1001, measurements_iterations=1):
        f_min, f_max = field_range
        self.f_min, self.f_max = f_min, f_max
        self.n = n  # number of measurements each point (qubit)
        self.iters = measurements_iterations
        self.m = mu / h
        self.field_manger = FluxBiasController(field_range=(f_min, f_max))

    @property
    def time(self) -> float:
        """Calculate optimum measurements time"""

        def t(n: int) -> float:
            """Return time ensures that the n peak falls at the beginning of the interval [f_min, f_max]"""
            if n < 0:
                # raise ValueError("n should be positive integer")
                return t(0)
            return pi * (1 + 2 * n) / self.m / self.f_max

        def peak(n, t) -> float:
            """Calculate position (F = ...) of n peak of cos^2 ( m * F * T)"""
            return 2 * pi * (n + 1) / self.m / t

        for n in range(10 ** 9):
            if peak(n - 1, t(n)) > self.f_min:
                return t(n - 1)  # TODO Действия в случае если n = 0

    def do_measurements(self) -> dict:
        measurements = []
        for k in range(self.n):
            q = Qubit(a=1 + 0 * i, b=0 + 0 * i)
            q.apply_gate(adamar_gate)

            self.field_manger.apply_field(q, time=self.time)

            q.apply_gate(adamar_gate)
            measurements.append(q.measure())

        measurements = np.bincount(measurements)  # Count quantity of |0> and |1> result
        if len(measurements) == 1:
            return {0: measurements[0], 1: 0}
        return {0: measurements[0], 1: measurements[1]}

    def work(self):
        raise Exception("This is Abstract class, use children instead of this")


class Kitaev(AbstractAlgorithm):
    def work(self):
        for k in range(self.iters):
            measurements = self.do_measurements()
            most_popular_state = max(measurements, key=measurements.get)  # | 0 > or | 1 >
            if most_popular_state == 0:
                self.f_max = (self.f_max + self.f_min) / 2
            else:
                self.f_min = (self.f_max + self.f_min) / 2

        return self.f_min, self.f_max


class Fourier(AbstractAlgorithm):
    def __init__(self, *args, truth_0: np.array = None, forces: np.array = None, **kwargs):
        if (forces is not None and truth_0 is None) or (forces is None and truth_0 is not None):
            raise Exception("You cannot pass truth_0 and forces separately to this __init__ method")
        super().__init__(*args, **kwargs)
        self.forces = np.linspace(self.f_min, self.f_max, truth_accuracy)
        self.truth = truth_0 or np.array(truth_accuracy * [1 / (self.f_max - self.f_min)])
        self.f_min0, self.f_max0 = self.f_min, self.f_max
    @property
    def probability(self) -> tuple:
        """Get probability  functions (Field -> [0,1]) for |0> and |1> state of single measure"""
        return lambda f: 1 / 2 * (np.cos(self.m * f * self.time) + 1), lambda f: 1 - 1 / 2 * (np.cos(self.m * f * self.time) + 1)

    def work(self):
        for k in range(self.iters):
            measurements = self.do_measurements()
            most_popular_state = max(measurements, key=measurements.get)  # | 0 > or | 1 >
            self.update_truth(prob_func=self.probability[most_popular_state])
            self.f_min, self.f_max = self.get_new_range()

    def get_truth(self, f) -> float:
        """Real probability of f field
        :param f - field
        "return prob - probability [0, 1] that the field is f
        """
        pass # TODO

    def update_truth(self, prob_func):
        """Update truth function:
        :param prob_func - single measurement probability lambda func (normally it is cos^2(m * F * t / 2) )
        """
        prob_data = prob_func(np.linspace(self.f_min, self.f_max, len(self.truth)))
        self.truth = self.truth * prob_data / np.sum(prob_data * self.truth)

    def draw_truth(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        x = np.linspace(self.f_min0, self.f_max0, len(self.truth))
        ax.plot(x, self.truth)
        ax.set_xlabel("f")
        ax.set_ylabel("P(f)")
        ax.plot([self.field_manger.field]*2, [0, max(self.truth)], c="red")
        return fig

    def get_new_range(self):
        level = 1/np.sqrt(2) * max(self.truth)
        delta = self.truth - level
        s = np.sign(delta)
        points = np.where(s > 0)[0]
        l, r = points[0], points[-1] # left and right border of the gap indexes
        f_min, f_max = self.forces[l], self.forces[r]
        return f_min, f_max
