"""Class that allows one to find the appropriate ranges for alpha and beta. Very much a prototype, and
should be double-checked."""
import numpy as np
import os


class RangeAdjustment:
    def __init__(self, ray_handler):
        self.ray = ray_handler
        self.ray.save_config = False
        self.ray.save_csv = False
        self.ray.save_redshift = False
        self.ray.save_data = False

        self.rho = self.ray.rho
        if self.rho > 1:
            raise ValueError('This Range finder can only handle for radii rho < 1.')

        self.width = 15
        self.resolution = 15

        self.alpha_centre = 0
        self.beta_centre = 0

    def start(self, guess=(0, 0), fp=''):
        self.alpha_centre, self.beta_centre = guess

        initial_hit = False

        self.ray.rho = 2

        while not initial_hit:
            initial_hit = self.check_hits()

        halve_rho_hit = False

        self.ray.rho /= 2
        self.resolution = 15

        while not halve_rho_hit:
            halve_rho_hit = self.check_hits()

        self.ray.rho = self.rho

        best_rho = False
        while not best_rho:
            best_rho = self.check_hits()

        print('Range found! Check if it is ok ...')
        self.width *= 1.25  # plus 25 percent
        self.width += 0.25  # plus at least 0.25
        self.resolution = 10
        self.ray.change_ranges(self.alpha_centre - self.width, self.alpha_centre + self.width,
                               self.beta_centre - self.width, self.beta_centre + self.width, self.resolution)
        info, number_of_collisions, hit_data = self.ray.run()

        if fp:
            self.save_range(number_of_collisions, fp)

        print('Finding range done! Continue...')

        return self.ray

    def check_hits(self):
        hit = False

        print(f'Searching for an hit with resolution of {self.resolution} around \n '
              f'alpha = {self.alpha_centre} and beta = {self.beta_centre} ...')
        self.ray.change_ranges(self.alpha_centre - self.width, self.alpha_centre + self.width,
                               self.beta_centre - self.width, self.beta_centre + self.width, self.resolution)

        info, number_of_collisions, hit_data = self.ray.run()

        if number_of_collisions > 0:
            print('- Found an hit!')
            print(hit_data)
            self.width, self.alpha_centre, self.beta_centre = self._find_new_width(hit_data)
            hit = True
        else:
            self.resolution += 5
            print('- Could not find the target, increasing resolution...')

        if self.resolution > 20:
            raise ValueError('Resolution too high; somethings not working.')

        return hit

    def save_range(self, noc, fp):
        if noc < 50:
            print('Warning: the range might be too small. See if that is the case.')

        save_msg = f'{self.ray.rem};{self.ray.tem};{self.ray.pem};{self.alpha_centre - self.width};' \
                   f'{self.alpha_centre + self.width};{self.beta_centre - self.width};{self.beta_centre + self.width}\n'

        if not os.path.isfile(fp):
            with open(fp, 'a') as file:
                file.write('#rem\ttem\tpem\tamin\tamax\tbmin\tbmax\n')

        with open(fp, 'a') as file:
            #file.write(b'\n')
            file.write(save_msg)

    def _find_new_width(self, hit_data):
        # First: check if there is only one hit. Then just make the width smaller
        if len(hit_data[:, 0]) == 0:
            return 5

        alpha_width = np.abs(np.amax(hit_data[:, 0]) - np.amin(hit_data[:, 0])) / 2
        beta_width = np.abs(np.amax(hit_data[:, 1]) - np.amin(hit_data[:, 1])) / 2

        alpha_centre = np.mean(hit_data[:, 0])
        beta_centre = np.mean(hit_data[:, 1])

        return np.amax([alpha_width, beta_width]), alpha_centre, beta_centre
