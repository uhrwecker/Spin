import matplotlib.pyplot as pl
import numpy as np
import os
import scipy.signal as signal


class FluxPlotter:
    def __init__(self, figsize=(13, 6), fp='./', labels=[]):
        self.fig = pl.figure(figsize=figsize)
        self.ax = self.fig.add_subplot(111)

        self.fp = fp

        self.labels = labels
        if not labels:
            self.labels = [str(f) for f in fp]

    def plot_monochrome(self):
        if not type(self.fp) == list:
            self.fp = [self.fp]

        for fp, label in zip(self.fp, self.labels):
            data, _ = self.load_redshift(fp)

            flux = []
            phis = []
            for redshift in data:
                fl, phi = self.calculate_flux(redshift)
                flux.append(fl)
                phis.append(phi)

            flux.append(flux[0])
            phis.append(np.pi*2)

            #flux, phis = _check_for_outliers(flux, phis)

            if fp == '/home/jan-menno/Data/no_v_orbit/s0/':
                flux[51:77] = flux[51] - np.abs(flux[51:77] - flux[51])
                #flux[77] = np.nan

            self.ax.plot(phis, flux, label=label)
            self.ax.fill_between(np.linspace(0, 4.25), 0, 1, color='grey', alpha=0.1)
            self.ax.set_xlim(0, np.pi * 2)
            self.ax.set_ylim(0, 0.1)
            self.ax.set_xticks(np.linspace(0, np.pi * 2, num=9, endpoint=True))
            self.ax.set_xticklabels(['0', r'$\pi$ / 4', r'$\pi$ / 2', r'3 $\pi$ / 4', r'$\pi$',
                        r'5 $\pi$ / 4', r'3 $\pi$ / 2', r'7 $\pi$ / 4', r'2 $\pi$'])
            self.ax.legend()
            self.ax.set_xlabel('orbit position')
            self.ax.set_ylabel('Flux')

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
        for phi in phis:
            if 'images' in phi:
                continue
            p = phi[len(fp):]
            f = phi + '/redshift.csv'
            redshift = np.loadtxt(f, delimiter=',', skiprows=1)
            g = redshift[:, 2]
            g[g == 0] = np.nan
            n = int(np.sqrt(len(g)))
            g = g.reshape(n, n)[::-1].T
            print(self.calculate_flux((g, np.amin(redshift[:, 0]), np.amax(redshift[:, 0]),
                         np.amin(redshift[:, 1]), np.amax(redshift[:, 1]), float(p))))

            data.append((g, np.amin(redshift[:, 0]), np.amax(redshift[:, 0]),
                         np.amin(redshift[:, 1]), np.amax(redshift[:, 1]), float(p)))

        return data, phis


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

#ff = FluxPlotter(fp=['/home/jan-menno/Data/17_12_21/s0/',
#                     '/home/jan-menno/Data/17_12_21/s-005/',
#                     '/home/jan-menno/Data/17_12_21/s-01/',
#                     '/home/jan-menno/Data/17_12_21/s-015/',
#                     '/home/jan-menno/Data/17_12_21/s-0175/',
#                     '/home/jan-menno/Data/17_12_21/s-0185/'],
#                 labels=['s = 0', 's =-0.0005', 's =-0.0010', 's =-0.0015', 's =-0.00175', 's =-0.00185'])
ff = FluxPlotter(fp=['/home/jan-menno/Data/19_12_21/s0/',
                     '/home/jan-menno/Data/19_12_21/s-015/',
                     '/home/jan-menno/Data/19_12_21/s-019/',
                     '/home/jan-menno/Data/19_12_21/s-0199/'],
                 labels=['s =  0.0000', 's = -0.0015', 's = -0.0019', 's = -0.00199'])
ff.plot_monochrome()
pl.grid()
ff.show()