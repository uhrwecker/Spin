import numpy as np


def geod(w, t, m=1, a=0.):
    """
        Defines the differential equations for lightlike geodesics in Schwarzschild background.
        :param w: iterable; vector of the state variables
                  [t, t', r, r', theta, theta', phi, phi']
        :param t: float; time parameter, deprecated here.
        :return: iterable; vector of differntiated variables
                  [t', t'', r', r'', theta', theta'', phi', phi'']
    """

    t, td, r, rd, th, thd, phi, phid = w

    f = [td,
         tdd(a, r, th, td, rd, thd, phid),
         rd,
         rdd(a, r, th, td, rd, thd, phid),
         thd,
         thdd(a, r, th, td, rd, thd, phid),
         phid,
         phidd(a, r, th, td, rd, thd, phid)]

    return f


# second order derivatives:

def tdd(a, r, th, td, rd, thd, phid):
    factor = - gphph(a, r, th) / (gtt(a, r, th) * gphph(a, r, th) + gtph(a, r, th) ** 2)

    sum1 = gtph(a, r, th) / gphph(a, r, th) * (td * ddtau_tph(a, r, th, thd, rd) +
                                               phid * ddtau_phph(a, r, th, thd, rd))
    sum2 = td * ddtau_tt(a, r, th, thd, rd) + phid * ddtau_tph(a, r, th, thd, rd)

    return factor * (sum1 + sum2)


def rdd(a, r, th, td, rd, thd, phid):
    sum = td ** 2 * ddr_gtt(a, r, th) + \
          2 * td * phid * ddr_gtph(a, r, th) + \
          phid ** 2 * ddr_gphph(a, r, th) + \
          rd ** 2 * ddr_grr(a, r, th) + \
          thd ** 2 * ddr_gthth(a, r, th) - \
          2 * rd * ddtau_rr(a, r, th, thd, rd)

    return sum / (2 * grr(a, r, th))


def thdd(a, r, th, td, rd, thd, phid):
    sum = td ** 2 * ddth_gtt(a, r, th) + \
          2 * td * phid * ddth_gtph(a, r, th) + \
          phid ** 2 * ddth_gphph(a, r, th) + \
          rd ** 2 * ddth_grr(a, r, th) + \
          thd ** 2 * ddth_gthth(a, r, th) - \
          2 * thd * ddtau_thth(a, r, th, thd, rd)

    return sum / (2 * gthth(a, r, th))


def phidd(a, r, th, td, rd, thd, phid):
    factor = - gtt(a, r, th) / (gtt(a, r, th) * gphph(a, r, th) + gtph(a, r, th) ** 2)

    sum1 = gtph(a, r, th) / gtt(a, r, th) * (td * ddtau_tt(a, r, th, thd, rd) +
                                               phid * ddtau_tph(a, r, th, thd, rd))

    sum2 = td * ddtau_tph(a, r, th, thd, rd) + phid * ddtau_phph(a, r, th, thd, rd)

    return factor * (sum1 + sum2)


# metric elements:


def gtt(a, r, th):
    return - (1 - 2 * r / (r ** 2 + a ** 2 * np.cos(th) ** 2))


def gtph(a, r, th):
    return - 4 * r * a * np.sin(th) ** 2 / (r ** 2 + a ** 2 * np.cos(th) ** 2)


def gphph(a, r, th):
    return np.sin(th) ** 2 * (r ** 2 + a ** 2 + 2 * r * a ** 2 / (r ** 2 + a ** 2 * np.cos(th) ** 2))


def grr(a, r, th):
    return (r ** 2 + a ** 2 * np.cos(th) ** 2) / (r ** 2 - 2 * r + a ** 2)


def gthth(a, r, th):
    return r ** 2 + a ** 2 * np.cos(th) ** 2


# derivatives theta:


def ddth_gtt(a, r, th):
    return 4 * r * a ** 2 * np.cos(th) * np.sin(th) / (r ** 2 + a ** 2 * np.cos(th) ** 2) ** 2


def ddth_grr(a, r, th):
    return - 2 * a ** 2 * np.sin(th) * np.cos(th) / (r**2 - 2 * r + a **2)


def ddth_gthth(a, r, th):
    return - 2 * a ** 2 * np.sin(th) * np.cos(th)


def ddth_gtph(a, r, th):
    return - 8 * r * a * np.sin(th) * np.cos(th) * (r**2 + a ** 2) / (r ** 2 + a ** 2 * np.cos(th) ** 2) ** 2


def ddth_gphph(a, r, th):
    return 2 * np.cos(th) * np.sin(th) * (r ** 2 + a ** 2 + 2 * r * a ** 2 * (r**2 + a ** 2) /
                                          (r ** 2 + a ** 2 * np.cos(th) ** 2)) ** 2


# derivatives r:


def ddr_gtt(a, r, th):
    return - 2 * (r - a ** 2 * np.cos(th) ** 2) / (r ** 2 + a ** 2 * np.cos(th) ** 2)


def ddr_gtph(a, r, th):
    return 4 * a * np.sin(th) ** 2 * (r - a ** 2 * np.cos(th) ** 2) / (r ** 2 + a ** 2 * np.cos(th) ** 2) ** 2


def ddr_gphph(a, r, th):
    return 2 * np.sin(th) ** 2 * (r - 2 * a ** 2 * (r - a ** 2 * np.cos(th) ** 2) / (r ** 2 + a ** 2 * np.cos(th) ** 2) ** 2)


def ddr_grr(a, r, th):
    return - (2 * r ** 2 - a ** 2 * (1 - 2 * np.cos(th) ** 2 * (r - 1))) / (r ** 2 + a ** 2 * np.cos(th) ** 2) ** 2


def ddr_gthth(a, r, th):
    return 2 * r


# derivatives total:


def ddtau_tt(a, r, th, dth, dr):
    return ddr_gtt(a, r, th) * dr + ddth_gtt(a, r, th) * dth


def ddtau_tph(a, r, th, dth, dr):
    return ddr_gtph(a, r, th) * dr + ddth_gtph(a, r, th) * dth


def ddtau_phph(a, r, th, dth, dr):
    return ddr_gphph(a, r, th) * dr + ddth_gphph(a, r, th) * dth


def ddtau_rr(a, r, th, dth, dr):
    return ddr_grr(a, r, th) * dr + ddth_grr(a, r, th) * dth


def ddtau_thth(a, r, th, dth, dr):
    return ddr_gthth(a, r, th) * dr + ddth_gthth(a, r, th) * dth
