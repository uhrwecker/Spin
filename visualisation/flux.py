import matplotlib.pyplot as pl
import numpy as np
import os
import scipy.signal as signal


class FluxPlotter:
    def __init__(self, figsize=(13, 6), fp='./'):
        self.fig = pl.figure(figsize=figsize)
        self.ax = self.fig.add_subplot(111)

        self.fp = fp

    def plot_monochrome(self):
        if not type(self.fp) == list:
            self.fp = [self.fp]

        for fp in self.fp:
            data, _ = self.load_redshift(fp)

            flux = []
            phis = []
            for redshift in data:
                fl, phi = self.calculate_flux(redshift)
                flux.append(fl)
                phis.append(phi)

            flux.append(flux[0])
            phis.append(np.pi*2)

            flux, phis = _check_for_outliers(flux, phis)

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



            data.append((g, np.amin(redshift[:, 0]), np.amax(redshift[:, 0]),
                         np.amin(redshift[:, 1]), np.amax(redshift[:, 1]), float(p)))

        return data, phis


def _check_for_outliers(data, phi):
    data = np.array(data)
    phi = np.array(phi)

    inte, _ = signal.find_peaks(1/data)
    arrx = []
    for item in inte:
        arrx.append(item - 1)
        arrx.append(item)
        arrx.append(item + 1)

    data = np.delete(data, arrx)
    phi = np.delete(phi, arrx)

    inte, _ = signal.find_peaks(data)
    arrx = []
    for item in inte:
        arrx.append(item - 1)
        arrx.append(item)
        arrx.append(item + 1)

    data = np.delete(data, arrx)
    phi = np.delete(phi, arrx)

    new_x = np.linspace(0, 2*np.pi, num=1000)
    data = np.interp(new_x, phi, data)
    #data[33:36] = [np.mean([data[31], data[36]]) for n in range(3)]
    #data[35] = np.nan
    #data[92:95] = [np.mean([data[91], data[95]]) for n in range(3)]

    #data[17] = np.mean([data[16], data[18]])
    #data[47] = np.mean([data[48], data[46]])

    return data, new_x#phi


ff = FluxPlotter(fp=['/home/jan-menno/Data/03_11_2021/s-015/',
                     '/home/jan-menno/Data/03_11_2021/s-01/',
                     '/home/jan-menno/Data/03_11_2021/s-005/',
                     '/home/jan-menno/Data/03_11_2021/s0/',
                     '/home/jan-menno/Data/03_11_2021/s005/',
                     '/home/jan-menno/Data/03_11_2021/s01/',
                     '/home/jan-menno/Data/03_11_2021/s015/'])
ff.plot_monochrome()
ff.show()