import numpy as np
import json
import os

from one_ray_solver.velocities import orbit_vel, relative_vel, surface_vel
from one_ray_solver.utility import redshift


def eval_spin_stuff(s, rem, fp_to_redshift, fp_to_new_redshift, robs=35., tobs=1., v3=0.5, spheroid=False):
    # step 0:
    fp_to_json = fp_to_redshift + 'data/'

    # step 1: get a list of every json file in specified directory
    filenames = next(os.walk(fp_to_json), (None, None, []))[2]

    # step 2: load .csv of redshift
    redshift_data = np.loadtxt(fp_to_redshift + 'redshift.csv', delimiter=',', skiprows=1)

    # step 3: iterate over redshift data:
    for n, row in enumerate(redshift_data):
        # step 3a: exclude redshift data for when there is no collision:
        if row[-1] == 0.:
            continue

        # step 4: load all json data one by one:
        for file in filenames:
            with open(fp_to_json + file, 'r') as f:
                config = json.load(f)

            # step 4a: if the row does not equal the alpha/beta of json, delete config
            if config['OBSERVER']['alpha'] != row[0] or config['OBSERVER']['beta'] != row[1]:
                del config
                continue

            # step 5: read the relevant data
            p0 = config['MOMENTA']['p_0']
            p1 = config['MOMENTA']['p_1']
            p3 = config['MOMENTA']['p_3']

            T = config['EMITTER']['Theta']
            P = config['EMITTER']['Phi']

            robs = 35.
            tobs = 1.0
            pobs = 0.0

            rem = config['INITIAL_DATA']['r0']
            tem = config['INITIAL_DATA']['theta0']
            pem = config['INITIAL_DATA']['phi0']

            try:
                a = config['EMITTER']['bh_a']
            except:
                a = 0.

            lamda = config['CONSTANTS_OF_MOTION']['lambda']
            qu = config['CONSTANTS_OF_MOTION']['q']

            # step 6a: setup velocities
            orbit = orbit_vel.OrbitVelocityKerr(s, a, rem)
            rel_vel = relative_vel.RelativeVelocityKerr(s, a, rem)
            if spheroid:
                aa = config['EMITTER']['a']
                surf = surface_vel.SurfaceVelocityMaclaurinEllipsoid(s, [aa, T, P])
            else:
                rho = config['EMITTER']['rho']
                surf = surface_vel.SurfaceVelocityRigidSphere(s, [rho, T, P])

            # step 6b: eval velocities
            #v3 = 0.1
            gv3 = 1/np.sqrt(1 - v3 ** 2)#(v3, ), gv3 = orbit.get_velocity()
            #(rv, ), grv = rel_vel.get_velocity()
            rv = 0.0
            grv = 1.0
            (u1, u3), gu = surf.get_velocity()

            # step 7: calculate redshift

            g = redshift.g(p0, p1, p3, v3, gv3, rv, grv, u1, u3, gu)
            #g = red(rem, tem, pem, robs, tobs, pobs, gv3, v3, gu, u1, u3)
            if g < 0:
                print(g, pem)
            
            # step 8: calc redshift at observer
            delta = robs ** 2 - 2 * robs + a ** 2
            A = (robs ** 2 + a ** 2) ** 2 - delta * a * np.sin(tobs) ** 2
            omega = 2 * a * robs / A
            e_min_nu = np.sqrt(A / ((robs ** 2 + a ** 2 * np.cos(tobs) ** 2) * delta))
            g = e_min_nu * (1 - lamda * omega) / g

            break

        # step 9a: save row
        row[-1] = g
        redshift_data[n] = row

        # step 9b: remove file from list
        if not filenames == []:
            filenames.remove(file)

    # step 10: save new redshift
    np.savetxt(fp_to_new_redshift + 'redshift.csv', redshift_data, delimiter=',', header='alpha,beta,redshift')
