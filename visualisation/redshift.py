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
    norm = mp.colors.Normalize(0.35341593438360724, 1.5904476791090183)

    ax.imshow(g, extent=(np.amin(data[:, 0]), np.amax(data[:, 0]),
                         np.amin(data[:, 1]), np.amax(data[:, 1])), norm=norm, cmap=cmap)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    #ax.imshow(g, extent=(-10, 10, -10, 10))
    #pl.show()
    pl.savefig(f'/home/jan-menno/Data/03_11_2021/s-01/images/{m}.png')
    ax.clear()

    return np.nanmin(g), np.nanmax(g)
    #print(fp[:-13])

#fp = '../redshift.csv'
phis = np.linspace(0, np.pi*2, num=128, endpoint=False)
gmax = []
gmin = []
for n, phi in enumerate(phis):
    fp = f'/home/jan-menno/Data/03_11_2021/s-01/{phi}/redshift.csv'
    g1, g2 = plot(fp, n)
    gmin.append(g1)
    gmax.append(g2)
    print(g1, g2, n)

print(np.amin(gmin), np.amax(gmax))