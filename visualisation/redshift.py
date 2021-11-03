import matplotlib.pyplot as pl
import matplotlib as mp
import numpy as np


def plot(fp):
    ax = pl.gca()

    data = np.loadtxt(fp, delimiter=',', skiprows=1)

    g = data[:, 2]
    g[g == 0] = np.nan
    n = int(np.sqrt(len(g)))
    g = g.reshape(n, n).T
    ax.imshow(g)
    pl.show()


fp = '../0.0/redshift.csv'
plot(fp)