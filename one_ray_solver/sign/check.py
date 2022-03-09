"""This class is here to check the signs and the four-momentum of the photon at the position of impact."""

import numpy as np


class SignImpactSchwarzschild:
    def __init__(self, solver, position, observer_position):
        self.solver = solver

        self.rem, self.tem, self.pem = position
        self.robs, self.tobs, self.pobs = observer_position

        self.problem = self.check_observer_collision()

    def check_observer_collision(self):
        problem_flag = False
        # all sign combinations, in order if likelihood:
        signs = [(-1, -1, -1), (1, -1, -1), (-1, 1, -1), (1, 1, -1),
                 (-1, -1, 1), (1, -1, 1), (-1, 1, 1), (1, 1, 1)]

        dist = 10000
        best_signs = (-1, -1, -1)

        for sign_comb in signs:
            # initial guess:
            sign_r = sign_comb[0]
            sign_q = sign_comb[1]
            sign_l = sign_comb[2]

            self.solver.change_signs(sign_r=sign_r, sign_q=sign_q, sign_l=sign_l, recalc=False)
            self.solver.change_emission_point(self.rem, self.tem, self.pem)
            _, data = self.solver.solve()

            coll, smallest_distance = self._check_if_at_observer(data)

            if dist > smallest_distance:
                dist = smallest_distance
                best_signs = sign_comb

        if not dist < 1e-1:
            print(f'Somethings not quite right here! Smallest distance {dist}.')
            problem_flag = True

        sign_r = best_signs[0]
        sign_q = best_signs[1]
        sign_l = best_signs[2]

        self.solver.change_signs(sign_r=sign_r, sign_q=sign_q, sign_l=sign_l, recalc=False)
        self.solver.change_emission_point(self.rem, self.tem, self.pem)

        return problem_flag

    def calculate_initial_velocities(self):
        return self.solver.dt, self.solver.dr, self.solver.dtheta, self.solver.dphi

    def calculate_initial_momenta_general(self):
        a = self.solver.bha
        delta = self.rem ** 2 - 2 * self.rem + a ** 2
        sigma = self.rem ** 2 + a ** 2 * np.cos(self.tem) ** 2
        A = (self.rem ** 2 + a ** 2) ** 2 - delta * a ** 2 * np.sin(self.tem)

        pt = - sigma * delta / A * self.solver.dt - \
             4 * self.rem * a * np.sin(self.tem) ** 2 / sigma * self.solver.dphi
        pr = sigma / delta * self.solver.dr
        pth = sigma * self.solver.dtheta
        pphi = A * np.sin(self.tem)**2 / sigma * self.solver.dphi - \
             8 * self.rem ** 2 * a ** 2 * np.sin(self.tem) ** 2 / (sigma * A) * self.solver.dt

        return pt, pr, pth, pphi

    def calculate_initial_momenta_ZAMO(self):
        a = self.solver.bha
        delta = self.rem ** 2 - 2 * self.rem + a ** 2
        A = (self.rem ** 2 + a ** 2) ** 2 - delta * a ** 2 * np.sin(self.tem)
        sigma = self.rem ** 2 + a ** 2 * np.cos(self.tem) ** 2

        e_nu = np.sqrt(A / (sigma * delta))
        e_psi = np.sqrt(sigma / (A * np.sin(self.tem) ** 2))
        e_mu1 = np.sqrt(delta / sigma)
        e_mu2 = np.sqrt(1 / sigma)
        omega = 2 * a * self.rem / A

        pt, pr, pth, pphi = self.calculate_initial_momenta_general()

        return e_nu * pt + omega * e_nu * pphi, e_mu1 * pr, e_mu2 * pth, e_psi * pphi

    def _solve(self):
        return self.solver.solve()

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
            return True, np.amin(dist)

        else:
            return False, np.amin(dist)