from PyQt5.QtWidgets import QWidget, QLineEdit, QGridLayout, QTextEdit, QProgressBar, QMessageBox, QPushButton
from PyQt5.QtGui import QColor
from PyQt5 import QtCore

import Common
import Timer
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
        self._counter = 0
        self._timer = Timer.Timer()

    def run(self, text):
        self.Running = True
        self._typeRacer.setText(text)
        self._createWindow()
        self._updateMainText(text, [None] * len(text))

    def _createWindow(self):
        self.resize(*self._windowLayout.windowSize)
        self.setWindowTitle(self._windowLayout.windowTitle)

        # input text box
        self.userInputTextBox = QLineEdit()
        self.userInputTextBox.setDisabled(True)
        self.userInputTextBox.textEdited.connect(self._textEdited)
        self.userInputTextBox.setMaxLength(len(self._typeRacer.Text))

        # main text
        self.mainText = QTextEdit()
        self.mainText.setReadOnly(True)
        # text non selectable
        self.mainText.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

        # progress bar
        self.progressBar = QProgressBar()

        # start button
        self.startButton = QPushButton()
        self.startButton.setText('Start')
        self.startButton.clicked.connect(self.startClick)

        # Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.progressBar, 0, 0, 1, 2)
        self.layout.addWidget(self.mainText, 1, 0, 1, 2)
        self.layout.addWidget(self.userInputTextBox, 2, 0, 1, 1)
        self.layout.addWidget(self.startButton, 2, 1, 1, 1)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        self.setLayout(self.layout)

        self.setMinimumSize(self.sizeHint())
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.deleteLater()
            self.Running = False
        event.accept()

    def startClick(self):
        self._startingCountdown(3)

    def _startingCountdown(self, duration):
        def handleTimer():
            self._counter -= 1
            self._setUserInputText(str(self._counter))
            if self._counter == 0:
                self.timer.stop()
                self.startGame()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(handleTimer)
        self.timer.start(1000)  # miliseconds
        self._counter = duration
        self._setUserInputText(str(self._counter))

    def startGame(self):
        self.startButton.setDisabled(True)
        self.userInputTextBox.setDisabled(False)
        self.userInputTextBox.clear()
        self.userInputTextBox.setFocus()
        self._timer.start()

    def reset(self):
        self._typeRacer.reset()
        self._checkpoint = 0
        self._updateWindow()
        self.startButton.setDisabled(False)

    def _setUserInputText(self, text):
        self.userInputTextBox.setText(text)

    def _textEdited(self):
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
        self._showResultMessageBox(self._timer.stop())

    def _showResultMessageBox(self, results):
        clickedButton = QMessageBox.question(self, 'Congratulations', str.format('Game time {0:.1f}s', results),
                             QMessageBox.Ok, QMessageBox.Ok)
        if clickedButton == QMessageBox.Ok:
            self.reset()

