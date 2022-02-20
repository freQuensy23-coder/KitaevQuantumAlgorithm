from unittest import TestCase

import numpy as np

from utils import rand_vec, randbin, adamar_gate, polar_to_cart
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
