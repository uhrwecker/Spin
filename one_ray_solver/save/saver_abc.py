"""Abstract base class that defines the interface for a saver  class. Should support all fields in it; raises
error otherwise."""


class DataSaverABC:
    def __init__(self, fp='./'):
        self.fp = fp

    def add_observer_info(self, robs, tobs, pobs, alpha, beta):
        """Add observer info to your internal configuration."""
        raise NotImplementedError('Add observer info to your saver class.')

    def add_emitter_info(self, s, rho, theta, phi):
        """Add emitter info to your internal configuration."""
        raise NotImplementedError('Add emitter info to your saver class.')

    def add_initial_data_info(self, t0, r0, th0, p0, dt, dr, dth, dp):
        """Add initial data info to your internal configuration."""
        raise NotImplementedError('Add initial data info to your saver class.')

    def add_momenta_info(self, pt, pr, ptheta, pphi, p0, p1, p2, p3):
        """Add momenta info to your internal configuration."""
        raise NotImplementedError('Add momenta info to your saver class.')

    def add_constants_of_motion(self, lamda, qu, redshift):
        """Add COM info to your internal configuration."""
        raise NotImplementedError('Add COM info to your saver class.')

    def add_velocities_info(self, orbit, gamma_orbit, rel_vel, gamma_rel_vel, u1, u3, gamma_u13):
        """Add velocities info to your internal configuration."""
        raise NotImplementedError('Add velocities info to your saver class.')

    def add_numerics_info(self, start, stop, num, abserr, relerr, interp_num, time):
        """Add ´numerical info to your internal configuration."""
        raise NotImplementedError('Add numerical info to your saver class.')

    def save(self, handle=None):
        """Add a saving function. The handle should be able to be indivualized, but the ending will be prefixed by you."""
        raise NotImplementedError('Add saving functionality to your saver duh.')

    def save_data_to_csv(self, sigma, ray, handle=None):
        """Add a functionality to save the light ray to .csv."""
        raise NotImplementedError('Add a .csv saving functionality.')