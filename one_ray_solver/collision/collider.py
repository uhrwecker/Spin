"""This class checks whether the emitter is hit by the light ray coming from the observer,
and gets the minimal distance and the position of impact."""

import numpy as np

import one_ray_solver.collision.sphere as sphere


class Collider:
    def __init__(self, robs, tobs, pobs, rem, tem, pem, geometry, interpolation_steps=10000):
        self.robs = robs
        self.tobs = tobs
        self.pobs = pobs

        self.rem = rem
        self.tem = tem
        self.pem = pem

        self.geometry = geometry

        self.interpolation_steps = interpolation_steps

    def check(self, ray):
        r = ray[:, 2]
        theta = ray[:, 4]
        phi = ray[:, 6]

        # TODO: include more than spherical geometry here, should not be that hard
        rho, = self.geometry
        # check if there is a collision in general:
        if not r[r < self.rem + rho]:
            return [], [], False

        # find the minimal distance:
        r_col, t_col, p_col = sphere.collision_with_sphere(r, theta, phi, (self.rem, self.tem, self.pem), self.geometry)

        # get the local coordinates, depending on the geometry:
        rr, T, P = sphere.convert_position_sphere((r_col, t_col, p_col), (self.rem, self.tem, self.pem), self.geometry)
        print(rr, rho)

        return (r_col, t_col, p_col), (T, P), True
