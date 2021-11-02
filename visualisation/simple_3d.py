import matplotlib.pyplot as pl
import numpy as np


class Simple3DPlotter:
    def __init__(self, observer_position, emitter_position, figsize=(10, 10), dpi=10, save=None,
                 central_object='schwarzschild'):
        self.observer_position = observer_position
        self.emitter_position = emitter_position

        self.dpi = dpi
        self.save = save
        self.central_object = central_object

        self.figure = pl.figure(figsize=figsize)
        self.ax = self.figure.add_subplot(projection='3d')

        self.plot_central_object()
        self.plot_emitter()
        self.plot_observer()

        self.adjust()

    def plot_observer(self):
        r, t, p = self.observer_position

        x = r * np.cos(p) * np.sin(t)
        y = r * np.sin(p) * np.sin(t)
        z = r * np.cos(t)

        self.ax.scatter(x, y, z, color='orange')

    def plot_emitter(self):
        r, t, p = self.emitter_position

        x = r * np.cos(p) * np.sin(t)
        y = r * np.sin(p) * np.sin(t)
        z = r * np.cos(t)

        self.ax.scatter(x, y, z, color='green')

    def plot_central_object(self):
        if self.central_object == 'schwarzschild':
            u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]

            # calculate the real cartesian coordinates (r_local + r_0)
            x = 2 * np.cos(u) * np.sin(v)
            y = 2 * np.sin(u) * np.sin(v)
            z = 2 * np.cos(v)

            # plot the black hole
            self.ax.plot_wireframe(x, y, z, color='black')

        else:
            raise ValueError(f'The central object {self.central_object} is not understood.')

    def plot_from_ray_data(self, ray):
            r = ray[:, 2]
            t = ray[:, 4]
            p = ray[:, 6]

            x = r * np.cos(p) * np.sin(t)
            y = r * np.sin(p) * np.sin(t)
            z = r * np.cos(t)

            self.ax.plot(x, y, z, color='blue')

    def plot_from_constants_of_motion(self, solver, lamda, qu, sign_r=1, sign_theta=1, sign_phi=-1,
                                      starting_from='emitter'):
        if starting_from == 'emitter':
            position = self.emitter_position
        elif starting_from == 'observer':
            position = self.observer_position
        elif type(starting_from) == list or type(starting_from) == tuple:
            position = starting_from
        else:
            raise ValueError(f'Cannot start from position {starting_from}; only from -emitter- or -observer- .')

        solver.change_emission_point(*position, recalc=False)
        solver.change_constants_of_motion(lamda, qu, recalc=False)
        solver.change_signs(sign_r=sign_r, sign_q=sign_theta, sign_l=sign_phi)

        _, ray = solver.solve()

        self.plot_from_ray_data(ray)

    def plot_from_alpha_beta(self, solver, alpha, beta, sign_r=1, sign_theta=1, sign_phi=-1,
                             starting_from='emitter'):
        from one_ray_solver.utility import screen_COM_converter
        lamda, qu = screen_COM_converter.lamda_qu_from_alpha_beta(alpha, beta,
                                                                  self.observer_position[0], self.observer_position[1])

        self.plot_from_constants_of_motion(solver, lamda, qu, sign_r, sign_theta, sign_phi, starting_from)

    def adjust(self):
        r, t, p = self.observer_position

        x = r * np.cos(p) * np.sin(t)
        y = r * np.sin(p) * np.sin(t)
        z = r * np.cos(t)

        xy = np.amax([x, y])

        self.ax.set_xlim(-xy-1, xy+1)
        self.ax.set_ylim(-xy-1, xy+1)
        self.ax.set_zlim(-3/4*xy, 3/4*xy)

        self.ax.set_xlabel('x / M')
        self.ax.set_ylabel('y / M')
        self.ax.set_zlabel('z / M')

    def show(self):
        # a simple wrapper around pl.show()
        pl.show()