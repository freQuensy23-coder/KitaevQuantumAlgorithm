from unittest import TestCase

import matplotlib.pyplot as plt
import numpy as np

from algorithms import Kitaev
from flux_bias import FluxBiasController
from utils import rand_vec, randbin, adamar_gate, polar_to_cart, h
from qubit import Qubit
from utils import not_gate


class TestQubit(TestCase):
    def setUp(self) -> None:
        self.q = Qubit()

    def test_measure(self):
        self.assertIn(self.q.measure(), [0, 1])
        self.assertIs(self.q.measured, True)

    def test_alpha_calc(self):
        self.assertAlmostEqual(abs(self.q._alpha) ** 2 + abs(self.q._beta) ** 2, 1)

    def test_apply_not(self):
        a, b = self.q._alpha, self.q._beta
        self.q.apply_gate(not_gate)
        self.assertEqual(a, self.q._beta)
        self.assertEqual(b, self.q._alpha)

    def test_apply_adamar(self):
        a, b = self.q._alpha, self.q._beta
        self.q.apply_gate(adamar_gate)
        self.assertNotEqual(self.q._alpha, a)
        self.q.apply_gate(adamar_gate)
        self.assertAlmostEqual(self.q._alpha, a)
        self.assertAlmostEqual(self.q._beta, b)

    def test_plot(self):
        self.assertIsInstance(self.q.plot(), plt.Figure)


class AlgorithmTest(TestCase):
    def setUp(self) -> None:
        self.alg = Kitaev((2.67, np.pi), mu=h)

    def test_time_work(self):
        self.assertIsInstance(self.alg.time(), float)

    def test_time_correct(self):
        self.assertAlmostEqual(self.alg.time(), 5.88235294118, places=2)

        alg_zero = Kitaev((0, 7), mu=h)  # f_min = 0
        self.assertAlmostEqual(alg_zero.time(), 0.45, places=2)



class TestUtils(TestCase):
    def test_rand_vec(self):
        vec = rand_vec(dim=5, norm=3 / 2)
        self.assertAlmostEqual(np.linalg.norm(vec), 3 / 2)
        self.assertEqual(len(vec), 5)

    def test_randbin(self):
        self.assertIn(randbin(0.5), [0, 1])
        self.assertEqual(randbin(0), 1)
        self.assertEqual(randbin(1), 0)

    def test_polar_to_cart(self):
        for i in range(3):
            self.assertAlmostEqual(polar_to_cart(0, np.pi / 2)[i], np.array([1, 0, 0])[i])

        for i in range(3):
            self.assertAlmostEqual(polar_to_cart(teta=np.pi / 4, phi=0)[i],
                                   np.array([np.sqrt(2) / 2, 0, np.sqrt(2) / 2])[i])
