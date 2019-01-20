import pygame
import TypeRacerHelper
from pygame.locals import *
import Common


# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)


class PyGameWrapper(object):

    _window = None
    _inputTextBox = ''
    Running = False
    CorrectnessColorsMap = {
        True: green,
        False: red,
        None: black
    }

    def __init__(self, windowLayout):
        pygame.init()
        pygame.font.init()
        self._layout = windowLayout
        self._font = pygame.font.SysFont(None, 25)
        self._typeRacer = TypeRacerHelper.TypeRacerHelper()

    def run(self, text):
        self.Running = True
        self._window = pygame.display.set_mode(self._layout.windowSize)
        self._typeRacer.setText(text)
        self._draw()


    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                self._keyPressed(event)
            elif event.type == QUIT:
                self.Running = False

    def _draw(self):
        self._clear()
        self._drawInputText()
        self._drawMainText()
        self._update()

    def _keyPressed(self, event):
        if event.key == K_ESCAPE:
            self.Running = False
        if event.key == K_BACKSPACE:
            self._charRemoved()
        elif event.unicode.isalpha():
            self._charTyped(event.unicode)

    def _drawInputText(self):
        pass

    def _drawMainText(self):
        text = self._typeRacer.Text
        correctnessList = Common.addNonePadding(self._typeRacer.getCorrectnessList(), len(text))
        self.displayText(text, correctnessList)

    def _charTyped(self, char):
        self._typeRacer.addChar(char)
        self._draw()

    def _charRemoved(self):
        if self._inputTextBox != '':
            self._typeRacer.removeChar()
            self._draw()

    def displayText(self, text, correctnessList):
        caretPosition = self._layout.mainTextPosition
        for value in [True, False, None]:
            color = self.CorrectnessColorsMap[value]
            textPart = ''.join(Common.applyMask(text, correctnessList, value))
            screenText = self._font.render(textPart, True, color)
            textWidth, textHeight = self._font.size(textPart)
            self._window.blit(screenText, caretPosition)
            caretPosition[0] += textWidth

    def _clear(self):
        self._window.fill(white)

    def _update(self):
        pygame.display.update()