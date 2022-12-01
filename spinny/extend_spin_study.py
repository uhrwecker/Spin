import os
import time

from eval_spin_sources_sphere import eval_spin_stuff


def main():
    s = -0.00175
    rem = 6.06747494
    v3 = 0.30959846265673047
    spheriod = True

    fp_to_data = '/media/jan-menno/T7/Kerr/maclaurin/a09/s0175/'
    fp_to_save = '/media/jan-menno/T7/Kerr/maclaurin/a09/s-0175/'

    print('Load data (this may take some time) ...')
    start = time.time()

    phis = [fp_to_data + name for name in os.listdir(fp_to_data) if os.path.isdir(os.path.join(fp_to_data, name))]
    phis = [phi for phi in phis if not (phi.endswith('data') or phi.endswith('extra'))]
    phis = [phi + '/' for phi in phis if not phi == fp_to_data]

    for n, file in enumerate(phis):
        phi = file[len(fp_to_data):-1]

        print(f'Now at {phi} ... ({n+1} / {len(phis)})')

        try:
            os.mkdir(fp_to_save + phi)
            os.mkdir(fp_to_save + phi + '/data')
        except FileExistsError:
            continue

        eval_spin_stuff(s, rem, file, fp_to_save + phi + '/', v3=v3, spheroid=spheriod)

    t = time.time() - start
    print(f'Done! Took {t} s (or {t / 60} min).')

if __name__ == '__main__':
    main()