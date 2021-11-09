import matplotlib.pyplot as pl
import numpy as np
import os


class FluxPlotter:
    def __init__(self, figsize=(13, 6), fp='./'):
        self.fig = pl.figure(figsize=figsize)
        self.ax = self.fig.add_subplot(111)

        self.fp = fp

    def plot_monochrome(self):
        data, phis = self.load_redshift()

        flux = []
        for redshift in data:
            flux.append(self.calculate_flux(redshift))

        pl.plot(phis, flux)
        pl.show()

    def calculate_flux(self, g):
        red, amin, amax, bmin, bmax = g
        n = int(np.sqrt(len(red)))

        dx = np.abs(amax - amin) / n
        dy = np.abs(bmax - bmin) / n

        column = [np.trapz(row[np.isnan(row)]**3, dx=dx) for row in red]

        return np.trapz(column, dx=dy)


    def load_redshift(self):
        phis = [f.path for f in os.scandir(self.fp) if f.is_dir()]
        phis.sort()

        data = []
        for phi in phis:
            fp = self.fp + f'/{phi}/redshift.csv'
            redshift = np.loadtxt(fp, delimiter=',', skiprows=1)
            g = redshift[:, 2]
            g[g == 0] = np.nan
            n = int(np.sqrt(len(g)))
            g = g.reshape(n, n)[::-1].T

            data.append((g, np.amin(redshift[:, 0]), np.amax(redshift[:, 0]),
                         np.amin(redshift[:, 1]), np.amax(redshift[:, 1])))

        return data, phis