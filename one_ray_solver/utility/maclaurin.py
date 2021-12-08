'''Calculate the polar semi-axis c from the spin and the equatorial semi-axis a numerically.'''

import numpy as np
from scipy.optimize import fsolve


def calculate_polar_semi_axis(s, a):
    def func(e):
        kappa_1 = 2 * (3 - 2 * e**2) / e**3 * np.arcsin(e)
        kappa_2 = 6 / e**2 * np.sqrt(1 - e**2)

        factor = 3 / a

        return s - a / 5 * np.sqrt(factor * (kappa_1 - kappa_2))

    e = fsolve(func, 0.5)
    if len(e) > 0:
        c = a * np.sqrt(1 - e)
    else:
        raise ValueError('Could not calculate the polar semi-major axis c.')

    return c

