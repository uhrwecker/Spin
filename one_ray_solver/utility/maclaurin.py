'''Calculate the polar semi-axis c from the spin and the equatorial semi-axis a numerically.'''

import numpy as np
from scipy.optimize import fsolve


def calculate_polar_semi_axis(s, a, dif=None):
    # critical dif:
    if s == 0:
        return [a]

    potenz = 1
    new_a = np.abs(a)
    while new_a < 1:
        new_a *= 10
        potenz *= 10
    dif = 1.3 / potenz

    def func(e):
        kappa_1 = 2 * (3 - 2 * e**2) / e**3 * np.arcsin(e)
        kappa_2 = 6 / e**2 * np.sqrt(1 - e**2)

        factor = 3 / np.pi

        return np.abs(s) - np.sqrt(dif * a) * np.sqrt(factor * (kappa_1 - kappa_2))

    e = fsolve(func, 0.8)
    if len(e) > 0:
        c = a * np.sqrt(1 - e**2)
    else:
        raise ValueError('Could not calculate the polar semi-major axis c.')

    return c