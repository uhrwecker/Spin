import numpy as np
import json
import matplotlib.pyplot as pl
import pandas as pd
import os

from one_ray_solver.utility import redshift


def down():
    fp = '/home/jan-menno/Data/fix/s-015/'
    save = '/home/jan-menno/Data/fix/cha/'

    phis = [f.path for f in os.scandir(fp) if f.is_dir() and not 'images' in f.path]
    phis.sort()

    data = []
    for phi in phis:
        save = '/home/jan-menno/Data/fix/cha/'
        if 'images' in phi:
            continue

        pp = phi[31:]
        save += pp + '/'

        phi += '/data/'

        files = [f for f in os.listdir(phi) if os.path.isfile(os.path.join(phi, f))]

        data = []

        for file in files:
            with open(phi+file, 'r') as f:
                config = json.load(f)

            alpha = config['OBSERVER']['alpha']
            beta = config['OBSERVER']['beta']

            p0 = config['MOMENTA']['p_0']
            p1 = config['MOMENTA']['p_1']
            p3 = config['MOMENTA']['p_3']

            vel = config['VELOCITIES']

            mv = vel['relative_velocitiy']
            gmv = vel['gamma_rel_vel']
            u1 = vel['surf_u1']
            u3 = vel['surf_u3']
            gu13 = vel['gamma_surf_u']

            data.append([alpha, beta, redshift.g(p0, p1, p3, 0, 1, mv, gmv, u1, u3, gu13)])

        data = np.array(data)

        data = data[data[:, 0].argsort()]

        alpha = data[:, 0]
        beta = data[:, 1]
        g = data[:, 2]

        os.mkdir(save)

        df = pd.DataFrame({'alpha': alpha, 'beta': beta, 'redshift': g})

        df.to_csv(save + 'redshift' + '.csv', index=False)


if __name__ == '__main__':
    pass