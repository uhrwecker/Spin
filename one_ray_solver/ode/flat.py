import numpy as np


def geod(w, t, m=1, a=0):
    """
        Defines the differential equations for lightlike geodesics in flat background.
        :param w: iterable; vector of the state variables
                  [t, t', r, r', theta, theta', phi, phi']
        :param t: float; time parameter, deprecated here.
        :return: iterable; vector of differntiated variables
                  [t', t'', r', r'', theta', theta'', phi', phi'']
    """

    t, td, r, rd, th, thd, phi, phid = w

    f = [td,
         0,
         rd,
         r * thd**2 + r * np.sin(th) ** 2 * phid ** 2,
         thd,
         -2 / r * rd * thd + np.cos(th) * np.sin(th) * phid ** 2,
         phid,
         - 2 / r * rd * phid - 2 / np.tan(th) * thd * phid]

    return f
