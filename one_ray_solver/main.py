"""Test script for trying some things."""
import numpy as np
from one_ray_solver.ode import solver
from one_ray_solver.collision import collider
from one_ray_solver.utility import screen_COM_converter
from one_ray_solver.sign import check

import matplotlib.pyplot as pl

def main():
    robs = 35
    tobs = 1
    pobs = 0

    rem = 8
    tem = np.pi / 2
    pem = 0

    rho = 0.5

    s = 0

    alpha = 0.5
    beta = -5

    l, q = screen_COM_converter.lamda_qu_from_alpha_beta(alpha, beta, robs, tobs)
    sol = solver.ODESolverSchwazrschild(robs, tobs, pobs, l, q)

    _, data = sol.solve()

    col = collider.Collider(rem, tem, pem, [rho])
    res = col.check(data)

    ch = check.SignImpactSchwarzschild(sol, res[0], (robs, tobs, pobs))
    vels = ch.calculate_initial_velocities()

if __name__ == '__main__':
    main()