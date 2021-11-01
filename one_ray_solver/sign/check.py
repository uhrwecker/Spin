"""This class is here to check the signs and the four-momentum of the photon at the position of impact."""

import numpy as np


class SignImpactSchwarzschild:
    def __init__(self, solver, position, observer_position, geometry):
        self.solver = solver

        self.rem, self.tem, self.pem = position
        self.robs, self.tobs, self.pobs = observer_position

        self.dt, self.dr, self.dtheta, self.dphi = self.calculate_initial_velocities()

    def calculate_initial_velocities(self, geometry, data):
        collision = True

        # initial guess:
        sign_r = self.solver.sign_r
        sign_q = self.solver.sign_q
        sign_l = self.solver.sign_l

        while not collision:
            # initial guess:
            self.solver.change_signs(sign_r, sign_q, sign_l)
            data = self.solver.solve()

            collision = self._check_if_at_observer(data)
            print(collision)

            collision = False

    def _check_if_at_observer(self, data):
        r0, t0, p0 = self.robs, self.tobs, self.pobs

        r = data[:, 2]
        t = data[:, 4]
        p = data[:, 6]

        x = r * np.cos(p) * np.sin(t)
        y = r * np.sin(p) * np.sin(t)
        z = r * np.cos(t)

        X = r0 * np.cos(p0) * np.sin(t0)
        Y = r0 * np.sin(p0) * np.sin(t0)
        Z = r0 * np.cos(t0)

        dist = np.sqrt((x - X) ** 2 + (y - Y) ** 2 + (z - Z) ** 2)

        if np.amin(dist) < 1e-2:
            return True

        else:
            return False