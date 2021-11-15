import numpy as np


class GenerateWindow:
    def __init__(self, app, s_limit=0.2):
        self.idd = 'Configuration'
        self.app = app

        self.s_limit = s_limit
        self.meta_data = './meta_data.txt'

        self.app.startSubWindow(self.idd, modal=True)
        self.setup_window_geometry()
        self.setup_boxes()
        # setup
        self.app.stopSubWindow()

    def setup_window_geometry(self):
        self.app.setBg('white') #idfk
        self.app.setStretch('both')
        self.app.setSticky('nesw')

    def setup_boxes(self):
        self.app.addLabel('header', 'Configure your simulation...', 0, 0, 5)

        self.app.addHorizontalSeparator(1, 0, 9)

        self.app.addLabel('robs_label', 'r_obs', 2, 0, colspan=2)
        self.app.addSpinBox('robs', np.linspace(20, 100, num=81, endpoint=True).tolist()[::-1], column=2, row=2, colspan=1)
        self.app.setSpinBox('robs', 35.0)

        self.app.addLabel('tobs_label', 'theta_obs [pi]', 3, 0, colspan=2)
        self.app.addSpinBox('tobs', np.linspace(0, 1, num=9, endpoint=True).tolist()[::-1], column=2, row=3, colspan=1)
        self.app.setSpinBox('tobs', 0.5)

        self.app.addLabel('pobs_label', 'phi_obs [pi]', 4, 0, colspan=2)
        self.app.addSpinBox('pobs', np.linspace(0, 2, num=17, endpoint=True).tolist()[::-1], column=2, row=4, colspan=1)
        self.app.setSpinBox('pobs', 0.0)

        self.app.addVerticalSeparator(1, 4, rowspan=5, colour='black')

        self.app.addLabel('rem_label', 'r_em', 2, 5, colspan=2)
        self.app.addSpinBox('rem', np.linspace(6, 20, num=29, endpoint=True).tolist()[::-1], column=7, row=2, colspan=1)
        self.app.setSpinBox('rem', 8.0)

        self.app.addLabel('tem_label', 'theta_em', 3, 5, colspan=2)
        self.app.addLabel('tem', 'pi / 2', 3, 7, colspan=1)

        self.app.addLabel('pem_label', 'phi_em [pi]', 4, 5, colspan=2)
        self.app.addSpinBox('pem', np.linspace(0, 2, num=17, endpoint=True).tolist()[::-1], column=7, row=4, colspan=1)
        self.app.setSpinBox('pem', 0.0)

        self.app.addHorizontalSeparator(5, 0, 9)

        self.app.addLabel('s_label', 's', 6, 0, colspan=2)
        self.app.addSpinBox('s', np.linspace(-self.s_limit, self.s_limit, num=101, endpoint=True).tolist()[::-1],
                            column=2, row=6, colspan=1)
        self.app.setSpinBox('s', 0.0)

        self.app.addLabel('rho_label', 'rho', 6, 5, colspan=2)
        self.app.addSpinBox('rho', np.linspace(0.1, 0.8, num=8).tolist()[::-1], column=7, row=6, colspan=1)
        self.app.setSpinBox('rho', 0.5)

        self.app.addHorizontalSeparator(7, 0, 9)

        self.app.addLabel('endpoint_label', 'Endpoint', 8, 0, colspan=2)
        self.app.addSpinBox('endpoint', np.arange(20, 300, 10).tolist()[::-1], column=2, row=8, colspan=1)
        self.app.setSpinBox('endpoint', 70)

        self.app.addLabel('num_label', 'Number of points', 8, 5, colspan=2)
        self.app.addSpinBox('num', np.arange(1000, 100000, 1000).tolist()[::-1], column=7, row=8, colspan=1)
        self.app.setSpinBox('num', 10000)

        errs = ['{:.1e}'.format(x * 1e-7) for x in np.arange(1, 10)][::-1]
        errs += ['{:.1e}'.format(x * 1e-8) for x in np.arange(1, 9)][::-1]

        self.app.addLabel('abs_label', 'Absolute error', 9, 0, colspan=2)
        self.app.addSpinBox('abs_err', errs, column=2, row=9, colspan=1)
        self.app.setSpinBox('abs_err', '1.0e-07')

        self.app.addLabel('rel_label', 'Relative error', 9, 5, colspan=2)
        self.app.addSpinBox('rel_err', errs, column=7, row=9, colspan=1)
        self.app.setSpinBox('rel_err', '1.0e-07')

        self.app.addHorizontalSeparator(10, 0, 9)

        self.app.addLabel('res_label', 'Resolution', 11, 0, colspan=2)
        self.app.addSpinBox('res', np.arange(10, 200, 5).tolist()[::-1], column=2, row=11, colspan=2)
        self.app.setSpinBox('res', 25)

        self.app.addHorizontalSeparator(12, 0, 9)

        self.app.addLabel('sr_label', 'Get screen range via ', 13, 0, colspan=2)

        self.app.addRadioButton('screen_range', 'automatic range finder (TM)', 13, 2, colspan=2)
        self.app.addRadioButton('screen_range', 'dedicated data file', 14, 2, colspan=2)

        self.app.setRadioButtonChangeFunction('screen_range', self.scrange)

        self.app.addButton('Open meta txt ...', self.open, 14, 5, colspan=1)
        self.app.addLabel('meta', self.meta_data, 14, 7, colspan=2)
        self.scrange()

        self.app.addButton('Cancel ...', self.hide, 17, 8, colspan=1)

    def open(self):
        fp = self.app.openBox('Open meta file ...', '../', fileTypes=[('meta txt', '.txt')], parent=self.idd)
        self.meta_data = fp
        self.app.setLabel('meta', self.meta_data)

    def hide(self):
        self.app.hideSubWindow(self.idd)

    def scrange(self):
        if self.app.getRadioButton('screen_range') == 'dedicated data file':
            self.app.setButtonState('Open meta txt ...', 'active')
            self.app.setLabelState('meta', 'active')

        elif self.app.getRadioButton('screen_range') == 'automatic range finder (TM)':
            self.app.setButtonState('Open meta txt ...', 'disabled')
            self.app.setLabelState('meta', 'disabled')