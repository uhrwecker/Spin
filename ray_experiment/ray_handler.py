"""This class handles the instanciation and running of several light rays, corresponding to a specified section on
the screen."""

import numpy as np
import time
import os

from one_ray_solver.solve import OneRaySolver
from ray_experiment.saving import save_experiment


class RayHandler:
    """
    This class will take the experiment input - resolution of the specified section of the screen, and emitter and
    observer properties - and runs the one ray solver for each combination. Afterwards, specific actions (saving etc)
    will be done by this handler.
    """
    def __init__(self, s=0., rem=8., tem=np.pi/2, pem=0., rho=0.5, robs=35., tobs=1., pobs=0.,
                 alpha_min=-1., alpha_max=1., beta_min=-6., beta_max=-4., resolution=10, m=1, start=0,
                 stop=70, num=100000, abserr=1e-7, relerr=1e-7, interp_num=10000,
                 sign_r=-1, sign_theta=1, sign_phi=1, fp='./', saver='json',
                 save_even_when_not_colliding=True, save_handle=None,
                 save_csv=False, save_redshift=False):
        self.s = s

        self.rem = rem
        self.tem = tem
        self.pem = pem

        self.rho = rho

        self.robs = robs
        self.tobs = tobs
        self.pobs = pobs

        self.alpha_min = alpha_min
        self.alpha_max = alpha_max
        self.beta_min = beta_min
        self.beta_max = beta_max
        self.resolution = resolution

        self.m = m

        self.start = start
        self.stop = stop
        self.ray_num = num
        self.abserr = abserr
        self.relerr = relerr

        self.interpolate_num = interp_num

        self.sign_r = sign_r
        self.sign_theta = sign_theta
        self.sign_phi = sign_phi

        self.fp = fp
        self.data_fp = self.setup()

        self.saver = saver
        self.save_exp = save_experiment.ExperimentSaver(self.fp, self.saver)
        self.save_handle = save_handle

        self.save_when_not_colliding = save_even_when_not_colliding
        self.save_csv = save_csv
        self.save_redshift = save_redshift

    def setup(self):
        data_fp = self.fp + 'data/'
        if not os.path.isdir(data_fp):
            os.mkdir(data_fp)

        return data_fp

    def run(self):
        total_time = 0
        number_of_collisions = 0

        solver = OneRaySolver(self.s, self.rem, self.tem, self.pem, self.rho, self.robs, self.tobs, self.pobs,
                              0., 0., self.m, self.start, self.stop, self.ray_num, self.abserr, self.relerr,
                              self.interpolate_num, self.sign_r, self.sign_theta, self.sign_phi, self.data_fp,
                              'json', self.save_when_not_colliding, self.save_handle, self.save_csv)

        data_form = []

        # generate the alpha - beta - matrix:
        alpha_beta_matrix = self._generate_alpha_beta_matrix()

        # main loop; for every alpha / beta pair, run the ray solver
        # also save total time, as well as the redshift
        for alpha, beta in alpha_beta_matrix:
            g, time_per_step = self.step(solver, alpha, beta)

            # save the redshift into data_form. Will need to sort for alpha (or beta) values later on.
            data_form.append([alpha, beta, g])

            # calculate total time took
            total_time += time_per_step

            # add to collision detector
            if g > 0:
                number_of_collisions += 1

        # save the experiment specific data
        self.save_exp.add_setup_information(self.alpha_min, self.alpha_max, self.beta_min, self.beta_max)
        self.save_exp.add_numeric_information(self.resolution, total_time, number_of_collisions)
        self.save_exp.save()

        if self.save_redshift:
            self.save_exp.save_redshift(data_form)

        #print(f'Took {total_time}s.')

    def step(self, solver, alpha, beta):
        # main routine to setup and calculate ONE ray from a specific solver (important for multithredding) and
        # save / do whatever has / wants to be done.
        start_time = time.time()
        solver.set_alpha_beta(alpha, beta)

        ray, info = solver.solve(full_output=True)
        took = time.time() - start_time

        return float(info['CONSTANTS_OF_MOTION']['redshift']), took

    def _generate_alpha_beta_matrix(self):
        alphas = np.linspace(self.alpha_min, self.alpha_max, num=self.resolution)
        betas = np.linspace(self.beta_min, self.beta_max, num=self.resolution)

        return [(a, b) for a in alphas for b in betas]