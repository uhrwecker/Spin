import numpy as np

import matplotlib.pyplot as pl
import matplotlib as mp


def check_for_missing_interlinks(data):
    data[data == 0] = np.nan
    n = int(np.sqrt(len(data)))
    g = data.reshape(n, n)

    missing_interlinks = False

    for m, row in enumerate(g):
        idx = np.diff(np.arange(0, n)[~np.isnan(row)])
        if idx[idx > 1].size > 0:
            if not idx[idx > 1].sum() == 0:
                missing_interlinks = True
                row = fix_missing_interlinks(row, n)

        g[m] = row

    return g.flatten(), missing_interlinks


def fix_missing_interlinks(row, n, min_batch_size=5):
    idx = np.arange(0, n)[~np.isnan(row)]
    num = idx[-1] - idx[0]

    if idx[1] - idx[0] > 1:
        row[idx[0]] = np.nan

        idx = np.delete(idx, 0)

        if idx.size == 1:
            row[idx[0]] = np.nan

            return row

        if idx.size == 0:
            return row

    if idx[-1] - idx[-2] > 1:
        row[idx[-1]] = np.nan

        idx = np.delete(idx, -1)

        if idx.size == 1:
            row[idx[-1]] = np.nan

            return row

        if idx.size == 0:
            return row

    diff = np.diff(idx)
    if diff[diff > 1].size > 0:
        point = np.where(diff > 1)[0]
        for idd in point:
            new_x = np.arange(idx[idd], idx[np.where(idx == idx[idd])[0][0] + 1] + 1)
            sample_x = [idx[idd], new_x[-1]]
            g_range = row[sample_x]
            new_g = np.interp(new_x, sample_x, g_range)

            row[new_x] = new_g

        return row

    else:
        return row

def plot_g(data):
    ax = pl.gca()

    g = data[:, 2]
    g[g == 0] = np.nan
    n = int(np.sqrt(len(g)))
    g = g.reshape(n, n).T[::-1]

    cmap = pl.cm.cool_r
    norm = mp.colors.Normalize(0.35341593438360724, 1.5904476791090183)

    ax.imshow(g, extent=(np.amin(data[:, 0]), np.amax(data[:, 0]),
                         np.amin(data[:, 1]), np.amax(data[:, 1])), norm=norm, cmap=cmap)

    ax.set_xlim(np.amin(data[:, 0]), np.amax(data[:, 0]))
    ax.set_ylim(np.amin(data[:, 1]), np.amax(data[:, 1]))

    pl.show()
    ax.clear()


def main():
    import os

    fp = '/home/jan-menno/Data/03_11_2021/s0/'

    phis = [f.path for f in os.scandir(fp) if f.is_dir() and not 'images' in f.path]
    phis.sort()

    for phi in phis:
        if 'images' in phi:
            continue
        p = phi[len(fp):]
        f = phi + '/redshift.csv'
        redshift = np.loadtxt(f, delimiter=',', skiprows=1)
        g = redshift[:, 2]

        plot_g(redshift)
        redshift[:, 2], flag = check_for_missing_interlinks(g)
        if flag:
            print('new')
            plot_g(redshift)


if __name__ == '__main__':
    main()