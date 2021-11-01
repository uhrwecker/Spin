from scipy.integrate import odeint
import numpy as np

from one_ray_solver.ode import schwarzschild


class ODESolverSchwazrschild:
    """Base class for solving the Schwarzschild field euqations!"""
    def __init__(self, robs, tobs, pobs, l, q, m=1, start=0, stop=70, num=100000, abserr=1e-7, relerr=1e-7,
                 sign_r=-1, sign_q=1, sign_l=1):
        self.m = m

        self.t0 = 0
        self.robs = robs
        self.tobs = tobs
        self.pobs = pobs

        self.dt, self.dr, self.dtheta, self.dphi = self.get_ic_from_com(l, q,
                                                                        sign_r=sign_r, sign_q=sign_q, sign_l=sign_l)

        self.start = start
        self.stop = stop
        self.num = num
        self.abserr = abserr
        self.relerr = relerr
        self.sigma = np.linspace(self.start, self.stop, num=self.num)

    def solve(self):
        """
            Main routine for solving with the previously specified initial conditions
            :return: iter; [sigma, result] where sigma is the array of affine parameter, and result includes all [x, x']
        """
        psi = np.array([self.t0, self.dt, self.robs, self.dr, self.tobs, self.dtheta, self.pobs, self.dphi])

        result = odeint(schwarzschild.geod, psi, self.sigma, args=(self.m, ), atol=self.abserr, rtol=self.relerr)

        return self.sigma, result

    def get_ic_from_com(self, l, q, sign_r=-1, sign_l=1, sign_q=1):
        dt = 1 / (1 - 2 * self.m / self.robs)

        dtheta = sign_q * np.sqrt(np.abs(q - l**2 / np.tan(self.tobs)**2)) / self.robs**2

        dr = sign_r * np.sqrt(1 - (q + l**2) / self.robs**2 * (1 - 2 * self.m / self.robs))

        dphi = sign_l * l / (self.robs * np.sin(self.tobs))**2

        return dt, dr, dtheta, dphi