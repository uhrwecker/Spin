import json
import configparser as cp
import pandas as pd
import os


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
        if not os.path.isdir(self.fp):
            os.mkdir(self.fp)

        if self.save_format == 'config' or self.save_format == 'cfg':
            with open(self.fp + handle + '.cfg', 'w') as file:
                self.config.write(file)

        elif self.save_format == 'json':
            with open(self.fp + handle + '.json', 'w') as file:
                json.dump(self.config, file, indent=4)

    def save_redshift(self, data, handle=None):
        import numpy as np

        if not handle:
            handle = 'redshift'

        data = np.array(data)

        data = data[data[:, 0].argsort()]

        new_data = []
        batched = np.split(data, int(np.sqrt(len(data))))
        for item in batched:
            new_data.append(item[item[:, 1].argsort()])
        new_data = np.array(new_data).reshape((len(data), 3))

        alpha = new_data[:, 0]
        beta = new_data[:, 1]
        g = new_data[:, 2]

        df = pd.DataFrame({'alpha': alpha, 'beta': beta, 'redshift': g})

        df.to_csv(self.fp + handle + '.csv', index=False)
