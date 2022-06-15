"""Converting the apparent position on screen (alpha, beta) into the constants of motion (qu, lamda)"""

import numpy as np


def alpha_beta_from_lamda_qu(lamda, qu, robs, tobs, m=1, a=0.):
    alpha = lamda / (np.sin(tobs) * np.sqrt(1 - (qu + lamda**2) / robs**2))
    beta = np.sqrt((qu - lamda ** 2 / np.tan(tobs)**2) / (1 - (qu + lamda**2) / robs**2))

    return alpha, beta


def lamda_qu_from_alpha_beta(alpha, beta, robs, tobs, m=1, a=0.):
    lamda = np.sqrt(alpha ** 2 * np.sin(tobs) ** 2 * robs ** 2 / (alpha ** 2 + beta ** 2 + robs ** 2))
    qu = (beta**2 + alpha ** 2 * np.cos(tobs)**2) * (robs ** 2 / (alpha ** 2 + beta ** 2 + robs ** 2))
    if alpha < 0:
        lamda *= -1
    return lamda, qu
