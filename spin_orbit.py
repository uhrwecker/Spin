import json
import time
import argparse

from ray_experiment.ray_handler import RayHandler
from ray_experiment.ranger import RangeAdjustment
from ray_experiment.orbit_handler import OrbitHandler
from one_ray_solver.utility.maclaurin import calculate_polar_semi_axis
from repair import fix


def get_parser():
    parser = argparse.ArgumentParser('Calculate the emission from a spinning light source in circular orbit around'
                                     ' the source of gravity.')
    parser.add_argument('-cfg', '--config', action='store', type=str,
                        help='Specify the location of the config file.', dest='fp', default='./doc/demo_input.json')
    parser.add_argument('-s', '--save', action='store', type=str, help='Specify the saving directory.', dest='save',
                        default='')
    parser.add_argument('-n', '--number-of-phi', action='store', type=int, default=2, dest='number',
                        help='Number of emitter positions (phi_em).')
    parser.add_argument('-k', '--range', action='store_true', dest='adjust_range', default=False,
                        help='Run the automatic range finder to find the range of (alpha, beta) for the emitter.')
    parser.add_argument('-ks', '--save-range', action='store', type=str, dest='save_range', default='',
                        help='Works only in conjunction with -k. Specify the file you want to save the range in; will be '
                             'appended.')
    parser.add_argument('-r', '--redshift', action='store_true', dest='save_redshift', default=False,
                        help='Save a dedicated file that contains the redshift data of the experiment.')
    parser.add_argument('-c', '--csv', action='store_true', dest='save_csv', default=False,
                        help='Save, for every ray, the whole ray as a .csv file.')
    parser.add_argument('--no-exp-cfg', action='store_true', dest='dont_save_exp_config', default=False,
                        help='Disable the saving of the experiment config. Not recommended.')
    parser.add_argument('--colliding', action='store_true', dest='save_even_when_not_colliding', default=False,
                        help='Save the light ray config, even if the light ray did not collide with the emitter.')
    parser.add_argument('-nr', '--no-repair', action='store_false', dest='repair', default=True,
                        help='Runs repair routine on any damaged or corrupted -redshift- files. Highly recommened. '
                             'Works only with -r flag on, as it only works on the redshift files.')
    parser.add_argument('--repair_only', action='store_true', dest='repair_only', default=False,
                        help='Only run the repair tool on existing redshift data; no further simulation will be done.')

    return parser


def main():
    start_time = time.time()

    pars = get_parser()
    args = pars.parse_args()

    with open(args.fp, 'r') as file:
        config = json.load(file)
        obs = config['observer_position']
        em = config['emitter_position']
        geo = config['emitter_geometry']
        screen = config['screen_range']
        num = config['numerics']

    save_fp = ''
    if args.save:
        save_fp = args.save

    if geo['shape'] == 'sphere':
        geometry = [geo['rho'],]
    elif geo['shape'] == 'ellipsoid':
        geometry = [geo['a']]
        c = calculate_polar_semi_axis(geo['s'], geo['a'])
        geometry.append(c[0])
    else:
        raise ValueError

    if args.adjust_range:
        import numpy as np
        phis = np.linspace(0, 2*np.pi, num=args.number)
        for n, phi in enumerate(phis):
            data = np.loadtxt(args.save_range+'2', delimiter=';')
            guess = (np.mean(data[n][3:5]), np.mean(data[n][5:]))
            rhh = RayHandler(s=geo['s'], bha=geo['a'], geometry=geometry,
                            rem=em['r_em'], tem=em['theta_em'], pem=phi,
                            robs=obs['r_obs'], tobs=obs['theta_obs'], pobs=obs['phi_obs'],
                            **screen, m=1, **num, fp=save_fp, saver='json', shape=geo['shape'],
                            save_even_when_not_colliding=args.save_even_when_not_colliding, save_handle=None,
                            save_csv=args.save_csv, save_redshift=args.save_redshift,
                            save_config=~args.dont_save_exp_config, save_data=args.save)

            rg = RangeAdjustment(rhh)
            rhh = rg.start(fp=args.save_range, guess=guess)

            rhh.resolution = screen['resolution']
            rhh.save_even_when_not_colliding = args.save_even_when_not_colliding
            rhh.save_csv = args.save_csv
            rhh.save_redshift = args.save_redshift
            rhh.save_config = ~args.dont_save_exp_config
            rhh.save_data = args.save

            if geo['shape'] == 'sphere':
                geometry = [geo['rho'], ]
            elif geo['shape'] == 'ellipsoid':
                geometry = [geo['a']]
                c = calculate_polar_semi_axis(geo['s'], geo['a'])
                geometry.append(c[0])
            else:
                raise ValueError

        del rhh

    # better save than sorry:
    if geo['shape'] == 'sphere':
        geometry = [geo['rho'], ]
    elif geo['shape'] == 'ellipsoid':
        geometry = [geo['a']]
        c = calculate_polar_semi_axis(geo['s'], geo['a'])
        geometry.append(c[0])
    else:
        raise ValueError

    rh = RayHandler(s=geo['s'], bha=geo['a'], geometry=geometry,
                    rem=em['r_em'], tem=em['theta_em'], pem=em['phi_em'],
                    robs=obs['r_obs'], tobs=obs['theta_obs'], pobs=obs['phi_obs'],
                    **screen, m=1, **num, fp=save_fp, saver='json', shape=geo['shape'],
                    save_even_when_not_colliding=args.save_even_when_not_colliding, save_handle=None,
                    save_csv=args.save_csv, save_redshift=args.save_redshift,
                    save_config=~args.dont_save_exp_config, save_data=args.save)

    if not args.repair_only:
        print('Starting the run...')
        oh = OrbitHandler(rh, number_of_orbit_points=args.number, meta_data=args.save_range, save_fp=args.save)
        oh.start()

    if (args.save_redshift and args.repair) or args.repair_only:
        print('Start repair tool...')
        fix.repair(save_fp)

    took = time.time() - start_time
    print(f'Done! \nWhole calculation took {took}s (or {took / 60}min).')


if __name__ == '__main__':
    main()