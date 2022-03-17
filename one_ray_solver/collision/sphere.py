"""Collision function that tests whether or not a light ray passes through an spherical object with radius rho."""

import numpy as np


def collision_with_object(r, t, p, position, geometry):
    """Return the collision point as a tuple if there is an collision, and an empty list if not."""
    r0, t0, p0 = position
    rho,  = geometry

    x = r * np.cos(p) * np.sin(t)
    y = r * np.sin(p) * np.sin(t)
    z = r * np.cos(t)

    X = r0 * np.cos(p0) * np.sin(t0)
    Y = r0 * np.sin(p0) * np.sin(t0)
    Z = r0 * np.cos(t0)

    dist = np.sqrt((x - X) ** 2 + (y - Y) ** 2 + (z - Z) ** 2)

    if np.amin(dist) < rho:
        idx = np.where(dist < rho)[0][0]
        return r[idx], t[idx], p[idx]

    else:
        return [], [], []


def convert_position(position, centre, geometry):
    r, t, p = position
    r0, t0, p0 = centre
    rho, = geometry

    x = r * np.cos(p) * np.sin(t)
    y = r * np.sin(p) * np.sin(t)
    z = r * np.cos(t)

    x -= r0 * np.cos(p0) * np.sin(t0)
    y -= r0 * np.sin(p0) * np.sin(t0)
    z -= r0 * np.cos(t0)

    xn = np.cos(p0) * x + np.sin(p0) * y
    yn = -np.sin(p0) * x + np.cos(p0) * y

    r = np.sqrt(xn ** 2 + yn ** 2 + z ** 2)
    theta = np.arccos(z / r)
    phi = get_phi(xn, yn, z)

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