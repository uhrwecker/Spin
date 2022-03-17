"""All that this class should do is putting the setup, execution and saving all together."""

import numpy as np
import time

from one_ray_solver.utility import screen_COM_converter, redshift
from one_ray_solver.ode import solver
from one_ray_solver.collision import collider
from one_ray_solver.save import saver_cfg, saver_json
from one_ray_solver.sign import check
from one_ray_solver.velocities import *


class OneRaySolver:
    def __init__(self, s=0., bha=0., rem=8., tem=np.pi/2, pem=0., geometry=(0.5,), robs=35., tobs=1., pobs=0.,
                 alpha=0., beta=-5., m=1, start=0, stop=70, num=100000, abserr=1e-7, relerr=1e-7, interp_num=10000,
                 sign_r=-1, sign_theta=1, sign_phi=1, fp='./', saver='json', shape='sphere',
                 save_even_when_not_colliding=True, save_handle=None,
                 save_csv=False, save_data=True):
        self.s = s
        self.bha = bha

        self.rem = rem
        self.tem = tem
        self.pem = pem

        self.geometry = geometry

        self.robs = robs
        self.tobs = tobs
        self.pobs = pobs

        self.alpha = alpha
        self.beta = beta

        self.m = m

        self.start = start
        self.stop = stop
        self.ray_num = num
        self.abserr = abserr
        self.relerr = relerr

        self.interpolate_num = interp_num
        self.shape = shape

        self.sign_r = sign_r
        self.sign_theta = sign_theta
        self.sign_phi = sign_phi

        self.collider = collider.Collider(self.rem, self.tem, self.pem, self.geometry, self.interpolate_num, self.shape)
        if saver == 'json':
            self.saver = saver_json.DataSaverJson(fp)
        elif saver == 'config':
            self.saver = saver_cfg.DataSaverConfig(fp)
        else:
            raise ValueError(f'Saver type {saver} is not supported.')
        self.orb = OrbitVelocityKerr(self.s, self.bha, self.rem)
        self.rel = RelativeVelocityKerr(self.s, self.bha, self.rem)

        self.lamda = None
        self.qu = None

        self.save_even_when_not_colliding_flag = save_even_when_not_colliding
        self.save_handle = save_handle
        self.save_csv = save_csv
        self.save_data = save_data

    def solve(self, full_output=False):
        start_time = time.time()
        # step 1: get the constants of motion
        self.lamda, self.qu = screen_COM_converter.lamda_qu_from_alpha_beta(self.alpha, self.beta,
                                                                            self.robs, self.tobs, self.m, self.bha)

        # step 2: setup the solver itself
        sol = solver.ODESolverKerr(self.robs, self.tobs, self.pobs, self.lamda, self.qu, self.m, self.bha,
                                            self.start, self.stop, self.ray_num, self.abserr, self.relerr,
                                            self.sign_r, self.sign_theta, self.sign_phi)

        sigma, ray = sol.solve()
        #return ray, None
        # step 3: see if there is a collision
        collision_point, local_coord, collision_flag = self.collider.check(ray)
        # step 3a: save the light ray that is not colliding
        if not collision_flag:
            return self._no_collision()

        # step 3b: continue with the colliding light ray
        else:
            # step 4: check the signs of initial velocities at impact
            self.checker = check.SignImpactSchwarzschild(sol, collision_point, [self.robs, self.tobs, self.pobs])
            #print(self.alpha, self.beta, self.geometry, self.lamda, self.qu)
            if self.checker.problem:

                return self._no_collision()

            sigma, ray = self.checker._solve()
            dt, dr, dtheta, dphi = self.checker.calculate_initial_velocities()
            pt, pr, ptheta, pphi = self.checker.calculate_initial_momenta_general()
            p0, p1, p2, p3 = self.checker.calculate_initial_momenta_ZAMO()

            # step 5: calculate the velocities
            (orbit_velocity, ), gamma_orb = self.orb.get_velocity()
            (relative_vel, ), gamma_rel_vel = self.rel.get_velocity()

            if self.shape == 'sphere':
                surface = SurfaceVelocityRigidSphere(self.s, (self.geometry[0], local_coord[0], local_coord[1]))
            elif self.shape == 'ellipsoid':
                surface = SurfaceVelocityMaclaurinEllipsoid(self.s, (self.geometry[0], local_coord[0], local_coord[1]))
            else:
                raise ValueError(f'The shape {self.shape} was not understood; must be either -sphere- or -ellipsoid-')

            (surf_vel_u1, surf_vel_u3), gamma_surf = surface.get_velocity()

            # step 6: calculate the redshift of the ray
            g = redshift.g(p0, p1, p3, orbit_velocity, gamma_orb, relative_vel, gamma_rel_vel,
                           surf_vel_u1, surf_vel_u3, gamma_surf)

            # step 6.1: calculate the p0 component of the observer
            delta = self.robs ** 2 - 2 * self.robs + self.bha ** 2
            A = (self.robs ** 2 + self.bha ** 2) ** 2 - delta * self.bha * np.sin(self.tobs) ** 2
            omega = 2 * self.bha * self.robs / A
            e_min_nu = np.sqrt(A / ((self.robs ** 2 + self.bha ** 2 * np.cos(self.tobs) ** 2) * delta))
            g = e_min_nu * (1 - self.lamda * omega) / g

            # step 6: save!
            self.saver.add_observer_info(self.robs, self.tobs, self.pobs, self.alpha, self.beta)
            self.saver.add_emitter_info(self.s, self.bha, self.geometry, *local_coord, self.shape)
            self.saver.add_constants_of_motion(self.lamda, self.qu, g)
            self.saver.add_initial_data_info(0, *collision_point, dt, dr, dtheta, dphi)
            self.saver.add_momenta_info(pt, pr, ptheta, pphi, p0, p1, p2, p3)
            self.saver.add_velocities_info(orbit_velocity, gamma_orb, relative_vel, gamma_rel_vel,
                                           surf_vel_u1, surf_vel_u3, gamma_surf)
            self.saver.add_numerics_info(self.start, self.stop, self.ray_num, self.abserr, self.relerr,
                                         self.interpolate_num, time.time() - start_time)

            if self.save_data:
                self.saver.save(self.save_handle)

            if self.save_csv:
                self.saver.save_data_to_csv(sigma, ray, self.save_handle)

            if full_output:
                return ray, self.saver.config

    def set_alpha_beta(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.sign_theta = - np.sign(beta)  # that should work

    def get_solver(self):
        # this method will allow the user to access a solver object, without running the whole solver wrapper.
        # especially useful for plotting shenanigans.
        sol = solver.ODESolverKerr(self.robs, self.tobs, self.pobs, 0, 0, self.m, self.bha,
                                            self.start, self.stop, self.ray_num, self.abserr, self.relerr,
                                            self.sign_r, self.sign_theta, self.sign_phi)

        return sol

    def _no_collision(self):
        self.saver.add_observer_info(self.robs, self.tobs, self.pobs, self.alpha, self.beta)
        self.saver.add_emitter_info(self.s, self.bha, self.geometry, 0, 0, self.shape)
        self.saver.add_constants_of_motion(0, 0, 0)
        self.saver.add_initial_data_info(0, 0, 0, 0, 0, 0, 0, 0)
        self.saver.add_momenta_info(0, 0, 0, 0, 0, 0, 0, 0)
        self.saver.add_numerics_info(self.start, self.stop, self.ray_num, self.abserr, self.relerr,
                                     self.interpolate_num, 0)
        self.saver.add_velocities_info(0, 0, 0, 0, 0, 0, 0)

        if self.save_even_when_not_colliding_flag and self.save_data:
            self.saver.save(self.save_handle)

        return None, self.saver.config