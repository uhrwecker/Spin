import configparser as cp
import pandas as pd

from one_ray_solver.save import saver_abc


class DataSaverConfig(saver_abc.DataSaverABC):
    def __init__(self, fp='./'):
        super().__init__(fp)
        self.config = cp.ConfigParser()

        self.config['OBSERVER'] = {}
        self.config['EMITTER'] = {}
        self.config['INITIAL_DATA'] = {}
        self.config['MOMENTA'] = {}
        self.config['CONSTANTS_OF_MOTION'] = {}
        self.config['VELOCITIES'] = {}
        self.config['NUMERICS'] = {}

    def add_observer_info(self, robs, tobs, pobs, alpha, beta):
        self.config['OBSERVER']['robs'] = str(robs)
        self.config['OBSERVER']['tobs'] = str(tobs)
        self.config['OBSERVER']['pobs'] = str(pobs)

        self.config['OBSERVER']['alpha'] = str(alpha)
        self.config['OBSERVER']['beta'] = str(beta)

    def add_emitter_info(self, s, a, geometry, theta, phi, shape):
        self.config['EMITTER']['shape'] = shape
        self.config['EMITTER']['s'] = str(s)
        self.config['EMITTER']['bh_a'] = str(a)
        if shape == 'sphere':
            self.config['EMITTER']['rho'] = str(geometry[0])
        elif shape == 'ellipsoid':
            self.config['EMITTER']['a'] = str(geometry[0])
            self.config['EMITTER']['c'] = str(geometry[1])
        self.config['EMITTER']['Theta'] = str(theta)
        self.config['EMITTER']['Phi'] = str(phi)

    def add_initial_data_info(self, t0, r0, th0, p0, dt, dr, dth, dp):
        self.config['INITIAL_DATA']['t0'] = str(t0)
        self.config['INITIAL_DATA']['r0'] = str(r0)
        self.config['INITIAL_DATA']['theta0'] = str(th0)
        self.config['INITIAL_DATA']['phi0'] = str(p0)

        self.config['INITIAL_DATA']['dt'] = str(dt)
        self.config['INITIAL_DATA']['dr'] = str(dr)
        self.config['INITIAL_DATA']['dtheta'] = str(dth)
        self.config['INITIAL_DATA']['dphi'] = str(dp)

    def add_momenta_info(self, pt, pr, ptheta, pphi, p0, p1, p2, p3):
        self.config['MOMENTA']['p_t'] = str(pt)
        self.config['MOMENTA']['p_r'] = str(pr)
        self.config['MOMENTA']['p_theta'] = str(ptheta)
        self.config['MOMENTA']['p_phi'] = str(pphi)

        self.config['MOMENTA']['p_0'] = str(p0)
        self.config['MOMENTA']['p_1'] = str(p1)
        self.config['MOMENTA']['p_2'] = str(p2)
        self.config['MOMENTA']['p_3'] = str(p3)

    def add_constants_of_motion(self, lamda, qu, redshift):
        self.config['CONSTANTS_OF_MOTION']['lambda'] = str(lamda)
        self.config['CONSTANTS_OF_MOTION']['q'] = str(qu)
        self.config['CONSTANTS_OF_MOTION']['redshift'] = str(redshift)

    def add_velocities_info(self, orbit, gamma_orbit, rel_vel, gamma_rel_vel, u1, u3, gamma_u13):
        self.config['VELOCITIES']['orbit'] = str(orbit)
        self.config['VELOCITIES']['gamma_orbit'] = str(gamma_orbit)

        self.config['VELOCITIES']['relative_velocitiy'] = str(rel_vel)
        self.config['VELOCITIES']['gamma_rel_vel'] = str(gamma_rel_vel)

        self.config['VELOCITIES']['surf_u1'] = str(u1)
        self.config['VELOCITIES']['surf_u3'] = str(u3)
        self.config['VELOCITIES']['gamma_surf_u'] = str(gamma_u13)

    def add_numerics_info(self, start, stop, num, abserr, relerr, interp_num, time):
        self.config['NUMERICS']['start'] = str(start)
        self.config['NUMERICS']['stop'] = str(stop)
        self.config['NUMERICS']['lightray_num'] = str(num)
        self.config['NUMERICS']['abserr'] = str(abserr)
        self.config['NUMERICS']['relerr'] = str(relerr)
        self.config['NUMERICS']['interpolation_num'] = str(interp_num)
        self.config['NUMERICS']['time_spent'] = str(time)

    def save(self, handle=None):
        if not handle:
            s = self.config['EMITTER']['s']
            alpha = self.config['OBSERVER']['alpha']
            beta = self.config['OBSERVER']['beta']
            handle = f'{s}_{alpha}_{beta}'

        with open(self.fp + handle + '.cfg', 'w') as file:
            self.config.write(file)

    def save_data_to_csv(self, sigma, ray, handle=None):
        data = {}
        data['sigma'] = sigma

        data['t'] = ray[:, 0]
        data['dt'] = ray[:, 1]
        data['r'] = ray[:, 2]
        data['dr'] = ray[:, 3]
        data['theta'] = ray[:, 4]
        data['dtheta'] = ray[:, 5]
        data['phi'] = ray[:, 6]
        data['dphi'] = ray[:, 7]

        frame = pd.DataFrame(data)

        if not handle:
            s = self.config['EMITTER']['s']
            alpha = self.config['OBSERVER']['alpha']
            beta = self.config['OBSERVER']['beta']
            handle = f'{s}_{alpha}_{beta}'

        frame.to_csv(self.fp + handle + '.csv', index=False)