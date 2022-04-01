

def g(p0, p1, p3, orbit_vel, gamma_orbit, rel_vel, gamma_rv, u1, u3, gamma_u):
    big_bracket = - gamma_u * gamma_rv * rel_vel + gamma_u * u3 * (1 + (gamma_rv**2 * rel_vel**2) / (1 + gamma_rv))

    factor_1 = gamma_orbit * (gamma_u * gamma_rv - gamma_u * u3 * gamma_rv * rel_vel) - \
               gamma_orbit * orbit_vel * big_bracket
    factor_1 *= p0

    factor_2 = - gamma_u * u1
    factor_2 *= p1

    factor_3 = - gamma_orbit * orbit_vel * (gamma_u * gamma_rv - gamma_u * u3 * gamma_rv * rel_vel) + \
               (1 + (gamma_orbit**2 * orbit_vel**2) / (1 + gamma_orbit)) * big_bracket
    factor_3 *= p3

    return factor_1 + factor_2 + factor_3
