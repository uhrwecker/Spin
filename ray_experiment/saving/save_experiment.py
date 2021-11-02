import json
import configparser as cp
import pandas as pd


class ExperimentSaver:
    def __init__(self, fp, save_format='json'):
        self.fp = fp
        self.save_format = save_format

        if self.save_format == 'json':
            self.config = {}
        elif self.save_format == 'config' or self.save_format == 'cfg':
            self.config = cp.ConfigParser()

        self.config['SETUP'] = {}
        self.config['NUMERICS'] = {}

    def add_setup_information(self, amin, amax, bmin, bmax):
        if self.save_format == 'config' or self.save_format == 'cfg':
            amin, amax, bmin, bmax = str(amin), str(amax), str(bmin), str(bmax)

        self.config['SETUP']['alpha_min'] = amin
        self.config['SETUP']['alpha_max'] = amax
        self.config['SETUP']['beta_min'] = bmin
        self.config['SETUP']['beta_max'] = bmax

    def add_numeric_information(self, resolution, total_time, number_of_collisions):
        total_min = total_time / 60
        mean_time = total_time / resolution**2
        if self.save_format == 'config' or self.save_format == 'cfg':
            resolution, total_time, mean_time, number_of_collisions = str(resolution), str(total_time), \
                                                                      str(mean_time), \
                                                                      str(number_of_collisions)
            total_min = str(total_min)

        self.config['NUMERICS']['resolution'] = resolution
        self.config['NUMERICS']['total_time_s'] = total_time
        self.config['NUMERICS']['total_time_min'] = total_min
        self.config['NUMERICS']['mean_time_s'] = mean_time
        self.config['NUMERICS']['number_of_collisions'] = number_of_collisions

    def save(self, handle=None):
        if not handle:
            handle = 'experiment_config'

        if self.save_format == 'config' or self.save_format == 'cfg':
            with open(self.fp + handle + '.cfg', 'w') as file:
                self.config.write(file)

        elif self.save_format == 'json':
            with open(self.fp + handle + '.json', 'w') as file:
                json.dump(self.config, file, indent=4)