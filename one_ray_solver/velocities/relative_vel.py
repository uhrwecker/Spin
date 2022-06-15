"""The relative velocity between the linear orbit momentum and the tangent of the worldline."""

import numpy as np
from one_ray_solver.velocities import velocity_abc


class RelativeVelocitySchwarzschild(velocity_abc.VelocityABC):
    """Relative velocity for a test particle moving in Schwarzschild background"""
    def __init__(self, s, position):
        super().__init__(s, position)

    def _calculate_velocity(self):
        chi_v = self._chi_v()

        chi_u = (self.position - self.s ** 2 / self.position ** 2) / \
                (self.position + 2 * self.s ** 2 / self.position ** 2) * chi_v

        v = 1 - (1 - chi_v ** 2) * (1 - chi_u ** 2) / (1 - chi_u * chi_v) ** 2

        return (v, ), 1 / np.sqrt(1 - v ** 2)

    def _chi_v(self):
        """Claculate Chi_v in particular. It is the same as the orbit velocity."""
        root = 4 * self.position ** 3 + 13 * self.s ** 2 - 8 * self.s ** 4 / self.position ** 3
        denominator = 2 * np.sqrt(self.position ** 2 - 2 * self.position) * (
                self.position - self.s ** 2 / self.position ** 2)

        v = (-3 * self.s + np.sqrt(root)) / denominator

        return v


class RelativeVelocityKerr(velocity_abc.VelocityABC):
    """Relative velocity for a test particle moving in Schwarzschild background"""
    def __init__(self, s, a, position):
        self.a = a
        super().__init__(s, position)

    def _calculate_velocity(self):
        chi_v = self._chi_v()

        chi_u = (self.position - self.s ** 2 / self.position ** 2) / \
                (self.position + 2 * self.s ** 2 / self.position ** 2) * chi_v

        v = 1 - (1 - chi_v ** 2) * (1 - chi_u ** 2) / (1 - chi_u * chi_v) ** 2

        return (v, ), 1 / np.sqrt(1 - v ** 2)

    def _chi_v(self):
        """Claculate Chi_v in particular. It is the same as the orbit velocity."""
        root = 4 * self.position ** 3 + \
               12 * self.a * self.position * self.s + \
               13 * self.s ** 2 + \
               6 * self.a * self.s ** 3 / self.position ** 2 - \
               8 * self.s ** 4 / self.position ** 3 + \
               9 * self.a ** 2 * self.s ** 4 / self.position ** 4
        denominator = 2 * np.sqrt(self.position ** 2 - 2 * self.position + self.a ** 2) * (
                self.position - self.s ** 2 / self.position ** 2)

        v = (- 2 * self.position * self.a - 3 * self.s - self.a * self.s ** 2 / self.position ** 2
             + np.sqrt(root)) / denominator

        return v
