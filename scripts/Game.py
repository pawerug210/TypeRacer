from PyQt5.QtWidgets import QApplication

import Common
import QtTypeRacer
import Tuples
import sys


class Game(object):

    @staticmethod
    def start():
        layout = Tuples.WindowLayout(windowTitle='Type Racer',
                                     windowSize=[400, 300])
        app = QApplication(sys.argv)
        instance = QtTypeRacer.QtTypeRacer(layout)
        instance.run(Common.readFile(sys.argv[1]))
        sys.exit(app.exec_())
