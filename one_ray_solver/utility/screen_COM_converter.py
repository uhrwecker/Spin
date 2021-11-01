"""Converting the apparent position on screen (alpha, beta) into the constants of motion (qu, lamda)"""

import numpy as np


def alpha_beta_from_lamda_qu(lamda, qu, robs, tobs, m=1):
    root = 1 / (1 - 2 * m / robs) - (qu + lamda**2) / robs **2

    alpha = - lamda / np.sin(tobs) * 1 / np.sqrt(root)
    beta = - np.sqrt((qu - lamda**2 / np.tan(tobs)**2) / root)

    return alpha, beta


def lamda_qu_from_alpha_beta(alpha, beta, robs, tobs, m=1):
    factor = robs **2 / (alpha ** 2 + beta ** 2 + robs ** 2)

    lamda = alpha * np.sin(tobs) * np.sqrt(factor / (1 - 2 * m / robs))
    qu = (beta**2 + alpha**2 * np.cos(tobs)**2) / (1 - 2/robs) * factor

    return lamda, qu
