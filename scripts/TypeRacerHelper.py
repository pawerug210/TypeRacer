

class TypeRacerHelper(object):

    def __init__(self, text=[]):
        self.Text = text
        self.UserText = []
        self._correctness = []

    def setText(self, text):
        self.Text = text
        self.reset()

    def addChar(self, char):
        self.UserText.append(char)
        self._correctness.append(self._isCharCorrect(char, len(self._correctness)))

    def removeChar(self, n=1):
        if n > 0:
            del self.UserText[-n:]
            del self._correctness[-n:]

    def addText(self, text, startPosition):
        # remove last chars to the point where word (text) starts
        self.removeChar(len(self.UserText) - startPosition)
        for char in text:
            self.addChar(char)

    def isNewWord(self):
        return any(self.UserText) and self.UserText[-1] == ' ' and all(self._correctness)

    def isFinished(self):
        return len(self._correctness) == len(self.Text) and all(self._correctness)

    def getCorrectnessList(self):
        return self._correctness

    def reset(self):
        self.UserText = []
        self._correctness = []

    def _isCharCorrect(self, char, index):
        return self.Text[index] == char and (len(self._correctness) == 0 or self._correctness[-1])
