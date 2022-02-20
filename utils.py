import numpy as np

i = complex(0, 1)
not_gate = np.array([[0, 1], [1, 0]])
adamar_gate = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]])


def rand_vec(dim: int, norm: float = 1) -> np.array:
    """Generate random dim - dimntional vector with norm - euclidian norm"""
    res = np.random.rand(dim)
    return norm * res / np.linalg.norm(res)


def randbin(p: float = 0.5) -> int:
    """Generate 0 with probability p and 1 with probability 1 - p"""
    return np.random.choice([0, 1], p=[p, 1 - p])


def polar_to_cart(phi, teta, mag=1) -> np.array:
    """Convert from polar to Cartesian coordinate system"""
    x: float = mag * np.sin(teta) * np.cos(phi)
    y: float = mag * np.sin(teta) * np.sin(phi)
    z: float = mag * np.cos(teta)
    return np.array([x, y, z], dtype=np.float64)
