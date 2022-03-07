"""Converting the apparent position on screen (alpha, beta) into the constants of motion (qu, lamda)"""

import numpy as np


def alpha_beta_from_lamda_qu(lamda, qu, robs, tobs, m=1, a=0.):
    sigma = robs ** 2 + a ** 2 * np.cos(tobs) ** 2
    delta = robs ** 2 - 2 * robs + a ** 2
    A = (robs ** 2 + a ** 2) ** 2 - delta * a ** 2 * np.sin(tobs) ** 2
    theta = qu + a ** 2 * np.cos(tobs) ** 2 - lamda ** 2 / np.tan(tobs) ** 2
    R = robs ** 4 - (qu + lamda ** 2 - a ** 2) * robs ** 2 + 2 * (qu + (lamda - a) ** 2) * robs - a ** 2 * qu

    alpha = robs * lamda * sigma * np.sqrt(delta) / (np.sqrt(R * A) * np.sin(tobs))
    beta = - robs * np.sqrt(theta * delta / R)

    return alpha, beta


def lamda_qu_from_alpha_beta(alpha, beta, robs, tobs, m=1, a=0.):
    delta = robs ** 2 - 2 * robs + a ** 2
    A = (robs ** 2 + a ** 2) ** 2 - delta * a ** 2 * np.sin(tobs) ** 2
    sigma = robs ** 2 + a ** 2 * np.cos(tobs) ** 2
    omega = 2 * a * robs / A

    lamda = - alpha * np.sin(tobs) / (omega * alpha * np.sin(tobs) - (sigma * np.sqrt(delta) / A) * np.sqrt(
        robs ** 2 + alpha ** 2 + beta ** 2))
    qu = (lamda ** 2 - a ** 2) * np.cos(tobs) ** 2 + beta ** 2 * (1 - omega * lamda) ** 2 * A / (
                delta * (robs ** 2 + alpha ** 2 + beta ** 2))

    return lamda, qu
