import os
import time

from eval_spin_sources_sphere import eval_spin_stuff


def main():
    s = 0.000
    rem = 8.0
    v3 = 0.

    fp_to_data = '/media/jan-menno/T7/Flat/v05/s0/'
    fp_to_save = '/media/jan-menno/T7/Flat/v0/s0/'

    print('Load data (this may take some time) ...')
    start = time.time()

    phis = [x[0] for x in os.walk(fp_to_data)]
    phis = [phi for phi in phis if not phi.endswith('data')]
    phis = [phi + '/' for phi in phis if not phi == fp_to_data]

    for n, file in enumerate(phis):
        phi = file[len(fp_to_data):-1]

        print(f'Now at {phi} ... ({n+1} / {len(phis)})')

        try:
            os.mkdir(fp_to_save + phi)
            os.mkdir(fp_to_save + phi + '/data')
        except FileExistsError:
            continue

        eval_spin_stuff(s, rem, file, fp_to_save + phi + '/', v3=v3)

    t = time.time() - start
    print(f'Done! Took {t} s (or {t / 60} min).')

if __name__ == '__main__':
    main()