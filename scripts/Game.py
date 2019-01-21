from PyQt5.QtWidgets import QApplication
import QtTypeRacer
import Tuples
import sys
import Common

text = 'By using Keras as the high-level API'


class Game(object):

    def start(self):
        layout = Tuples.WindowLayout(inputTextPosition=[20, 100],
                                     mainTextPosition=[20, 50],
                                     progressIndicatorPosition=[20, 20],
                                     windowSize=[800, 600])
        app = QApplication(sys.argv)
        instance = QtTypeRacer.QtTypeRacer(layout)
        instance.run(text)
        sys.exit(app.exec_())
