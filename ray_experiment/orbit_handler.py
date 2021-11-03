"""This class will handle an experiment that is a ray experiment but for different orbit positions of the emitter."""
import os
import numpy as np
from ray_experiment import ranger


class OrbitHandler:
    def __init__(self, ray_handler, number_of_orbit_points=16, meta_data='', save_fp='./'):
        self.rh = ray_handler
        self.noop = number_of_orbit_points
        self.meta_data = meta_data
        self.save_fp = save_fp

        self.phi_em = np.linspace(0, np.pi*2, num=self.noop, endpoint=False)

    def start(self):
        if self.meta_data:
            self.run_from_meta_data()

        else:
            self.run_with_range_finder()

    def run_with_range_finder(self):
        res = self.rh.resolution
        col = self.rh.save_when_not_colliding
        csv = self.rh.save_csv
        red = self.rh.save_redshift
        cfg = self.rh.save_config
        da = self.rh.save_data

        for pem in self.phi_em:
            print(f'\nNow at phi_em = {pem}')
            self.change_rh_fp(pem)

            rg = ranger.RangeAdjustment(self.rh)
            rh = rg.start(fp=self.save_fp+'meta_data.txt')

            rh.resolution = res
            rh.save_even_when_not_colliding = col
            rh.save_csv = csv
            rh.save_redshift = red
            rh.save_config = cfg
            rh.save_data = da

            self.rh.run()

    def run_from_meta_data(self):
        data = np.loadtxt(self.meta_data, delimiter=';', usecols=(2, 3, 4, 5, 6))

        for row in data:
            pem, amin, amax, bmin, bmax = row
            print(f'\nNow at phi_em = {pem}')

            self.rh.change_ranges(amin, amax, bmin, bmax, self.rh.resolution)

            self.change_rh_fp(pem)

            self.rh.run()

    def change_rh_fp(self, pem):
        self.rh.pem = pem

        fp = self.setup_directory(pem)

        self.rh.save_exp.fp = fp
        self.rh.fp = fp
        self.rh.data_fp = self.rh.setup()

    def setup_directory(self, pem):
        path = self.save_fp + str(pem) + '/'
        if not os.path.isdir(path):
            os.mkdir(path)

        return path