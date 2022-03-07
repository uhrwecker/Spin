from scipy.integrate import odeint
import numpy as np
import contextlib
import os
import sys

from one_ray_solver.ode import kerr


def fileno(file_or_fd):
    fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd

@contextlib.contextmanager
def stdout_redirected(to=os.devnull, stdout=None):
    """
    https://stackoverflow.com/a/22434262/190597 (J.F. Sebastian)
    """
    if stdout is None:
       stdout = sys.stdout

    stdout_fd = fileno(stdout)
    # copy stdout_fd before it is overwritten
    #NOTE: `copied` is inheritable on Windows when duplicating a standard stream
    with os.fdopen(os.dup(stdout_fd), 'wb') as copied:
        stdout.flush()  # flush library buffers that dup2 knows nothing about
        try:
            os.dup2(fileno(to), stdout_fd)  # $ exec >&to
        except ValueError:  # filename
            with open(to, 'wb') as to_file:
                os.dup2(to_file.fileno(), stdout_fd)  # $ exec > to
        try:
            yield stdout # allow code to be run with the redirected stdout
        finally:
            # restore stdout to its previous value
            #NOTE: dup2 makes stdout_fd inheritable unconditionally
            stdout.flush()
            os.dup2(copied.fileno(), stdout_fd)  # $ exec >&copied


class ODESolverKerr:
    """Base class for solving the Kerr field euqations!"""
    def __init__(self, robs, tobs, pobs, l, q, m=1, bha=0., start=0, stop=70, num=100000, abserr=1e-7, relerr=1e-7,
                 sign_r=-1, sign_q=1, sign_l=1):
        self.m = m
        self.bha = bha

        self.t0 = 0
        self.robs = robs
        self.tobs = tobs
        self.pobs = pobs

        self.l = l
        self.q = q

        self.sign_r = sign_r
        self.sign_q = sign_q
        self.sign_l = sign_l

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

        with stdout_redirected():
            result = odeint(kerr.geod, psi, self.sigma, args=(self.m, self.bha), atol=self.abserr, rtol=self.relerr)

        return self.sigma, result

    def get_ic_from_com(self, l, q, sign_r=-1, sign_l=1, sign_q=1):
        delta = self.robs ** 2 - 2 * self.robs + self.bha ** 2
        sigma = self.robs ** 2 + self.bha ** 2 * np.cos(self.tobs) ** 2
        T_func = self.robs ** 2 + self.bha ** 2 - l * self.bha
        R_func = self.robs ** 4 - (q + l ** 2 - self.bha ** 2) * self.robs ** 2 + \
                 2 * (q + (l - self.bha) ** 2) * self.robs - self.bha ** 2 * q
        Th_func = q + self.bha ** 2 * np.cos(self.tobs) ** 2 - l ** 2 / np.tan(self.tobs) ** 2

        dt = 1 / sigma * (- self.bha * (self.bha * np.sin(self.tobs) ** 2 - l) +
                          (self.robs ** 2 + self.bha ** 2) * T_func / delta)

        dtheta = sign_q / sigma * np.sqrt(Th_func)

        dr = sign_r / sigma * np.sqrt(R_func)

        dphi = sign_l / sigma * (- self.bha + l / np.sin(self.tobs) ** 2 + self.bha * T_func / delta)

        print(dt, dr, dtheta, dphi)
        return dt, dr, dtheta, dphi

    def change_emission_point(self, r, t, p, recalc=True):
        self.robs = r
        self.tobs = t
        self.pobs = p

        if recalc:
            self.dt, self.dr, self.dtheta, self.dphi = self.get_ic_from_com(self.l, self.q, self.sign_r, self.sign_l,
                                                                            self.sign_q)

    def change_signs(self, sign_r, sign_q, sign_l, recalc=True):
        self.sign_r = sign_r
        self.sign_q = sign_q
        self.sign_l = sign_l

        if recalc:
            self.dt, self.dr, self.dtheta, self.dphi = self.get_ic_from_com(self.l, self.q, self.sign_r, self.sign_l,
                                                                            self.sign_q)

    def change_constants_of_motion(self, lamda, qu, recalc=True):
        self.l = lamda
        self.q = qu

        if recalc:
            self.dt, self.dr, self.dtheta, self.dphi = self.get_ic_from_com(self.l, self.q, self.sign_r, self.sign_l,
                                                                            self.sign_q)