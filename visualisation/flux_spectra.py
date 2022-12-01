import numpy as np
import matplotlib.pyplot as pl
import scipy.stats as stats


def absorption_line(nu, nu_0=762248812611238, width=4, depth=0.4):
    # nu_0 = 762248812611238 is Ca K Line
    func = 1 - stats.norm.pdf(nu, nu_0, width)

    return func


def main():
    nu_0 = 76.2248812611238
    nu = np.linspace(nu_0 * 0.1, nu_0 * 2.8, num=10000)

    y = absorption_line(nu, nu_0=nu_0)

    pl.plot(nu, y)
    #pl.xscale('log')
    pl.grid()
    pl.show()


if __name__ == '__main__':
    main()
