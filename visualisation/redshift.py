import matplotlib.pyplot as pl
import matplotlib as mp
import numpy as np


def plot(fp, m):
    ax = pl.gca()

    data = np.loadtxt(fp, delimiter=',', skiprows=1)

    g = data[:, 2]
    g[g == 0] = np.nan
    n = int(np.sqrt(len(g)))
    g = g.reshape(n, n).T[::-1]

    cmap = pl.cm.cool_r
    norm = mp.colors.Normalize(0.34601869016144915, 2.5392203360441967)

    ax.imshow(g, extent=(np.amin(data[:, 0]), np.amax(data[:, 0]),
                         np.amin(data[:, 1]), np.amax(data[:, 1])), norm=norm, cmap=cmap)
    ax.scatter(0, 0, label='s=-0.00175')
    ax.legend()
    ax.set_xlim(np.amin(data[:, 0]), np.amax(data[:, 0]))#-10, 10)
    ax.set_ylim(np.amin(data[:, 1]), np.amax(data[:, 1]))
    #ax.imshow(g, extent=(-10, 10, -10, 10))
    pl.show()
    #pl.savefig('/home/jan-menno/Data/10_12_21/s0/images/%03d.png' % m)
    ax.clear()

    return np.nanmin(g), np.nanmax(g)


phis = np.linspace(0, np.pi*2, num=128)#, endpoint=False)
gmax = []
gmin = []
afx = 0
for n, phi in enumerate(phis):
    fp = f'/home/jan-menno/Data/02_01_22/s0/{phi}/redshift.csv'
    g1, g2 = plot(fp, n+afx)
    gmin.append(g1)
    gmax.append(g2)
    print(g1, g2, n)

print(np.amin(gmin), np.amax(gmax))