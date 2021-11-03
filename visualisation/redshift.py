import matplotlib.pyplot as pl
import matplotlib as mp
import numpy as np


def plot(fp):
    ax = pl.gca()

    data = np.loadtxt(fp, delimiter=',', skiprows=1)

    g = data[:, 2]
    g[g == 0] = np.nan
    n = int(np.sqrt(len(g)))
    g = g.reshape(n, n).T[::-1]
    ax.imshow(g, extent=(np.amin(data[:, 0]), np.amax(data[:, 0]),
                         np.amin(data[:, 1]), np.amax(data[:, 1])))
    pl.show()

fp = '../redshift.csv'
#fp = '/home/jan-menno/Data/03_11_2021/3.141592653589793/redshift.csv'
plot(fp)