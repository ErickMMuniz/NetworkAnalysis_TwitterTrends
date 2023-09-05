import numpy as np

from src.values import *


def choice(array, n, replace=False):
    np.random.seed(SEED)
    return np.random.choice(array, n, replace=replace)
