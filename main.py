"""Test script for trying some things."""
import numpy as np
from one_ray_solver import solve
from visualisation import simple_3d
from ray_experiment import ray_handler


def main():
    robs = 35
    tobs = 1
    pobs = 0

    rem = 8
    tem = np.pi / 2
    pem = 0

    rho = 0.5

    s = 0.

    alpha = -5
    beta = -5

    rh = ray_handler.RayHandler(s, rem, tem, pem, rho, robs, tobs, pobs, fp='./', save_redshift=True)
    rh.run()

    #ray = solve.OneRaySolver(s, rem, tem, pem, rho, robs, tobs, pobs, alpha, beta, fp='../')
    #solver = ray.get_solver()
    #plot = simple_3d.Simple3DPlotter([robs, tobs, pobs], [rem, tem, pem])

    #data, info = ray.solve(full_output=True)
    #if info:
    #    emitting_point = (info['INITIAL_DATA']['r0'], info['INITIAL_DATA']['theta0'], info['INITIAL_DATA']['phi0'])
    #plot.plot_from_alpha_beta(solver, alpha, beta, sign_r=-1, sign_theta=1, sign_phi=1, starting_from='observer')
    #plot.show()



if __name__ == '__main__':
    main()