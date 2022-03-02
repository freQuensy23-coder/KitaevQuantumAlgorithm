from unittest import TestCase

import matplotlib.pyplot as plt
import numpy as np

from algorithms import Kitaev, KitaevTruthScaling
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


class TestAlgorithm(TestCase):
    def setUp(self) -> None:
        self.alg = Kitaev(field_range=(2.67, np.pi), mu=h)  # mu = h => self.m = mu/h = 1

    def test_time_work(self):
        self.assertIsInstance(self.alg.time, float)

    def test_time_correct(self):
        self.assertAlmostEqual(self.alg.time, 5.0, places=2)

        alg_zero = Kitaev((0, 7), mu=h)  # f_min = 0
        self.assertAlmostEqual(alg_zero.time, 0.45, places=2)

        alg = Kitaev((11, 13), mu=h)  # f_min = 0
        self.assertAlmostEqual(alg.time, 1.21, places=2)

        alg = Kitaev((13.7, 16.5), mu=31 * h)  # f_min = 0
        self.assertAlmostEqual(alg.time, 	0.031, places=2)

        alg = Kitaev((21, 22), mu=31 * h)  # f_min = 0
        self.assertAlmostEqual(alg.time, 0.0967352576619, places=2)


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


class TestKitaevTruth(TestCase):
    def setUp(self) -> None:
        self.alg0 = KitaevTruthScaling(field_range=(0, 100))
        self.alg = KitaevTruthScaling(field_range=(80, 100))

    def test_prob0(self):
        self.assertEqual(self.alg0.probability[0](0), 1)
        self.assertAlmostEqual(self.alg0.probability[0](50), 0.5)

    def test_prob(self):
        self.assertAlmostEqual(self.alg.probability[0](100), 0)

        f_min, f_max = field_range = (75, 100)
        alg2 = KitaevTruthScaling(field_range=field_range)
        data = []
        for i in np.linspace(f_min, f_max, 15):
            pr = alg2.probability[0](i)
            print(pr)
            data.append(pr)
        plt.plot(np.linspace(f_min, f_max, 15), data)
        plt.show()
