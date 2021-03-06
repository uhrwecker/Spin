"""The orbit velocity for a spinning test particle on an circular orbit with spin (anti)parallel to the
orbit angular momentum"""

import numpy as np
from one_ray_solver.velocities import velocity_abc


class OrbitVelocitySchwarzschild(velocity_abc.VelocityABC):
    """Class that contains the information for the orbit velocity of a spinning test particle in a Schwarzschild back-
    ground."""
    def __init__(self, s, position):
        super().__init__(s, position)

    def _calculate_velocity(self):
        root = 4 * self.position ** 3 + 13 * self.s ** 2 - 8 * self.s ** 4 / self.position ** 3
        denominator = 2 * np.sqrt(self.position ** 2 - 2 * self.position) * (
                self.position - self.s ** 2 / self.position ** 2)

        v = (-3 * self.s + np.sqrt(root)) / denominator

        return (v, ), 1 / np.sqrt(1 - v ** 2)
