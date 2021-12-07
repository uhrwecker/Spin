import matplotlib.pyplot as pl
import numpy as np
import os
import scipy.signal as signal


class FluxPlotter:
    def __init__(self, figsize=(13, 6), fp='./'):
        self.fig = pl.figure(figsize=figsize)
        self.ax = self.fig.add_subplot(111)

        self.fp = fp

        self.data = None

    def plot_monochrome(self):
        if not type(self.fp) == list:
            self.fp = [self.fp]

        for fp in self.fp:
            data, _, ng = self.load_redshift(fp)

            flux = []
            fl22 = []
            phis = []
            for redshift, ng3 in zip(data, ng):
                fl, phi = self.calculate_flux(redshift)
                flux.append(fl)
                if fp == self.fp[0]:
                    fl2, phi2 = self.calculate_flux(ng3)
                    fl22.append(fl2)
                phis.append(phi)

            flux.append(flux[0])
            if fp == self.fp[0]:
                fl22.append(fl22[0])
                self.data = fl22
            phis.append(np.pi*2)

            flux, phis = _check_for_outliers(flux, phis)
            if fp == self.fp[0]:
                fl22, phis = _check_for_outliers(fl22, phis)
                fl22 = fl22[::-1]
                fl22[33:35] = [np.mean([fl22[32], fl22[35]]), np.mean([fl22[32], fl22[35]])]
                fl22[93] = np.mean([fl22[92], fl22[94]])

                self.ax.plot(phis, np.array(fl22)-400, label='no orbit vel')
            self.ax.plot(phis, flux, label=fp)
            self.ax.set_xlim(0, np.pi * 2)
            # ax.set_ylim(0, 2.8)
            self.ax.set_xticks(np.linspace(0, np.pi * 2, num=9, endpoint=True))
            self.ax.set_xticklabels(['0', r'$\pi$ / 4', r'$\pi$ / 2', r'3 $\pi$ / 4', r'$\pi$',
                        r'5 $\pi$ / 4', r'3 $\pi$ / 2', r'7 $\pi$ / 4', r'2 $\pi$'])
            self.ax.legend()

    def show(self):
        pl.show()

    def calculate_flux(self, g):
        red, amin, amax, bmin, bmax, phi = g
        n = int(np.sqrt(len(red)))

        dx = np.abs(amax - amin) / n
        dy = np.abs(bmax - bmin) / n

        column = [np.trapz(row[~np.isnan(row)]**3, dx=dx) for row in red]

        return np.trapz(column, dx=dy), phi

    def load_redshift(self, fp):
        phis = [f.path for f in os.scandir(fp) if f.is_dir() and not 'images' in f.path]
        phis.sort()

        data = []
        d2 = []
        for phi in phis:
            if 'images' in phi:
                continue
            p = phi[len(fp):]
            f = phi + '/redshift.csv'
            redshift = np.loadtxt(f, delimiter=',', skiprows=1)
            g = redshift[:, 2]

            g[g == 0] = np.nan
            n = int(np.sqrt(len(g)))
            if not self.data:
                ng = get_new_g(redshift, f)
                ng = ng[:, 2].reshape(n, n)[::-1].T
            g = g.reshape(n, n)[::-1].T

            data.append((g, np.amin(redshift[:, 0]), np.amax(redshift[:, 0]),
                         np.amin(redshift[:, 1]), np.amax(redshift[:, 1]), float(p)))
            if not self.data:
                d2.append((ng, np.amin(redshift[:, 0]), np.amax(redshift[:, 0]),
                            np.amin(redshift[:, 1]), np.amax(redshift[:, 1]), float(p)))
            else:
                d2.append(None)

        return data, phis, d2


def get_new_g(g, f):
    f = f[30:]
    redshift = np.loadtxt('/home/jan-menno/Data/fix/cha' + f, delimiter=',', skiprows=1)
    data = []
    for row in g:
        #print(row)
        if row[0] in redshift[:, 0] and row[1] in redshift[:, 1]:
            choice = redshift[row[0] == redshift[:, 0]]
            ch = choice[row[1] == choice[:, 1]]
            if ch.size:
                data.append(ch[0])
            else:
                data.append(row)
        else:
            data.append(row)

    return np.array(data)

def _check_for_outliers(data, phi):
    start = 122
    yp = [data[start], data[-1]]
    x = np.arange(start, len(data))
    xp = [start, 128]

    data[start:] = np.interp(x, xp, yp)

    data[95] = np.mean([data[94], data[96]])

    start = 6
    yp = [data[0], data[start]]
    x = np.arange(0, start)
    xp = [0, start]

    print(len(data))
    data[:start] = np.interp(x, xp, yp)
    print(len(data))

    return data, phi


ff = FluxPlotter(fp=['/home/jan-menno/Data/fix/s-015/',
                     '/home/jan-menno/Data/fix/s0/'])
ff.plot_monochrome()
ff.show()