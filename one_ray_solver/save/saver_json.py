import json
import pandas as pd
import os

from one_ray_solver.save import saver_abc


class DataSaverJson(saver_abc.DataSaverABC):
    def __init__(self, fp='./'):
        super().__init__(fp)
        self.config = {'OBSERVER': {}, 'EMITTER': {}, 'INITIAL_DATA': {}, 'MOMENTA': {}, 'CONSTANTS_OF_MOTION': {},
                       'VELOCITIES': {}, 'NUMERICS': {}}

    def add_observer_info(self, robs, tobs, pobs, alpha, beta):
        self.config['OBSERVER']['robs'] = robs
        self.config['OBSERVER']['tobs'] = tobs
        self.config['OBSERVER']['pobs'] = pobs

        self.config['OBSERVER']['alpha'] = alpha
        self.config['OBSERVER']['beta'] = beta

    def add_emitter_info(self, s, geometry, theta, phi, shape):
        self.config['EMITTER']['shape'] = shape
        self.config['EMITTER']['s'] = s
        if shape == 'sphere':
            self.config['EMITTER']['rho'] = geometry[0]
        elif shape == 'ellipsoid':
            self.config['EMITTER']['a'] = geometry[0]
            self.config['EMITTER']['c'] = geometry[1]
        self.config['EMITTER']['Theta'] = theta
        self.config['EMITTER']['Phi'] = phi

    def add_initial_data_info(self, t0, r0, th0, p0, dt, dr, dth, dp):
        self.config['INITIAL_DATA']['t0'] = t0
        self.config['INITIAL_DATA']['r0'] = r0
        self.config['INITIAL_DATA']['theta0'] = th0
        self.config['INITIAL_DATA']['phi0'] = p0

        self.config['INITIAL_DATA']['dt'] = dt
        self.config['INITIAL_DATA']['dr'] = dr
        self.config['INITIAL_DATA']['dtheta'] = dth
        self.config['INITIAL_DATA']['dphi'] = dp

    def add_momenta_info(self, pt, pr, ptheta, pphi, p0, p1, p2, p3):
        self.config['MOMENTA']['p_t'] = pt
        self.config['MOMENTA']['p_r'] = pr
        self.config['MOMENTA']['p_theta'] = ptheta
        self.config['MOMENTA']['p_phi'] = pphi

        self.config['MOMENTA']['p_0'] = p0
        self.config['MOMENTA']['p_1'] = p1
        self.config['MOMENTA']['p_2'] = p2
        self.config['MOMENTA']['p_3'] = p3

    def add_constants_of_motion(self, lamda, qu, redshift):
        self.config['CONSTANTS_OF_MOTION']['lambda'] = lamda
        self.config['CONSTANTS_OF_MOTION']['q'] = qu
        self.config['CONSTANTS_OF_MOTION']['redshift'] = redshift

    def add_velocities_info(self, orbit, gamma_orbit, rel_vel, gamma_rel_vel, u1, u3, gamma_u13):
        self.config['VELOCITIES']['orbit'] = orbit
        self.config['VELOCITIES']['gamma_orbit'] = gamma_orbit

        self.config['VELOCITIES']['relative_velocitiy'] = rel_vel
        self.config['VELOCITIES']['gamma_rel_vel'] = gamma_rel_vel

        self.config['VELOCITIES']['surf_u1'] = u1
        self.config['VELOCITIES']['surf_u3'] = u3
        self.config['VELOCITIES']['gamma_surf_u'] = gamma_u13

    def add_numerics_info(self, start, stop, num, abserr, relerr, interp_num, time):
        self.config['NUMERICS']['start'] = start
        self.config['NUMERICS']['stop'] = stop
        self.config['NUMERICS']['lightray_num'] = num
        self.config['NUMERICS']['abserr'] = abserr
        self.config['NUMERICS']['relerr'] = relerr
        self.config['NUMERICS']['interpolation_num'] = interp_num
        self.config['NUMERICS']['time_spent'] = time

    def save(self, handle=None):
        if not handle:
            s = self.config['EMITTER']['s']
            alpha = self.config['OBSERVER']['alpha']
            beta = self.config['OBSERVER']['beta']
            handle = f'{s}_{alpha}_{beta}'

        if not os.path.isdir(self.fp):
            os.mkdir(self.fp)

        with open(self.fp + handle + '.json', 'w') as file:
            json.dump(self.config, file, indent=4)

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