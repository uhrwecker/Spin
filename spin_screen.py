#!/usr/bin/env python3
"""Test script for trying some things."""
import argparse
import json
import time

from ray_experiment import ranger, ray_handler
from repair import fix
from one_ray_solver.utility.maclaurin import calculate_polar_semi_axis


def get_parser():
    parser = argparse.ArgumentParser('Calculate the emission from a spinning light source in circular orbit around'
                                     ' the source of gravity.')
    parser.add_argument('-cfg', '--config', action='store', type=str,
                        help='Specify the location of the config file.', dest='fp', default='./doc/demo_input.json')
    parser.add_argument('-s', '--save', action='store', type=str, help='Specify the saving directory.', dest='save',
                        default='')
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
    parser.add_argument('-d', '--debug', action='extend', nargs=2, type=float, default=[],
                        help='Debug mode. Specify a pair of (alpha, beta) to calculate a single ray from, and plot it.')
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
        geometry = (geo['rho'],)
    elif geo['shape'] == 'ellipsoid':
        geometry = [geo['a']]
        c = calculate_polar_semi_axis(geo['s'], geo['a'])
        geometry.append(c)
    else:
        raise ValueError

    if not args.debug:
        rh = ray_handler.RayHandler(s=geo['s'], bha=geo['bh_a'], geometry=geometry,
                                    rem=em['r_em'], tem=em['theta_em'], pem=em['phi_em'],
                                    robs=obs['r_obs'], tobs=obs['theta_obs'], pobs=obs['phi_obs'],
                                    **screen, m=1, **num, fp=save_fp, saver='json', shape=geo['shape'],
                                    save_even_when_not_colliding=args.save_even_when_not_colliding, save_handle=None,
                                    save_csv=args.save_csv, save_redshift=args.save_redshift,
                                    save_config=~args.dont_save_exp_config, save_data=args.save)
        if args.adjust_range:
            rg = ranger.RangeAdjustment(rh)
            rh = rg.start(fp=args.save_range)

            rh.resolution = screen['resolution']
            rh.save_even_when_not_colliding = args.save_even_when_not_colliding
            rh.save_csv = args.save_csv
            rh.save_redshift = args.save_redshift
            rh.save_config = ~args.dont_save_exp_config
            rh.save_data = args.save

        if not args.repair_only:
            print('Starting the run...')
            rh.run()

        if args.save_redshift and args.repair:
            print('Start repair tool...')
            fix.repair(save_fp)

    elif args.debug:
        alpha, beta = args.debug
        from one_ray_solver.solve import OneRaySolver
        from visualisation.simple_3d import Simple3DPlotter

        ors = OneRaySolver(s=geo['s'], geometry=geometry,
                           rem=em['r_em'], tem=em['theta_em'], pem=em['phi_em'],
                           robs=obs['r_obs'], tobs=obs['theta_obs'], pobs=obs['phi_obs'], m=1, **num,
                           alpha=0, beta=0, shape=geo['shape'], save_even_when_not_colliding=False,
                           save_csv=False, save_data=False)
        ors.set_alpha_beta(alpha, beta)
        ray, cfg = ors.solve(full_output=True)

        p = Simple3DPlotter([obs['r_obs'], obs['theta_obs'], obs['phi_obs']],
                            [em['r_em'], em['theta_em'], em['phi_em']])
        p.plot_from_ray_data(ray)
        p.show()

    took = time.time() - start_time
    print(f'Done! \nWhole calculation took {took}s (or {took / 60}min).')

if __name__ == '__main__':
    main()