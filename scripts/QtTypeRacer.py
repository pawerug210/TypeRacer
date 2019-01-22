from PyQt5.QtWidgets import QWidget, QLineEdit, QGridLayout, QTextEdit, QProgressBar, QMessageBox
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
        self._updateMainText(text, [None] * len(text))

    def _createWindow(self):
        self.resize(*self._windowLayout.windowSize)
        self.setWindowTitle("Type Racer")

        # input text box
        self.userInputTextBox = QLineEdit()
        self.userInputTextBox.move(20, 20)
        self.userInputTextBox.resize(280, 40)
        self.userInputTextBox.textEdited.connect(self._textEdited)
        self.userInputTextBox.setMaxLength(len(self._typeRacer.Text))

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
        self._updateWindow()
        if self.progress == 100:
            self._proceedGameFinish()

    def _updateWindow(self):
        wholeText = self._typeRacer.Text
        correctnessListPadded = Common.addNonePadding(self._typeRacer.getCorrectnessList(), len(wholeText))
        self._updateInputTextBox()
        self._updateMainText(wholeText, correctnessListPadded)
        self._updateProgressBar(correctnessListPadded)

    def _updateProgressBar(self, correctnessList):
        self.progress = (len([x for x in correctnessList if x]) / len(correctnessList)) * 100
        self.progressBar.setValue(self.progress)

    def _updateInputTextBox(self):
        self.userInputTextBox.setMaxLength(len(self._typeRacer.Text) - self._checkpoint)

    def _updateMainText(self, text, correctnessList):
        self.mainText.clear()
        for value in [True, False, None]:
            color = self.CorrectnessColorsMap[value]
            textPart = ''.join(Common.applyMask(text, correctnessList, value))
            self.mainText.setTextColor(QColor(color))
            self.mainText.insertPlainText(textPart)

    def _proceedGameFinish(self):
        self.userInputTextBox.clear()
        self.userInputTextBox.setDisabled(True)
        self._showResultMessageBox(10.0)

    def _showResultMessageBox(self, results):
        QMessageBox.question(self, 'Congratulations', str.format('Game time {0}s', results),
                             QMessageBox.Ok, QMessageBox.Ok)
