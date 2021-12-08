"""This class checks whether the emitter is hit by the light ray coming from the observer,
and gets the minimal distance and the position of impact."""

import numpy as np

import one_ray_solver.collision.sphere as sphere
import one_ray_solver.collision.ellipse as ellipse


class Collider:
    def __init__(self, rem, tem, pem, geometry, interpolation_steps=10000, shape='sphere'):
        self.rem = rem
        self.tem = tem
        self.pem = pem

        self.geometry = geometry

        self.interpolation_steps = interpolation_steps

        if shape == 'sphere':
            self.shape = sphere
        elif shape == 'ellipsoid':
            self.shape = ellipse

    def check(self, ray):
        r = ray[:, 2]
        theta = ray[:, 4]
        phi = ray[:, 6]

        # check if there is a collision in general:
        if not r[r < self.rem + self.geometry[0]].size:
            return [], [], False

        # find the minimal distance:
        r_col, t_col, p_col = self.shape.collision_with_object(r, theta, phi, (self.rem, self.tem, self.pem), self.geometry)

        if not r_col:
            return [], [], False

        # get the local coordinates, depending on the geometry:
        rr, T, P = self.shape.convert_position((r_col, t_col, p_col), (self.rem, self.tem, self.pem), self.geometry)
        if P < 0:
            P += np.pi * 2

        if not np.isclose(rr, self.geometry[0], rtol=1e-2, atol=1e-1) and len(self.geometry) == 1:
            print('Numerically, there seems to be an error, as the collision detected. See the corresponding developer.')

        return (r_col, t_col, p_col), (T, P), True
