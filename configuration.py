import json
import numpy as np


def main():
    # create a standard demo input file
    config = {}

    # add observer position
    config['observer_position'] = {
        'r_obs': 35.,
        'theta_obs': 1.,
        'phi_obs': 0.
    }

    # add emitter position
    config['emitter_position'] = {
        'r_em': 8.,
        'theta_em': np.pi / 2,
        'phi_em': 0.
    }

    # add emitter geometry
    config['emitter_geometry'] = {
        's': 0.,
        'rho': 0.5
    }

    # add screen range
    config['screen_range'] = {
        'alpha_min': -1.,
        'alpha_max': 1.,
        'beta_min': -6.,
        'beta_max': -4.,
        'resolution': 10
    }

    # add numerical config
    config['numerics'] = {
        'start': 0,
        'end': 70,
        'integration_num': 10000,
        'relerr': 1e-7,
        'abserr': 1e-7,
        'interp_num': 10000
    }

    with open('doc/demo_input.json', 'w') as file:
        json.dump(config, file, indent=4)


if __name__ == '__main__':
    main()