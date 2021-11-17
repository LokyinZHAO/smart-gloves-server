import numpy as np


def sigmoidlize(x: np.ndarray):
    """sigmoid normalization to [-1,1]

    @param x:
    @return:
    """
    _range = np.max(x) - np.min(x)
    min_max = [(i - np.min(x)) / _range for i in x]
    min_max_to_ten = [((i * 20) - 10) for i in min_max]
    sig = [1.0 / (1 + np.exp(-float(i))) for i in min_max_to_ten]
    sig_to_1 = np.array([ i*2-1 for i in sig  ])
    return sig_to_1