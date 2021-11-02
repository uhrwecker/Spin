"""This class handles the instanciation and running of several light rays, corresponding to a specified section on
the screen."""

import numpy as np

from one_ray_solver.solve import OneRaySolver


class RayHandler:
    """
    This class will take the experiment input - resolution of the specified section of the screen, and emitter and
    observer properties - and runs the one ray solver for each combination. Afterwards, specific actions (saving etc)
    will be done by this handler.
    """
    def __init__(self, s=0., rem=8., tem=np.pi/2, pem=0., rho=0.5, robs=35., tobs=1., pobs=0.,
                 alpha_min=0., alpha_max=1., beta_min=-5., beta_max=-2., resolution=10, m=1, start=0,
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
        self.saver = saver
        self.save_handle = save_handle

        self.save_when_not_colliding = save_even_when_not_colliding
        self.save_csv = save_csv
        self.save_redshift = save_redshift

    def setup(self):
        solver = OneRaySolver(self.s, self.rem, self.tem, self.pem, self.rho, self.robs, self.tobs, self.pobs,
                              0., 0., self.m, self.start, self.stop, self.ray_num, self.abserr, self.relerr,
                              self.interpolate_num, self.sign_r, self.sign_theta, self.sign_phi, self.fp,
                              self.saver, self.save_when_not_colliding, self.save_handle, self.save_csv)

    def step(self, solver, alpha, beta):
        # main routine to setup and calculate ONE ray from a specific solver (important for multithredding) and
        # save / do whatever has / wants to be done.
        solver.set_alpha_beta(alpha, beta)

