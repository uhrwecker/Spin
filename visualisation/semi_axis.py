import numpy as np
import matplotlib.pyplot as pl
from scipy.optimize import fsolve


def calculate_polar_semi_axis(s, a):
    def func(e):
        kappa_1 = 2 * (3 - 2 * e**2) / e**3 * np.arcsin(e)
        kappa_2 = 6 / e**2 * np.sqrt(1 - e**2)

        factor = 3 / a

        return np.abs(s) - a / 5 * np.sqrt(factor * (kappa_1 - kappa_2))

    e = fsolve(func, a)
    if len(e) > 0:
        c = a * np.sqrt(1 - e**2)
    else:
        raise ValueError('Could not calculate the polar semi-major axis c.')

    return c


def main():
    a = 0.5
    s = np.linspace(-0.214, 0.214, num=1000)

    pl.plot(s, [calculate_polar_semi_axis(ss, a) for ss in s], label='c(s, a) at a = 0.5')
    pl.fill_between(np.linspace(-0.2, 0.2), 0, 1, color='DEEPSKYBLUE', alpha=0.2, label='geometrical limit')
    pl.xlim(-0.25, 0.25)
    pl.ylim(0, 0.6)
    pl.xlabel('s')
    pl.ylabel('c')
    pl.grid()
    pl.legend()
    pl.show()


if __name__ == '__main__':
    main()