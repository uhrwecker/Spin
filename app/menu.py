import os
from app.generation import GenerateWindow


class MainMenuBar:
    def __init__(self, app):
        self.app = app
        self.setup_items()

        self.gw = GenerateWindow(self.app)

        self.cwd = None
        self.save_fp = None

    def setup_items(self):
        self.app.createMenu('File')
        self.app.addMenuItem('File', 'New', self.open_new, shortcut='Control-n')
        self.app.addMenuItem('File', '-', self.placeholder)
        self.app.addMenuItem('File', 'Open data', self.open, shortcut='Control-o')
        self.app.addMenuItem('File', '-', self.placeholder)
        self.app.addMenuItem('File', 'Save', self.save)
        self.app.addMenuItem('File', '-', self.placeholder)
        self.app.addMenuItem('File', 'Close', self.app.stop, shortcut='Control-q')

        self.app.disableMenuItem('File', 'Save')

        self.app.createMenu('Edit')
        self.app.addMenuItem('Edit', 'Change appearance', self.app.showAccess)

    def enable(self):
        self.app.enableMenuItem('File', 'Save')

    def open(self):
        fp = self.app.directoryBox('Open the directory where the files are...')
        self.cwd = fp

    def save(self):
        fp = self.app.saveBox('Save the images displayed...', fileName='flux', fileExt='.png')
        self.save_fp = fp

    def open_new(self):
        self.app.showSubWindow('Configuration')

    def placeholder(self):
        pass