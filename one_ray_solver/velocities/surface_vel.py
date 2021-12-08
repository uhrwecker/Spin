"""Surface velocity of any spinning object with radius rho and local spherical coordinates Phi and Theta."""

import numpy as np
from one_ray_solver.velocities import velocity_abc


class SurfaceVelocityRigidSphere(velocity_abc.VelocityABC):
    """Surface velocities u1 and u3 of a perfect rigid sphere."""
    def __init__(self, s, position):
        super().__init__(s, position)

        # note that position should be an iterable with
        # position = (rho, theta, phi)

    def _calculate_velocity(self):
        rho, theta, phi = self.position

        u1 = 5 * self.s / (2 * rho) * np.sin(phi) * np.sin(theta)
        u3 = 5 * self.s / (2 * rho) * np.cos(phi) * np.sin(theta)

        if 1 - u1 ** 2 - u3 ** 2 < 0:
            print('Velocities too high; returning nan.')
            return np.nan, np.nan, np.nan

        return (-u1, -u3), 1 / np.sqrt(1 - u1 ** 2 - u3 ** 2)


class SurfaceVelocityMaclaurinEllipsoid(velocity_abc.VelocityABC):
    def __init__(self, s, position):
        super().__init__(s, position)

        # note that position should be an iterable with
        # position = (a, theta, phi)

    def _calculate_velocity(self):
        a, theta, phi = self.position

        u1 = 5 * self.s / (2 * a) * np.sin(phi) * np.sin(theta)
        u3 = 5 * self.s / (2 * a) * np.cos(phi) * np.sin(theta)

        if 1 - u1 ** 2 - u3 ** 2 < 0:
            print('Velocities too high; returning nan.')
            return np.nan, np.nan, np.nan

        return (-u1, -u3), 1 / np.sqrt(1 - u1 ** 2 - u3 ** 2)