from appJar import gui

from app.menu import MainMenuBar


class MainWindow:
    def __init__(self):
        self.app = gui()

        self.setup_geometry()
        self.mb = self.setup_menu()

    def setup_geometry(self):
        self.app.setTitle('You spin me right round')
        self.app.setSize('1900x950')
        self.app.setLocation(0, 0)

        self.app.setFont(size=20, family='Times')
        self.app.setLabelFont(size=18, family='Times')
        self.app.setButtonFont(size=18, family='Times')

    def setup_menu(self):
        return MainMenuBar(self.app)

    def start(self):
        self.app.go()


def main():
    mw = MainWindow()
    mw.start()


if __name__ == '__main__':
    main()
