"""Test script for trying some things."""
import numpy as np
from one_ray_solver import solve

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

    ray = solve.OneRaySolver(s, rem, tem, pem, rho, robs, tobs, pobs, alpha, beta)
    ray.solve()

if __name__ == '__main__':
    main()