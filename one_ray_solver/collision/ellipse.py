"""Collision function that tests whether or not a light ray passes through an elliptical object (Maclaurin)
with eq. semi-major axis a and vertical semi-major axis c."""

import numpy as np


def collision_with_object(r, t, p, position, geometry):
    """Return the collision point as a tuple if there is an collision, and an empty list if not."""
    r0, t0, p0 = position
    a, c = geometry

    re, te, pe = (r, t, p)#convert_position((r, t, p), position, geometry)#

    x = re * np.cos(pe) * np.sin(te)
    y = re * np.sin(pe) * np.sin(te)
    z = re * np.cos(te)

    xc = r0 * np.cos(p0) * np.sin(t0)
    yc = r0 * np.sin(p0) * np.sin(t0)
    zc = r0 * np.cos(t0)

    quest = (x - xc)**2 / a**2 + (y - yc)**2 / a**2 + (z - zc)**2 / c**2

    if np.nanmin(quest) < 1:
        idx = np.where(quest < 1)[0][0]
        return r[idx], t[idx], p[idx]

    else:
        return [], [], []


def convert_position(position, centre, geometry):
    r, t, p = position
    r0, t0, p0 = centre
    a, c = geometry

    x = r * np.cos(p) * np.sin(t)
    y = r * np.sin(p) * np.sin(t)
    z = r * np.cos(t)

    x -= r0 * np.cos(p0) * np.sin(t0)
    y -= r0 * np.sin(p0) * np.sin(t0)
    z -= r0 * np.cos(t0)

    xn = np.cos(p0) * x + np.sin(p0) * y
    yn = -np.sin(p0) * x + np.cos(p0) * y

    r = np.sqrt(xn ** 2 / a**2 + yn ** 2 / a**2 + z ** 2 / c**2) # not really sensible
    theta = np.arccos(z / c)#np.arcsin(a / np.sqrt(xn**2 + yn**2))
    #print(z / c)
    #print(theta, np.arcsin(a / np.sqrt(xn**2 + yn**2)))
    phi = get_phi(xn, yn, z)#np.array([get_phi(xn[n], yn[n], z[n]) for n in range(len(xn))])

    return r, theta, phi


def get_phi(x, y, z, tol=1e-4):
    """
    From cartesian x, y, z coordinates, get the angle phi.
    """
    if x > tol:
        return np.arctan(y / x)
    elif -tol < x < tol:
        return np.sign(y) * np.pi / 2
    elif x < tol and y >= 0:
        return np.arctan(y / x) + np.pi
    elif x < tol and y < 0:
        return np.arctan(y / x) - np.pi
