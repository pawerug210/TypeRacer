import math
from PyQt5.QtWidgets import QWidget, QLineEdit, QGridLayout, QTextEdit, QProgressBar
from PyQt5.QtGui import QColor
from PyQt5 import QtCore

import Common
import TypeRacerHelper


class QtTypeRacer(QWidget):

    Running = False
    CorrectnessColorsMap = {
        True: 'green',
        False: 'red',
        None: 'black'
    }

    def __init__(self, layout, parent=None):
        super().__init__(parent)
        self._windowLayout = layout
        self._typeRacer = TypeRacerHelper.TypeRacerHelper()
        self._checkpoint = 0
        self.progress = 0

    def run(self, text):
        self.Running = True
        self._typeRacer.setText(text)
        self._createWindow()
        self._writeText(text, [None] * len(text))

    def _createWindow(self):
        self.resize(*self._windowLayout.windowSize)
        self.setWindowTitle("Type Racer")

        # input text box
        self.userInputTextBox = QLineEdit()
        self.userInputTextBox.move(20, 20)
        self.userInputTextBox.resize(280, 40)
        self.userInputTextBox.textEdited.connect(self._textEdited)

        # main text
        self.mainText = QTextEdit()
        self.mainText.setReadOnly(True)
        # text non selectable
        self.mainText.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

        # progress bar
        self.progressBar = QProgressBar()
        self.progressBar.setGeometry(200, 80, 250, 20)

        # Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.progressBar, 0, 0)
        self.layout.addWidget(self.mainText, 1, 0)
        self.layout.addWidget(self.userInputTextBox, 2, 0)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)

        self.setLayout(self.layout)

        self.setMinimumSize(self.sizeHint())
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.deleteLater()
            self.Running = False
        event.accept()

    def _textEdited(self, widget, *args):
        inputText = self.userInputTextBox.text()
        self._typeRacer.addText(inputText, self._checkpoint)
        if self._typeRacer.isNewWord():
            self.userInputTextBox.clear()
            self._checkpoint += len(inputText)
        wholeText = self._typeRacer.Text
        correctnessListPadded = Common.addNonePadding(self._typeRacer.getCorrectnessList(), len(wholeText))
        self._writeText(wholeText, correctnessListPadded)
        self._updateProgressBar(correctnessListPadded)

    def _writeText(self, text, correctnessList):
        self.mainText.clear()
        for value in [True, False, None]:
            color = self.CorrectnessColorsMap[value]
            textPart = ''.join(Common.applyMask(text, correctnessList, value))
            self.mainText.setTextColor(QColor(color))
            self.mainText.insertPlainText(textPart)

    def _updateProgressBar(self, correctnessList):
        self.progress = (len([x for x in correctnessList if x]) / len(correctnessList)) * 100
        self.progressBar.setValue(self.progress)


